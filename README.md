# p2f-client-py
Python client library for the Past to Future projects Portal. Past to Future is an EU Horizon funded project. 

## Installation

    pip install p2f-client-py


## Usage

Create a client

    from p2f_client import P2F_Client

    p2f_api_url = "{fill in API URL here}"
    port = 443

    client = P2F_Client(hostname=p2f_api_url, https=True, email="your@email.dm")

    # request a token
    client.request_token()

    # Open your local file and update the configuration with your new p2f token. 
    client.set_token()

On your first usage of the client on a computer the library will create a .p2f folder for storing a configuration of your account. 
A config file is used because this will prevent tokens from being uploaded to a remote Git repository where they could theoretically be exploited. 

## Authentication

If you are a member of the P2F Consortium, your email has been registered with the API as allowed to perform certain actions. 
As seen in the usage above, you need to request a token, which will make a request to the API, the API will then send you an email from the project email address with a token. 
The token is a password that is valid for 24-hours (subject to change in the future). 
You will need to add the token to the config file which will be located in your user profile folder at `.p2f/CONFIG`. 
The function in the client `.set_token()` will give you the path for the token. 
When you request a token the client will add a timestamp into the config file to indicate when the token expires. 
5 minutes after requesting a token, if you make another request, nothing will happen, if you're still waiting on the token, please be patient, it should arrive. 
If a token never arrives, please message the P2F Portal developer. 
The API uses the email and token in almost every request, and will block most un-authenticated requests. 

## Library Naming Conventions

Within this client library are sub-clients for interacting with datasets, data, locations, references, etc on the API. 
Within each of these are functions to perform the different interactions:

* upload - directly upload an item to the API
* list - get a list of items, with filters to narrow down your results
* get - get a single item by its item type id
* delete - delete a record by its item type id
* assign - assign an item type (through its id) to either a record or dataset
* remove - remove the assigned item type from its associated record or dataset, does not delete the item type

## Data Types 

The P2F portal has many different kinds of data to represent, for the different kinds of portal data items (datasets, records, species, locations, etc), in this README they will be referred to as item types. 

The P2F portal is a relational model where most items are related to a dataset directly, or to a dataset indirectly through a record. 
Datasets are any collection of data, preferrably with a DOI, datasets are identified by `dataset_id`. 
Records are individual data points (or rows) within a dataset, records are identified by their `record_hash`. 

Items that associate directly to a Dataset:

* Sub-datasets
* Records
* Git Repositories

Items that associate directly to a Record:

* HARM Numerical - Harmonized Numerical records, Integer, Integer with Confidence Interval, Float, Float with Confidence Interval
* HARM Species
* HARM Location
* HARM Timeslice - A named timeslice from the P2F project
* HARM Age - The calculated represented age for a data point in years before present
* HARM Reference

Items that associate to HARM Numerical:

* HARM Data Type

## Pydantic

The above items are all defined by a Pydantic object.
Pydantic is a library that allows validates data structures and are easily convertible to dictionaries and json strings. 
These data structures are very handy for standardizing the data that goes into the portal, and required for the API library. 
A p2f-pydantic library was created as a separate project to standardize the data models of the API and this client library. 
When you install p2f-client-py, p2f-pydantic is a dependency and will be installed alongside, so you can `import p2f_pydantic` objects as necessary. 

HOWEVER, new in v0.0.18, each of the item classes has a `.data_type` that references the p2f_pydantic object directly