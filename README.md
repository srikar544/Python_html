**Python HTML- This Project is full stack basic application which has below flow**

**Templates** -> folder has base.html, home.html, login.html, sign_up.html
base.html is like a super html from which other templates inherits and can use their own templates or keep base.html data
home.html will navigate to the home link
login.html will navigate to the login page
sign_up.html will navigate to the sign_up page which has to enter the data to register to the website


================================================================================
Authentication Module (__init__.py) - High-Level Overview
================================================================================

**quote_plus**: Encodes passwords/URLs safely for MySQL.
**Flask**: Main Flask framework.
**redirect, url_for**: Used to redirect users to routes.
**LoginManager**: Flask-Login manager for user session handling.
**SQLAlchemy:** ORM for database access.
**path:** Standard OS path utilities.

**Creates a Flask app using a factory (create_app).
Configures MySQL database connection via SQLAlchemy.
Sets secret keys for sessions and JWT.
Registers blueprints for modular routes (views and auth).
Adds shortcut routes to redirect /login and /sign-up.
Sets up Flask-Login for user session management.
Implements user loader to fetch users from the database.
Automatically creates database tables if they don’t exist.
here we register the routes of the different pages as /login,/sign-up
create_database method creates the database -> it could be MySQL/SQLite anything for this Project I have used MySQL server 8.0.44**
 When a user logs in, Flask-Login stores their user ID in the session (like a cookie).

================================================================================
Authentication Module (auth.py) - High-Level Overview
================================================================================
Responsibilities:
- Handle user login, logout, and registration
- Hash and verify passwords securely
- Manage user sessions using Flask-Login
- Provide flash messages for feedback (success/error)

Key Components:
- Flask Blueprint for auth routes
- SQLAlchemy ORM for database access (User model)
- Werkzeug security for password hashing
- Flask-Login for session management and current_user access

Routes:
- /login   -> GET: show login form, POST: authenticate user
- /logout  -> GET: log out current user
- /sign-up -> GET: show registration form, POST: create new user and log in

Data Flow:
1. User submits form (login or sign-up)
2. Server validates input and queries User table
3. Passwords are hashed (sign-up) or verified (login)
4. Flask-Login stores user_id in session
5. current_user proxy provides logged-in user access
================================================================================


'/login'
it checks the login is required by the user and the user should be in the system if user is the system show the message login successfully
else incorrect password

'/sign-up'

it is for the first time user who wants to register in this site if user already exists shows the error message if user is not there create an user 

================================================================================
Authentication Module (Models.py) - High-Level Overview
================================================================================

It is like a Pydantic Model which creates database tables for User and Note and the relationship is one User can  have multiple notes
Defines database models (User and Note) for the Flask app using SQLAlchemy.

**User model:**

Stores user info: email, password, first_name.
Inherits UserMixin for Flask-Login authentication.
Has a one-to-many relationship with Note (a user can have multiple notes).

**Note model:**

Stores data (note content) and date (timestamp).
Linked to a User via user_id foreign key.
Integrates with Flask-SQLAlchemy and Flask-Login.


================================================================================
Application Views Module (views.py) - High-Level Overview
================================================================================

Responsibilities:
- Display the home page and user-specific notes
- Allow users to create new notes
- Allow users to delete their own notes via AJAX
- Enforce authentication using Flask-Login

Key Components:
- Flask Blueprint for main routes
- SQLAlchemy ORM for database access (Note model)
- Flask-Login for access control and current_user
- AJAX/fetch API for seamless note deletion

Routes:
- /           -> GET: show notes, POST: create new note
- /delete-note -> POST: delete note via AJAX (validates ownership)

Data Flow:
1. User submits form to add a note
2. Server validates and saves note linked to current_user
3. User triggers note deletion via AJAX
4. Server verifies ownership and deletes note from database
================================================================================

================================================================================
Application Views Module (main.py) - High-Level Overview
================================================================================

Imports the Flask app factory create_app from your website package.
Calls create_app() to create and configure the Flask app.
if __name__ == '__main__': ensures the app runs only when this file is executed directly (not when imported).
app.run(debug=True) starts the development server with debug mode enabled (auto-reloads on code changes and shows detailed error pages).

**Output**

<img width="1091" height="298" alt="image" src="https://github.com/user-attachments/assets/73c5b2f5-87ea-40e6-85b3-616a32389d9f" />




