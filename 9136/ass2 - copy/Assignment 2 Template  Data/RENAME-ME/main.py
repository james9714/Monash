# your imports goes here
from car_retailer import CarRetailer
from car import Car
from retailer import Retailer
from order import Order
def main_menu():
	print("""a) Look for the nearest car retailer
b) Get car purchase advice
c) Place a car order
d) Exit""")

def generate_test_data():
	for i in range(3):
		
		retailer_id = generate_retailer_id()

def main():
	while True:
		main_menu()
		menu_choice= input('Please input your choice (a,b,c,d):')
		if menu_choice.lower() == 'a':
			customer_postcode = int(input('Please input your postcode:'))
			CarRetailer.get_postcode_distance(customer_postcode)
			
			pass
		elif menu_choice.lower() == 'b':
			pass
		elif menu_choice.lower() == 'c':
			pass
		elif menu_choice.lower() == 'd':
			break
		else:
			continue


if __name__ == "__main__":
	main()