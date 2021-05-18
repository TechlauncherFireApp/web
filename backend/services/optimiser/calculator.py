import json
from datetime import timedelta, datetime
from typing import List
from sqlalchemy import orm, func, alias

from domain import User, AssetRequestVehicle, AssetType, Role, UserRole, AssetTypeRole


class Calculator:
    """
    Calculates many helper data structures for the optimiser to then use in the actual linear optimiser step. This code
    is split out to enable testing and ease of understanding.
    """

    # Master list of all volunteers, these fetched once so that the order of the records in the list is deterministic.
    # This matters as the lists passed to Minizinc are not keyed and are instead used by index.
    _users_ = []
    _asset_request_vehicles_ = []
    _asset_types_ = []
    _roles_ = []
    _asset_type_seats_ = []

    # A single database session is used for all transactions in the optimiser. This is initialised by the calling
    # function.
    _session_ = None

    # This is the granularity of the optimiser, it won't consider any times more specific thann this number of minutes
    # when scheduling employees.
    # It should match the volunteer's shift planner granularity
    _time_granularity_ = timedelta(minutes=30)

    # The request to optimise.
    request_id = None

    # Used to map between datetime.datetime().weekday() to the users availability as its agnostic of the time of year.
    _week_map_ = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    def __init__(self, session: orm.session, request_id: int):
        self._session_ = session
        self.request_id = request_id

        # Fetch all the request data that will be used in the optimisation functions once.
        self.__get_request_data()

    def get_number_of_vehicles(self) -> int:
        """
        @return: The number of vehicles to be optimised.
        """
        return len(self._asset_request_vehicles_)

    def get_number_of_roles(self):
        """
        @return: The number of roles to be optimised
        """
        return len(self._roles_)

    def get_number_of_volunteers(self) -> int:
        """
        @return: The number of users to be optimised.
        """
        return len(self._users_)

    def get_volunteer_by_index(self, index) -> User:
        return self._users_[index]

    def get_role_by_index(self, index) -> Role:
        return self._roles_[index]

    def get_asset_request_by_index(self, index) -> AssetRequestVehicle:
        return self._asset_request_vehicles_[index]

    def get_asset_requests(self) -> List[AssetRequestVehicle]:
        return self._asset_request_vehicles_

    def get_roles(self) -> List[Role]:
        return self._roles_

    def __get_request_data(self):
        """
        Initialising function that fetches a list of reference data from the database. This is done to simplify future
        functions as they don't need to be concerned about data fetching.
        @return:
        """
        self._users_ = self._session_.query(User) \
            .all()
        self._asset_request_vehicles_ = self._session_.query(AssetRequestVehicle) \
            .filter(AssetRequestVehicle.request_id == self.request_id) \
            .all()
        self._asset_types_ = self._session_.query(AssetType) \
            .filter(AssetType.deleted == False) \
            .all()
        self._roles_ = self._session_.query(Role) \
            .filter(Role.deleted == False) \
            .all()
        self._asset_type_seats_ = self._session_.query(AssetTypeRole) \
            .join(Role, Role.id == AssetTypeRole.role_id) \
            .filter(Role.deleted == False) \
            .all()

    def calculate_deltas(self, start: datetime, end: datetime) -> List[datetime]:
        """
        Given the start time and end time of a shift, generate a list of shift "blocks" which represent a
        self._time_granularity_ period that the user would need to be available for
        @param start: The start time of the shift.
        @param end: The end time of the shift.
        @return: A list of dates between the two dates.
        """
        deltas = []
        curr = start
        while curr < end:
            deltas.append(curr)
            curr += self._time_granularity_
        return deltas

    @staticmethod
    def float_time_to_datetime(float_hours: float, d: datetime) -> datetime:
        """
        Given a users available time as a date agnostic decimal hour and a shift blocks date, combine the two into a
        datetime that can be used for equality and range comparisons.
        @param float_hours: The users decimal hour availability, i.e. 3.5 is 3:30am, 4.0 is 4am,
        @param d: The shift blocks date time
        @return: The decimal hours time on the shift blocks day as datetime
        """
        # Assertion to ensure the front end garbage hasn't continued
        assert 0 <= float_hours <= 23.5

        # Calculate the actual datetime
        hours = int(float_hours)
        minutes = int((float_hours * 60) % 60)
        return datetime(d.year, d.month, d.day, hours, minutes, 0)

    def calculate_compatibility(self) -> List[List[bool]]:
        """
        Generates a 2D array of compatibilities between volunteers availabilities and the requirements of the shift.
        This is the fairly critical function of the optimiser as its determining in a simple manner if a user is
        even available for assignment, regardless of role.

        Example 1: The volunteer is available between 2pm to 3pm and the shift is from 2pm to 2:30pm:
            Result: True
        Example 2: The volunteer is available from 1pm to 2pm and the shift is from 1pm to 3pm:
            Result: False
        @return:
        """
        compatibilities = []
        # Iterate through each shift in the request
        for asset_request_vehicle in self._asset_request_vehicles_:
            # Each shift gets its own row in the result set.
            shift_compatibility = []

            # Shift blocks are the _time_granularity_ sections the volunteer would need to be available for.
            # Its calculated by finding all the 30 minute slots between the start time and end time (inclusive)
            shift_blocks = self.calculate_deltas(asset_request_vehicle.from_date_time,
                                                 asset_request_vehicle.to_date_time)
            # Iterate through the users, this makes each element of the array
            for user in self._users_:
                # We start by assuming the user is available, then prove this wrong.
                user_available = True

                # Iterate through each block to see if the user is available on this shift
                shift_block_availability = []
                for shift_block in shift_blocks:
                    available_in_shift = False
                    for day_availability in user.availabilities[self._week_map_[shift_block.weekday()]]:
                        # Generate a new datetime object that is the start time and end time of their availability, but
                        # using the date of the shift block. This lets us calculate availability regardless of the day
                        # of the year
                        start_time = self.float_time_to_datetime(day_availability[0], shift_block)
                        end_time = self.float_time_to_datetime(day_availability[1], shift_block)
                        if end_time >= shift_block >= start_time:
                            available_in_shift = True
                    shift_block_availability.append(available_in_shift)

                # If every element in the shift block availability is true, then the user can do this shift.
                if False in shift_block_availability:
                    user_available = False

                shift_compatibility.append(user_available)
            # Append the shift compatibilities to the overall result
            compatibilities.append(shift_compatibility)
        # Return the 2D array
        return compatibilities

    def calculate_clashes(self) -> List[List[bool]]:
        """
        Generate a 2d array of vehicle requests that overlap. This is to ensure that a single user isn't assigned to
        multiple vehicles simultaneously. Its expected that each shift is incompatible with itself too.
        @return: A 2D array of clashes.
        """
        clashes = []
        # Iterate through each shift in the request
        for this_vehicle in self._asset_request_vehicles_:
            this_vehicle_clashes = []
            this_shift_blocks = self.calculate_deltas(this_vehicle.from_date_time,
                                                      this_vehicle.to_date_time)
            for other_vehicle in self._asset_request_vehicles_:
                has_clash = False
                for this_shift_block in this_shift_blocks:
                    if other_vehicle.from_date_time <= this_shift_block <= other_vehicle.to_date_time \
                            and other_vehicle.id != this_vehicle.id:
                        has_clash = True
                this_vehicle_clashes.append(has_clash)
            clashes.append(this_vehicle_clashes)
        return clashes

    def calculate_skill_requirement(self):
        """
        Return a 2D array showing the number of people required for each skill in a asset shift. Might look something
        like:
                        Driver Pilot  Ninja
                      ----------------------
           Vehicle 1  [[1,       0,      0]
           Vehicle 2  [F,       1,      1]]
        @return:
        """
        rtn = []
        for vehicle in self._asset_request_vehicles_:
            this_vehicle = []
            for role in self._roles_:
                print(vehicle)
                print(role)
                this_vehicle.append(self.get_role_count(vehicle.asset_type.id, role.id))
            rtn.append(this_vehicle)
        return rtn

    def get_role_count(self, asset_type_id, role_id):
        """
        Determines the number of each role required for each asset type or 0 if not required.
        @param asset_type_id: The asset type to search for.
        @param role_id: The role to search for.
        @return: The volunteers required or 0 if not required.
        """
        query = self._session_.query(AssetTypeRole) \
            .join(Role, Role.id == AssetTypeRole.role_id) \
            .join(AssetType, AssetType.id == AssetTypeRole.asset_type_id) \
            .filter(Role.deleted == False) \
            .filter(Role.id == role_id) \
            .filter(AssetType.id == asset_type_id)
        result = self._session_.query(func.count('*')).select_from(alias(query)).scalar()
        if result is None:
            result = 0
        return result

    def calculate_mastery(self):
        """
        For all active roles, return a 2D array of what user can perform what roles.
        For example, if the database has two users, both can drive but only 1 is advanced, the result would look like:
        name the indexes:
                      Driver   Advanced  CrewLeader
                      ----------------------------
              User 1 [[T,         F,          F]
              User 2  [T,         T,          F]]
        @return: A 2D array explaining what users can perform what roles.
        """
        rtn = []
        for user in self._users_:
            user_role = []
            for role in self._roles_:
                user_has_role = self._session_.query(UserRole) \
                    .filter(UserRole.user == user) \
                    .filter(UserRole.role == role) \
                    .first()
                user_role.append(user_has_role is not None)
            rtn.append(user_role)
        return rtn
