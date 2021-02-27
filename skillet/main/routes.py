from flask import Blueprint, request, render_template, redirect, url_for, flash

main = Blueprint("main", __name__, template_folder='templates')

##########################################
#           Main Routes                  #
##########################################


@main.route('/')
def home():
    """Displays the homepage."""
    return render_template('home.html')
