from retailer import Retailer
from car import Car

class CarRetailer(Retailer):
	def __init__(self, retailer_id=12345678, retailer_name='RETAILER NAME', carretailer_address='ADDRESS, VIC 3000', carretailer_business_hour=(6,11),carretailer_stock=[]):
		super().__init__(retailer_id, retailer_name)
		self.carretailer_address = carretailer_address
		self.carretailer_business_hour = carretailer_business_hour
		self.carretailer_stock = carretailer_stock
	
	def __str__(self):
		return super().__str__() + ', ' + self.carretailer_address + ', ' + str(self.carretailer_business_hour) + ', ' + str(self.carretailer_stock)
	
	def load_current_stock(self, stock_file_path):
		with open(stock_file_path,'r',encoding='utf-8') as f:
			data = f.readlines()
			data = [x.strip() for x in data]
		data = [x.split(',') for x in data]
		for line in data:
			line_id = line[0]
			if line_id == int(self.retailer_id):
				temp_list = eval(','.join(line[6:]))
				car_code_list = [x.split(', ')[0] for x in temp_list]
				self.carretailer_stock = car_code_list	


	def is_operating(self, cur_hour):
		if cur_hour >= self.carretailer_business_hour[0] and cur_hour <= self.carretailer_business_hour[1]:
			return True
		else:
			return False

	def get_all_stock(self):
		car_obj_list = []
		for car_code in self.carretailer_stock:
			if Car().found_matching_car(car_code):
				car_obj_list.append(Car())
		return car_obj_list

	def get_postcode_distance(self, postcode):
		address = self.carretailer_address.split(', ')[1]
		diff = abs(int(address) - int(postcode))
		return diff
	
	def remove_from_stock(self, car_code):
		
		stock_file_path ='9136\ass2 - copy\Assignment 2 Template  Data\data\stock.txt'
		if car_code in self.carretailer_stock:
			self.carretailer_stock.remove(car_code)
			return True
		else:
			return False
