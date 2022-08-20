from numpy.lib.function_base import append
import streamlit as st
import pandas as pd
import time
from matplotlib import pyplot as plt
from streamlit.proto.NumberInput_pb2 import NumberInput
from plotly import graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np

data=pd.read_csv("salary.csv")

x=np.array(data['YearsExperience']).reshape(-1,1)
lr=LinearRegression()
lr.fit(x,np.array(data['Salary']))

st.title("\n\n Earnalyzer \n\n")

nav=st.sidebar.radio("Navigation",["Home","Prediction","Contribute","About me"])

if nav=="Home":
    st.image("Earnalyzer-logos_white.png",width=130)
    
    if st.checkbox("Show Data"):
        st.table(data)

    gr_opt=st.selectbox("What kind of graph do you want to analyze?",["Interactive","Non-Interactive"])

    val=st.slider("Filter data using years: ",0,20)
    data=data.loc[data["YearsExperience"]>=val]
    if gr_opt== "Non-Interactive":
        plt.figure(figsize=(10,5))
        plt.scatter(data["YearsExperience"],data["Salary"])
        plt.ylim(0)
        plt.xlabel("Years of experience")
        plt.ylabel("Salary")
        plt.tight_layout()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    if gr_opt=="Interactive":
        layout=go.Layout(
            xaxis=dict(range=[0,20]),
            yaxis=dict(range=[0,300000])
        )
        fig=go.Figure(data=go.Scatter(x=data["YearsExperience"],y=data["Salary"],mode="markers"), layout = layout)
        st.plotly_chart(fig)


if nav=="Prediction":
    st.header("Know your salary")
    val=st.number_input("Enter your experience: ",0.00,30.00,step=0.5)
    val=np.array(val).reshape(1,-1)
    pred=lr.predict(val)[0]

    if st.button("Predict"):
        progress=st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)
        st.success(f"Your predicted salary is: {round(pred)}")
        st.balloons()

if nav=="Contribute":
    st.header("Contribute to our dataset.")
    ex=st.number_input("Enter your experience: ",0,30)
    sal=st.number_input("Enter your salary: ",0.00,200000.00,step=1000.00)
    if st.button("SUBMIT"):
        to_add={"YearsExperience":ex,"Salary":sal}
        to_add=pd.DataFrame(to_add,index=[0])
        to_add.to_csv("salary.csv",mode='a',header=False,index=False)
        st.success("Submitted")
        st.balloons()