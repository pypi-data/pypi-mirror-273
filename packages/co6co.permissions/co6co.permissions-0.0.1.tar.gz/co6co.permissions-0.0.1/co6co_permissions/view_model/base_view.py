from co6co_web_db.view_model import BaseMethodView,Request
from ..model.pos.right import UserPO

from .aop.api_auth import authorized


def getCtxUserId(request:Request):
   return request.ctx.current_user["id"]  

def getCtxData(user:UserPO):
   """
   通过user获取 dict 保存在 request.ctx.current_user 中 
   """
   return user.to_jwt_dict()

class AuthMethodView(BaseMethodView): 
   decorators=[authorized] 
   
   def getUserId(self, request: Request):
      """
      获取用户ID
      """  
      return getCtxUserId(request)
   
   def getUserName(self, request: Request): 
       """
       获取当前用户名
       """
       current_user=request.ctx.current_user  
       return current_user.get("userName") 
      