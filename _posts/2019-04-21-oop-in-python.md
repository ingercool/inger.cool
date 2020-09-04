---
title: "面向对象的 Python 实现"
layout: post
date: 2019-04-21 22:14
tag:
- Python
category: blog
author: ingerchao
description: The notes of python learning
---

#### 类的创建

```python
class Model:
    pass
def main():
    # Model()实例化一个Model对象
    model = Model()
    print(model)
if __name__ == '__main__':
    main()
```

```
<__main__.Model object at 0x7fe4a0ceaf28>
```

- 类名一般大写，实例化出来的对象，名称一遍小写；
- 类在被定义时，也创建了一个局部作用域；
- 本质上讲，类本身就是一个对象，继承自 object 类。

#### 类的数据绑定

```python
class Model:
    name = "Model name"
def main():
    print(Model.name)
    model = Model()
    # 当model作用域中不含有 name 变量时，会向上逐级查找，查看Model类中有无 name 变量
    print(model.name)
    model.name = "model name"
    print(Model.name)
    print(model.name)
if __name__ == '__main__':
    main()
```

```
Model name
Model name
Model name
model name
```

- 实例化的对象拥有自己的作用域，对应 self 作用域，类本身也有自己独立的作用域。
- 对实例化出来的对象引用属性时，先从自己的作用域找，未找到则向上找；
- 实例化出来的对象是可以在运行时绑定数据的。

#### 类的自定义实例化：`__init__`

```python
class Model:
    name = "Model"
    # 在函数中又创建了新的作用域
    def __init__(self, name):
        self.name = name
def main():
    firstmodel = Model("first")
    secondmodel = Model("second")
    print(Model.name, firstmodel.name, secondmodel.name)
    firstmodel.name, secondmodel.name = "model1", "model2"
    print(Model.name, firstmodel.name, secondmodel.name)

if __name__ == '__main__':
    main()
```

```
Model first second
Model model1 model2
```

- 类定义体中，self 指代实例化出来的对象；没有跟在 self 后面的属性属于类属性；
- 可以使用 `__init__()`函数自定义初始化方式，也就是构建函数；
- 隶属于类的方法是共享的，隶属于对象的方法是每个对象私有的。

#### 类方法和对象方法

```python
class Model:
    name = "Model"
    # 在函数中又创建了新的作用域
    def __init__(self, name):
        self.name = name
    # 对象方法，self指向对象
    def print_name(self):
        print(self.name)
    # 使用 @classmethod 与 cls 可以将方法绑定到类本身上
    # 此时类不用初始化就可以调用方法
    @classmethod
    def print_class_name(cls):
        print(cls.name)
def main():
    model = Model("model")
    model.print_name()
    Model.print_class_name()

if __name__ == '__main__':
    main()
```

```
model
Model
```

#### 属性封装

```python
class Model:
    # 在属性前加 __ 可以将属性对外私有化，也就是只能由对象使用，在外访问是不可以的。
    __name = "Model"
    # 在函数中又创建了新的作用域
    def __init__(self, name):
        self.__name = name
    def print_name(self):
        print(self.__name)
    # 使用 @classmethod 与 cls 可以将方法绑定到类本身上
    @classmethod
    def print_class_name(cls):
        print(cls.__name)
def main():
    model = Model("model")
    print(Model.__name)
    print(model.__name)

if __name__ == '__main__':
    main()
```

```
AttributeError: type object 'Model' has no attribute '__name'
AttributeError: 'Model' object has no attribute '__name'
```

- 通过双下划线开头，可以将数据属性私有化，对于方法一样适用；
- 从报错信息也能看出， Model 是一个 type object ， model是一个 Model object。

> Python中的私有化是假的，本质上是做了一次名称替换，因此实际中也有为了方便调试而适
> 用单下划线的情况，而私有化也就全凭自觉了。

#### 继承

##### 隐式实例化

```python
class Model:
    __name = "Model"
    def __init__(self, name):
        self.__name = name
    def print_name(self):
        print(self.__name)
    @classmethod
    def print_class_name(cls):
        print(cls.__name)
    
# 隐式继承
# 如果子类没有定义自己的 __init__(), 则隐式调用父类的
# 子类可以使用父类的方法，但类方法要注意
class CNNModel(Model):
    __name = "CNN"
    
def main():
    cnnmodel = CNNModel("CNN Model")
    cnnmodel.print_name()
    CNNModel.print_class_name()

if __name__ == '__main__':
    main()
```

```
CNN Model
Model
```

> 使用了 @classmethod 后的方法虽然可以继承，但是方法里面的 cls 参数绑定了父类，即使
> 在子类中调用了类方法，但通过 cls 引用的属性依旧是父类的类属性

##### 显式实例化

```python
class Model:
    __name = "Model"
    def __init__(self, name):
        self.__name = name
    def print_name(self):
        print(self.__name)
    @classmethod
    def print_class_name(cls):
        print(cls.__name)
    
# 显式继承
class CNNModel(Model):
    __name = "CNN"
    def __init__(self, name, layer_num):
        # 子类中的 init 方法必须显式调用父类的 init 方法
        Model.__init__(self, name)
        self.__layer_num = layer_num
    def print_layer_num(self):
        print(self.__layer_num)
    
def main():
    cnnmodel = CNNModel("CNN Model", 6)
    cnnmodel.print_name()
    cnnmodel.print_layer_num()

if __name__ == '__main__':
    main()
```

```
CNN Model
6
```

#### 多态

```python
class Model:
    __name = "Model"
    def __init__(self, name):
        self.__name = name
    def print_name(self):
        print(self.__name)
    @classmethod
    def print_class_name(cls):
        print(cls.__name)
    
class CNNModel(Model):
    __name = "CNN"
    def __init__(self, name, layer_num):
        # 子类中的 init 方法必须显式调用父类的 init 方法
        Model.__init__(self, name)
        self.__layer_num = layer_num
    # 重写子类中的print_name
    def print_name(self):
        print(self.__name)
        print(self.__layer_num)
        
class RNNModel(Model):
    __name = "RNN"
    def __init__(self, name, nn_type):
        Model.__init__(self, name)
        self.__nn_type = nn_type
    def print_name(self):
        print(self.__name)
        print(self.__nn_type)

def print_model(model):
    model.print_name()
    
def main():
    model = Model("model")
    cnnmodel = CNNModel("CNN Model", 6)
    rnnmodel = RNNModel("RNN Model", "LSTM")
    [print_model(m) for m in [model, cnnmodel, rnnmodel]]
if __name__ == '__main__':
    main()
```

```
model
CNN
6
RNN
LSTM
```

- 多态的设计就是要完成**对于不同类型对象使用相同的方法调用能得到各自期望的输出**;
- 在数据封装，继承和多态中，多态是 Python 设计的核心，也叫鸭子类型。