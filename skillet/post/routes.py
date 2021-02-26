from skillet import app, db
from flask import Blueprint, request, render_template, redirect, url_for, flash
from skillet.post.forms import MealForm, RecipeForm
from skillet.models import Meal, Recipe
from flask_login import current_user, login_required

post = Blueprint("from skillet.models import Userpost",
                 __name__, template_folder='templates')

##########################################
#           Recipe Routes                #
##########################################


@post.route('/create_recipe')
@login_required
def create_recipe():
    """Gets the create_recipe page"""

    form = RecipeForm()
    if form.validate_on_submit():

        recipe = Recipe(
            name=form.name.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            process=form.process.data
        )

        db.session.add(recipe)
        db.session.commit()

        flash('Recipe Created.')
        return redirect(url_for('auth.profile', id=current_user.id))

    print(form.errors)

    return render_template('create_recipe.html', form=form)


@post.route('/edit_recipe/<id>')
@login_required
def edit_recipe(id):
    """Gets the edit_recipe page"""
    recipe = Recipe.query.get(id)
    form = RecipeForm(obj=recipe)

    if form.validate_on_submit() and current_user.id == recipe.created_by_id:

        recipe.name = form.name.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.process = form.process.data

        db.session.add(recipe)
        db.session.commit()

        flash('Recipe Updated.')
        return redirect(url_for('auth.profile', id=current_user.id))

    print(form.errors)

    return render_template('edit_recipe.html', form=form, recipe=recipe)


@post.route('/view_recipe/<id>')
def view_recipe(id):
    """Gets the recipe detail page"""
    recipe = db.Recipe.query_by(id=id)

    return render_template('recipe.html', recipe=recipe)


##########################################
#           Meal Routes                  #
##########################################

@post.route('/create_meal')
@login_required
def create_meal():
    """Gets the create_meal page"""
    return render_template('create_meal.html')


@post.route('/edit_meal')
@login_required
def edit_meal():
    """Gets the edit_meal page"""
    return render_template('edit_meal.html')


@post.route('/delete_meal/<id>')
@login_required
def delete_meal(id):
    """deletes a meal"""
    return render_template('meal.html')


@post.route('/view_meal/<id>')
def view_meal(id):
    """Gets the meal detail page"""
    meal = db.Meal.query_by(id=id)

    return render_template('meal.html', meal=meal)
