import itertools
import sqlite3
import logging
from urllib import response
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


homepage_view = 0

def count_db_connection():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    db_connection_count = cursor.execute(
        'SELECT SUM(title) FROM posts').fetchall()
    connection.close()
    return db_connection_count[0][0] + homepage_view


c = 0  # global variable


def add():
    global c
    c = c + 2  # increment by 2
    print("Inside add():", c)

