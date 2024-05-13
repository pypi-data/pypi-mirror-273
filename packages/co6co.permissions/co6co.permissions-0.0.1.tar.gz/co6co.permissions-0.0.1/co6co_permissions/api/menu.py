

from sanic import Sanic, Blueprint,Request
from ..view_model.menu_view import menu_tree_view,menu_view,menus_view
from co6co_sanic_ext.api import add_routes

menu_api = Blueprint("menu_API",url_prefix="/menu") 
add_routes(menu_api,menus_view,menu_tree_view,menu_view)
'''
menu_api.add_route(menus_view.as_view(),"/",name=menus_view.__name__) 
menu_api.add_route(menu_tree_view.as_view(),"/tree",name=menu_tree_view.__name__) 
menu_api.add_route(menu_view.as_view(),"/<pk:int>",name=menu_view.__name__) 
'''
 