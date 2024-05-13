# -*- encoding:utf-8 -*-
from __future__ import annotations 
from co6co.enums import Base_Enum
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.engine.result import ChunkedIteratorResult
class Result: 
    def __new__(cls,code:int,data:any,message:str) -> Result:
        """
        先执行 __new__ 在执行 __init__
        在单例模式中 __init__ 会执行多次
        _instance=None
        __new__(cls):
            if cls._instance ==None: cls._instance=object.__new__(cls)
            return cls._instance 
        __init__(self):
            print("init")
        """
        obj = object.__new__(cls)
        obj.code = code 
        obj.message = message  
        #if isinstance(obj,RowMapping):obj.data=[dict(a)  for a in  data]  
        #elif isinstance(obj,ChunkedIteratorResult): obj.data=[dict(zip(a._fields,a))  for a in  data]  
        obj.data=data 
        return obj  
    
    code:int
    message:str
    data:any
   
    @staticmethod
    def create(code:int=0,data:any=None,message:str="操作成功")-> Result:
       return Result(code,data ,message ) 
    @staticmethod
    def success(data:any=None,message:str="操作成功")-> Result:
        return Result.create(data=data,  message=message)
    @staticmethod
    def fail(data:any=None,message:str="处理失败")-> Result:
        return Result.create(data=data,code=500, message=message)
    
    def __repr__(self) -> str:
        return f"class=> <code:{self.code},message:{self.message},data:{self.data}>"
 

class Page_Result(Result):
    total:int
    def __new__(cls,code:int,data:any,message:str,total:int) -> Page_Result: 
        obj:Page_Result=super().__new__(cls,code,data,message)
        obj.total = total  
        return obj    
    @staticmethod
    def create(code:int=0,data:any=None,message:str="操作成功",total:int=-1)-> Page_Result:
        result=Page_Result(code=code,data=data,message=message,total=total) 
        return result 
    @staticmethod
    def success(data:any=None,message:str="操作成功",total:int=-1)-> Page_Result:
         return Page_Result.create(data=data,code=0, message=message,total=total)
    @staticmethod
    def fail(data:any=None,message:str="处理失败",total:int=-1)-> Page_Result:
         return Page_Result.create(data=data,code=500, message=message,total=total)
    
    def __repr__(self) -> str:
        return f"class=> <code:{self.code},message:{self.message},total:{self.total},data:{self.data}>"

        

