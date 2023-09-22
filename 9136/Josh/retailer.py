import random

class Retailer:
    def __init__(self, retailer_id=11111111, retailer_name=""):
        self.retailer_id = retailer_id
        self.retailer_name = retailer_name

    def __str__(self):
        return "{}, {}".format(self.retailer_id, self.retailer_name)

    def generate_retailer_id(self, list_retailer):
        while True:
            retailer_id = random.randint(10000000, 99999999)
            if retailer_id not in list_retailer:
                return retailer_id
