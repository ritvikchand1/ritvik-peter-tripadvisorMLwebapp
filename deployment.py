from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import pickle
import os

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def predict():
    if request.method == "POST": 
        print(request.method)
        review_text = request.form.get("review-content")

        # predictions
        pred_rating = pred(review_text)
        return render_template("index.html", rating = pred_rating)
    else:
        print(request.method)
        return render_template("index.html", rating = 0)

def pred(good_user_input):
    # good_reviews = [input("Enter a positive hotel review --> ")]  #user inputs both a good and bad review
    # bad_reviews = [input("Enter a negative hotel review --> ")]

    encoded_good_reviews = tokenizer.texts_to_matrix([good_user_input], mode='binary')
    predicted_good_ratings = model.predict(encoded_good_reviews)    #user inputed good review is encoded as binary matrix
    # encoded_bad_reviews = tokenizer.texts_to_matrix(bad_reviews, mode='binary')   #user inputed bad review is encoded as binary matrix
    # predicted_bad_ratings = model.predict(encoded_bad_reviews)


    # testing_encoded_ratings = np.array(testing_ratings) / 5.0   #testing ratings are converted from 1-5 to 0-1
    # testing_encoded_reviews = tokenizer.texts_to_matrix(testing_reviews, mode='binary')  #testing reviews are converted to binary

    predicted_good_ratings_list = predicted_good_ratings.flatten().tolist() #matrix is flatened and made into a list
    predicted_good_rating = 0 #place holder initial values of 0 are ste before the code enters the for loop
    max_good_probability = 0
    for i in range(len(predicted_good_ratings_list)):   #for values in the range from 0 to the end of the list
        if predicted_good_ratings_list[i] > max_good_probability:   #if any i value is greater than the current max probability
            predicted_good_rating = i+1   #the i value is increased by 1 and saved as the new max probability
            max_good_probability = predicted_good_ratings_list[i]
    # print("good review prediction: ", predicted_good_rating, "stars")
    return predicted_good_rating

    # predicted_bad_ratings_list = predicted_bad_ratings.flatten().tolist()
    # predicted_bad_rating = 0
    # max_bad_probability = 0
    # for i in range(len(predicted_bad_ratings_list)):
    #     if predicted_bad_ratings_list[i] > max_bad_probability:
    #         predicted_bad_rating = i+1
    #         max_bad_probability = predicted_bad_ratings_list[i]
    # print("bad review prediction: ",predicted_bad_rating , "stars")

if __name__ == "__main__":
    os.system('gdown 1NMIiYh5tiqvg5oBl9lIj_z2MvK9VdLB1')
    os.system('gdown 1-2sorE2PLDsGFwOl6KNtqJ8UDb6U1CmS')

    model = load_model('model.keras')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    app.run(host='0.0.0.0', port = 8080, debug=False)
