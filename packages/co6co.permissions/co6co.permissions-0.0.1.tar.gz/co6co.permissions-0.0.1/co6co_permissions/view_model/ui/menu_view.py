
from sanic.response import text
from sanic import Request
from co6co_sanic_ext.utils import JSON_util
from co6co_sanic_ext.model.res.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.sql import Select ,or_,and_
from co6co_db_ext.db_utils import db_tools
from ..base_view import AuthMethodView
from ...model.enum import menu_type
from ...model.pos.right import menuPO 
from ...model.filters.menu_filter import menu_filter

  
class ui_tree_view(AuthMethodView):
    routePath="/tree"
    
    async def get(self, request: Request):
        """
        树形选择下拉框数据
        selectTree :  el-Tree
        """
        
        select = (
            Select(menuPO.id, menuPO.category, menuPO.parentId,menuPO.name, menuPO.code, menuPO.icon,  menuPO.url,menuPO.component,menuPO.permissionKey )

            .filter(  or_( menuPO.category.__eq__(menu_type.view.val),menuPO.category.__eq__(menu_type.button.val)))
            .order_by(menuPO.parentId.asc())
        )
        def getRoot(i:dict)->bool:
            return i.get("category")==menu_type.view.val
        return await self.query_tree(request,select,getRoot, pid_field='parentId', id_field="id", isPO=False)

    async def post(self, request: Request):
        """
        树形 table数据
        tree 形状 table
        """
        param = menu_filter()
        param.__dict__.update(request.json)
        if len(param.filter()) > 0:
            return await self.query_page(request, param)
        return await self.query_tree(request, param.create_List_select(), rootValue=0, pid_field='parentId', id_field="id")

 