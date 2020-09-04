---
title: "Python 装饰器"
layout: post
date: 2019-04-12 15:35
tag:
- Python
category: blog
author: ingerchao
description: The notes of python learning
---

### 装饰器

#### 装饰函数

有时候写一个闭包仅仅是为了增强一个函数的功能，功能增强了之后，只对增强了功能的最终函数感兴趣，装饰之前的函数引用就变得多余。

```python
# 装饰函数修改 doc
def decorate(func):
    func.__doc__ += '\n decorated by decorate'
    return func
def add(x,y):
    '''return the sum of x + y'''
    return x + y
# 显式调用装饰函数
add = decorate(add)
```

之前的 add 函数在一般情况下在后面的程序都不会再用到，这样的代码**没有新的变量名引入**，提升了变量名的使用效率。但问题是装饰函数的执行代码需要单独调用，可能不符合就近原则。

#### 就近原则

装饰函数的显式调用在装饰次数多了之后，就会显得非常多余，集中处理又会不符合就近原则。为了编码更加优雅，保持显式调用，遵循就近原则，出现了`@`这个语法糖：

```python
def decorate(func):
    func.__doc__ += '\n decorated by decorate'
    return func
# @decorate 等价于 add = decorate(add)
@decorate
def add(x,y):
    '''return the sum of x + y'''
    return x + y
```

通过语法糖，保证了装饰过程与原函数彼此之间的独立性；同时又保证了两者代码之间的就近原则，形成一个有机的整体。

但问题是装饰定义函数与被装饰函数在同一个模块中实现，影响了复用效率。

#### 分层封装，充分复用

可以将装饰器单独封装在一个模块中：

`DecorateToolBox.py`

```python
class DecorateToolBox:
	@classmethod
    def decorate(self, func):
        func.__doc__ += '\nDecorated by decorate.'
        return func
```

`test.py`

```python
from DecorateToolBox import DecorateToolBox
	# 使用 @class.method
	@DecorateToolBox.decorate
    def add(x, y):
        '''Return the sum of x and y.'''
        return x + y 
```

启动 Python 解释器：

```python
>>> from test import add
>>> help(add)
```

```
Help on function add in module test:

add(x, y)
	Return the sum of x and y.
	Decorated by decorate.
(END) 
```

将不同级别的功能模块封装在不同文件中是编写大型程序的基础。而且实现一个装饰器，并不一定需要写出一个闭包。有了`@classmethod`装饰器，类可以不依赖于一个实体而直接调用其方法。

#### 装饰器的堆叠

```python
def deco_1(func):
    print('running deco_1')
    return func
def deco_2(func):
    print('running deco_2')
    return func
def deco_3(func):
    print('running deco_3')
    return func
@deco_3
@deco_1
@deco_2
def f():
    print('running f...')
    
if __name__ == '__main__':
    f()
```

```
running deco_2
running deco_1
running deco_3
running f...
```

当有多个装饰器堆叠在一起时，按照`@decorate`的顺序，从下向上依次执行，最后执行函数本身。

#### 装饰器在导入时立即执行

```python
def deco_1(func):
    print('running deco_1')
    return func
def deco_2(func):
    print('running deco_2')
    return func

@deco_1
@deco_2
def f():
    print('running f...')
    
if __name__ == '__main__':
    pass
```

```
running deco_2
running deco_1
```

并没有显式调用 f()，而装饰器依然执行了，也就是说装饰器在导入时就执行了。

#### 带参数的装饰器

问题分析：我们发现装饰器只能接受一个位置参数，且这个位置参数已经被**被装饰函数的引用**占据了。但我们希望装饰器能够使用外部传入的其他参数，也就是说装饰器需要访问或修改外部参数。

三种备选方案：

1. 在装饰器内访问全局不可变对象，若需要修改，则使用`global`声明（不安全）
2. 在装饰器内访问外部可变对象（不安全）
3. 让装饰器成为闭包的返回（较安全）

前两种方法可能会造成全局作用域中变量的混乱，当具备修改全局作用域的装饰器数量过多时，会导致修改混乱情况，无从得知是哪个装饰器修改了全局变量，也可能会出现不希望的全局变量值。

带参数的装饰器一定是闭包的实现，接受外部参数，返回一个装饰器。

```python
# 参数化之前的装饰器
registry = set()
def register(func):
    registry.add(func)
    return func
@register
def f1():
    print('running f1')
@register
def f2():
    print('running f2')
def f3():
    print('running f3')
def main():
    f1()
    f2()
    f3()

if __name__== '__main__':
    print(registry)
    main()
```

