from flask import Flask,render_template,request
import pickle
import pandas
import numpy as np
item_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load((open('pt.pkl','rb')))
movies=pickle.load(open('movies.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           movie_name=list(item_df['title'].values),
                           votes=list(item_df['num_rating'].values.round(1)),
                           ratings=list(item_df['avg_rating'].values.round(1))
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movies',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = movies[movies['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        # item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        # item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)
if __name__=='__main__':
    app.run(debug=True)