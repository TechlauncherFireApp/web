# fire-app

Bushfire Volunteer Management Application (TL 20-S1-2-C Fire App)

A web app to assist with firefighting scheduling activities

https://redmine.cecs.anu.edu.au/redmine/projects/bushfire-volunteer-management-application

Fire-app is a Techlauncher project for the Client Accenture.

Here is our project [landing page](https://docs.google.com/document/d/1VTIfrLQDojY8VdxfnAeQHJnm1f4dmMVVjPfmVvs3oQs/edit?usp=sharing).


# Development Environment Setup

The development environment works through vscode docker remote development. See the link below to set this environment up.

[Install Docker and VScode](https://gitlab.cecs.anu.edu.au/u6377372/fire-app/wikis/Install-Docker).


# Running the App

Start Docker in a VSCode Dev Container.

The first time you do this on a machine, you need to login to the private repository.

## Frontend

Ensure Docker is running.

To run the local React App (front-end), in the terminal:
```
cd ui
npm start
```
Now you can navigate to the displayed 'local' web address to see the React Website. (localhost:3000/)

To close the React App webserver simply ctrl+c in the terminal.


## Backend

Ensure Docker is running.

To run the backend, in the terminal:
```
cd backend
python3.8 api.py
```
The backend automatically reloads when changes are made to files. 
Sometimes these changes throw errors which will cause the backend to stop. 
Run `python3.8 api.py` again after the problem is fixed.

To close the backend, simply ctrl+c in the terminal.

### Configuring Python

To install a new package use `python3.8 -m pip install package-name`.

To install packages from file use `python3.8 -m pip install -r requirements.txt`.

To save installed packages to file use `python3.8 -m pip freeze > requirements.txt`.

## Database

Our .devcontainer/docker-compose.yml opens our mysql database alongside our workspace when started in a container.

If the DEVELOPMENT field is set true in the /backend/.env file then the backend automatically gets the IP address of the MYSQL host.

Otherwise in release or production, the MYSQL_HOST field in the /backend/.env should be set. Or the same environment variable set manually.
