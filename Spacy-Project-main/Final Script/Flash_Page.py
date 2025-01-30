from flask import Flask, request, render_template
from English_model import English_Prediction
from Hindi_model import Hindi_Prediction
from langdetect import detect

app= Flask(__name__)

@app.route('/')
def my_form():
    return render_template('PageOutlook.html')
@app.route('/', methods=['POST'])
def my_form_post():
    Input = request.form['Label']
    if(len(Input)==0):
        return "Please Input a Valid Statement"
    if(detect(Input)=='en'):
        return English_Prediction(Input)
    else:
        return Hindi_Prediction(Input)


if __name__=="__main__":
    app.run()
