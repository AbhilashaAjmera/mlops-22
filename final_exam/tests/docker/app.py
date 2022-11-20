from flask import Flask ,request
from joblib import load
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
  
 @app.route('/svm_predict")
            def svm_predict():
            input = request.args.get('input')
            return " called svm_predict with input:{input} "
@app.route("/svm_predict_second" , method = ['POST'])
            def svm_predict_pos():
            image = request.json["image"]
            return " called svm_predict_second with input :{image}"
