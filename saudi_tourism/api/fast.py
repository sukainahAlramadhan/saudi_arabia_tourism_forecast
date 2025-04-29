from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

app = FastAPI()

def load_model(filename):

    loaded_model = pickle.load(open(filename, 'rb'))

    return loaded_model

@app.get("/")
def hello_world():
    return {"greating": "Hello World"}

@app.get("/predict")
def predict(
        year: str,  # 2014-07-06
    ):

    model1 = load_model('saudi_tourism/models/prophet_number_of_visitors.pkl') #renamae to demostic vistor number
    model2 = load_model('saudi_tourism/models/prophet_spends.pkl') #renamae to demostic vistor number #5 #rename to demostic spend
    model3 = load_model('saudi_tourism/models/AutoTBATS_number_of_visitors.pkl') #renamae to demostic vistor number #5 #rename to inbound visitor number
    model4 = load_model('saudi_tourism/models/AutoTBATS_spends.pkl')

    year_clean1 = pd.DataFrame({'ds': [year]}) # '2023-07-01'
    year_clean2 =  int(float(year) - 2024)

    pred_demo_vis = model1.predict(year_clean1)['yhat'] #for demostic visitors number
    pred_demo_spend = model2.predict(year_clean1)['yhat'] #for demostic spend
    pred_inbound_vis = model3.predict(year_clean2)#[-1] #for inbound visitors number
    pred_inbound_spend = model4.predict(year_clean2) #for inbound spend

    pred_inbound_vis_value = pred_inbound_vis.values()  # Correctly extract the float
    pred_inbound_spe_value = pred_inbound_spend.values()


    return {
    "year": year,
    "predicted number of domestic visitors": float(pred_demo_vis[0]),
    "predicted spending of domestic  visitors": float(pred_demo_spend[0]),
    "predicted number of inbound visitors": float(pred_inbound_vis_value[-1]),
    "predicted spending of inbound visitors": float(pred_inbound_spe_value[-1])
    }
