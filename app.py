import os
from flask import Flask , render_template, request
from model import get_recipe_info , get_category_id , predict_food
import pandas as pd

UPLOAD_FOLDER='./static/food_image'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new' ,methods=['GET', 'POST'])
def new():
        return render_template('new.html')

@app.route('/show',methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        return render_template('show.html')

    elif request.method == 'POST':
        upload_file = request.files['upload_file']
        img_path = os.path.join(UPLOAD_FOLDER,upload_file.filename)
        upload_file.save(img_path)
        name = predict_food(img_path)
        id = get_category_id(name)
        result = get_recipe_info(id)
        return render_template('show.html', res = result ,idx=len(result.columns))

if __name__ == '__main__':
    app.run(debug=True)

