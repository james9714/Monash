# your imports goes here
from random import choice, choices, randint
from string import ascii_letters, ascii_uppercase
from math import ceil
from car import Car
from car_retailer import CarRetailer
from order import Order
from time import time, strftime


def main_menu():
    print("a) Look for the nearest car retailer")
    print("b) Get car purchase advice")
    print("c) Place a car order")
    print("d) Exit")


def generate_test_data():
    car_list = []
    retailer_list = []
    retailer_id_list = []
    all_letters = ascii_letters
    all_upper = ascii_uppercase
    address_list = [
        "Clayton Rd Clayton, VIC3170",
        "Clayton Rd Clayton, VIC3170",
        "Clayton Rd Mount Waverley, VIC3168",
    ]
    for i in range(12):
        car_code = "".join(choices(all_upper, k=2))
        car_code += str(randint(100000, 999999))
        car_name = "".join(choices(all_letters, k=18))
        car_capacity = randint(4, 18)
        car_horsepower = randint(140, 280)
        car_weight = randint(1500, 2800)
        car_type = choice(["FWD", "AWD", "RWD"])
        car_list.append(
            Car(car_code, car_name, car_capacity, car_horsepower, car_weight, car_type)
        )
    for i in range(3):
        retailer_id = -1
        retailer_name = "".join(choices(all_letters, k=12))
        carretailer_address = address_list[i]
        start_time = randint(80, 120) / 10
        end_time = randint(120, 180) / 10
        carretailer_business_hours = (start_time, end_time)
        retailer_cars = car_list[0 + i * 4 : 4 + i * 4]
        retailer_cars = [car.__str__() for car in retailer_cars]
        retailer = CarRetailer(
            retailer_id,
            retailer_name,
            carretailer_address,
            carretailer_business_hours,
            [],
        )
        retailer.retailer_id = retailer.generate_retailer_id(retailer_id_list)
        retailer_id_list.append(retailer.retailer_id)
        retailer_list.append(
            "{}, {}, {}, {}, {}".format(
                retailer.retailer_id,
                retailer.retailer_name,
                retailer.carretailer_address,
                retailer.carretailer_business_hours,
                retailer_cars,
            )
        )

    with open("../data/stock.txt", "w", encoding="utf-8") as f:
        for retailer in retailer_list:
            f.write(retailer + "\n")


