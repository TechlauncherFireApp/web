# FireApp2.0

Bushfire Volunteer Management Application (TL 20-S1-2-C Fire App), a web app to assist with firefighting scheduling 
activities.

[Redmine](https://redmine.cecs.anu.edu.au/redmine/projects/bushfire-volunteer-management-application)\
[Project landing page](https://docs.google.com/document/d/1VTIfrLQDojY8VdxfnAeQHJnm1f4dmMVVjPfmVvs3oQs/edit?usp=sharing)

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
    Target Type: `Script Path`\
    Target: `/backend/app.py`\
    FLASK_ENV: `development`\
    FLASK_DEBUG: `true`\
    Working Directory: `/backend`
    Add Contents Root to Python Path: `true`
    Add Source Root to Python Path: `true` 


### Frontend Steps

// TODO