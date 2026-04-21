import requests
from furl import furl

### We're having an issue with the API needing a connection
###   open to actually get data into the portal. Here we're
###   making a decorator function to probe the health-check
###   endpoint first, opening the connection to the API. 

def health_probe(base_url):
    """An untested decorator for performing a health check before making an API call"""
    def health_probe_func_level(func):
        base_url = furl(base_url)
        prefix = "health-check"
        healthcheckurl = base_url / f"{prefix}/"
        r = requests.get(healthcheckurl)
        if r.ok:
            # Run the decorated function
            def innerfunc(*args, **kwargs):
                return func(*args, **kwargs)
            return innerfunc
        else:
            # Due to above commented issue, if we can't get a GET, then raise an error
            raise requests.exceptions.HTTPError("The client could not connect to the API server.")
    return health_probe_func_level

def health_check(base_url: furl):
    """A basic function that is called to make sure the API is running. This is also
        important due to an issue with v0.0 API and the Ingress controller not sending
        data from the client to the API without an open connection. Using this function
        will open a connection that can be used for POST and PUT requests."""
    prefix = "health-check"
    healthcheck_url = base_url / f"{prefix}/"
    r = requests.get(healthcheck_url)
    if r.ok:
        return True
    else:
        return False