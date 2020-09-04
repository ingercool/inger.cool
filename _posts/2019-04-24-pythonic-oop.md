---
title: "Pythonic OOP"
layout: post
date: 2019-04-24
tag: 
- Python
category: blog
author: ingerchao
description: The notes of python learning
---



Pythonic 的含义有两点：

1. 符合 Python 设计理念；
2. 写出更像 Python 原生的代码。 

#### 双下划线

##### 读法

- `_name` : single underscore name
- `__name`: double underscore name
- `__name__`：dunder name (double-under, 便于口头沟通创建的单词)
- `__init__()`：dunder init method (function)

##### 双下划线开头和结尾的变量或方法叫什么

- 类别：special；magic；dunder
- 实体：attribute；method

##### Special method

- **special method：**method with special name (dunder)
- **Why use it?**: A class can implement certain operations that are invoked by special syntax
- **original intention of design:** operator overloading

> Allowing classes to define their own behavior with respect to language operators.

#### 从语言设计层面理解 Python 的数据模型

##### 一切都是对象

- Python 中的**数据模型**是 `objects`;
- Python程序中**所有数据**都是用 `objects` 或者 `objects`之间的关系表示的；
- 甚至Python**代码**都是`objects`。

##### `objects` 的组成：identity

`objects`创建后，identity 再也不会改变直到被销毁。`id()` 和 `is`关注的就是一个`object`的 identity。

```python
a = 1.0
print(id(a))
a = 1.1
print(id(a))
a = 1.0
print(id(a))
b = 1.0
print(id(b))
c = 1.1
print(id(c))
```

```
4410044608
4410044656
4410044608
4410044608
4410044656
```

由以上代码可以看出，`1.0`本身拥有 identity，a 拿到的实际上是不可变对象`1.0`的 identity。

变量存的实际上是`object`的identity，创建出来的不同`object`有不同的 identity，变量的 id 变了并不是因为 `object`的identity改变，而是**变量存的`object`变了**。

对于不可变对象（` immutable object`），计算结果如果已经存在可直接返回相同的 identity。

##### `objects` 的组成：type

`objects`创建后，type 也不会改变直到被销毁。

`type()`函数返回一个 `object` 的type，type 表示对象属于哪个 class。type 决定了一个 object 支持哪些运算，可能的值在什么范围。

##### `objects` 的组成：value

- 可变对象（mutable object）value 可变；
- 不可变对象（immutable object）value不能改变；
- 当 `object` 是个 container 的情况，尤其需要注意可变和不可变。比如前面学到的 Tuple 中嵌套的 List。
- `Object`的type决定了它是否可变。

##### Container: 存放其他 Object reference 的 Object

当我们聚焦于Container的 values 时，我们关注的是value；当我们聚焦于Container的mutability时，关注的是identity。

#### Pythonic OOP with Speical Method and Attribute

```python
class X:
    pass
class Y(X):
    pass
def main():
    x = X()
    y = Y()
    # 输出对象的 class name
    print(x.__class__.__name__)
    print(y.__class__.__name__)
    # 输出类X所属类的 name 属性
    print(X.__class__.__name__)
    print(Y.__class__.__name__)
    # 输出对象父类所属类的name
    print(x.__class__.__base__.__name__)
    print(y.__class__.__base__.__name__)
    # 输出类父类所属类的name
    print(X.__class__.__base__.__name__)
    print(Y.__class__.__base__.__name__)
if __name__ == '__main__':
    main()
```

```
X
Y
type
type
object
X
object
object
```

可以看出每一个自定义的 class 都是一个 type object，每一个 class 在定义的时候如果没有继承，都会隐式继承 object 这个superclass。

- `object.__class__` ：对象的所属类
- `class.__name__`：类的name属性
- `class.__base__`：类的父类

#### Integrating Seamlessly with Python

```python
class X:
    pass
class Y(X):
    '''Class Y'''
    # 定义 3 个 special method
    def __str__(self):
        return "{} object".format(self.__class__.__name__)
    def __len__(self):
        return 10
    def __bool__(self):
        return False
def check_bool(x):
    if x:
        print("I'm {}. My bool value is True.".format(str(x)))
    else:
        print("I'm {}. My bool value is False.".format(str(x)))

def main():
    x = X()
    y = Y()
    print(x)
    # 隐式调用 __str__(self)
    print(y)
    # print(len(x)) 不注释会报错
    # 调用 __len__(self)
    print(len(y))
    check_bool(x)
    # 通过__bool__(self)修改 bool 的值
    check_bool(y)
    print(X.__doc__)
    print(Y.__doc__)
if __name__ == '__main__':
    main()
```

