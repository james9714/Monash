import random


class Retailer:
    def __init__(
        self,
        retailer_id=-1,
        retailer_name=''
    ):
        self.retailer_id = retailer_id
        self.retailer_name = retailer_name

    def __str__(self):
        return(f"{self.retailer_id}, {self.retailer_name}")

    def generate_retailer_id(self, list_of_retailers):
        existing_retailer_ids = [
            retailer.retailer_id for retailer in list_of_retailers]
    
        while True:
            # Generate a random 8 digit number as the retailer id
            id = random.randint(10000000, 99999999)
            if id not in existing_retailer_ids:
                self.retailer_id = id
                break
