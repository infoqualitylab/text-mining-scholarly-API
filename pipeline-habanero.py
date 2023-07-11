# Importing necessary libraries 
from __future__ import absolute_import
from habanero import Crossref   # python library that interacts with Crossref REST API
import requests     # used to send HTTP requests to the URL 
import pymongo  # used to access MongoDB database 
from bson.binary import Binary # used to convert full text to appropriate Binary format to store in MongoDB

cr = Crossref(mailto="sarraf.ishita@gmail.com")  # initializing instance of Crossref API and providing email address to get into the polite pool of Crossref API

client = pymongo.MongoClient() # connecting to MongoDB client 
mydb = client["career_project_dreu"] # accessing database
mycol = mydb["publications"] # accessing collection in that database 

# function to store doi in the database
# doi : string of DOI
def store_doi(doi):
    data = {'DOI':doi} 
    # Check if a document with the given DOI already exists
    check = mycol.find_one(data)
    if check:
        print("DOI already exists in the database.")
        return
    # else
    # Insert the publication data into the collection
    mycol.insert_one(data)

# function to get license url from the DOI
# doi : string of DOI
def get_license_url(doi):
    try:
        work = cr.works(ids=doi)  # retrieving metadata from DOI
        print(work)
        if "message" in work and "license" in work["message"]:  # checking if license url exists 
            license_url = work["message"]["license"][0]["URL"]  # saving license url 
            print(f"License URL for DOI {doi}: {license_url}")  # printing the license url 
            
            # Find the document with the matching DOI in the database 
            data = mycol.find_one({'DOI': doi})
            
            # Update the document with the license URL in the database 
            mycol.update_one({'_id': data['_id']}, {'$set': {'license_url': license_url}})
    
        else:
            print(f"No license information found for DOI: {doi}")  
    except Exception as e:
        print(f"Error occurred while retrieving license information for DOI: {doi}: {str(e)}")

# function to get pdf and xml urls (if the exist) from the DOI
# doi : string of DOI
def get_text_urls(doi):
    try:
        works = cr.works(ids=doi) # retrieving metadata from DOI
        # Find the document with the matching DOI
        data = mycol.find_one({'DOI': doi})
        if works and "message" in works:  
            message = works["message"]  # storing the 'message' dictionary from works 
            urls = {}  # empty dictionary to store the urls 
            if "link" in message:  # checking if urls exist 
                links = message["link"]  # storing the urls dictionary 
                for link in links:  # iterating through the urls 
                    if "URL" in link and "content-type" in link:  
                        url = link["URL"]  # accessing url 
                        content_type = link["content-type"]
                        intended_application = link.get("intended-application", "")  # storing intended application
                        if content_type == "application/pdf" or content_type == "application/xml" :  # checking if urls are either in .pdf or .xml format 
                            if intended_application == "text-mining": # checking if the urls can be text-mined 
                                urls[content_type] = url  # saving corresponding url with corresponding file type 
                                
                                # Update the document with the license URL in the database 
                                mycol.update_one({'_id': data['_id']}, {'$set': {content_type: url}})
                return urls   
            else:
                print(f"No URLs appropriate for text-mining found for DOI: {doi}")
        else:
            print(f"No information found for DOI: {doi}")
    except Exception as e:
        print(f"Error occurred while retrieving URLs for DOI: {doi}: {str(e)}")

# function to get title of the article from the DOI
# doi : string of DOI
def get_title(doi):
    try:
        works = cr.works(ids=doi)  # retrieving metadata 
        if works and "title" in works["message"]:  # checking if title exists
            title = works['message']['title'][0]  # storing title 
        return title 
    except Exception as e:
        print(f"Error occured in getting title of the paper:  {str(e)}")
        
# function to download full-text pdf and store locally 
# URL : string of the pdf url 
# title: string of the title 
def download_pdftext(URL, title):
    try:
        response = requests.get(URL)  # sends a GET request to the url 
        with open(f"{title}.pdf", 'wb') as file: # opens a pdf file to store locally 
            file.write(response.content)  # writes to file 
    except Exception as e:
        print("Error occured in downloading full text pdf: ", str(e))    
        
# function to download full-text xml and store locally 
# URL : string of the pdf url 
# title: string of the title 
def download_xmltext(URL, title):
    try:
        response = requests.get(URL)  # sends a GET request to the url 
        with open(f"{title}.xml", 'wb') as file:  # opens an xml file to store locally 
            file.write(response.content)  # write to file 
    except Exception as e:
        print("Error occured in downloading full text xml: ", str(e))

# function to store the pdf full-text in the database 
# URL : string of the pdf url 
# doi : string of DOI
def store_pdftext(URL, doi):
    try:
        response = requests.get(URL)  # sends a GET request to the url 
        
        # Update the document with the PDF text field
        mycol.update_one({'DOI': doi}, {'$set': {'pdf_text': Binary(response.content)}})
        
    except Exception as e:
        print("Error occured in storing full text pdf: ", str(e))

# function to extract the pdf text from mongoDB and store locally 
# doi : string of DOI
# title: string of the title    
def read_pdf_from_mongodb(doi, title):
    # Find the document by DOI
    document = mycol.find_one({'DOI': doi})
    # Access the PDF field and retrieve the binary data
    pdf_binary = document['pdf_text']
    
    # Save the binary data to a file
    with open(f"{title}.pdf", 'wb') as file:
        file.write(pdf_binary)
        
# function to store the pdf full-text in the database 
# URL : string of the xml url 
# doi : string of DOI
def store_xmltext(URL, doi):
    try:
        response = requests.get(URL)  # sends a GET request to the url 
        
        # Update the document with the XML text field
        mycol.update_one({'DOI': doi}, {'$set': {'xml_text': Binary(response.content)}})
        
    except Exception as e:
        print("Error occured in storing full text pdf: ", str(e))

# function to extract the xml text from mongoDB and store locally 
# doi : string of DOI
# title: string of the title    
def read_xml_from_mongodb(doi, title):
    # Find the document by DOI
    document = mycol.find_one({'DOI': doi})
    
    # Access the XML field and retrieve the binary data
    xml_binary = document['xml_text']
    
    # Save the binary data to a file
    with open(f"{title}.xml", 'wb') as file:
        file.write(xml_binary)
    
 
   
# Testing
doi = "10.7554/eLife.09561"   # Creative Commons

# doi = "10.1111/aman.13865"  # Wiley 

# doi = "10.1016/j.cell.2005.01.027" # Elsevier 

store_doi(doi)   # command to store DOI in database
get_license_url(doi)  # command to print and store license URL in database 
urls = get_text_urls(doi)  # command to store full text URLs in database 
print(urls)  # command to print the URLs
title = get_title(doi)  # command to get title of article 
print(title)  # command to print title of article 

#store_pdftext(urls["application/pdf"], doi)   # command to store pdf in database 

#store_xmltext(urls["application/xml"], doi)   # command to store xml in database 