```
{<function f2 at 0x7fb316f63e18>, <function f1 at 0x7fb3177df840>}
running f1
running f2
running f3
```

```PYTHON
# 参数化之后的装饰器，增加了开关功能
registry = set()
# 标准带参数的装饰器写法，根据装饰器参数动态执行
# 闭包最外层负责接收参数
def register(flag = True):
    # 内层就是个装饰器实现细节
    def decorate(func):
        if flag:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate
# @register() 告诉解释器需要先执行闭包，register()方法返回的是一个decorator，用@语法糖实现装饰器显式调用对f1()进行装饰
@register()
def f1():
    print('running f1')
@register(False)
def f2():
    print('running f2')
@register(True)
def f3():
    print('running f3')
    
def main():
    f1()
    f2()
    f3()

if __name__== '__main__':
    print(registry)
    main()
```

```python
# 此时，register变量被使用了两次
{<function f1 at 0x7fb316f63ea0>, <function f3 at 0x7fb316f63f28>}
running f1
running f2
running f3
```

#### 装饰器的使用

##### 常见使用场景

- 运行前处理：比如确认用户授权；
- 运行时注册：比如注册新号系统；
- 运行后清理：如序列化返回值。

##### 注册机制或授权机制

##### 参数的数据验证或清洗（往往跟数据清洗或异常处理相关）

```python
def require_ints(func):
    def temp_func(*args):
        if not all([isinstance(arg, int) for arg in args]):
            raise TypeError("{} only accepts integers as arguments.".format(func.__name__))
        return func(*args)
    return temp_func

def add(x,y):
    return x+y

@require_ints
def require_ints_add(x,y):
    return x + y 

if __name__ == '__main__':
    print(add(1.0, 2.0))
    # type error
    print(require_ints_add(1.0, 2.0)) 
```

```
3.0
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-30-c8de43773e59> in <module>
     15 if __name__ == '__main__':
     16     print(add(1.0, 2.0))
---> 17     print(require_ints_add(1.0, 2.0))

<ipython-input-30-c8de43773e59> in temp_func(*args)
      2     def temp_func(*args):
      3         if not all([isinstance(arg, int) for arg in args]):
----> 4             raise TypeError("{} only accepts integers as arguments.".format(func.__name__))
      5         return func(*args)
      6     return temp_func

TypeError: require_ints_add only accepts integers as arguments.
```

##### 复用核心计算模块，仅改变输出方式

让原本返回 Python 原生数据结构的函数输出 JSON 结构：

```python
import json
def json_output(func):
    def temp_func(*args, **kw):
        result = func(*args, **kw)
        return json.dumps(result)
    return temp_func
def generate_a_dict(x):
    return {str(i): i**2 for i in range(x)}

@json_output
def generate_a_dict_json_output(x):
    return {str(i): i**2 for i in range(x)}

if __name__ == '__main__':
    a, b = generate_a_dict(5),generate_a_dict_json_output(5)
    print(a,type(a))
    print(b,type(b))
```

```
{'3': 9, '2': 4, '0': 0, '1': 1, '4': 16} <class 'dict'>
{"3": 9, "2": 4, "0": 0, "1": 1, "4": 16} <class 'str'>
```

### 总结

- 装饰器是一个可调用的**对象**，以某种方式**增强函数的功能**，并不是修改函数的功能；如果一个装饰器牵扯到函数内部实现，那就不是一个设计合理的装饰器了。
- 装饰器是一个语法糖，在源码中标记函数；
- 解释器解析源码的时候将被装饰的函数作为第一个位置参数传给装饰器；
- 装饰器可能会**直接处理**被装饰函数，然后返回它（一般仅修改属性，不修改代码）；
- 装饰器也可能用一个新的函数或可调用对象 **替换** 被装饰函数，但核心功能是不变的；
- 装饰器仅仅是看着像闭包，其实功能的定位与闭包有重合也有很大区别；
- 装饰器模式的本质是 **元编程**：在运行时改变程序行为；
- 装饰器的一个不可忽视的特性：**在模块加载时立即执行**；
- 装饰器是可以堆叠的，**自底向上逐个修饰**；
- 装饰器是可以带参数的，但此时至少要写两个装饰器；
- 装饰器的更加 Pythonic 的实现方式其实是在类中实现`__call__()`方法。