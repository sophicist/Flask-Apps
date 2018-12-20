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

app = Flask(__name__)
print(os.listdir())

 
   
@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST'])
def result():
   X1 = pd.read_csv("X1.csv")
   Y1 = pd.read_csv("Y1.csv")
   
   X_train,X_test,Y_train,Y_test = train_test_split(X1,Y1,test_size = 0.2)
   sc = MinMaxScaler()
   clf1 = RandomForestClassifier(n_estimators = 100 ,verbose=1,random_state=324) 
   clf = LogisticRegression(penalty='l1', C=0.01,verbose = 1)

   Model = Pipeline([('scaler', sc), ('clf1', clf1)])
   Model.fit(X_train, Y_train)

   def credit_score(row):
    probability = Model.predict_proba(row)
    df = pd.DataFrame(probability)
    print(probability[:,0])
    thresh = 10
    return float(probability[:,0]*thresh)

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
      Home = str(['RENT' if home.upper()=="RENT" else 'OWN' if home.upper() == "OWN" else 'MORTGAGE'if home.upper() == "MORTGAGE" else'OTHER_Home_Ownership'][0])
      Loan_Purpose = str(['small_business' if purpose.lower() == "business"  else "educational" if purpose.lower() == "school" else 'OTHER_Purposes' ][0])

      
      loan_duration = str([' 36 months' if Duration == 36 else ' 60 months'][0])
      employment_length = str([ '< 1 year' if emp <1 else '1 year' if emp ==1 else '3 years' if emp==3 else '8 years' if emp ==8 else '9 years' if emp==9 else  '4 years' if emp ==4 else '5 years' if emp==5 else '6 years' if emp== 6 else '2 years' if emp==2 else '7 years' if emp ==7 else '10+ years'][0])
      
      Verification_status =str( ['Verified' if verification.capitalize() == "Verified" else 'Not Verified'][0])
      df = cleaner(loan_amount,funded_amount,loan_duration,ints,Installment,employment_length,Home,Annual,Verification_status,Loan_Purpose)
   #score = credit_score(df)[0]
      score = credit_score(df)
  
      print(df.shape)
      print(score)
   return render_template("result.html", score =score,result = result )

if __name__ == '__main__':
   app.run(debug = True)