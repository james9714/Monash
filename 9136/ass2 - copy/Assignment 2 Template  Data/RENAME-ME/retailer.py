import random

class Retailer:
	def __init__(self, retailer_id=12345678, retailer_name=''):
		self.retailer_id = retailer_id
		self.retailer_name = retailer_name

	def __str__(self):
		return(f"{self.retailer_id}, {self.retailer_name}")
	
	def generate_retailer_id(self, list_of_retailers):
		# Generate a randomly generated unique retailer ID that is different from
		# the existing retailer IDs and set it as the retailer_id (8 digits number)
		existing_retailer_ids = [retailer.retailer_id for retailer in list_of_retailers]
		# step 1 generate an id 
		id = random.randint(10000000,99999999)
		# step 2 check if the id exist in the list
		while id in existing_retailer_ids:
			# step 3 if existing re-generate id until the new one not in the list
			id = random.randint(10000000,99999999)
		self.retailer_id = id
