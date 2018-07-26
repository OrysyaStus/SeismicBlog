import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from azure.storage.file import FileService
from azure.storage.blob import BlockBlobService
import pickle
import time

def uploadToBlobStorage(dataToUpload, customer, dataName, storage_account_name, storage_account_key):
    # Create a blob container for each customer
    blockblobService = BlockBlobService(account_name = storage_account_name, account_key = storage_account_key)
    blockblobService.create_container(customer) 
    
    # Upload the data to the correct blob container, under the correct dataname    
    blockblobService.create_blob_from_bytes(customer, dataName, dataToUpload)
    print('{} for {} has been uploaded'.format(dataName, customer))
    
def readDataBlob(customer, dataName, storage_account_name, storage_account_key):
    blockblobService = BlockBlobService(account_name=storage_account_name, account_key=storage_account_key)
    blobString = blockblobService.get_blob_to_bytes(customer.lower(), dataName).content
    df = pd.DataFrame(np.fromstring(string=blobString, dtype=(np.record, [('ds', '<M8[ns]'), ('y', '<f8')])))
    return df

def saveModel(customer, modelName, model, storage_account_name, storage_account_key):
    fileService = FileService(account_name=storage_account_name, account_key=storage_account_key)
    if not fileService.exists('trainedmodels', customer):
        fileService.create_share('trainedmodels')
        fileService.create_directory('trainedmodels', customer)
        
    if not fileService.exists('trainedmodels', customer + '/' + modelName):
        fileService.create_directory('trainedmodels', customer + '/' + modelName)
        
    modelPickle = pickle.dumps(model)
    timestr = time.strftime('%Y%m%d-%H%M%S')
    fileName = modelName + '_' + timestr+'.pkl'
    fileService.create_file_from_bytes('trainedmodels', customer + '/' + modelName, fileName, modelPickle)
    print(fileName + ' saved.')
        
def getLatestModel(customer, modelName, storage_account_name, storage_account_key):
    fileService = FileService(account_name=storage_account_name, account_key=storage_account_key)
    if fileService.exists('trainedmodels', customer):
        modelTimestampArr = []
        files = fileService.list_directories_and_files('trainedmodels', customer + '/' + modelName, prefix=modelName)
        
        for file in files:
            date = file.name.split('.')[0].split('_')[1]
            modelTimestampArr.append(date)
            
        latestModelFileName = modelName+'_'+max(modelTimestampArr)+'.pkl'
        print(latestModelFileName)
        
        file = fileService.get_file_to_bytes('trainedmodels', customer + '/' + modelName, latestModelFileName)
        model = pickle.loads(file.content)['model']
        return model
    else:
        print('Customer or model not found.')