# your imports goes here
from car import Car
from retailer import Retailer
from order import Order
from car_retailer import CarRetailer
import random,datetime,string


def main_menu():
	print("""a) Look for the nearest car retailer
b) Get car purchase advice
c) Place a car order
d) Exit""")

def generate_test_data():	
	car_capacities = [4, 5, 7]
	car_horsepowers = [150, 200, 250, 300]
	car_weights = [3000, 3500, 4000, 4500]
	car_types = ["FWD", "RWD", "AWD"]

	cars= []
	while len(cars) < 12:
		car_code = ''.join(random.choices(string.ascii_uppercase,k=2)) +\
			''.join(random.choice([str(i) for i in range(0,10)]) for _ in range(6))
		car_names = ''.join(random.choices(string.ascii_letters, k=6))

		cars.append([car_code, car_names, \
			random.choice(car_capacities),random.choice(car_horsepowers), \
			random.choice(car_weights), random.choice(car_types)])
	cars = [', '.join([str(v) for v in car]) for car in cars]

	# Generate three random 8-digit numbers
	# retailer_ids = [random.randint(10000000, 99999999) for _ in range(3)]
	retailer_names = ["Flyby", "Vecent", "Coles"]
	retailers_addresses = [
		'Lonsdale St Melbourne City, VIC3000', \
		'Whitehorse Rd Blackburn, VIC3130',\
		'Clayton Rd Clayton, VIC3170']
	retailer_hour =[(9,20),(10,22),(8,22)]

	stocks = []
	retailers = []
	# Generate 3 stock records
	for i in range(3):
		retailer =Retailer(-1,retailer_names[i])
		retailers.append(retailer)
		retailer.generate_retailer_id(retailers)

		stock = [retailer.retailer_id, retailer.retailer_name, \
				retailers_addresses[i], retailer_hour[i], \
				cars[i*4:i*4+4]]
		stock = ', '.join([str(v) for v in stock])
		stocks.append(stock)

	with open('../data/stock.txt', 'w',encoding='utf-8') as f:
		for line in stocks:
			f.write(line + '\n')


