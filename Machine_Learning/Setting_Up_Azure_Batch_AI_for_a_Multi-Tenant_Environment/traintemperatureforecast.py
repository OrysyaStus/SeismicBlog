from fbprophet import Prophet
import argparse
from modelfilemanager import readDataBlob, saveModel

def trainTemperatureForecast(customer, modelName, storage_account_name, storage_account_key):
    
    dataName ='historicalWeatherForecast'
    trainingData = readDataBlob(customer, dataName, storage_account_name, storage_account_key)
    
    #train the model
    model = Prophet()
    model.fit(trainingData)
    
    forecaster = {'model': model}
    
    saveModel(customer, modelName, forecaster, storage_account_name, storage_account_key)

# Accept the storage_account_name, storage_account_key, customer, and model name from the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--customer", help="Customer name")
parser.add_argument("-m", "--modelName", help="Model name")
parser.add_argument("-san", "--storage_account_name", help="Storage account name")
parser.add_argument("-sak", "--storage_account_key", help="Storage account key")

args = parser.parse_args()

customer = args.customer
modelName = args.modelName
storage_account_name = args.storage_account_name 
storage_account_key = args.storage_account_key
    
# Train the model
trainTemperatureForecast(customer, modelName, storage_account_name, storage_account_key)