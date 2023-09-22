from retailer import Retailer
from car import Car
from order import Order
import random


class CarRetailer(Retailer):
    def __init__(
        self,
        retailer_id=-1,
        retailer_name='',
        carretailer_address='',
        carretailer_business_hour=(6, 11),
        carretailer_stock=[]
    ):
        super().__init__(retailer_id, retailer_name)
        self.carretailer_address = carretailer_address
        self.carretailer_business_hour = carretailer_business_hour
        self.carretailer_stock = carretailer_stock

    def __str__(self):
        return super().__str__() + ', ' + str(self.carretailer_address) + ', ' + str(self.carretailer_business_hour) + ', ' + str(self.carretailer_stock)

    def load_current_stock(self, stock_file_path):
        # load the data
        with open(stock_file_path, 'r', encoding='utf-8') as f:
            stocks = f.readlines()
        stocks = [x.strip().split(', ') for x in stocks]
        for stock in stocks:
            # for each line, the first element is the retailer id
            # if the id is same, get the stock info
            if int(stock[0]) == int(self.retailer_id):
                carcode_list = []
                for car_info in stock[6:]:
                    car_info = car_info.strip("\[\]\'")
                    carcode_list.append(car_info)
                self.carretailer_stock = carcode_list[0::6]

    def is_operating(self, cur_hour):
        # the first element in the tuple is opening time
        # the second element in the tuple is closing time
        if (
            cur_hour >= int(self.carretailer_business_hour[0])
            and cur_hour < int(self.carretailer_business_hour[1])
        ):
            return True
        return False

    def get_all_stock(self):
        with open('..\data\stock.txt', 'r', encoding='utf-8') as f:
            stocks = f.readlines()
        stocks = [x.strip().split(', ') for x in stocks]

        for stock in stocks:
            if int(stock[0]) == int(self.retailer_id):
				# get the car information
				# remove the [ ] and ' in the string
                car_info_list = []
                for car_info in stock[6:]:
                    car_info = car_info.strip("\[\]\'")
                    car_info_list.append(car_info)
                    
        car_obj_list = []
        for i in range(0,len(car_info_list),6):
            car_obj_list.append(
                Car(
                    car_info_list[i],
                    car_info_list[i+1],
                    car_info_list[i+2], 
                    car_info_list[i+3], 
                    car_info_list[i+4], 
                    car_info_list[i+5]
                )
			)
        return car_obj_list

    def get_postcode_distance(self, postcode):
        retailer_postcode = self.carretailer_address[-4:]
        difference = abs(int(retailer_postcode) - int(postcode))
        return difference

    def remove_from_stock(self, car_code):
        if car_code not in self.carretailer_stock:
            return False

        with open('..\data\stock.txt', 'r', encoding='utf-8') as f:
            stocks = f.readlines()

        flag = False
        for idx in range(len(stocks)):
            line_id = stocks[idx].strip().split(', ')[0]
            if int(line_id) == self.retailer_id:
                cars = self.get_all_stock()
                for car in cars:
                    if  car.car_code == car_code:
                        flag = True
                    else:
                        stock_cars = [car.__str__() for car in cars]
                    
                stocks[idx] = ', '.join(stocks[idx].strip().split(', ')[:6]) + str(stock_cars) 

        with open('..\data\stock.txt', 'w', encoding='utf-8') as f:
            for line in stocks:
                f.write(line)

        return flag

    # 2.3.8
    def add_to_stock(self, car_obj):
        # if the car_obj already in the carretailer stock, return False
        if car_obj.car_code in self.carretailer_stock:
            return False

        with open('..\data\stock.txt', 'r', encoding='utf-8') as f:
            stocks = f.readlines()

        for idx in range(len(stocks)):
            line_id = stocks[idx].strip().split(', ')[0]
            if int(line_id) == self.retailer_id:
                cars = self.get_all_stock()
                cars.append(car_obj)
                stock_cars = [car.__str__() for car in cars]
                stocks[idx] = ', '.join(stocks[idx].strip().split(', ')[:6]) + str(stock_cars)

        with open('..\data\stock.txt', 'w', encoding='utf-8') as f:
            for line in stocks:
                f.write(line)
        return True

    # 2.3.9
    def get_stock_by_cartype(self, car_types):
        result = []
        car_obj_list = self.get_all_stock()
        for type in car_types:
            for car in car_obj_list:
                if type == car.car_type:
                    result.append(car)
        return result

    def get_stock_by_licence_type(self, licence_type):
        car_obj_list = self.get_all_stock()
        cars = []
        if licence_type == 'P':
            for car in car_obj_list:
                if car.probationary_licence_prohibited_vehicle():
                    pass
                else:
                    cars.append(car)
        else:
            return car_obj_list

        return cars

    def car_recommendation(self):
        car_obj_list = self.get_all_stock()
        random_car = random.choice(car_obj_list)
        return random_car

    def create_order(self, car_code):
        car_obj_list = self.get_all_stock()
        self.remove_from_stock(car_code)

        for car in car_obj_list:
            if car.car_code == car_code:
                retailer = Retailer(self.retailer_id, self.retailer_name)
                order_id = Order().generate_order_id(car_code)
                order_creation_time = order_id[-10:]
                order_obj = Order(order_id, car, retailer, order_creation_time)
                line = [order_id, car.car_code,
                        self.retailer_id, order_creation_time]

        with open('../data/order.txt', 'a', encoding='utf-8') as f:
            f.write(', '.join(line)+'\n')
        return order_obj
