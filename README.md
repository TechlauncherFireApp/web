# fire-app

Bushfire Volunteer Management Application (TL 20-S1-2-C Fire App)

A web app to assist with firefighting scheduling activities

https://redmine.cecs.anu.edu.au/redmine/projects/bushfire-volunteer-management-application


# Development Environment Setup

The development environment has two fronts. Dokcer is used for the front end, and a pip virtual environment for the backend.

The backend cannot be hosted by a Docker container because Gurobi with an acadmeic licence doesn't work in Docker.

Here are the two links for setting these environments up:

[Install Docker and VScode](https://gitlab.cecs.anu.edu.au/u6377372/fire-app/wikis/Install-Docker)

[Install Gurobi and setup a Python virtual environment](https://gitlab.cecs.anu.edu.au/u6377372/fire-app/wikis/Install-Gurobi-and-Setup-Backend)

# Running the App

If you are running both the front and backend, you can open two windows of vscode. One with Docker, one without.

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

Ensure Docker is not running.

In the terminal:
```
cd backend
.\env\Scripts\activate
python api.py
```
The backend automatically reloads when changes are made to files. 
Sometimes these changes throw error which will cause the backend to stop. 
Run `python api.py` again after the problem is fixed.

To close the backend, simply ctrl+c in the terminal.
