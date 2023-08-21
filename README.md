# CS50’s Web Programming with Python and JavaScript (Project 2: Commerce)

## Commerce

This project is a Django application that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.” The application also allows users to close the auction listing and declare a winner. This project is part of the [CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/) course.

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [Django 4](https://www.djangoproject.com/download/)

## How to Run

1. Clone this repository.
2. Open a terminal window and navigate to the project folder.
3. Install the required packages: `pip install -r requirements.txt`
4. Run `python manage.py makemigrations auctions` to make migrations for the auctions app.
5. Run `python manage.py migrate` to apply migrations to your database.
6. Run `python manage.py runserver` to start the server.
7. In a web browser, go the URL provided by the terminal.