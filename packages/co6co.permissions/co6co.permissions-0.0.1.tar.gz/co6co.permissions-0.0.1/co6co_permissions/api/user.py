from sanic import Sanic, Blueprint,Request
from co6co_sanic_ext .api import add_routes
from ..view_model.user import user_ass_view,users_view,user_view,sys_users_view
from ..view_model .currentUser import changePwd_view ,user_info_view
from ..view_model.login import login_view

user_api = Blueprint("users_API",url_prefix="/users") 
add_routes(user_api,login_view) 
add_routes(user_api,changePwd_view ,user_info_view)
add_routes(user_api,user_ass_view,users_view,user_view,sys_users_view) 
