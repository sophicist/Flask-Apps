from flask import Flask, render_template, request
from model import cleaner
import pickle
import os 
import pandas as pd
from random import choice
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

app = Flask(__name__)
print(os.listdir())

# Functions for the Mpesa Simulation
def Mpesa_no(x):
    "returns a weight depending on the number of Mpesa transactions x"
    mpesa = ["The number has to be positive" if x <0 else 5 if x < 15 else 10 if x <30 else 15 if x < 45 else 20]
    try:
        no= mpesa[0] / 100
    except:
        no = "The number has to be positive"
    return no

def receive_send(send,receive):
    "returns a positive weight if receive > send or a negative weight if receive < send. the weight is between -5 & 5"
    if send < 0 or receive < 0:
        return "The number has to be positive"
    elif receive>send:
        if send ==0:
            net = [.5]
        else:
            net = [0.15 if receive/send <1.25 else 0.2 if receive/send <1.5 else .3 if receive/send <1.75 else .4 if receive/send <2.5 else .5 ]
        return net[0]
    elif receive<send:
        if receive == 0:
            net =[ -.5 ]
        else:
             net = [-0.1 if receive/send > 0.75 else -0.2 if receive/send > 0.5 else -0.4 if receive/send > 0.3 else -.5 ]
        return net[0]
    else:# when they are equal
        return 0.1
    
def creditors(number):
    "returns .3 if you have no creditors or a negative number that grows as the number of creditors increase"
    if number < 0:
        return "The number has to be positive"
    else:
        creditors  = [.30 if number == 0 else -.05 if number ==1 else -.10 if number == 2 else -.20 if number == 3 else -.30]
        return creditors[0]
    
def scored(mpesa_no,send,receive,cred,initial_score):
          "returns a credit score that is between 1 and 0 "
          score = creditors(cred)
          Num = Mpesa_no(mpesa_no)
          R_S = receive_send(send,receive)
          total = score + Num + R_S + initial_score
          return total/2
 
   
@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST'])
def result():
   """Trains a machine learning model using cleaned dataset X,Y  and returns probability score. The function also gets data from
   an online form and returns the specific probability score for that data."""
   X1 = pd.read_csv("X1.csv")
   Y1 = pd.read_csv("Y1.csv")
   
   X_train,X_test,Y_train,Y_test = train_test_split(X1,Y1,test_size = 0.2)
   sc = MinMaxScaler()
   clf1 = RandomForestClassifier(n_estimators = 100 ,verbose=1,random_state=324) 
   Model = Pipeline([('scaler', sc), ('clf1', clf1)])
   Model.fit(X_train, Y_train)

   def credit_score(row):
      """ Uses  the machine learning model and predicts a row of variables and converts them to the range [0,10]"""
      probability = Model.predict_proba(row)
      df = pd.DataFrame(probability)
      print(probability[:,0])
      thresh = 10
      return probability[:,0]*thresh

   if request.method == "POST":
      
      result = request.form
      Name = request.form["Names"]
      loan_amount = request.form["loan_amount"]
      funded_amount = request.form["funded_amount"]
      Duration = request.form["Duration"]
      ints = request.form["int"]
      Installment = request.form["Installment"]
      emp = int(request.form["emp"])
      home = request.form["Home"]
      Annual = request.form["Annual"]
      verification = request.form["verification"]
      purpose = request.form["purpose"]
      age = request.form["age"]
      ids = request.form["id"]
      no = request.form["no"]
      sent = request.form["sent"]
      received = request.form["received"]
      creditors = request.form["creditors"]


      Home = str(['RENT' if home.upper()=="RENT" else 'OWN' if home.upper() == "OWN" else 'MORTGAGE'if home.upper() == "MORTGAGE" else'OTHER_Home_Ownership'][0])
      Loan_Purpose = str(['small_business' if purpose.lower() == "business"  else "educational" if purpose.lower() == "school" else 'OTHER_Purposes' ][0])

      
      loan_duration = str([' 36 months' if Duration == 36 else ' 60 months'][0])
      employment_length = str([ '< 1 year' if emp <1 else '1 year' if emp ==1 else '3 years' if emp==3 else '8 years' if emp ==8 else '9 years' if emp==9 else  '4 years' if emp ==4 else '5 years' if emp==5 else '6 years' if emp== 6 else '2 years' if emp==2 else '7 years' if emp ==7 else '10+ years'][0])
      
      Verification_status =str( ['Verified' if verification.capitalize() == "Verified" else 'Not Verified'][0])
      df = cleaner(loan_amount,funded_amount,loan_duration,ints,Installment,employment_length,Home,Annual,Verification_status,Loan_Purpose)
   #score = credit_score(df)[0]
      score = credit_score(df)
      scores = scored(2,int(sent),int(received),int(creditors),score)

      
      H = plt.pie([1,3,4,2])
      plt.savefig('new_plot.png')

     
  
      print(df.shape)
      print(score)
   return render_template("result.html", score =scores,result = result ,name = Name,age = age,id = ids,)
if __name__ == "__main__":
   app.run(debug = True)