```
<__main__.X object at 0x7fcd741655f8>
Y object
10
I'm 0<__main__.X object at 0x7fcd741655f8>. My bool value is True.
I'm Y object. My bool value is False.
None
Class Y
```

- 之所以要实现 Special method，是为了让自定义的 class 与 Python 的内置函数无缝衔接；
- Python 有大量的内置函数，而这些函数大部分都是调用对象里的 special method。
- [Python 中所有的 special method](https://rszalski.github.io/magicmethods/)（大部分并不会用到）。

#### Attribute Access and Properties

Attribute 相关的一般操作是：Create、Read、Update 和 Delete。

> 数据库领域中的 CRUD 亦是如此。

```python
class X:
    pass

if __name__ == '__main__':
    # print(X.a)
    X.a = "a"
    print(X.a)
    X.a = "aa"
    print(X.a)
    del X.a
    # print(X.a)
```

- 默认情况下，CRUD 操作都支持，甚至说不用创建对象都可以做到（双下划线开头的除外）。
- 而如果对象中没有这个 Attribute，访问时会报错。

#### Property

设计初衷：

- 代码复用：AI领域实际上并不常用， 面向对象可能更常用。
- 延迟计算：Property 可以在不改变代码的情况下做到延迟计算
- 更加规范的对象属性访问管理。

```python
# 场景：监控 BMI 指标，每天更新体重，隔几天看一次BMI指数
class X:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.BMI = w/h ** 2
def main():
    x = X(46,1.57)
    print(x.BMI)
    x.w = 47
    x.w = 48
    x.w = 49
    print(x.BMI)
if __name__ == "__main__":
    main()
```

```
18.662014686194166
18.662014686194166
```

由于 `__init__()`只执行一次，所以 self.BMI 一直会保持在初始化时的状态，而 BMI 是由两个成员变量计算得到的，就无法动态改变 BMI 的值。

改进版（一）：

```python
# 场景：监控 BMI 指标，每天更新体重，隔几天看一次BMI指数
class X:
    def __init__(self, w, h):
        self.__w = w
        self.__h = h
        self.BMI = w/h ** 2
    # 通过函数来改变 w 的值，在改变时调用私有的 update bmi 方法改变 bmi 属性的值
    def update_w(self, w):
        self.__w = w
        self._update_bmi()
    def _update_bmi(self):
        self.BMI = self.__w /self.__h ** 2
def main():
    x = X(46,1.57)
    print(x.BMI)
    x.update_w(46.5)
    x.update_w(47.5)
    x.update_w(48)
    print(x.BMI)
if __name__ == "__main__":
    main()
```

```
18.662014686194166
19.473406629072173
```

分析改进版一的程序：

-  w 变为私有了，更新必须通过对象方法类执行，并将 BMI 的更新放于其中，实现功能逻辑；
- BMI 属性依旧可以被外部访问和修改，那也就是说外部可以随意改变 BMI 的值，这显然是不合理的；
- 与 w 相关的代码全部被更改，在项目维护中可能会导致工作量巨大；
- 无论 BMI 属性是否被访问，每次 w 更新均会更新 BMI，有可能一万天都不看BMI，但每天都要更新 w，就进行了一万次计算，**造成了一定的计算浪费**。

改进版（二）：

```python
# 场景：监控 BMI 指标，每天更新体重，隔几天看一次BMI指数
class X:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def get_bmi(self):
        return self.w / self.h ** 2

def main():
    x = X(46,1.57)
    print(x.get_bmi())
    x.w = 47
    x.w = 48
    x.w = 49
    print(x.get_bmi())
if __name__ == "__main__":
    main()
```

```
18.662014686194166
19.879102600511175
```

分析改进版二的程序：

- 保持 w 和 h 属性可以随意更改，但 bmi 指数仅在被访问时实时计算出结果，但无法在类内部方法中用到 bmi 属性。
- 访问 BMI 的方式由属性改为方法，造成了一定程度上的代码修改。
- 在 w 更新频率高于 BMI 访问频率时，节省了计算资源；但当 w 未更新却多次访问 BMI 指数时，却造成了重复计算。

改进版（三）：

```python
# 场景：监控 BMI 指标，每天更新体重，隔几天看一次BMI指数
class X:
    def __init__(self, w, h):
        self._w = w
        self._h = h
        self._bmi = w / h ** 2
        
    def get_w(self):
        return self._w
    def set_w(self,value):
        if value <= 0:
            raise ValueError("Weight below 0 is not possible")
        self._w = value
        self._bmi = self._w / self._h ** 2
    def get_bmi(self):
        return self._bmi
    # 通过 property 对象显式的控制属性访问
    w = property(get_w,set_w)
    BMI = property(get_bmi)

def main():
    x = X(46,1.57)
    print(x.BMI)
    x.w = 47
    x.w = 48
    x.w = 49
    print(x.BMI)
if __name__ == "__main__":
    main()
```

```
18.662014686194166
19.879102600511175
```

分析改进版三的程序：

- 通过 Property 对象显式的控制属性的访问；

- 仅在 w 被更改时更新 BMI，充分避免了重复计算；
- 很容易的增加了异常处理，对更新属性进行了预检验；
- 完美复用原始调用代码，在调用方不知情的情况下完成功能添加。

> 注：Property 对象声明必须在访问控制函数之后，否则无法完成 Property 对象的创建。

改进版三只是为了深入剖析 Property 对象，实际情况下我们采用下面改进版四的写法，更加优雅。

```python
# 场景：监控 BMI 指标，每天更新体重，隔几天看一次BMI指数
class X:
    def __init__(self, w, h):
        self._w = w
        self._h = h
        self._bmi = w / h ** 2
    
    @property
    def w(self):
        return self._w
    @w.setter
    def w(self,value):
        if value <= 0:
            raise ValueError("Weight below 0 is not possible")
        self._w = value
        self._bmi = self._w / self._h ** 2
    @property
    def BMI(self):
        return self._bmi

def main():
    x = X(46,1.57)
    print(x.BMI)
    x.w = 47
    x.w = 48
    x.w = 49
    print(x.BMI)
if __name__ == "__main__":
    main()
```

从改进版三的程序中我们发现传给 Property 对象的是函数名，那么对优雅的方式是用 Decorator 来实现。

##### 总结：Property用法

- `property(fget=None, fset=None, fdel=None, doc=None)`，四个参数为：访问变量的方法，变量赋值的方法，删除变量的方法，和方法的注释；
- 使用 `@Property` **默认**实现了**可读**；
- 被 `@Property` 修饰过的 method 可以通过 `@method.setter` **继续装饰单输入参数方法**实现可写。 

#### Cross-Cutting and Duck Typing

##### 传统 OOP VS 鸭子类型

- 传统 OOP 基于类别进行设计，从类别出发逐步扩展；
- 鸭子类型仅考虑功能，从需要满足的功能触发进行设计。

##### 传统 OOP 的多态 VS 鸭子类型的多态

- 传统 OOP 中的多态大多基于共同的父类进行设计；
- Python 中的鸭子类型无需考虑继承关系，实现了某个通用的接口就可以完成多态设计，比如说 special method。

#### Mixln：基于鸭子类型的视角看多继承（Multi-Inheritance）

```python
class X:
    def f1():
        pass
# Y 类中含有 f1 和 f2
class Y(X):
    def f2():
        pass
class A:
    def f3():
        pass
def do_f1(x):
    x.f1()
def do_f2(x):
    x.f2()
def do_f3(x):
    x.f3()
# Z 继承自 Y 和 A，那么 Z 中含有 f1, f2 和 f3
class Z(Y, A):
    pass
```

#### Cross-Cutting：基于鸭子类型的视角看 Decorator 与 Special Method

- 通过给一个类实现一个个的 Special Method，可以让该类越来越像 Python 的 Built-in Class
- 实现 Special Method 是从语言衔接层面为 Class 赋能；
- 实现 Decorator 是从通用的函数功能层面为 Class 赋能；
- 通过多继承（Multi-Inheritance），利用 MixIn 的理念，可以为 Class 批量化的赋能。

-----------------------------

说实话，这节课实在是听得云里雾里，很多东西并不怎么清楚具体概念，后续需要自己研读一些书籍，比如《流畅的 Python》。但其实做 AI 并不需要很深刻的 Python 语言知识，而 Python 中关于 OOP 的自己短时间也不打算再去学更深入的东西了。