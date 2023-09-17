import math
class Car:
	def __init__(self, car_code='MB123456', car_name='', car_capacity=0, car_horsepower=0, car_weight=0, car_type='FWD'):
		self.car_code = car_code
		self.car_name = car_name
		self.car_capacity = car_capacity
		self.car_horsepower = car_horsepower
		self.car_weight = car_weight
		self.car_type = car_type

	def __str__(self) -> str:
		return(f"{self.car_code}, {self.car_name}, {self.car_capacity}, {self.car_horsepower}, {self.car_weight}, {self.car_type}")
	
	def probationary_licence_prohibited_vehicle(self):
		# use math ceil function to round up the value
		if math.ceil(self.car_horsepower/self.car_weight)*1000 > 130:
			# if the reuslt is largger than 130 return True
			return True
		else:
			return False
		
	def found_matching_car(self, car_code):
		if self.car_code == car_code:
			return True
		else:
			return False
		
	def get_car_type(self):
		return self.car_type
	
# test=Car('MB123456', 'TEST', 0, 0, 1, 'CARTYPE')
# print(test.get_car_type())