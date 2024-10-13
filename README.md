# Text mining scholarly API

The project helps download the full text of scholarly publications for a given list of DOIs using the Crossref API. It then stores the full text files in a MongoDB database. 

The project runs using Python3 code and requires the following Python libraries:
1. habanero
2. pymongo
3. bson
4. requests
5. lxml
6. io

For more detailed descriptions for running, please refer to the `requirements.txt` file. 


`dois.txt` : Text file that contains the 286 DOIs

`output.txt` : Text file that produces after running through the API pipeline

`pipeline-habanero.py` : Python file that contains code to run the API pipeline 

`scopus-api-mining.py` : Python file that extracts full text for Elsevier DOIs

`requirements.txt` : Text file that contains which Python packages are needed and a thorough explanation for how to run the code

`setup.sh` : UNIX shell scripting file that downloads all necessary packages needed to run the Python files
