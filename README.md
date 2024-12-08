# CS50w Project 2 - Commerce


## Description
This project is an implementation of an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings and add listings to a "watchlist".

The application is built using the [Django](https://www.djangoproject.com) web framework and SQLite as the database backend.

[Project specification](https://cs50.harvard.edu/web/2020/projects/2/commerce/)

[Demonstration Video](https://youtu.be/e19B2Tq2TiI?si=uXRhBq8eUveAnlTM)

## Technologies Used
- **Django**: A Python web framework for rapid development.
- **SQLite**: A lightweight relational database to manage the application's data.
- **HTML/CSS**: For structuring and styling the web pages.
- **Bootstrap**: A CSS framework for responsive design.
- **JavaScript**: For adding interactivity and dynamic behavior to web pages.
- **Django Authentication**: Built-in authentication system for managing users.
- **Django Admin**: For managing database records and overseeing content.

## Setup
Follow these steps to set up and run the project locally:
> Python and [Git](https://git-scm.com) must be installed on your computer.  
Clone this repository
```bash
git clone https://github.com/kjown/CS50w-Commerce.git
```
Install any required dependencies
```
pip install -r requirements.txt
```
Initialise the database
```
python manage.py makemigrations auctions
python manage.py migrate
```  
Run the development server
```
python manage.py runserver
```
Access the application
```
http://127.0.0.1:8000
```

## License
This project is part of the CS50 Web Programming with Python and JavaScript course and is for educational purposes.




