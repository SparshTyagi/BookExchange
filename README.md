# Book Exchange Platform
==========================

## Overview
------------

The Book Exchange Platform is a web application designed to facilitate the easy listing, searching, and exchanging of books among users. This platform aims to promote a culture of sharing and sustainability, reducing waste, and fostering a community of readers who can benefit from each other's collections.

## Key Features
------------

* User registration and login functionality
* User profile creation and management
* Book listing and management
* Search functionality to find books and users
* Exchange mechanism for users to exchange books
* Community engagement features, such as discussion boards and reviews

## Technical Requirements
-------------------------

* Flask==3.0.3
* Flask-SQLAlchemy==3.1.1
* Flask-Login==0.6.3
* Flask-WTF==1.2.1
* WTForms==3.1.2
* SQLAlchemy==2.0.35
* Werkzeug==3.0.4

## Installation
---------------

1. Clone the repository: `https://github.com/SparshTyagi/BookExchange.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `flask run`

(Feel free to delete the book_exchange.db file to reset the database at any time.)

## Usage
---------

1. Open a web browser and navigate to `http://localhost:5000`
2. Register for an account or log in if you already have one
3. Create a user profile and add books to your collection
4. Search for books and users to exchange books with, or post public exchange notices
5. Participate in discussions on the discussion board

## Decisions Worth Noting
------------------------

* The search functionality is the keystone of this platform, allowing users to find books, listed exchanges, and other users with similar interests.
* The platform uses a peer-to-peer exchange mechanism, allowing users to exchange books directly with each other.
* The community engagement features, such as discussion boards and reviews, are designed to foster a sense of community among users.

## Project Plan and Milestones
-----------------------------

### Short-term (next 2 weeks)

* Develop user profile management features
* Create book listing management features
* Implement search functionality to find books and users
* Develop exchange mechanism for users to exchange books natively

### Medium-term (next 4 weeks)

* Implement AI-enhanced features, such as book recommendations and user matching
* Develop mobile app for on-the-go access
* Integrate with social media platforms for increased visibility and engagement

## Future Extension
-------------------

### Phase 2

* Implement payment processing for users to purchase books from each other
* Develop shipping and logistics features for users to send and receive books
* Create a User rating system for users to rate each other

### Phase 3

* Implement machine learning algorithms to improve book recommendations and user matching
* Develop a gamification system to encourage users to participate in the community
* Create a leaderboard to showcase top users and books

## Contributing
------------

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## License
-------

The Book Exchange Platform is licensed under the MIT License. See `LICENSE` for details.

## Acknowledgments
----------------

* Flask and Flask-Login for providing a robust web framework and authentication system
* SQLAlchemy for providing a powerful ORM system
* Bootstrap for providing a responsive and mobile-friendly front-end framework
