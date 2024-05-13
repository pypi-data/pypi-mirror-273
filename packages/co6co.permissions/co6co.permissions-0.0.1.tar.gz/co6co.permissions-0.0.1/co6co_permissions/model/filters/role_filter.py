

from ..pos.right import RolePO
from sqlalchemy .orm.attributes import InstrumentedAttribute
from typing import Tuple
from co6co_db_ext.db_filter import absFilterItems
from co6co.utils import log
from sqlalchemy import func, or_, and_, Select


class role_filter(absFilterItems): 
    """
    角色 filter
    """ 
    name: str = None
    code: str = None 

    def __init__(self): 
        super().__init__(RolePO) 
 
    def filter(self) -> list:
        """
        过滤条件
        """
        filters_arr = []
        
        if self.checkFieldValue(self.name)  : 
            filters_arr.append(RolePO.name.like(f"%{self.name}%"))
        if self.checkFieldValue(self.code):
            filters_arr.append(RolePO.code.like(f"%{self.code}%")) 
        return filters_arr

   
    def getDefaultOrderBy(self) -> Tuple[InstrumentedAttribute]:
        """
        默认排序
        """
        return (RolePO.order.asc(),)
