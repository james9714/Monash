class Car:
	def __init__(self, car_node='MB123456', car_name='CARNAME', car_capacity=0, car_horsepower=0, car_weight=1, car_type='CARTYPE'):
		self.car_node = car_node
		self.car_name = car_name
		self.car_capacity = car_capacity
		self.car_horsepower = car_horsepower
		self.car_weight = car_weight
		self.car_type = car_type

	def __str__(self) -> str:
		return(f"{self.car_node}, {self.car_name}, {self.car_capacity}, {self.car_horsepower}, {self.car_type}")
	
	def probationary_licence_prohibited_vehicle(self):
		if round(self.car_horsepower/self.car_weight)*1000 > 130:
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
	
#test=Car('MB123456', 'TEST', 0, 0, 1, 'CARTYPE')
#print(test.get_car_type())