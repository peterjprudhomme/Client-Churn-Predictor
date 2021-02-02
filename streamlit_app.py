import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import base64
from sklearn.preprocessing import StandardScaler

st.write('''# *Client Churn Predictor*''')
  
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    st.write(
    '''
    ### Input Data ({} Customers)
    '''.format(input_df.shape[0])
    )
    st.dataframe(input_df)
    st.write('')
    rfm = pickle.load( open( "../Project 3/ran_forest_mod.p", "rb" ) )

    X = input_df.drop(labels = ['CustomerId'], axis = 1)

    threshold = .22
    y_preds = rfm.predict(X)
    predicted_proba = rfm.predict_proba(X)
    y_preds = (predicted_proba [:,1] >= threshold).astype('int')
    op_list = []
    for idx, exited in enumerate(y_preds):
        if exited == 1:
            op_list.append(input_df.CustomerId.iloc[idx])
    st.write('''### Number of Potentially Churning Customers''')
    st.write('''There are **{} customers** at risk of closing their accounts.'''.format(len(op_list)))

    csv = pd.DataFrame(op_list).to_csv(index=False, header = False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.write('''''')
    st.write('''''')
    st.write('''### **⬇️ Download At-Risk Customer Id's**''')
    href = f'<a href="data:file/csv;base64,{b64}" download="at_risk_customerids.csv">Download csv file</a>'
    st.write(href, unsafe_allow_html=True)
    
    

