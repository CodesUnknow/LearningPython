# EX1，可以接收任意数量参数的函数，可以使用一个星号开头作为参数
# 可以使用双星号接收任意数量的关键词参数的参数
# 在Python中一个星号开头的参数只能作为最后一个位置参数出现，以后的参数都视为关键词参数
def avg(first,*rest):
	return (first+sum(rest))/(1+len(rest))
def element_ex(name,value,**attrs):
	pass
avg(0,1,2)
element_ex(name = '',value = '',key = '',num = '')
# EX2,从函数中返回多个值，只需要将一个元组作为返回值即可
def exreturn():
	return 1,2,3
a,b,c = exreturn()
# EX3,用lambda表达式取代单行的函数
sum = lambda x,y:x+y
