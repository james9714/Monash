import pandas as pd
import numpy as np

class LoadData:
    def extract_property_info(file_path):
        df = pd.read_csv(file_path)
        return df
    
    def currency_exchange(dataframe, exchange_rate):
        transformed_price = dataframe['price'] * exchange_rate
        return np.array(transformed_price)
    
    def reverse_insertion_sort(price_list):
        price_list = [int(x) for x in price_list]
        for i in range(1, len(price_list)):
            value = price_list[i]
            j = i - 1
            while j >= 0 and value > price_list[j]:
                price_list[j + 1] = price_list[j]
                j -= 1
            price_list[j + 1] = value
        return price_list
    

    def recursive_binary_search(price_list, low, high, tagert_price):
        # 检查基本情况，如果low大于high，表示价格列表中没有找到目标价格
        if low <= high:
            mid = low + (high - low) // 2
            
            # 如果目标价格等于价格列表中间值
            if price_list[mid] == tagert_price:
                return mid
            
            # 如果目标价格比价格列表中间值小，只需要在右半部分继续查找
            # [7,6,5,4,3,2,1], 找1，列表会变成[4,3,2,1]
            elif price_list[mid] < tagert_price:
                return LoadData.recursive_binary_search(price_list, low, mid - 1, tagert_price)
            
            # 如果目标价格比价格列表中间值大，只需要在左半部分继续查找
            else:
                return LoadData.recursive_binary_search(price_list, mid + 1, high, tagert_price)
        else:
            # 目标价格不在列表中
            return -1

# test = LoadData.reverse_insertion_sort([1, 2, 3, 4, 5])
# print(test)

# test = LoadData.recursive_binary_search([1, 2, 3, 4, 5], 0, 4, 3)
# print(test)