def main():
	generate_test_data()

	stock_file_path ='../data/stock.txt'
	with open(stock_file_path, 'r',encoding='utf-8') as f:
		stocks = f.readlines()
	stocks = [line.strip().split(', ') for line in stocks]
	carretailer_list = []
	for stock in stocks:
		retailer_id = stock[0]
		retailer_name = stock[1]
		retailers_addresses = stock[2]+', '+stock[3]
		open_time  = stock[4].strip('()')
		close_time = stock[5].strip('()')
		retailer_hour = (int(open_time), int(close_time))
		carretailer_stock = [i.strip("\[\]\'") for i in stock[6:]][0::6]
		carretailer = CarRetailer(
			retailer_id, 
			retailer_name, 
			retailers_addresses,
			retailer_hour, 
			carretailer_stock)
		carretailer.load_current_stock("../data/stock.txt")
		carretailer_list.append(carretailer)

	while True:
		main_menu()
		menu_selection = input("Please select your option(a,b,c,d): ")
		if menu_selection.lower() == 'a':
			postcode = input("Enter your postcode: ")
			if postcode.isdigit() and int(postcode) in range(3000, 4000):
				distance_list = [
					carretailer.get_postcode_distance(int(postcode))
					for carretailer in carretailer_list]
				for i in range(len(distance_list)):
					carretailer_obj = carretailer_list[i]
					if distance_list[i] == min(distance_list):
						print('-'*40)
						print("The nearest car retailer is: ", carretailer_obj.retailer_name)
						print("Address: ", carretailer_obj.carretailer_address)
						print("Business hours: ", carretailer_obj.carretailer_business_hour)
						print('-'*40)
			else:
				print("Invalid postcode. Please try again.\n")
		elif menu_selection.lower() == 'b':
			while True:
				n = 1
				temp_list = []
				for car_retailer in carretailer_list:
					temp_list.append(n)
					print (f"""----------------------------------------
		|{n}|
Retail Name: {car_retailer.retailer_name}
Address: {car_retailer.carretailer_address}
Business Hours: {car_retailer.carretailer_business_hour}
----------------------------------------\n""")
					n+=1
				selection_retailer =  input("Please enter the title number(1,2 or 3) to choose a retailer: ")
				if selection_retailer.isdigit() and int(selection_retailer) in temp_list:
					car_retailer = carretailer_list[int(selection_retailer)-1]
					while True:		
						print("""\ni) Recommend a car
ii) Get all cars in stock
iii) Get cars in stock by car types (the car types is a list of strings, e.g.,
[“AWD”, “RWD”,"FWD"])
iv) Get probationary licence permitted cars in stock\n""")
						sub_menu_function = input('please input(1,2,3,4): ')
						if sub_menu_function.isdigit() and int(selection_retailer) in [1,2,3,4]:
							if int(sub_menu_function) == 1:
								recommend_car = car_retailer.car_recommendation()
								print("\nWe recommend you this car: ")
								print('Car code: ', recommend_car.car_code)
								print('Car name: ', recommend_car.car_name)
								print('Car capacity: ', recommend_car.car_capacity)
								print('Car horsepower: ', recommend_car.car_horsepower)
								print('Car weight: ', recommend_car.car_weight)
								print('Car type: ', recommend_car.car_type)
							elif int(sub_menu_function) == 2:
								car_stock = car_retailer.get_all_stock()
								print(f"Car retailer name:     {car_retailer.retailer_name}    Car retailer id:    {car_retailer.retailer_id}")
								print("Car code|Car name|Car capacity|Car horsepower|Car weight|Car type")
								for car in car_stock:
									print(f"""{car.car_code}| {car.car_name} |      {car.car_capacity}     |     {car.car_horsepower}      |   {car.car_weight}   |   {car.car_type}""")
							elif int(sub_menu_function) == 3:
								print("""\na). AWD
b). RWD
c). FWD
You could select AWD by input a;
If you wan to select AWD and FWD, you could input ac.
""")
								type_choice = input("Please select car type by input:")
								type_choice = [i for i in type_choice]
								type_list = ["AWD", "RWD","FWD"]
								for i in range(len(type_choice)):
									if type_choice[i] == 'a':
										type_choice[i] = type_list[0]
									elif type_choice[i] == 'b':
										type_choice[i] = type_list[1]
									elif type_choice[i] == 'c':
										type_choice[i] = type_list[2]
									else:
										print("Include unkown car type.\n")
										break
								car_stock = car_retailer.get_stock_by_cartype(type_choice)
								
								print("Car code|Car name|Car capacity|Car horsepower|Car weight|Car type")
								for car in car_stock:
									print(f"""{car.car_code}| {car.car_name} |      {car.car_capacity}     |     {car.car_horsepower}      |   {car.car_weight}   |   {car.car_type}""")							
							elif int(sub_menu_function) == 4:
								match_list = car_retailer.get_stock_by_licence_type('P')
								print(f"Car retailer name:     {car_retailer.retailer_name}    Car retailer id:    {car_retailer.retailer_id}")
								for car in match_list:
									print(f"""{car.car_code}| {car.car_name} |      {car.car_capacity}     |     {car.car_horsepower}      |   {car.car_weight}   |   {car.car_type}""")
						else:
							print("Invalid input. Please try again.\n")
				elif selection_retailer.lower() == 'q':
					break
				else:
					print("Invalid retailer choosen. Please try again.\n")
		elif menu_selection.lower() == 'c':
			#current_time = datetime.datetime.now().hour
			current_time = 10	
			while True:
				print("Please type in your prefered retailer id and car code (seperated by a space).")
				print("For example, 36113365 EL597970")

				order_input = input("Please input the retailer id and car code: ")
				if len(order_input) != 17 and order_input[8] != ' ':
					print("Invalid input. Please try again.\n")
					continue
				order_retailer_id, order_car_code = order_input.split(' ')

				carretailer_id_list = [carretailer.retailer_id for carretailer in carretailer_list]
				if order_retailer_id in carretailer_id_list:
					for carretailer in carretailer_list:
						if carretailer.retailer_id == order_retailer_id:
							if order_car_code in carretailer.carretailer_stock:
								if carretailer.is_operating(current_time):
									order_obj = carretailer.create_order(order_car_code)
									print("\nOrder created successfully!")
									print("Order id: ", order_obj.order_id)
									print("Retailer id: ", order_retailer_id)
									print("Car code: ", order_car_code)
									timestamp_int = int(order_obj.order_creation_time)
									datetime_obj = datetime.datetime.fromtimestamp(timestamp_int)
									date_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
									print("Order creation time: ", date_str,'\n')
									break
								else:
									print("\nThe retailer is not open now. Please try again later.\n")
									break
							else:
								print("\nThe car code is not in stock. Please try again.\n")
								break
				else:
					print("\nThe retailer id is not in the list. Please try again.\n")
					continue

		elif menu_selection.lower() == 'd':
			break
		else:
			print("Invalid choice. Please try again.\n")



if __name__ == "__main__":
	main()