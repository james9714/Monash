import pandas as pd
import numpy as np
from handle_data import LoadData

class Suburb:
    def suburb_summary(dataframe, suburb):
        # 获取suburb列表
        suburb_list = dataframe['suburb'].unique()

        # 根据suburb筛选数据
        if suburb in suburb_list:
            df = dataframe[dataframe['suburb']==suburb].reset_index(drop=True)
        # 如果suburb为'all'，则使用整个数据集
        elif suburb == 'all':
            df = dataframe
        # 如果不在列表中，返回提示
        else:
            print ('Suburb not found')
            df = None
            
        if df is not None:
            # 计算bedrooms的四个统计量
            mean_bedrooms = df['bedrooms'].mean().round(4)
            std_deviation_bedrooms = df['bedrooms'].std().round(4)
            median_bedrooms = df['bedrooms'].median()
            min_bedrooms = df['bedrooms'].min()
            max_bedrooms = df['bedrooms'].max()

            mean_bathrooms = df['bathrooms'].mean().round(4)
            std_deviation_bathrooms = df['bathrooms'].std().round(4)
            median_bathrooms = df['bathrooms'].median()
            min_bathrooms = df['bathrooms'].min()
            max_bathrooms = df['bathrooms'].max()

            mean_parking = df['parking_spaces'].mean().round(4)
            std_deviation_parking = df['parking_spaces'].std().round(4)
            median_parking = df['parking_spaces'].median()
            min_parking = df['parking_spaces'].min()
            max_parking = df['parking_spaces'].max()

            # 打印结果
            print('-'*30)
            print("Suburb summary for:", suburb)
            print("\nStatistics for 'bedrooms':")
            print("Mean:", mean_bedrooms)
            print("Standard Deviation:", std_deviation_bedrooms)
            print("Median:", median_bedrooms)
            print("Minimum:", min_bedrooms)
            print("Maximum:", max_bedrooms)

            print("\nStatistics for 'bathrooms':")
            print("Mean:", mean_bathrooms)
            print("Standard Deviation:", std_deviation_bathrooms)
            print("Median:", median_bathrooms)
            print("Minimum:", min_bathrooms)
            print("Maximum:", max_bathrooms)

            print("\nStatistics for 'parking_spaces':")
            print("Mean:", mean_parking)
            print("Standard Deviation:", std_deviation_parking)
            print("Median:", median_parking)
            print("Minimum:", min_parking)
            print("Maximum:", max_parking)
        else:
            return 

    def  avg_land_size(dataframe, suburb):
        suburb_list = dataframe['suburb'].unique()
        # 根据suburb筛选数据
        if suburb in suburb_list:
            df = dataframe[dataframe['suburb']==suburb].reset_index(drop=True)
            avg_land_size = df['land_size'].mean().round(4)
            return avg_land_size
        # 如果suburb为'all'，则使用整个数据集
        elif suburb == 'all':
            df = dataframe
            avg_land_size = df['land_size'].mean().round(4)
            return avg_land_size
        # 如果不在列表中，返回提示
        else:
            return None
        
            
    def locate_price(target_price, data, target_suburb):
        # 获取suburb列表
        df = data[data['suburb']==target_suburb].reset_index(drop=True)
        # 去除price为空的数据
        df = df.dropna(subset=['price']).reset_index(drop=True)
        # 获取price列的数据，转化为列表
        price_list = df['price'].tolist()

        #   排序 从大到小
        price_list = LoadData.reverse_insertion_sort(price_list)
        
        # 二分查找
        result = LoadData.recursive_binary_search(price_list, 0, len(price_list) - 1, int(target_price))

        if result != -1:
            return True
        else:
            return False
        
#print(Suburb.locate_price(405000.0, pd.read_csv("9136/ass3/property_information.csv"), 'Clayton'))