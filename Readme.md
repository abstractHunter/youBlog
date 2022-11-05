# YouBlog

## A web app were you can read and interact with the articles of your favorite bloggers, or start your own blogger advanture

<br/>
<hr/>

## Features:
- As a Reader:
    - read posts
    - comment on posts
    - like posts
    - share posts

- As a Blogger:
    - write posts
    - publish / unpublish a post
    - anything a reader can do


<br/>
<hr/>

## Installation

***On Unix based systems (Linux and MacOs)***

You must have python 3.6 or django 4.1 or higher versions installed

- clone the project: `git clone`
- navigate to the project directory: `cd youBlog`
- create a virtual environment: `python3 -m venv venv`
- activate the environment: `source venv/bin/activate`
- install dependencies: `pip install -r requirements.txt`
- create database and tables: `./manage.py makemigrations accounts blog && ./manage.py migrate`
- start the server: `./manage.py runserver`
