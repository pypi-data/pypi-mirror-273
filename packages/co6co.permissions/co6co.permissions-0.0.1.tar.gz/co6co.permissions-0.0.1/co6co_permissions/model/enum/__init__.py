from co6co.enums import Base_Enum, Base_EC_Enum


class menu_type(Base_EC_Enum):
    """
    菜单类型 
    """
    group = "group","分组", 0  # 分组菜单
    api = "api","API接口", 1   # api
    view = "view", "页面视图",2  # a视图
    button = "button","视图功能", 3  # 视图中的按钮等。
   

class menu_state(Base_EC_Enum):
    """
    菜单类型 
    """ 

    enabled = "enabled","启用", 0   
    disabled = "disabled", "禁用",1 

class user_state(Base_EC_Enum):
    enabled="enabled","启用",0
    disabled="disabled","禁用",1
    locked="locked","锁定",2 
