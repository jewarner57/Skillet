from datetime import datetime
from skillet import app, db
from flask import Blueprint, request, render_template, redirect, url_for, flash
from skillet.post.forms import MealForm, RecipeForm
from skillet.models import Meal, Recipe
from flask_login import current_user, login_required
from skillet.post.utils import update_user_activity

post = Blueprint("post",
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

        update_user_activity(current_user)

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

        update_user_activity(current_user)

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
    form = MealForm()
    if form.validate_on_submit():

        update_user_activity(current_user)

        meal = Meal(
            name=form.name.data,
            description=form.description.data,
            image_url=form.image_url.data,
            date_prepared=datetime.now()
        )

        db.session.add(meal)
        db.session.commit()

        flash('Meal Created.')
        return redirect(url_for('auth.profile', id=current_user.id))

    print(form.errors)

    return render_template('create_meal.html', form=form)


@post.route('/edit_meal/<id>')
@login_required
def edit_meal(id):
    """Gets the edit_meal page"""
    meal = Meal.query.get(id)
    form = MealForm(obj=meal)

    if form.validate_on_submit() and current_user.id == meal.created_by_id:

        update_user_activity(current_user)

        meal.name = form.name.data
        meal.description = form.description.data
        meal.image_url = form.image_url.data,
        meal.date_prepared = datetime.now()

        db.session.add(meal)
        db.session.commit()

    flash('Meal Updated.')
    return redirect(url_for('auth.profile', id=current_user.id))

    print(form.errors)

    return render_template('edit_meal.html', form=form, meal=meal)


@post.route('/delete_meal/<id>')
@login_required
def delete_meal(id):
    """deletes a meal"""
    meal = Meal.query.get(id)

    if current_user.id == meal.created_by_id:
        update_user_activity(current_user)

        db.session.delete(meal)
        db.session.commit()
        flash("Meal Deleted")

    return redirect(url_for('auth.profile', id=current_user.id))


@post.route('/view_meal/<id>')
def view_meal(id):
    """Gets the meal detail page"""
    meal = Meal.query.get(id=id)

    return render_template('meal.html', meal=meal)
