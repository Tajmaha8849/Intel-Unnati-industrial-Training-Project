# 1. Imports
from flask import Flask, render_template, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import joblib

# 2. create an instance of the Flask class
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asecretkey'

# 3. define a prediction function
def return_prediction(model, input_json):

    input_data = [[input_json[k] for k in input_json.keys()]]
    prediction = model.predict(input_data)[0]

    return prediction

# 4. load our abalone age predictor model
model = joblib.load('Dragon.joblib')

# 5. create a WTForm Class
class PredictForm(FlaskForm):

    CRIM = StringField("CRIM")
    ZN= StringField("ZN")
    INDUS = StringField("INDUSt")
    CHAS = StringField("CHAS")
    NOX = StringField("NOX")

    RM = StringField("RM")
    AGE= StringField("AGE")
    DIS = StringField("DIS")
    RAD = StringField("RAD")
    TAX = StringField("TAX")

    PTRATIO = StringField("PTRATIO")
    B = StringField("B")
    LSTATE = StringField("LSTATE")
    submit = SubmitField("Predict")

# 6. set up our home page
@app.route("/", methods=["GET", "POST"])
def index():

    # Create instance of the form
    form = PredictForm()

    # Validate the form
    if form.validate_on_submit():
        session['CRIM'] = form.CRIM.data
        session['ZN'] = form.ZN.data
        session['INDUS'] = form.INDUS.data
        session['CHAS'] = form.CHAS.data
        session['NOX'] = form.NOX.data
        session['RM'] = form.RM.data
        session['AGE'] = form.AGE.data
        session['DIS'] = form.DIS.data
        session['RAD'] = form.RAD.data
        session['TAX'] = form.TAX.data
        session['PTRATIO'] = form.PTRATIO.data
        session['B'] = form.B.data
        session['LSTATE'] = form.LSTATE.data
        return redirect(url_for("prediction"))

    return render_template('home.html', form=form)

# 7. define a new "prediction" route that processes form input and returns a model prediction
@app.route('/prediction')
def prediction():

    content = {}
    content['CRIM'] = float(session['CRIMHello'])
    content['ZN'] = float(session['ZN'])
    content['INDUS'] = float(session['INDUS'])
    content['CHAS'] = float(session['CHAS'])

    content['NOX'] = float(session['NOX'])
    content['RM'] = float(session['RM'])
    content['AGE'] = float(session['AGE'])
    content['DIS'] = float(session['DIS'])
    content['RAD'] = float(session['RAD'])
    content['TAX'] = float(session['TAX'])
    
    content['PTRATIO'] = float(session['PTRATIO'])
    content['B'] = float(session['B'])
    content['LSTATE'] = float(session['CHAS'])
    

    results = return_prediction(model, content)
    return render_template('prediction.html', results=results)

# 8. allows us to run flask using $ python app.py
if __name__ == '__main__':
    app.run(debug=True,port=8000)
