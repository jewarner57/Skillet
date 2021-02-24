from flask import Blueprint, request, render_template, redirect, url_for, flash

main = Blueprint("main", __name__)

##########################################
#           Main Routes                  #
##########################################


@main.route('/')
def home():
    """Gets the homepage."""
    return render_template('home.html')
