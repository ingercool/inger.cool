---
title: "Python 迭代器和生成器"
layout: post
date: 2019-04-25 13:22
tag:
- Python
category: blog
author: ingerchao
description: The notes of Python learning
---

### Iterator Protocol

- 迭代器是一个对象，Python中一切都是对象，迭代器也不例外；
- 迭代器可以被 `next()` 调用，并返回一个值；
- 迭代器可以被`iter()`调用，并返回迭代器自己；
- 连续被 `next()`调用时一次返回一系列的值；
- 如果到了迭代的末尾，则抛出 `StopIteration` 异常；
- 迭代器也可以没有末尾，只要被 `next()`调用，就一定会返回一个值；
- Python中，`next()`内置函数调用的是对象的 `__next__()`方法；
- Python 中，`iter()`内置函数调用的是对象的`__iter__()`方法；
- 一个实现了迭代器协议的对象可以被 for 语句循环迭代，直到抛出 `StopIteration` 异常终止。

**Example 1**：`__next__()`方法的使用

```python
class XIterator:
    def __init__(self):
        self.elements = list(range(5))
    def __next__(self):
        if self.elements:
            return self.elements.pop()
def main():
    x_it = XIterator()
    [print(next(x_it)) for i in range(10)]
if __name__ == "__main__":
    main()
```

```
4
3
2
1
0
None
None
None
None
None
```

XIterator 初始化是拥有 5 个元素的一个 List，`next(x_it)`调用`__next__(self)`函数，当 list 中没有元素时输出 None。由于此时没有实现`__iter__()`，所以使用 for 语句迭代会报错。

**Example 2**：实现了 `__iter__()`

```python
class XIterator:
    def __init__(self):
        self.elements = list(range(5))
    def __next__(self):
        if self.elements:
            return self.elements.pop()
    def __iter__(self):
        return self
def main():
    x_it = XIterator()
    # 永远不会结束，因为 __next__(self) 可以一直返回 None；因为程序不会报错，也不会抛出异常
    for x in x_it:
        print(x)
if __name__ == "__main__":
    main()
```

#### for 语句的内部实现

```python
for element in iterable:
    # do something with element
```

```python
# create an iterator object from that iterable
iter_obj = iter(iterable)

# infinite loop
while True:
    try:
        # get the next item
        element = next(iter_obj)
        # do something with element
    except StopIteration:
        # if StopIteration is raised, break from loop
        break
```

- for 语句里用的是可迭代对象 `iterable`，而非 迭代器`iterator`；
- for 语句执行的第一个操作是从可迭代对象生成一个迭代器；
- for 语句的循环体其实是靠检测 `StopIteration` 异常来中断的；
- 要想被 for 语句迭代需要三个条件：`__iter__()` `__next__()` `StopIteration`.

> 如果我们可以从一个对象里获得 Iterator，那么这个对象就是可迭代对象（Iterable）。
>
> 迭代器都是可迭代对象，因为实现了 `__iter__()`，但可迭代对象不一定是迭代器。

**Example 3**:

```python
 class XIterator:
    def __init__(self):
        self.elements = list(range(5))
    def __next__(self):
        if self.elements:
            return self.elements.pop()
        else:
            # 主动抛出异常
            raise StopIteration
    def __iter__(self):
        return self
def main():
    x_it = XIterator()
    for x in x_it:
        print(x)
if __name__ == "__main__":
    main()
```

```
4
3
2
1
0
```

当我们在 `__next__(self)`中主动抛出异常是，for循环正常终止。

### Generator

迭代器协议很有用，但实现起来却有些繁琐，需要自己编写一个类再实现相应的方法。这时候就可以使用生成器，生成器在保持代码简介优雅的同时，自动实现了迭代器协议。

**Example 1**：使用 `yield` 表达式实现生成器

```python
def f():
    # 通过 yield 关键字可以自动实现迭代器协议
    yield 1
    yield 2
    yield 3
def main():
    f_gen = f()
    [print(next(f_gen)) for i in range(5)]
    
if __name__ == "__main__":
    main()
```

```
1
2
3
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
```

既然实现了迭代器协议，就说明可以被 for 迭代：

```python
def f():
    # 通过 yield 关键字可以自动实现迭代器协议
    yield 1
    yield 2
    yield 3
def main():
    f_gen = f()
    for x in f_gen:
        print(x)
    
if __name__ == "__main__":
    main()
```

```
1
2
3
```

简单地讲，yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，调用 f() 不会执行 f 函数，而是返回一个 iterable 对象！

在 for 循环执行时，每次循环都会执行 f 函数内部的代码，执行到 yield 1 时，fab 函数就返回一个迭代值，下次迭代时，代码从 yield 1 的下一条语句继续执行，而函数的本地变量看起来和上次中断执行前是完全一样的，于是函数继续执行，直到再次遇到 yield。

在一个 generator function 中，如果没有 return，则默认执行至函数完毕，如果在执行过程中 return，则直接抛出 StopIteration 终止迭代。

**Example 2：**`Generator Expression`

```python
# List comprehension
[print(x) for x in (x ** 2 for x in range(5))]
```

```
0
1
4
9
16
[None, None, None, None, None]
```

`x ** 2 for x in range(5)`会返回生成一个生成器，生成器又可以再次被迭代成为 x，对每个 x 进行 print 操作。

**不要小瞧任何看似微小的区别**。

```python
# 把 List 传给 sum
sum([x ** 2 for x in range(10000000)])
# 把 generator 传给 sum
sum(x ** 2 for x in range(10000000))
```

第一个表达式需要在内存中保存 10000000 个数，内存可能会爆掉，而第二个表达式则不会，只是会进行 10000000 -1 次运算得到结果，内存中只保存运算的几个数而已。

如果 List 的价值是为了迭代，那么完全不需要 List，直接用 Generator 就可以了。

#### Generator 的使用场景

- 使用 Generator 替代在 List 中对元素进行操作，可以 **节省大量内存**；
- 无法在内存中存放的 **无线数据流**，比如表示全部的斐波那契数列；
- **生成器管道**，可以把复杂的操作拆成很多个生成器，那么任意时刻只需要一小部分内存，内存又会进一步降低。

**使用生成器表示全部的斐波那契数列**

```python
def fab():
    tmp = [1,1]
    while True:
        tmp.append(sum(tmp))
        yield tmp.pop(0)
if __name__ == "__main__":
    for n in fab():
        print(n)
```

```
1
1
2
……
# 无穷无尽的打印
```

**通过⽣成器管道模块化处理数据**

```python
def fab():
    tmp = [1,1]
    while True:
        tmp.append(sum(tmp))
        yield tmp.pop(0)
def dataflow():
    for x in fab():
        yield x ** 2
if __name__ == "__main__":
    for x in dataflow():
        print(x)
        if x > 100000:
            break
```

```
1
1
4
9
25
64
169
441
1156
3025
7921
20736
54289
142129
```

### 总结：Python 中的迭代思维

- Python 中有两类运算：
  - 可以并行的矢量化运算：Numpy；
  - 必须一个个的操作的迭代式运算：Generator
- Python 中有两类数据：
  - 内存中放得下的；
  - 内存中放不下的：数据量较大或者无穷大的数据
- Python 中有两种思维：
  - Eager：需要的话必须全都准备好，比如将所有数据放在List中；
  - Lazy：将一个运算拆分成迭代运算的东西。
- Python 中处处是迭代器。