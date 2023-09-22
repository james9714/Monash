from car import Car
import time
import random
import string


class Order:
    def __init__(
        self,
        order_id="",
        order_car=None,
        order_retailer=None,
        order_creation_time=round(time.time()),
    ):
        self.order_id = order_id
        self.order_car = order_car
        self.order_retailer = order_retailer
        self.order_creation_time = order_creation_time

    def __str__(self):
        return "{}, {}, {}, {}".format(
            self.order_id,
            self.order_car.car_code,
            self.order_retailer.retailer_id,
            self.order_creation_time,
        )

    def generate_order_id(self, car_code):
        str_1 = "~!@#$%^&*"
        upper_char = string.ascii_uppercase
        random_str = random.choices(upper_char, k=6)

        temp_str = ""
        for n in range(len(random_str)):
            if n % 2 == 1:
                temp_str += random_str[n].upper()
            else:
                temp_str += random_str[n]

        final_str = ""
        for i in range(len(temp_str)):
            ord_code = ord(temp_str[i])
            final_str += str_1[ord_code % len(str_1)] * i

        return temp_str + final_str + car_code + str(self.order_creation_time)
