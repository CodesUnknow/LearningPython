"""
关于进程、线程、协程的练习
进程和线程的语法规则类似，为要执行的函数创建一个进程或者线程，开启需要并发的线程或者进程，等待执行结束，语法的规则符合人类普通的抽象过程；
python的协程语法有些不好理解，要追溯到生成器函数，在生成器函数控制流程的基础上，增加了交互的过程，将协程的关键词yield理解为控制流程的阀门是关键。
"""
import requests
import re
import redis
import os, time, random, threading
from multiprocessing import Process, Pool, Queue
import subprocess
import aiohttp
import asyncio
from functools import wraps
from collections import namedtuple


# EX1,进程和线程的练习，两个子函数分别从不同的代理网站爬取页面上的代理，并存储到一个List中去；
# 正常的执行顺序下，需要爬取完其中一个web，再去执行另外一个web
# 可以利用进程和线程让这两个爬取工作同时完成。
"""
#run_proc1 和run_proc2是单独的爬取函数；
def run_proc1():
    url = 'https://www.kuaidaili.com/free/inha/'
    pages = PAGES_SET
    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    pattern = '<td data-title="IP">(.*?)</td>[\d|\D]+?<td data-title="PORT">(.*?)</td>'
    proxylist = []
    for index in range(1, pages):
        html = get_html(url, index, header).text
        get_ProAddrList(html, pattern, proxylist)
    time.sleep(1)
    return proxylist


def run_proc2():
    url = 'http://www.xicidaili.com/nn/'
    pages = PAGES_SET
    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    pattern = '<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png"\
 alt="Cn" /></td>[\d|\D]*?<td>(.*?)</td>[\d|\D]*?<td>(.*?)</td>'
    proxylist = []
    for index in range(1, pages):
        html = get_html(url, index, header).text
        get_ProAddrList(html, pattern, proxylist)
    time.sleep(1)
    return proxylist
if __name__ == '__main__':
    #process way
    p1 = Process(target=run_proc1, args=('test1',))
    p2 = Process(target=run_proc2, args=('test2',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    #threading way
    t1 = threading.Thread(target=run_proc1, name='Thread1')
    t2 = threading.Thread(target=run_proc2, name='Thread2')
    t1.start()
    t2.start()
    t2.join()
    t1.join()
"""
# EX1.2 一个线程被创建以后，需要调用start来启动这个线程，启动后的线程会在所属的系统级线程中执行，一旦启动以后
# 这些线程会完全由操作系统管理，直到目标函数返回为止，可以查询线程的对象来判断它是否还在运行
# 如果要终止进程，就要使得目标函数能够在某个制定的点上退出，需要在程序中设置相应的判断
# 因此实现起来的话有几种方式，或者设置一个全局变量在目标函数之外改变它；或者将目标函数设置为类的一个函数，通过
# 类中的其他函数改变类的属性的方式实现；或者函数之间通信（协程），下面先用类的方式来实现
def count(n):
	while n>0:
		print('T-mius',n)
		n -= 1
		time.sleep(1)
t = threading.Thread(target=count,args=(3,))
t.start()
n = 3
while n>0:
	if t.is_alive():
		print('thread still alive')
		time.sleep(0.5)
	else:
		print('dead')
	n -= 1
# class实现退出线程的判断,根据running标志位来判断是否退出函数
class countdown:
	def __init__(self):
		self.running = True
	def terminate(self):
		self.running = False
	def run(self,n):
		while self.running and n>0 :
			print('class T-mius',n)
			n -= 1
			time.sleep(1)
		print('t1 blocked!')
count1 = countdown()
t1 = threading.Thread(target=count1.run,args=(3,))
t1.start()
count1.terminate()

		

# EX2 coroutine way
#正常情况下，声明一个生成器函数对象之后，这个对象的状态是创建，需要使用next函数激活使其处于挂起状态才可以接收外部send
#可以借助函数装饰器，在装饰器中完成next函数的功能，这样我们就无需预先激活，直接向这个对象发送参数了。
#以下是借助函数装饰器完成预激过程的例子（取自《fluent python》)
"""
def coroutine(func):
    @wraps(func)
    def prime(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return prime

@coroutine
def averager1():
    result = namedtuple('Result','count average')
    total = 0.0
    average1 = None
    count = 0
    while True:
        print('son of averager created')
        term = yield average1
        if term is None:
            break
        total += term
        count += 1
        average1 = total/count
    return result(total,average1)
# 委派生成器
def grouper1(results,key):
    while True:
        results[key] = yield from averager()
"""
# EX3,使用委派生成器，灵活的实现对协程的控制以及结果的读取
# yield from的具体语义在PEP380中有阐释，之所以不用对子生成器进行显示预激，是因为在委派生成器中已经进行了处理。
"""
data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}
def averager():
	count = 0
	term = 0.0
	total = 0.0
	average = 0.0
	while True:
		term = yield average
		if term is None:
			break
		total += term
		count += 1
		average = total / count
	return average

def grouper(result,key):
	while True:
		result[key] = yield from averager() 

if __name__ == '__main__':
	result = {}
	for key,values in data.items():
		group = grouper(result,key)
		next(group)
		for value in values:
			group.send(value)
		group.send(None)
	print(result)
"""
