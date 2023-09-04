import random

class Retailer:
	def __init__(self, retailer_id=12345678, retailer_name='RETAILER NAME'):
		self.retailer_id = retailer_id
		self.retailer_name = retailer_name

	def __str__(self):
		return(f"{self.retailer_id}, {self.retailer_name}")
	
	def generate_retailer_id(self, existing_retailer_ids):
		# Generate a randomly generated unique retailer ID that is different from
		# the existing retailer IDs and set it as the retailer_id (8 digits number)
		id = random.randint(10000000,99999999)
		while id in existing_retailer_ids:
			id = random.randint(10000000,99999999)
		self.retailer_id = id
