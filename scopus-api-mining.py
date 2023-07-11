import requests
import pymongo
from bson.binary import Binary

client = pymongo.MongoClient() # connecting to MongoDB client 
mydb = client["career_project_dreu"] # accessing database
mycol = mydb["publications"] # accessing collection in that database 

# Download full text locally
def download_full_text(doi, api_key, output_format='xml'):
    url = f'https://api.elsevier.com/content/article/doi/{doi}?apiKey={api_key}&httpAccept=text%2F{output_format}'
    response = requests.get(url)

    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        if content_type.startswith('text/'):
            if (output_format == "plain"):
                filename = f'{doi.replace("/", "_")}.txt'
            else:
                filename = f'{doi.replace("/", "_")}.xml'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Full text downloaded and saved as '{filename}'")
        else:
            print("Error: Unexpected content type received.")
    else:
        print(f"Error: Failed to retrieve full text. Status code: {response.status_code}")
     
# Store full text in database    
def store_full_text(doi, api_key, output_format='xml'):
    url = f'https://api.elsevier.com/content/article/doi/{doi}?apiKey={api_key}&httpAccept=text%2F{output_format}'
    response = requests.get(url)

    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        if content_type.startswith('text/'):
            if (output_format == "plain"):
                mycol.update_one({'DOI': doi}, {'$set': {'plain_text': Binary(response.content)}})
            else:
                mycol.update_one({'DOI': doi}, {'$set': {'xml_text': Binary(response.content)}})
            print("Full text stored in MongoDB")
        else:
            print("Error: Unexpected content type received.")
    else:
        print(f"Error: Failed to retrieve full text. Status code: {response.status_code}")
        


# Testing
doi = '10.1016/j.cell.2005.01.027'
api_key = '11852fb061166663a048c15071f4d873'

store_full_text(doi, api_key, output_format='xml')
store_full_text(doi, api_key, output_format='plain')