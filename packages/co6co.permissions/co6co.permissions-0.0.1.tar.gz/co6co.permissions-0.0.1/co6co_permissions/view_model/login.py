
from co6co_web_db.view_model import BaseMethodView
from .base_view import getCtxData

from sanic.response import text
from sanic import  Request  
from co6co_sanic_ext.utils import JSON_util
from co6co_sanic_ext.model.res.result import  Result   
from sqlalchemy.ext.asyncio import AsyncSession 

from sqlalchemy.sql import Select,Delete
from co6co_db_ext.db_utils  import db_tools 
from co6co_web_db.services.jwt_service import createToken,setCurrentUser
from co6co.utils import log

from co6co_web_db.view_model import get_one
from ..model.pos.right import UserPO, RolePO,UserRolePO,AccountPO 
from .aop.login_log import loginLog

async def generateUserToken(request:Result,sessionId:str,data=None,userId:int=None,userOpenId:str=None,expire_seconds:int=86400): 
    token=""  
    SECRET=request.app.config.SECRET 
    if data!=None:
        token=await createToken(SECRET,data,expire_seconds)
    else: 
        select=Select(UserPO ).filter(UserPO.id.__eq__(userId)) 
        user:UserPO=await get_one(request,select)
        token=await createToken(SECRET,getCtxData(user),expire_seconds)  
    return  { "token":token,"expireSeconds":expire_seconds,"sessionId":str(sessionId),"role":userOpenId}




class login_view(BaseMethodView):
    routePath="/login" 
    @loginLog
    async def post(self, request:Request ): 
        """
        登录
        """
        where =UserPO()
        where.__dict__.update(request.json) 
        select=Select(UserPO ).filter(UserPO.userName.__eq__(where.userName)) 
        user:UserPO= await self.get_one(request,select)
        if user !=None:
            if user.password==user.encrypt(where.password):   
                token=await generateUserToken(request,user.id,user.to_jwt_dict(),expire_seconds=86400,userOpenId=user.userGroupId)
                await setCurrentUser(request,user.to_jwt_dict()) # loginLog 获取登录ID等
                return  JSON_util.response(Result.success(data=token, message="登录成功"))
            else :return JSON_util.response(Result.fail(message="登录用户名或者密码不正确!"))
        else:
            log.warn(f"未找到用户名[{where.userName}]。")
            return JSON_util.response(Result.fail(message="登录用户名或者密码不正确!")) 