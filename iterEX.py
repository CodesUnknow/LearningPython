#EX1 使用while循环实现迭代，对于迭代的结束打印提示字符 
#items = [1,2,3,4,5]
#it = iter(items)
#try:
	#while True:
		#x1 = next(it)
		#print('%s\n'%str(x1))
#except StopIteration:
	#print('end of the iterator')

#EX2 通过修改类的iter方法，构建一个自己使用的可迭代容器(取自'Python cookbook')
#其中的repr返回的字符串与普通的str不同，是等同于类创造的对象的
#迭代请求直接转发给类中的属性列表转换成的迭代器
#class Node:
	#def __init__(self,value):
		#self._value = value
		#self._children = []
	#def __repr__(self):
		#return 'Node({!r})'.format(self._value)
	#def add_children(self,node):
		#self._children.append(node)
	#def __iter__(self):
		#return iter(self._children)
#
#if __name__=='__main__':
	#root = Node(0)
	#child1 = Node(1)
	#child2 = Node(2)
	#root.add_children(child1)
	#root.add_children(child2)
	#for child in root:
		#print(child)
	#print(child1)
	#print(child2)
#EX3 创建一个对象能够实现迭代功能，并能够以深度优先的模式遍历节点
class Node:
	def __init__(self,value):
		self._value = value
		self._children = []
	def __repr__(self):
		return 'Node({!r})'.format(self._value)
	def add_children(self,node):
		self._children.append(node)
	def __iter__(self):
		return iter(self._children)
	def depth_first(self):
		yield self
		for c in self:
			yield from c.depth_first()

