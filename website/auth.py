"""
auth.py
================================================================================
This file handles all authentication-related functionality for the Flask app.

Responsibilities:
- User login
- User logout
- User registration (sign-up)
- Password hashing and verification
- Session management using Flask-Login

Key Technologies Used:
- Flask Blueprints (modular routing)
- SQLAlchemy ORM (database access)
- Werkzeug security (password hashing)
- Flask-Login (user session management)
================================================================================
"""

# ----------------------------
# Imports
# ----------------------------

# Flask utilities for routing, templates, forms, redirects, and flash messages
from flask import Blueprint, app, render_template, request, flash, redirect, url_for

# User model (SQLAlchemy)
from .models import User

# Password hashing & verification helpers
from werkzeug.security import generate_password_hash, check_password_hash

# Database instance (imported from __init__.py)
from . import db   # means: from app.__init__ import db

# Flask-Login utilities for authentication/session handling
from flask_login import login_user, login_required, logout_user, current_user


# ----------------------------
# Blueprint Setup
# ----------------------------

# Create an authentication blueprint
# This allows auth routes to be grouped and registered separately
auth = Blueprint('auth', __name__)


# ----------------------------
# Login Route
# ----------------------------


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    GET  -> Displays the login page
    POST -> Validates credentials and logs the user in
    """

    if request.method == 'POST':
        # Read form data submitted by the user
        email = request.form.get('email')
        password = request.form.get('password')

        # Look up the user by email
        user = User.query.filter_by(email=email).first()

        if user:
            # Compare hashed password stored in DB with user input
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')

                # Log the user in and create a session
                login_user(user, remember=True)

                # Redirect to home page after successful login
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    # Render login page (for GET or failed POST)
    return render_template("login.html", user=current_user)


# ----------------------------
# Logout Route
# ----------------------------

@auth.route('/logout')
@login_required
def logout():
    """
    Logs out the currently authenticated user.

    - login_required ensures only logged-in users can access this route
    - Session is cleared using Flask-Login
    """
    logout_user()
    return redirect(url_for('auth.login'))


# ----------------------------
# Sign-Up (Registration) Route
# ----------------------------

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handles new user registration.

    GET  -> Displays the sign-up form
    POST -> Validates input, creates a new user, logs them in
    """

    if request.method == 'POST':
        # Read user input from the form
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if user already exists
        user = User.query.filter_by(email=email).first()

        # Validation checks
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user with hashed password
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='sha256')
            )

            # Save user to the database
            db.session.add(new_user)
            db.session.commit()

            # Automatically log in the newly registered user
            login_user(new_user, remember=True)

            flash('Account created!', category='success')

            # Redirect to home page after successful registration
            return redirect(url_for('views.home'))

    # Render sign-up page
    return render_template("sign_up.html", user=current_user)
