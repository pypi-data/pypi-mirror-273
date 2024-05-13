
from functools import wraps
from sanic import Blueprint,Sanic
from sanic.response import  json
from sanic.request import Request 

from co6co_web_db.services.jwt_service import validToken
from co6co_db_ext.res.result import Result
from co6co_sanic_ext.utils import JSON_util 

def authorized(f): 
    @wraps(f)
    async def decorated_function(request:Request, *args, **kwargs):
        # run some method that checks the request
        # for the client's authorization status
        is_authorized = await validToken(request,request.app.config.SECRET)
        # //dodo debug
        #is_authorized= True

        if is_authorized:
            # the user is authorized.
            # run the handler method and return the response
            response = await f(request, *args, **kwargs)
            return response
        else:
            # the user is not authorized.
            return JSON_util.response(Result.fail(message="not_authorized"), status= 403)
    return decorated_function 