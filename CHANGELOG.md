# CHANGELOG

### v0.0.26 - 2026-06-19

* Due to usage of the client library change, the .p2f config file and setup is removed. As most interaction and use of the p2f-client-py library will be through the Streamlit based Portal, variable based usage will be better. In the future the authentication method will be moved to OpenID Connect (OIDC) and this method will go away. 

### v0.0.25 - 2026-06-19

* Add Season
* Add seasonality

### v0.0.24 - 2026-06-19

* Together with v0.0.23 as CHANGELOG was missed
* Add keywords with v0.0.80 of the API library

### v0.0.22 - 2026-06-08

* More bug fixes from previous authorization method

### v0.0.21 - 2026-06-08

* Upgrade minimum p2f-pydantic version
* Bug fixes from p2f-pydantic upgrade

### v0.0.20 - 2026-05-04

* Fix issue with .p2f/CONFIG file and TOKEN vs TOKEN_EXPIRATION parameter recognition
* Re-align with API and new security model with API Key and Email in headers

### v0.0.18 - 2026-04-21

* Elaborate more the README.md
* Add .data_model to client libraries for easy p2f-pydantic model access

### v0.0.17 - 2026-04-21

* Add link_git functionality to link a git repository to a dataset
* Change authorization json serializer name
* Add and fix assign and remove urls and methods within several functions

### v0.0.16 - 2026-04-21

* Added docstrings to client library
* Removed the queue and upload queue functions
* Removed the queue and upload queue example from the client_library_testing.ipynb
* Filled out more return types in many objects