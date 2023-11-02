import json
import pickle
import numpy as np
locations=None
__data_columns=None
__model=None

def get_estimated_price(sqft,location,bhk,bath):
    load_saved_artifacts()
    try:
        loc_index=__data_columns.index(location.lower())
    except:
        loc_index=-1
    X=np.zeros(len(__data_columns))
    X[0]=sqft
    X[1]=bath
    X[2]=bhk
    if(X[0]/X[2]>=500 and X[2]!=0 and X[1]!=0 ):
        if loc_index>=0:
            X[loc_index]=1
        if round(__model.predict([X])[0],2)>0:
            return round(__model.predict([X])[0],2)
        else:
            return "INVALID DATA"
    else:
        return "INVALID DATA !!!!"

def get_location_names():
    load_saved_artifacts()
    return __locations

def load_saved_artifacts():
    print("loading saved artifacts ... start")
    global __data_columns
    global __locations

    with open('./artifacts/columns.json','r') as f:
        __data_columns=json.load(f)['data_columns']
        __locations=__data_columns[3:]

    global __model
    with open('./artifacts/bengaluru_house_prices_model.pickle','rb') as f:
        __model=pickle.load(f)
    print("loading saved artifact...done")

if __name__=='__main__':
    print("hello")
    load_saved_artifacts()
    print(get_estimated_price(2000,'Indra Nagar',3,2))