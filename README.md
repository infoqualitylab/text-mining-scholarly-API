# Text mining scholarly API

The project helps download the full text of scholarly publications for a given list of DOIs using the Crossref API. It then stores the full text files in a MongoDB database. 

This code is used in the following studies:

Zheng, H. Fu, Yuanxi, Sarol, J. M., Sarraf, I., Schneider J. “Addressing Unreliability Propagation in Scientific Digital Libraries.” Accepted to the ACM/IEEE-CS Joint Conference on Digital Libraries 2024, Hong Kong. [https://doi.org/10.1145/3677389.3702526] (https://doi.org/10.1145/3677389.3702526)

Sarraf, I., Fu, Y., Schneider, J. (2023, October 27). “Text Mining Scholarly Publications using APIs.” METSTI 2023: Workshop on Informetric, Scientometric, and Scientific and Technical Information Research, Association for Information Science and Technology, London. [https://doi.org/10.5281/zenodo.10581542] (https://doi.org/10.5281/zenodo.10581542)

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
