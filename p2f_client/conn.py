import requests
from requests.exceptions import HTTPError
from furl import furl

def eval_non_ok_return(return_code):
    """Raises warnings and errors for the user

    :param return_code: int or requests.status_code
    :type return_code: Errors and Warnings
    """
    DeveloperReportText = "Please report this error to the P2F developer with the context of which functions you were using, and rougly the time you experienced the error."
    match return_code:
        case 400:
            raise HTTPError(f"400: Bad request. {DeveloperReportText}")
        case 401:
            raise HTTPError("401: Your credentials are unauthorized, are you a member of the P2F consortium or are you using an expired token?")
        case 403:
            raise HTTPError("403: You do not have the permissions to perform this action. If you believe you should, contact the P2F administrator")
        case 404:
            raise HTTPError("404: Requested object not found, perhaps the object you were looking for has changed or has been deleted")
        case 405:
            raise HTTPError(f"405: Method not allowed.  {DeveloperReportText}")
        case 406:
            raise HTTPError(f"406: There was an error with data exchange with this action.  {DeveloperReportText}")
        case 408:
            raise HTTPError("408: The action took too long on your client side, please try again in a few seconds")
        case 409:
            raise HTTPError("409: The action is in conflict with another action, please try again in a few seconds")
        case 410:
            raise HTTPError("410: The resource you were looking for is gone, if you believe this is a mistake please contact the p2f admin")
        case 422:
            raise HTTPError(f"422: The action was unprocessable. {DeveloperReportText}")
        case 429:
            raise HTTPError("429: The server is reporting you are making too many requests, please add sleeps to your upload script and try again in a few minutes")
        case 500:
            raise HTTPError(f"500: The server experienced an error. {DeveloperReportText}")
        case 501: 
            raise HTTPError(f"501: Not implemented. {DeveloperReportText}")
        case 502: 
            raise HTTPError("502: There was a connection issue within the P2F infrastructure, please try again in a few minutes. ")
        case 503:
            raise HTTPError("503: Service unavailable, please try again in a few minutes. The service can be unavailable when a new API version is rolled out.")
        case 504:
            raise HTTPError("504: The server took too long to respond, please try again in a few minutes")
        case 505:
            raise HTTPError(f"505: HTTP version not supported. {DeveloperReportText}")
        case _:
            raise HTTPError(f"{return_code}: An exceptional exception has occured.  {DeveloperReportText}. Please include the HTTP error code ({return_code}) in your report of the issue to the P2F developer. ")

        
ACCEPT_DICT = {"json": "application/json",
               "parquet": "application/vnd.apache.parquet",
               "csv": "text/csv",
               "pandas": "application/vnd.apache.parquet"}
ACCEPT_LIST = ["csv", "json", "parquet", "pandas"]