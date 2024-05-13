# -*- encoding:utf-8 -*-
from __future__ import annotations 
class Result:
    code:int
    message:str
    data:any
    @classmethod
    def __new__(cls,**kvargs) -> Result:
        self=object.__new__(cls)
        self.__dict__.update(kvargs)  
        return self  
    @staticmethod
    def success(data:any=None,message:str="操作成功")-> Result:
        return Result.__new__(data=data,code=0, message=message)
    @staticmethod
    def fail(data:any=None,message:str="处理失败")-> Result:
        return Result.__new__(data=data,code=500, message=message) 
    
class Page_Result(Result):
    total:int=-1  
    @classmethod
    def __new__(cls,**kvargs) -> Page_Result: 
        self=object.__new__(cls)
        self.__dict__.update(kvargs)  
        self.total=-1 if self.total==None else self.total
        return self   
    @staticmethod
    def success(data:any=None,message:str="操作成功",**kvargs)-> Page_Result:
        return Page_Result.__new__(data=data,code=0,message =message,total=kvargs.get("total"))
    @staticmethod
    def fail(data:any=None,message:str="处理失败",**kvargs)-> Page_Result: 
        return Page_Result.__new__(data=data,code=500,message =message,total=kvargs.get("total"))

        

