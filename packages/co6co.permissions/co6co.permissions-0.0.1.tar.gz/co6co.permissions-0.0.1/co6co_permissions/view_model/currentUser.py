from sanic.response import text
from sanic import  Request  
from co6co_sanic_ext.utils import JSON_util
from co6co_sanic_ext.model.res.result import  Result   
from sqlalchemy.ext.asyncio import AsyncSession 

from sqlalchemy.sql import Select,Delete
from co6co_db_ext.db_utils  import db_tools
from co6co_web_db.model.params import associationParam


from .base_view import AuthMethodView
from ..model.pos.right import UserPO, RolePO,UserRolePO,AccountPO
from ..model.filters.user_filter import user_filter


class changePwd_view(AuthMethodView):
    routePath="/changePwd" 
    async def post(self, request:Request ): 
        """
        修改密码：
        {
               oldPassword:""
               newPassword:""
        }
        """ 
        data=request.json
        current_user=request.ctx.current_user 
        self.getUserId()
        userName=current_user.get("userName") 
        oldPassword=data["oldPassword"]
        password=data["newPassword"] 
        select=(Select(UserPO).filter(UserPO.userName==userName))
        async def edit(_,one:UserPO): 
            if one!=None:
                if one.password!=one.encrypt(oldPassword) :return JSON_util.response(Result.fail(message="输入的旧密码不正确！"))
                one.password=one.encrypt(password)
            return JSON_util.response(Result.success()) 
        return await self.update_one(request,select,edit) 

class user_info_view(AuthMethodView):
    routePath="/currentUser" 
    async def get(self, request:Request):
        """
        当前用户信息  
        return {
            data:{
                avatar:""
                remark:""
            } 
        }
        """ 
        userName=self.getUserName(request)
        select=Select(UserPO.avatar,UserPO.remark).filter(UserPO.userName==userName)
        dict= self.get_one(request,select,isPO=False)
        return JSON_util.response(Result.success(data=dict)) 
     

            