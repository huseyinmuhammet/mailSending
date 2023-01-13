"""This class is for establishing connection and communicate between 
our program and GoogleAPI. 
"""
#Libraries
import pickle 
import os
#Necassary google libraries
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    """ Creating connection on GoogleAPI 
    
    Args:
        client_secret_file (str): secret file name, credentials.json
        api_name(str): the API name, in our case API name is gmail
        api_version(str): the version of API
        scopes(tuple string list): authantication url address
    """
    print(client_secret_file, api_name, api_version, scopes, sep='-') #for feedback purposes
    #Initializations
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)
    
    #checking if pickle file's URL exist
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
    #checking if crediantial exist and valid
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    #preparing service features and checking if connection successfull
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None