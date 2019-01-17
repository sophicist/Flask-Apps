import pickle
import random
import numpy as np
import pandas as pd


def cleaner(loan_amnt,funded_amnt,term,int_rate,installment,emp_length,home_ownership,annual_inc,
            verification_status,purpose,**kwargs):
    
    cols = ['loan_amnt','funded_amnt','term','int_rate','installment','emp_length','home_ownership','annual_inc',
            'verification_status','purpose']
    import pandas as pd
    data = pd.DataFrame(columns =cols )
    data.loc[0 ] = (loan_amnt,funded_amnt,term,int_rate,installment,emp_length,home_ownership,annual_inc,
            verification_status,purpose)
    # Create Dummies
    lis = ['term','emp_length','home_ownership','verification_status','purpose']
    df_clean = pd.DataFrame(index = data.index)
    for i in lis:
        H = data[i]

        H_dum = pd.get_dummies(H)

        B = pd.concat((df_clean,H_dum),1)
        df_clean = B

        
    df_cleans = pd.concat((data,B),1)
    df_cleans = df_cleans[df_cleans.columns.difference(lis)]
    others  =  [' 36 months', ' 60 months', '1 year', '10+ years', '2 years', '3 years',
       '4 years', '5 years', '6 years', '7 years', '8 years', '9 years',
       '< 1 year', 'MORTGAGE', 'Not Verified', 'OTHER_Home_Ownership',
       'OTHER_Purposes', 'OWN', 'RENT', 'Source Verified', 'Verified',
       'annual_inc', 'car', 'credit_card', 'debt_consolidation', 'educational',
       'funded_amnt', 'home_improvement', 'house', 'installment', 'int_rate',
       'loan_amnt', 'major_purchase', 'medical', 'moving', 'renewable_energy',
       'small_business', 'vacation', 'wedding']
    for i in others:
        if not i in df_cleans.columns:
            df_cleans[str(i)] = 0 
            
            
    print(df_cleans.shape)
    return df_cleans

def credit_score(row):
    probability = Model.predict_proba(row)
    df = pd.DataFrame(probability)
    print(probability[:,0])
    thresh = 10
    return probability[:,0]*thresh
