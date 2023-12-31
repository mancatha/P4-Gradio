import gradio as gr
import pandas as pd 
import numpy as np
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier


# key lists
expected_inputs = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure','PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity','OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV','StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod','MonthlyCharges', 'TotalCharges']
numerics = ['tenure', 'MonthlyCharges', 'TotalCharges']
categoricals = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService','MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup','DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies','Contract', 'PaperlessBilling', 'PaymentMethod']
# Load the model and pipeline

# Define helper functions
# Function to load the pipeline
def load_pipeline(file_path = r"model\pipeline.pkl"):
    with open(file_path, "rb") as file:
        pipeline = pickle.load(file)
    return pipeline

# Import the model
model= RandomForestClassifier()
model=joblib.load(r"model\ml.pkl")

# Instantiate the pipeline
pipeline= load_pipeline()

scaler = None
encoder = None

# Function to process inputs and return prediction


def predict_customer_attrition(*args, pipeline=pipeline, model=model, scaler= scaler, encoder=encoder):
    # Convert inputs into a dataframe
    input_data = pd.DataFrame([args], columns=expected_inputs)
    

    # Make the prediction 
    model_output = pipeline.predict(input_data)

    if model_output == "Yes":
        prediction = 1
    else:
        prediction = 0


    # Return the prediction
    return {"Prediction: Customer is likely to LEAVE": prediction,
            "Prediction: Customer is likely to STAY": 1 - prediction}
# Define a function for text prediction
def predict(text):
    # Your text prediction code here
    return "Prediction: " + text

      # Set up interface
    # Inputs
gender= gr.Dropdown(label = "What is the gender of the customer?", choices = ["Female", "Male"], value= "Male")
SeniorCitizen= gr.Dropdown( label="Is the customer a senior citizen?", choices= ["No","Yes"], value="No")
Partner= gr.Radio(label= "Does the customer have a partner?", choices= ["No", "Yes"], value="No")
Dependents= gr.Radio(label= "Does the customer have dependents?", choices= ["No", "Yes"], value="No")
tenure= gr.Number(label= "How many months has the customer stayed with the company?", minimum= 1, maximum= 72, interactive= True, value= 1, step =1)
PhoneService= gr.Dropdown(label=" Does the customer has a phone service?", choices=["No", "Yes"],interactive=True, value= "Yes")
MultipleLines= gr.Radio(label="Does the customer has multiple lines?", choices=["No", "Yes", "No phone service"], value="No")
InternetService= gr.Dropdown(label="What is the customer's internet service provider?", choices=["Fiber optic", "DSL", "No Internet Service"], value="Fiber optic")
OnlineSecurity= gr.Radio(label="Does the customer has online security?", choices=["No", "Yes", "No internet service"], value="No")
OnlineBackup= gr.Radio(label="Does the customer has online backup?", choices=["No", "Yes", "No internet service"], value="No")
DeviceProtection= gr.Dropdown(label="Does the customer has device protection?", choices=["No", "Yes", "No internet service"], value="No")
TechSupport= gr.Radio(label="Does the customer have tech support?", choices=["No", "Yes", "No internet service"], value="No")
StreamingTV= gr.Dropdown(label="Does the customer stream TV?", choices=["No", "Yes", "No internet service"], value="No")
StreamingMovies= gr.Dropdown(label="Does the customer stream movies?", choices=["No", "Yes", "No internet service"], value="No")
Contract= gr.Radio(label="What is the contract term of the customer?", choices=["Month-to-month", "Two year", "One year"], value="Month-to-month")
PaperlessBilling= gr.Dropdown(label="Does the customer has paperless billing?", choices=["No", "Yes"], value="Yes")
PaymentMethod= gr.Dropdown(label="What is the customer's payment method?", choices=["Electronic check", "Mailed check", "Credit card (automatic)","Bank transfer (automatic)"], value="Electronic check")
MonthlyCharges= gr.Slider(label= "What is the monthly amount charged to the customer?", minimum= 15, maximum= 150, value= 20, interactive= True)    
TotalCharges= gr.Slider(label= "What is the total amount charged to the customer?", minimum= 15, maximum= 9000, value= 220, interactive= True)




# Create the Gradio interface
gr.Interface(inputs=[gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges ],
             fn=predict_customer_attrition,
             outputs= gr.Label("Awaiting Submission...."),
             title="Telecommunication Customer Attrition Prediction App",
             description="This app was created by Santorini during our Project 4 ", live=True).launch(inbrowser=True, show_error=True)


