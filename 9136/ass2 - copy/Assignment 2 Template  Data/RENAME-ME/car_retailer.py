from retailer import Retailer
from car import Car

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

		flag = False
		for idx in range(len(data)):
			line_id = data[idx][0]
			if int(line_id) == self.retailer_id:
				temp = [i.strip("\[\]\'") for i in data[idx][6:]]
				new_car_list = []
				for i in range(0,len(temp),6):
					if temp[i] == car_code:
						flag = True
					else:
						car_info = ', '.join(temp[i:i+6])
						new_car_list.append(car_info)
				data[idx] = data[idx][:6] + str(new_car_list).split(', ')

		with open('..\data\stock.txt','w',encoding='utf-8') as f:
			for line in data:
				f.write(', '.join(line)+'\n')

		return flag

	# 2.3.8
	def add_to_stock(self, car_obj):
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
				new_car = ', '.join([car_obj.car_code, car_obj.car_name, str(car_obj.car_capacity), str(car_obj.car_horsepower), str(car_obj.car_weight), car_obj.car_type])
				new_car_list.append(new_car)
				data[idx] = data[idx][:6] + str(new_car_list).split(', ')

		with open('..\data\stock.txt','w',encoding='utf-8') as f:
			for line in data:
				f.write(', '.join(line)+'\n')
		return True
	
	# 2.3.9
	