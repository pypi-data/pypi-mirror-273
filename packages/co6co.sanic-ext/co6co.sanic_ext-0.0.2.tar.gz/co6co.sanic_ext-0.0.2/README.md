# 扩展sanic
 


# (sanic Demo)[https://www.osgeo.cn/sanic/sanic/examples.html/]
(task)[https://python.hotexamples.com/zh/examples/sanic/Sanic/add_task/python-sanic-add_task-method-examples.html]


# 历史记录
0.0.1 初始版本 




# 类属性与对象属性

```
class A: 
    def __init__(self) -> None:
       self.a="12"
       pass

class B(A):
    b:str="abc"
    @classmethod
    def geA(cls) -> str:
        print(cls.a)
        return cls.a

a=A()
print(a.a)

b=B()
b.a="456" 
print(b.a,B.a,"b.geA:", b.geA(),"B.geA:",B.geA())

a=A()
print(a.a,A.a)
```
