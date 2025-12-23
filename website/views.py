"""
views.py
================================================================================
This file contains the main application views (routes) that handle
user interactions after authentication.

Responsibilities:
- Display the home page
- Allow users to create notes
- Allow users to delete their own notes
- Enforce authentication using Flask-Login

Key Concepts Used:
- Blueprints for modular routing
- Flask-Login for access control
- SQLAlchemy for database operations
- AJAX (fetch API) for deleting notes without page reload
================================================================================
"""

# ----------------------------
# Imports
# ----------------------------

# Flask utilities
from flask import Blueprint, render_template, request, flash, jsonify

# Flask-Login helpers
from flask_login import login_required, current_user

# Database model
from .models import Note

# Database session
from . import db

# JSON handling for AJAX requests
import json


# ----------------------------
# Blueprint Setup
# ----------------------------

# Blueprint for main application views
views = Blueprint('views', __name__)


# ----------------------------
# Home Route
# ----------------------------

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Home page route.

    GET:
    - Displays the home page
    - Shows all notes belonging to the logged-in user

    POST:
    - Handles creation of a new note
    - Validates note content
    - Saves the note to the database
    """

    if request.method == 'POST':
        # Get note text submitted from the form
        note = request.form.get('note')

        # Validation: prevent empty notes
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # Create a new Note linked to the logged-in user
            new_note = Note(
                data=note,
                user_id=current_user.id
            )

            # Save note to the database
            db.session.add(new_note)
            db.session.commit()

            flash('Note added!', category='success')

    # Render home page and pass current user to template
    return render_template("home.html", user=current_user)


# ----------------------------
# Delete Note Route (AJAX)
# ----------------------------

@views.route('/delete-note', methods=['POST'])
def delete_note():
    """
    Deletes a note using an AJAX request.

    Expected Input:
    - JSON payload: { "noteId": <id> }

    Security:
    - Ensures the note exists
    - Ensures the note belongs to the current user
    """

    # Parse JSON data sent from JavaScript (fetch API)
    note_data = json.loads(request.data)
    note_id = note_data['noteId']

    # Fetch note from database
    note = Note.query.get(note_id)

    # Ensure note exists and belongs to logged-in user
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    # Return empty JSON response (required for fetch)
    return jsonify({})
