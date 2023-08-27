from flask import Flask, request, render_template
import numpy as np
import pickle
import sklearn
import joblib

model_version = "1.3.0."  # Update this with the version used to train and pickle the model

def load_model(model_path):
    try:
        with open(model_path, 'rb') as model_file:
            if sklearn.__version__ == model_version:
                model = pickle.load(model_file)
            else:
                model = joblib.load(model_file)
        return model
    except (pickle.UnpicklingError, ValueError, ImportError) as e:
        print("Error loading model:", e)
        return None

app = Flask(__name__)

# Load models using the version-handling function
model = load_model('models/greensitecropmodel.pkl')
sc = load_model('models/greensitecropstandscaler.pkl')
ms = load_model('models/greensitecropminmaxscaler.pkl')

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    scaled_features = ms.transform(single_pred)
    final_features = sc.transform(scaled_features)
    prediction = model.predict(final_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = "{} is the best crop to be cultivated right there".format(crop)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template('index.html',result = result)


    
    

if __name__ == "__main__":
    app.run(debug=True)
