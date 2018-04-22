# EX1，python对于可迭代对象的操作
# 任何一个可迭代的变量类型，都可以通过拆包赋值的方式赋值给多个变量，前提是变量的个数和可迭代对象中元素个数相同
# 对于变量个数与可迭代对象中变量个数不同的情况，在执行过程中会抛出一个异常
# 避免这种异常（或者说对于迭代对象未知的情况下要赋值的情况）可以采用*的表达方式（代表若干个变量）
# 变量个数与迭代对象中元素个数相同的情况
i = (1,2,3)
x,y,z = i
print(x)
print(y)
print(z)
# 不同的话会产生异常
#x,y = i
#another example
data = [ 'APP', 12.5, 91.1, (2012, 12, 21) ]
stock,pe,price,time = data
print(stock)
stock,pe,price,(year,month,day) = data
print(year,month,day)
#利用*来表示未知个数的元素，此时*的类型是一个列表
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name,email,*phone_number = record
print(phone_number)
#更深层次的引用，利用*进行递归，字符分割，等具体参考<python cookbook3>中的例子
items = [1, 10, 7, 4, 5, 9]
def sum(items):
    head,*tail = items
    return head + sum(tail) if tail else head
print(sum(items))

# EX2 利用collection和yield简便的实现只保留有限的最近的N个元素的查询
# 此例有助于初步了解yield在生成器函数中的用法，它有将函数作为生成器或者迭代器使用的功能
from collections import deque
def search(numbers, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for li in numbers:
        if pattern > li:
            yield li, previous_lines
        previous_lines.append(li)
# Example use on a file
if __name__ == '__main__':
    num = [1,4,5,6,2,3,5,9]
for line, prevlines in search(num,4, 3):
    print(line,' ',prevlines)
    print('-' * 20)
