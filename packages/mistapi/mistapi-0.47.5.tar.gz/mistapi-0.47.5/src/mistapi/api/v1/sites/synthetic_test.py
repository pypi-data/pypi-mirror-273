'''
--------------------------------------------------------------------------------
------------------------- Mist API Python CLI Session --------------------------

    Written by: Thomas Munzer (tmunzer@juniper.net)
    Github    : https://github.com/tmunzer/mistapi_python

    This package is licensed under the MIT License.

--------------------------------------------------------------------------------
'''

from mistapi import APISession as _APISession
from mistapi.__api_response import APIResponse as _APIResponse
import deprecation

def getSiteSyntheticTestStatus(mist_session:_APISession, site_id:str) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSyntheticTestStatus
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    site_id : str        
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/synthetic_test"
    query_params={}
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def triggerSiteSyntheticTest(mist_session:_APISession, site_id:str, body:object) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/triggerSiteSyntheticTest
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    site_id : str        
    
    BODY PARAMS
    -----------
    body : dict
        JSON object to send to Mist Cloud (see API doc above for more details)
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/synthetic_test"
    resp = mist_session.mist_post(uri=uri, body=body)
    return resp
    