import requests
import pandas as pd
import json
from pandas import json_normalize
from keras.models import load_model
import pickle
import cv2
import numpy as np
import tensorflow as tf

#model = load_model('static/cnn.h5')
model = tf.keras.models.load_model('static/cnn.h5', compile=False)
model.compile()

classes = pickle.load(open('static/classes.sav', 'rb'))

base_url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?' #レシピランキングAPIのベースとなるURL
# カテゴリid を取得してその結果をdfで返す関数
def get_recipe_info(category_id):
    item_parameters = {
        'applicationId': '1003217176771647154', #アプリID
        'format': 'json',
        'formatVersion': 2,
        'categoryId':str(category_id)
    }

    r = requests.get(base_url, params=item_parameters)
    item_data = r.json()
    df_rank = pd.DataFrame()

    for i , recipe in enumerate(item_data['result']):
        df_rank_tmp = pd.Series([
            recipe['rank'],
            recipe['recipeId'],
            recipe['recipeTitle'],
            recipe['recipeDescription'],
            recipe['recipeUrl'],
            recipe['foodImageUrl'],
            recipe['recipeCost'],
            recipe['recipeIndication'],
            recipe['recipeMaterial'],
            recipe['recipePublishday']
        ] ,name=i)
        df_rank = df_rank.append(df_rank_tmp)
    return df_rank


# カテゴリ名からidを取得するコード
## 複数ヒットする場合はより短いものを返す
def get_category_id(category):
    df = pd.read_csv('category_id.csv')
    df_selected = df.query('categoryName == @category')
    return df_selected.iloc[0,0]


#追加しました！！

def predict_food(input_filename):
    img = cv2.imread(input_filename)
    img = cv2.resize(img,dsize=(224,224))
    img = img.astype('float32')
    img /= 255.0
    img = img[None, ...]
    result = model.predict(img)

    np.set_printoptions(precision=3, suppress=True)
    result *100

    pred = result.argmax()

    return classes[pred]