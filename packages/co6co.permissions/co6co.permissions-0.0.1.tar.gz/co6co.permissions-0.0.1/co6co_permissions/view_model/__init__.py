from ..api.menu import menu_api
from ..api.user import user_api
from .aop.api_auth import authorized
from sanic.response import text
from sanic import Request
from co6co_sanic_ext.utils import JSON_util
from co6co_sanic_ext.model.res.result import Result

from ..model.enum import menu_type, menu_state,user_state
from co6co_db_ext.db_utils import db_tools 
from ..model.pos.right import UserPO

"""
__init__.py 还是有其他用处的

菜单
""" 
@menu_api.route("/status", methods=["GET", "POST"])
@authorized
async def getMenuStatus(request: Request):
    """
    菜单状态
    """
    states = menu_state.to_dict_list()
    return JSON_util.response(Result.success(data=states))


@menu_api.route("/category", methods=["GET", "POST"])
@authorized
async def getMenuCategory(request: Request):
    """
    菜单类别
    """
    states = menu_type.to_dict_list()
    return JSON_util.response(Result.success(data=states))

"""
用户
"""
@user_api.route("/status", methods=["GET", "POST"])
@authorized
async def getUserStatus(request: Request):
    """
    用户状态
    """
    states = user_state.to_dict_list()
    return JSON_util.response(Result.success(data=states))

@user_api.route("/exist/<userName:str>/<pk:int>", methods=["GET"])
@authorized
async def userExist(request: Request,userName:str,pk:int=0): 
        """
        用户名是否存在
        """
        result=await db_tools.exist(request.ctx.session,UserPO.userName==userName,UserPO.id!=pk)
        if result:return JSON_util.response(Result.success(message=f"用户'{userName}'已存在。"))
        else: return JSON_util.response(Result.fail(  message=f"用户'{userName}'不已存在。"))

@user_api.route("/exist", methods=["POST"])
@authorized
async def userExistPost(request: Request ):   
    """
    用户名是否存在
    """
    id=request.json.get("id")
    userName=request.json.get("userName")
    result=await db_tools.exist(request.ctx.session,UserPO.userName==userName,UserPO.id!=id)
    if result:return JSON_util.response(Result.success(message=f"用户'{userName}'已存在。"))
    else: return JSON_util.response(Result.fail(  message=f"用户'{userName}'不已存在。"))


