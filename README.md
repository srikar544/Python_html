**Python HTML- This Project is full stack basic application which has below flow**

**Templates** -> folder has base.html, home.html, login.html, sign_up.html
base.html is like a super html from which other templates inherits and can use their own templates or keep base.html data
home.html will navigate to the home link
login.html will navigate to the login page
sign_up.html will navigate to the sign_up page which has to enter the data to register to the website

__init__.py -> starting flow

here we register the routes of the different pages as /login,/sign-up
create_database method creates the database -> it could be MySQL/SQLite anything for this Project I have used MySQL server 8.0.44

user_loader

When a user logs in, Flask-Login stores their user ID in the session (like a cookie).

auth.py has below routes 

'/login'
it checks the login is required by the user and the user should be in the system if user is the system show the message login successfully
else incorrect password

'/sign-up'

it is for the first time user who wants to register in this site if user already exists shows the error message if user is not there create an user 

Models.py

It is like a Pydantic Model which creates database tables for User and Note and the relationship is one User can  have multiple notes

views.py

it will create a new note to the user and also deletes a note to the user





