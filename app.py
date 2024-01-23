from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes
                      (ingredients TEXT, recipe_name TEXT)''')  # Removed image_url
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT recipe_name FROM recipes WHERE ingredients=?", (ingredients,))
        recipes = cursor.fetchall()
        conn.close()

    return render_template('index.html', recipes=recipes)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    ingredients = request.form['ingredients']
    recipe_name = request.form['recipe_name']

    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (ingredients, recipe_name) VALUES (?, ?)", 
                   (ingredients, recipe_name))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
