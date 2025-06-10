# import libraries
import pandas as pd
from fastapi import FastAPI, HTTPException, Header
from datetime import datetime
from pydantic import BaseModel


# membuat objek FastAPI
app = FastAPI()

# API KEY
key = 'Hacktiv8!'


# root endpoint
@app.get("/")
def getRoot():
    return {
        'msg' : 'Welcome the Simple API'
    }

# menampilkan data
@app.get("/data")
def getData():
    # read csv
    df = pd.read_csv('dataset.csv')

    return df.to_dict(orient='records')

@app.get("/data/{location}")
def getDataLocation(location:str):
    
    # read data
    df = pd.read_csv('dataset.csv')

    # filter data
    df_filter = df[df['location']==location]

    # validasi
    if len(df_filter) == 0 :
        raise HTTPException(status_code=404, detail='Location is not found !')

    # return data
    return df_filter.to_dict(orient='records')

# menghapus record
@app.delete("/del/{id}")
def deleteData(id:int, api_key:str = Header(None)):
    # load data
    df = pd.read_csv('dataset.csv')

    # exclude id
    result = df[df['id'] != id]

    # cek key
    if api_key != key or api_key == None :
        raise HTTPException(status_code=401, detail='You have no access !')

    # save
    result.to_csv('dataset.csv', index=False)

    return {
        'msg' :'Data has been deleted !'
    }

class Person(BaseModel):
    name:str
    age:int
    location:str

# function post, menambahkan data
@app.post("/post")
def addData(information:Person):
    # read dataframe
    df = pd.read_csv('dataset.csv')

    # get new id
    new_id = df.tail(1).id.values[0] + 1
    # add new row
    df.loc[len(df)] = [new_id, information.name, information.age, 
                       information.location, datetime.now().date()]
    
    # save
    df.to_csv('dataset.csv', index=False)

    return {
        'msg':'Data has been created !'
    }

# contoh put
@app.put("/update/{id}")
def updateLocation(id:int, location:str):
    # read data
    df = pd.read_csv('dataset.csv')

    # update
    df.loc[df['id'] == id, 'location'] = location

    # save
    df.to_csv('dataset.csv', index=False)

    return {
        'msg' : "Data has been updated !"
    }