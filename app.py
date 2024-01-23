from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    # Adding an 'id' column as primary key
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, ingredients TEXT, recipe_name TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    message = ''
    if request.method == 'POST':
        ingredients = standardize_ingredients(request.form['ingredients'])
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, recipe_name FROM recipes WHERE ingredients=?", (ingredients,))
        recipes = cursor.fetchall()
        conn.close()
        if not recipes:
            message = "No recipes found for the given ingredients."

    return render_template('index.html', recipes=recipes, message=message)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    ingredients = standardize_ingredients(request.form['ingredients'])
    recipe_name = request.form['recipe_name']

    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (ingredients, recipe_name) VALUES (?, ?)", 
                   (ingredients, recipe_name))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    origin = request.args.get('origin', 'index')  # Default to 'index' if not specified

    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
    conn.commit()
    conn.close()

    return redirect(url_for(origin))



@app.route('/all_recipes')
def all_recipes():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, ingredients, recipe_name FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return render_template('all_recipes.html', recipes=recipes)

def standardize_ingredients(ingredient_string):
    ingredients = [ingredient.strip().lower() for ingredient in ingredient_string.split()]
    ingredients.sort()
    return ' '.join(ingredients)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
