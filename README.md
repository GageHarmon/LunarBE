# Lunar Ticketing API

This project is a REST API developed using Flask, Flask-RESTful, Flask-SQLAlchemy, and Flask-Migrate. It provides features to manage users, tickets, and ticket comments.

# Getting Started

These instructions will help you to get a copy of the project up and running on your local machine for development and testing purposes.

# Prerequisites

Ensure you have the following installed on your local development machine:

Python 3.7+
Pip for package installation
Virtualenv for creating isolated Python environments

# Installation

Clone the repo:

# cd Server

Change directory into the project:

# python3 -m venv venv

Create a virtual environment and activate it:

# flask db upgrade

Run the migrations:

# python seed.py

Populate the database with example data:

# python app.py

flask run --port 5555 (replaces python app.py for a better port)

The API has endpoints for creating, reading, updating and deleting users, tickets, and ticket comments. It also supports user login and session management.

# Users

GET /api/users: Returns a list of all users.
POST /api/users: Creates a new user.
GET /api/users/<id>: Returns a specific user.
PATCH /api/users/<id>: Updates a specific user.
DELETE /api/users/<id>: Deletes a specific user.

# Tickets

GET /api/tickets: Returns a list of all tickets.
POST /api/tickets: Creates a new ticket.
GET /api/tickets/<ticket_id>: Returns a specific ticket along with its associated comments.
PATCH /api/tickets/<ticket_id>: Updates a specific ticket.
DELETE /api/tickets/<ticket_id>: Deletes a specific ticket.

# Comments

GET /api/ticket_comments: Returns a list of all comments.
POST /api/ticket_comments: Creates a new comment.
GET /api/ticket_comments/<id>: Returns a specific comment.
PATCH /api/ticket_comments/<id>: Updates a specific comment.
DELETE /api/ticket_comments/<id>: Deletes a specific comment.

# Session Management

POST /login: Logs in a user.
GET /logged_user: Returns the currently logged in user.
GET /check: Checks if a user is logged in.
DELETE /logout: Logs out the current user.
