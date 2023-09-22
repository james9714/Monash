from retailer import Retailer
from car import Car
from order import Order
from random import choice
from math import ceil
import re
import time


class CarRetailer(Retailer):
    def __init__(
        self,
        retailer_id=11111111,
        retailer_name="",
        carretailer_address="",
        carretailer_business_hours=(0, 0),
        carretailer_stock=[],
    ):
        super().__init__(retailer_id, retailer_name)
        self.carretailer_address = carretailer_address
        self.carretailer_business_hours = carretailer_business_hours
        self.carretailer_stock = carretailer_stock

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(
            self.retailer_id,
            self.retailer_name,
            self.carretailer_address,
            self.carretailer_business_hours,
            self.carretailer_stock,
        )

    def load_current_stock(self, path):
        with open(path, "r", encoding="utf-8") as f:
            stocks = f.readlines()

        for stock in stocks:
            if str(self.retailer_id) in stock:
                stock_info = stock.strip("\n").split(", ")
                car_stock = ", ".join(stock_info[6:])
                car_code_list = re.findall(r"[A-Z]{2}\d{6}", car_stock)
                self.carretailer_stock = car_code_list
                break

    def is_operating(self, cur_hour):
        if (
            cur_hour <= self.carretailer_business_hours[1]
            and cur_hour >= self.carretailer_business_hours[0]
        ):
            return True
        return False

    def get_all_stock(self):
        with open("../data/stock.txt", "r", encoding="utf-8") as f:
            stocks = f.readlines()

        cars = []
        for stock in stocks:
            if str(self.retailer_id) in stock:
                stock_info = stock.strip("\n").split(", ")
                car_info = stock_info[6:]
                num_of_cars = len(car_info) // 6
                for num in range(num_of_cars):
                    car_code = car_info[num * 6 + 0].strip("[']")
                    car_name = car_info[num * 6 + 1]
                    car_capacity = int(car_info[num * 6 + 2])
                    car_horsepower = int(car_info[num * 6 + 3])
                    car_weight = int(car_info[num * 6 + 4])
                    car_type = car_info[num * 6 + 5].strip("[']")
                    cars.append(
                        Car(
                            car_code,
                            car_name,
                            car_capacity,
                            car_horsepower,
                            car_weight,
                            car_type,
                        )
                    )
                return cars

    def get_postcode_distance(self, postcode):
        retailer_postcode = self.carretailer_address[-4:]
        distance = abs(int(retailer_postcode) - postcode)
        return distance

    def remove_from_stock(self, car_code):
        if car_code not in self.carretailer_stock:
            return False
        else:
            self.carretailer_business_hours.remove(car_code)

            cars = self.get_all_stock()
            target = -1
            for i in range(len(cars)):
                if cars[i].car_code == car_code:
                    target = i
                    break
            cars.pop(target)

            with open("../data/stock.txt", "r", encoding="utf-8") as f:
                stocks = f.readlines()

            for i in range(len(stocks)):
                if self.retailer_id in stocks[i]:
                    stock_cars = [car.__str__() for car in cars]
                    retailer_str = "{}, {}, {}, {}, {}\n".format(
                        self.retailer_id,
                        self.retailer_name,
                        self.carretailer_address,
                        self.carretailer_business_hours,
                        stock_cars,
                    )
                    stocks[i] = retailer_str

            with open("../data/stock.txt", "w", encoding="utf-8") as f:
                for stock in stocks:
                    f.write(stock)
                return True

    def add_to_stock(self, car):
        if car.car_code in self.carretailer_stock:
            return False
        else:
            self.carretailer_stock.append(car.car_code)

            cars = self.get_all_stock()
            cars.append(car)

            with open("../data/stock.txt", "r", encoding="utf-8") as f:
                stocks = f.readlines()

            for i in range(len(stocks)):
                if self.retailer_id in stocks[i]:
                    stock_cars = [car.__str__() for car in cars]
                    retailer_str = "{}, {}, {}, {}, {}\n".format(
                        self.retailer_id,
                        self.retailer_name,
                        self.carretailer_address,
                        self.carretailer_business_hours,
                        stock_cars,
                    )
                    stocks[i] = retailer_str
                    break

            with open("../data/stock.txt", "w", encoding="utf-8") as f:
                for stock in stocks:
                    f.write(stock)
                return True

    def get_stock_by_car_type(self, car_types):
        cars = self.get_all_stock()

        result = [car for car in cars if car.car_type in car_types]
        return result

    def get_stock_by_licence_type(self, licence_type):
        cars = self.get_all_stock()
        if licence_type == "P":
            cars = [
                car
                for car in cars
                if car.probationary_licence_prohibited_vehicle() == False
            ]
            return cars
        else:
            return cars

    def car_recommendation(self):
        cars = self.get_all_stock()

        car = choice(cars)
        return car

    def create_order(self, car_code):
        cars = self.get_all_stock()
        self.remove_from_stock(car_code)
        for car in cars:
            if car.car_code == car_code:
                retailer = CarRetailer(
                    self.retailer_id,
                    self.retailer_name,
                    self.carretailer_address,
                    self.carretailer_business_hours,
                    self.carretailer_stock,
                )
                order = Order("", car, retailer, ceil(time.time()))
                order.order_id = order.generate_order_id(car_code)
                with open("../data/order.txt", "a", encoding="utf-8") as f:
                    f.write(order.__str__() + "\n")
