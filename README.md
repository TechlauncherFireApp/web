# FireApp2.0

Bushfire Volunteer Management Application (TL 20-S1-2-C Fire App), a web app to assist with firefighting scheduling 
activities.

[Redmine](https://redmine.cecs.anu.edu.au/redmine/projects/bushfire-volunteer-management-application)\
[Project landing page](https://fireapp2.atlassian.net/wiki/spaces/F2/overview)

### Backend Setup

The following steps describe the _operations_ required to get the backend environment setup and working on a system.
The specific steps for _your_ system will vary and are therefore not detailed beyond linking to the individual install
instructions. If  you require help getting started, please post in the discord #general.

Its recommended you use [PyCharm Ultimate](https://www.jetbrains.com/pycharm/download/), you get it for free with you
`anu.edu.au` email address. 

1. **Install Python 3.8+**: [Steps](https://www.python.org/downloads/)
2. **Run** the following commands in a terminal:\
    a. `cd backend`\
    b. `pip install pipenv`\
    c. `pipenv install`
3. **Install Minizinc**:  [Steps](https://www.minizinc.org/software.html)
4. **Install the AWS CLI**: [Steps](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
5. **Configure the AWS CLI**: [Steps](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)\
    **Note:** Use the `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY` provided to you when you joined the team. 
6. **Restart** your IDE so as to update your path. 
7. **Create** a run configuration by adding a `Flask` runtime using the settings:\
    _Target Type:_ `Script Path`\
    _Target:_ `/backend/application.py`\
    _FLASK_ENV:_ `development`\
    _FLASK_DEBUG:_ `true`\
    _Working Directory:_ `/backend`\
    _Add Contents Root to Python Path:_ `true`\
    _Add Source Root to Python Path:_ `true` 


### Frontend Steps

1. **Install NodeJS**: [Steps](https://nodejs.org/en/download/)
2. **Run** the following commands in a terminal:\
    a. `cd ui`\
    b. `npm install`
3. **Create** a run configuration by adding a `npm` runtime using the settings:\
    _Package JSON:_ `<where you've cloned the repo>\FireApp2.0\ui\package.json`\
    _Command:_ `run`\
    _Script:_ `start`\


### Generate  a Database Migration
1. `cd backend`
2. `pipenv activate`
3. `alembic revision --autogenerate -m "<meaningful message>"`

To run the migration: 
1. `alembic upgrade head`
