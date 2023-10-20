import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from handle_data import LoadData


class Graphy:
    def prop_val_distribution(dataframe, suburb, target_currency):
        suburb_list = dataframe['suburb'].unique()
        # 根据suburb筛选数据
        if suburb in suburb_list:
            df = dataframe[dataframe['suburb']==suburb].reset_index(drop=True)
        # 如果suburb为'all'，则使用整个数据集
        elif suburb == 'all':
            df = dataframe
        # 如果不在列表中，返回提示
        else:
            print ('Suburb not found, generating graph for all suburbs')
            suburb = 'all'
            df = dataframe

        # 去除price为空的数据
        df_price = df.dropna(subset=['price']).reset_index(drop=True)

        currency_dict = {"AUD": 1, "USD": 0.66, "INR": 54.25, "CNY":
        4.72, "JPY": 93.87, "HKD": 5.12, "KRW": 860.92, "GBP": 0.51,
        "EUR": 0.60, "SGD": 0.88}

        # 获取汇率
        currency = currency_dict[target_currency]
        # invoke currency_exchange function获取numpy array
        data = LoadData.currency_exchange(df_price, currency)
        
        # 将数据分成100个区间
        bins = np.linspace(min(data), max(data), num=101)

        # 绘制直方图
        plt.hist(data, bins=bins, alpha=0.7, color='orange', edgecolor='white')

        # 设置图形标题和轴标签
        plt.title('Property Value Distribution')
        plt.xlabel('Price in ' + target_currency)
        plt.ylabel('Number of properties')

        # 保存图形
        plt.savefig(suburb + '_' + target_currency+ '_distribution.png')
        plt.close()


    def sales_trend(dataframe):
        # 去除sold_date列的空值
        df = dataframe.dropna(subset=['sold_date']).reset_index(drop=True)
        
        # 将sold_date列转换为datetime格式
        df['sold_date'] = pd.to_datetime(df['sold_date'])
        df['sold_year'] = df['sold_date'].dt.year

        # 通过id计数，获取每年的销售量
        df_group_year = df.groupby('sold_year').count()['id'].to_frame().rename(columns={'id':'number_of_properties_sold'})
        df_group_year.reset_index(inplace=True)

        # 生成折线图
        plt.plot(df_group_year['sold_year'], df_group_year['number_of_properties_sold'], color='orange', marker='o')
        plt.title('Number of Properties Sold in Each Year')
        plt.xlabel('Year')
        plt.ylabel('Number')

        # 保存图形
        plt.savefig('number_of_properties_sold.png')
        plt.close()


# Graphy.prop_val_distribution(LoadData.extract_property_info('property_information.csv'), 'Clayton', 'AUD')
# Graphy.sales_trend(LoadData.extract_property_info('property_information.csv'))