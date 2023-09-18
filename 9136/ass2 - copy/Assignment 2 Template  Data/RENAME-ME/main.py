# your imports goes here
import random,datetime
from car_retailer import CarRetailer

def main_menu():
	print("""a) Look for the nearest car retailer
b) Get car purchase advice
c) Place a car order
d) Exit""")

def generate_test_data():
	car_names = ["Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Mercedes"]
	car_capacities = [4, 5, 7]
	car_horsepowers = [150, 200, 250, 300]
	car_weights = [3000, 3500, 4000, 4500]
	car_types = ["FWD", "RWD", "AWD"]

	# Generate 12 unique random car codes
	used_codes = set()
	unique_car_codes = []
	while len(unique_car_codes) < 12:
		code = ''.join(random.choice(['A','B','C','D','E']) for _ in range(2)) +\
			''.join(random.choice([str(i) for i in range(0,10)]) for _ in range(6))
		if code not in used_codes:
			used_codes.add(code)
			unique_car_codes.append(code)

	# Generate 12 random cars
	cars = []
	for i in range(12):
		cars.append([unique_car_codes[i], random.choice(car_names), \
			random.choice(car_capacities),random.choice(car_horsepowers), \
			random.choice(car_weights), random.choice(car_types)])
	cars = [', '.join([str(v) for v in car]) for car in cars]

	# Generate three random 8-digit numbers
	retailer_ids = [random.randint(10000000, 99999999) for _ in range(3)]
	retailer_names = ["CarMax", "Carvana", "Vroom"]
	retailers_addresses = ['Southern Cross Station Docklands, VIC3008', \
						'151 Whitehorse Rd Blackburn, VIC3130',\
						'2137 Princes Hwy Clayton, VIC3168']
	retailer_hour =[(9,17),(10,20),(8,22)]

	file = []
	# Generate 3 stock records
	for i in range(3):
		stock = [retailer_ids[i], retailer_names[i], \
				retailers_addresses[i], retailer_hour[i], \
				cars[i*4:i*4+4]]
		stock = ', '.join([str(v) for v in stock])
		file.append(stock)

	with open('../data/stock1.txt', 'w') as f:
		for line in file:
			f.write(line + '\n')


def main():
	generate_test_data()
	stock_file_path ='../data/stock1.txt'
	with open(stock_file_path, 'r',encoding='utf-8') as f:
		stock = f.readlines()
	stock = [line.strip().split(', ') for line in stock]
	carretailer_list = []
	for line in stock:
		retailer_id = line[0]
		retailer_name = line[1]
		retailers_addresses = line[2]+', '+line[3]
		retailer_hour = line[4]+', '+line[5]
		carretailer_stock = [i.strip("\[\]\'") for i in line[6:]][0::6]
		carretailer = CarRetailer(retailer_id, retailer_name, retailers_addresses, retailer_hour, carretailer_stock)
		carretailer_list.append(carretailer)

	while True:
		main_menu()
		menu_choice = input("Enter your choice(a,b,c,d): ")
		if menu_choice.lower() == 'a':
			cus_postcode = input("Enter your postcode: ")
			if cus_postcode.isdigit() and int(cus_postcode) in range(3000, 4000):
				temp_distance = [carretailer.get_postcode_distance(cus_postcode) for carretailer in carretailer_list]
				for i in range(len(temp_distance)):
					if temp_distance[i] == min(temp_distance):
						print('-'*40)
						print("The nearest car retailer is: ", carretailer_list[i].retailer_name)
						print("Address: ", carretailer_list[i].carretailer_address)
						print("Business hours: ", carretailer_list[i].carretailer_business_hour)
						print('-'*40)
					else:
						pass
			else:
				print("Invalid postcode. Please try again.\n")
		elif menu_choice.lower() == 'b':
			n = 1
			temp_list = []
			print("Here is the list of car retailers: ")
			for car_retailer in carretailer_list:
				temp_list.append(n)
				print (f"""----------------------------------------
				{n}
Retail Name: {car_retailer.retailer_name}
Address: {car_retailer.carretailer_address}
Business Hours: {car_retailer.carretailer_business_hour}
----------------------------------------\n""")
				n+=1
			while True:
				cus_select_retailer =  input("Enter the title number(1,2 or 3) to select a retailer: ")
				if cus_select_retailer.isdigit() and int(cus_select_retailer) in temp_list:
					cus_car_retailer = carretailer_list[n-1]		
					print("""i) Recommend a car
ii) Get all cars in stock
iii) Get cars in stock by car types (the car types is a list of strings, e.g.,
[“AWD”, “RWD”,"FWD"])
iv) Get probationary licence permitted cars in stock""")
					cus_sub_choice = input('please input(1,2,3,4): ')
					if cus_sub_choice.isdigit() and int(cus_select_retailer) in [1,2,3,4]:
						if int(cus_sub_choice) == 1:
							recommend_car = cus_car_retailer.CarRetailer().car_recommendation()
							print("We recommend you this car: ")
							print(recommend_car)
						elif int(cus_sub_choice) == 2:
							car_stock = cus_car_retailer.CarRetailer().get_all_stock()
							for car in car_stock:
								print(car)
						elif int(cus_sub_choice) == 3:
							print("""1. AWD
2. RWD
3. FWD
You could select AWD by input 1;
If you wan to select more than one type such as AWD and FWD, you could input 12.
""")
							type_choice = input("Please select car type by input:")
							type_list = ["AWD", "RWD","FWD"]
							type_choice = [i for i in type_choice]
							car_types_list = [type_list[int(i)-1] for i in type_choice]
							avaiable_list = cus_car_retailer.CarRetailer(car_types_list)
							for car in avaiable_list:
								print(car)
						elif int(cus_sub_choice) == 4:
							licence_type = 'P'
							match_list = cus_car_retailer.CarRetailer().get_stock_by_licence_type(licence_type)
							for car in match_list:
								print(car)
					else:
						print("Invalid input. Please try again.\n")
				else:
					print("Invalid retailer number. Please try again.\n")
		elif menu_choice.lower() == 'c':
			time = 9
			retailer_car_id = input("Please input retailer ID and the car ID separated by a space: ")\
			retailer_id, car_id = retailer_car_id.split(' ')
			# if retailer_id in carretailer_list
			# if car_id in carretailer_stock
			# order_obj = create_order(car_id)
			# if current <> carretailer_business hour
			print(order_obj)

		elif menu_choice.lower() == 'd':
			break
		else:
			print("Invalid choice. Please try again.\n")
if __name__ == "__main__":
	main()