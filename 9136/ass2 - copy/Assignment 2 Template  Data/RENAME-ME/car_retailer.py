import Retailer from retailer

class CarRetailer(Retailer):
	def __init__(self, retailer_id=12345678, retailer_name='RETAILER NAME', carretailer_address='ADDRESS, VIC 3000', carretailer_business_hour=(6,11),carretailer_stock=[]):
		super().__init__(retailer_id, retailer_name)
		self.carretailer_address = carretailer_address
		self.carretailer_business_hour = carretailer_business_hour
		self.carretailer_stock = carretailer_stock
	
	def __str__(self):
		return super().__str__() + ' ' + self.carretailer_address + ' ' + str(self.carretailer_business_hour) + ' ' + str(self.carretailer_stock)