import datetime,random
from retailer import Retailer
from car import Car

class Order:
	def __init__(self, order_id = '',order_car = Car(), \
			  order_retailer= Retailer(),order_creation_time=0):
		self.order_id = order_id
		self.order_car = order_car
		self.order_retailer = order_retailer
		self.order_creation_time = order_creation_time
	
	def __str__(self) -> str:
		return(f"{self.order_id}, {self.order_car}, {self.order_retailer}, {self.order_creation_time}")	

	def generate_order_id(self,car_code):
		random_str = []
		for i in range(6):
			random_str.append(chr(random.randint(97,122)))

		for i in range(1,len(random_str),2):
			random_str[i] = random_str[i].upper()

		str_convert_num = [(ord(v)**2)%7 for v in random_str]

		str_1 = "~!@#$%^&*"
		symbol_res = ''
		for i in range(len(str_convert_num)):
			symbol_res += i * str_1[str_convert_num[i]]

		order_time = str(int(datetime.datetime.now().timestamp()))

		generate_id = ''.join(random_str) + symbol_res + car_code + order_time
		return generate_id