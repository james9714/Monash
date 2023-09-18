from retailer import Retailer
from car import Car
from order import Order
import random

class CarRetailer(Retailer):
	def __init__(self, retailer_id=12345678, retailer_name='', carretailer_address='', carretailer_business_hour=(6,11),carretailer_stock=[]):
		super().__init__(retailer_id, retailer_name)
		self.carretailer_address = carretailer_address
		self.carretailer_business_hour = carretailer_business_hour
		self.carretailer_stock = carretailer_stock
	
	def __str__(self):
		return super().__str__() + ', ' + str(self.carretailer_address) + ', ' + str(self.carretailer_business_hour) + ', ' + str(self.carretailer_stock)
	
	def load_current_stock(self, stock_file_path):
		# load the data
		with open(stock_file_path,'r',encoding='utf-8') as f:
			data = f.readlines()
		data = [x.strip().split(', ') for x in data]
		for line in data:
			# for each line, the first element is the retailer id
			# if the id is same, get the stock info
			line_id = line[0]
			if int(line_id) == self.retailer_id:
				# the car stock infomations start from index 6 in the list
				# use the strip() function to remove the symbol
				# we just need the car_code
				# one car has 6 informations, so the step length is 6
				car_code_list = [i.strip("\[\]\'") for i in line[6:]][0::6]
				self.carretailer_stock = car_code_list	


	def is_operating(self, cur_hour):
		# the first element in the tuple is opening time
		# the second element in the tuple is closing time
		if cur_hour >= self.carretailer_business_hour[0] and cur_hour <= self.carretailer_business_hour[1]:
			return True
		else:
			return False

	def get_all_stock(self):
		with open('..\data\stock.txt','r',encoding='utf-8') as f:
			data = f.readlines()
		data = [x.strip().split(', ') for x in data]
		for line in data:
			line_id = line[0]
			if int(line_id) == self.retailer_id:
				temp = [i.strip("\[\]\'") for i in line[6:]]
				# the logic is similar with the load_current_stock function
				# but the difference is we need get all information of the car
				car_info_list = [temp[i:i+6] for i in range(0, len(temp), 6)]

		car_obj_list = []
		# after get the car informartion, transfer it to object and save in a list
		for car_info in car_info_list:
			car_obj_list.append(Car(car_info[0], car_info[1],int(car_info[2]), int(car_info[3]), car_info[4], car_info[5]))
		
		return car_obj_list

	def get_postcode_distance(self, postcode):
		retailer_postcode = self.carretailer_address[-4:]
		diff = abs(int(retailer_postcode) - int(postcode))
		return diff
	
	def remove_from_stock(self, car_code):
		with open('..\data\stock.txt','r',encoding='utf-8') as f:
			data = f.readlines()
		data = [x.strip().split(', ') for x in data]

		# Set a flag to record if car_code be removed
		flag = False
		for idx in range(len(data)):
			line_id = data[idx][0]
			# Use id to locate line number
			if int(line_id) == self.retailer_id:
				temp = [i.strip("\[\]\'") for i in data[idx][6:]]
				new_car_list = []
				# six steps include one car information
				for i in range(0,len(temp),6):
					if temp[i] == car_code:
						# if removed, turn flag to True
						flag = True
					else:
						# store other cars info
						car_info = ', '.join(temp[i:i+6])
						new_car_list.append(car_info)
				# update the line
				data[idx] = data[idx][:6] + str(new_car_list).split(', ')

		with open('..\data\stock.txt','w',encoding='utf-8') as f:
			for line in data:
				f.write(', '.join(line)+'\n')

		return flag

	# 2.3.8
	def add_to_stock(self, car_obj):
		# if the car_obj already in the carretailer stock, return False
		if car_obj.car_code not in self.carretailer_stock:
			return False
		
		with open('..\data\stock.txt','r',encoding='utf-8') as f:
			data = f.readlines()
		data = [x.strip().split(', ') for x in data]

		for idx in range(len(data)):
			line_id = data[idx][0]
			if int(line_id) == self.retailer_id:
				new_car_list = []
				temp = [i.strip("\[\]\'") for i in data[idx][6:]]
				for i in range(0,len(temp),6):
					car_info = ', '.join(temp[i:i+6])
					new_car_list.append(car_info)
				# get the attribute of the Car Object and convert it to a sting, add it to the  existing list
				new_car = ', '.join([car_obj.car_code, car_obj.car_name, int(car_obj.car_capacity), int(car_obj.car_horsepower), int(car_obj.car_weight), car_obj.car_type])
				new_car_list.append(new_car)
				# uodate the line
				data[idx] = data[idx][:6] + str(new_car_list).split(', ')

		with open('..\data\stock.txt','w',encoding='utf-8') as f:
			for line in data:
				f.write(', '.join(line)+'\n')
		return True
	
	# 2.3.9
	def get_stock_by_cartype(self,car_types_list):
		find_list=[]
		car_obj_list = self.get_all_stock()
		# iterate the type list and car object list
		for type in car_types_list:
			for car in car_obj_list:
				# if the type is same, save it to find list
				if type == car.car_type:
					find_list.append(car)
		return find_list
	
	def get_stock_by_licence_type(self,licence_type):
		car_obj_list = self.get_all_stock()
		match_list=[]
		if licence_type == 'P':
			for car in car_obj_list:
				# if boolen value is True means the P licence driver couldn't drive the car
				if car.Car().probationary_licence_prohibited_vehicle():
					pass
				else:
					match_list.append(car)
		else:
			match_list = car_obj_list
		
		return match_list
	
	def car_recommendation(self):
		car_obj_list = self.get_all_stock()
		random_car = random.choice(car_obj_list)
		return random_car
	
	def create_order(self,car_code):
		car_obj_list = self.get_all_stock()
		new_car_code_list = []
		for car in car_obj_list:
			if car.car_code != car_code:
				new_car_code_list.append(car.car_code)
			else:
				self.remove_from_stock(car_code)
				order_id = Order().generate_order_id(car_code)
				retailer = Retailer(self.retailer_id,self.retailer_name)
				order_creation_time = order_id[-10:]
				order_obj = Order(order_id, car, retailer, order_creation_time)
				line = order_id +  car.car_code +self.retailer_id +order_creation_time
		self.carretailer_stock = new_car_code_list

		
		with open('../data/order.txt', 'a', encoding='utf-8') as f:
			f.write(line, +'/n')
		return order_obj
		