def main():
    generate_test_data()

    cars = []
    retailers = []
    retailer_id_list = []
    with open("../data/stock.txt") as f:
        stocks = f.readlines()

    for stock in stocks:
        stock_info = stock.strip("\n").split(", ")
        retailer_id = int(stock_info[0])
        retailer_name = stock_info[1]
        carretailer_address = ", ".join(stock_info[2:4])
        start_time = float(stock_info[4].strip("()"))
        end_time = float(stock_info[5].strip("()"))
        carretailer_business_hours = (start_time, end_time)
        retailer_id_list.append(retailer_id)
        retailer = CarRetailer(
            retailer_id, retailer_name, carretailer_address, carretailer_business_hours
        )
        retailer_cars = retailer.get_all_stock()
        retailer.load_current_stock("../data/stock.txt")
        retailers.append(retailer)
        cars.extend(retailer_cars)

    print("Welcome to Car Purchase Advisor System!")
    while True:
        main_menu()
        menu_option = input("Please select your option: ")
        if menu_option == "a":
            postcode = input("Please type in your postcode: ")
            if len(postcode) != 4 or not postcode.isdigit():
                print("The input postcode is not valid. Please try again.")
                continue
            nearest_retailer = CarRetailer()
            min_distance = 9999
            for retailer in retailers:
                retailer_distance = retailer.get_postcode_distance(int(postcode))
                if retailer_distance < min_distance:
                    nearest_retailer = retailer
                    min_distance = retailer_distance
            print("Nearest retailer:")
            print("Retailer id: {}".format(nearest_retailer.retailer_id))
            print("Retailer name: {}".format(nearest_retailer.retailer_name))
            print("Retailer address: {}".format(nearest_retailer.carretailer_address))
            print(
                "Retailer business hours: {}".format(
                    nearest_retailer.carretailer_business_hours
                )
            )
            print("Retailer stock: {}".format(nearest_retailer.carretailer_stock))
        elif menu_option == "b":
            print("Available retailers:")
            for retailer_idx in range(len(retailers)):
                print(
                    "Retailer {}: {}".format(
                        retailer_idx + 1, retailers[retailer_idx].__str__()
                    )
                )
            selected_retailer_id = input(
                "Please select a retailer by typing the retailer id:"
            )
            if len(selected_retailer_id) != 8 or not selected_retailer_id.isdigit():
                print("The input retailer id is invalid. Please try again.")
                continue
            if int(selected_retailer_id) not in retailer_id_list:
                print("The input retailer id does not exist. Please try again.")
                continue
            for retailer in retailers:
                if retailer.retailer_id == int(selected_retailer_id):
                    current_retailer = retailer
            cur_retailer_cars = current_retailer.get_all_stock()
            print("i)   Recommend a car")
            print("ii)  Get all cars in stock")
            print(
                "iii) Get cars in stock by car types (the car types is a list of strings, e.g., [“AWD”, “RWD”])"
            )
            print("iv)  Get probationary licence permitted cars in stock")
            submenu_option = input("Please select your option: ")
            if submenu_option == "i":
                rec_car_code = choice(current_retailer.carretailer_stock)
                for car in cur_retailer_cars:
                    if car.car_code == rec_car_code:
                        print("Recommended car:")
                        print("Car code: {}".format(car.car_code))
                        print("Car name: {}".format(car.car_name))
                        print("Car capacity: {}".format(car.car_capacity))
                        print("Car horsepower: {}".format(car.car_horsepower))
                        print("Car weight: {}".format(car.car_weight))
                        print("Car type: {}".format(car.car_type))
                        break
            elif submenu_option == "ii":
                print("Retailer id: {}".format(current_retailer.retailer_id))
                print("Retailer name: {}".format(current_retailer.retailer_name))
                for car in cur_retailer_cars:
                    print("---")
                    print("Car code: {}".format(car.car_code))
                    print("Car name: {}".format(car.car_name))
                    print("Car capacity: {}".format(car.car_capacity))
                    print("Car horsepower: {}".format(car.car_horsepower))
                    print("Car weight: {}".format(car.car_weight))
                    print("Car type: {}".format(car.car_type))
                    print("---")
            elif submenu_option == "iii":
                car_types_input = input(
                    "Please type in the car types and seperate them with a whitespace: "
                )
                if len(car_types_input.split(" ")) > 3:
                    print("The number of inputs are invalid. Please try again.")
                    continue
                car_types_input = car_types_input.split(" ")
                invalid_type = False
                for car_type in car_types_input:
                    if car_type not in ["AWD", "FWD", "RWD"]:
                        invalid_type = True
                        print("The input type is not valid. Please try again.")
                        break
                if invalid_type == True:
                    continue
                selected_cars = current_retailer.get_stock_by_car_type(car_types_input)
                print("Car types: {}".format(car_types_input))
                for car in selected_cars:
                    print("---")
                    print("Car code: {}".format(car.car_code))
                    print("Car name: {}".format(car.car_name))
                    print("Car capacity: {}".format(car.car_capacity))
                    print("Car horsepower: {}".format(car.car_horsepower))
                    print("Car weight: {}".format(car.car_weight))
                    print("Car type: {}".format(car.car_type))
                    print("---")
            elif submenu_option == "iv":
                print("Retailer id: {}".format(current_retailer.retailer_id))
                print("Retailer name: {}".format(current_retailer.retailer_name))
                for car in cur_retailer_cars:
                    if car.probationary_licence_prohibited_vehicle() != True:
                        print("---")
                        print("Car code: {}".format(car.car_code))
                        print("Car name: {}".format(car.car_name))
                        print("Car capacity: {}".format(car.car_capacity))
                        print("Car horsepower: {}".format(car.car_horsepower))
                        print("Car weight: {}".format(car.car_weight))
                        print("Car type: {}".format(car.car_type))
                        print("---")
            else:
                print("The input is not valid. Please try again.")
                continue
        elif menu_option == "c":
            order_info = input(
                "Please type in your prefered retailer id and car id (seperated by a whitespace): "
            )
            if len(order_info.split(" ")) != 2:
                print("The input is not valid. Please try again.")
                continue
            order_retailer_id, order_car_id = order_info.split(" ")
            if (
                len(order_retailer_id) != 8
                or not order_retailer_id.isdigit()
                or int(order_retailer_id) not in retailer_id_list
            ):
                print("The input retailer id is not valid. Please try again.")
                continue
            for retailer in retailers:
                if retailer.retailer_id == int(order_retailer_id):
                    current_retailer = retailer
                    break
            if (
                len(order_car_id) != 8
                or not order_car_id.isalnum()
                or order_car_id not in current_retailer.carretailer_stock
            ):
                print("The input car id is not valid. Please try again.")
            cur_retailer_cars = current_retailer.get_all_stock()
            for car in cur_retailer_cars:
                if car.car_code == order_car_id:
                    current_car = car
                    break
            current_hour, current_minute = strftime("%H %M").split(" ")
            current_hour = int(current_hour) + int(current_minute) / 60
            if not current_retailer.is_operating(current_hour):
                print("The retailer currently is closed. Please try again.")
                continue
            order = Order("", current_car, current_retailer, ceil(time()))
            order.order_id = order.generate_order_id(current_car.car_code)
            with open("../data/order.txt", "a", encoding="utf-8") as f:
                f.write(order.__str__() + "\n")
            print("The order has been placed successfully!")
            print(order)
        elif menu_option == "d":
            print("Thank you for using our system. Hope to see you soon.")
            break
        else:
            print("The input is invalid. Please try again.")


if __name__ == "__main__":
    main()
