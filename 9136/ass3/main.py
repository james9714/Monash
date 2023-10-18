from graph_generate import Graphy
from suburb_analyse import Suburb
from handle_data import LoadData

def main_menu():
    print('\n1.Suburb infomations')
    print('2.Property sales trend')
    print('3.Found a property')
    print('4.Exit\n')


def main():
    # 读取数据
    df = LoadData.extract_property_info('property_information.csv')
    suburb_list = df['suburb'].unique()
    currency_dict = {"AUD": 1, "USD": 0.66, "INR": 54.25, "CNY":
    4.72, "JPY": 93.87, "HKD": 5.12, "KRW": 860.92, "GBP": 0.51,
    "EUR": 0.60, "SGD": 0.88}
    currency_list = list(currency_dict.keys())
    while True:
        main_menu()
        choice = int(input('Please enter your choice(1,2,3,4): '))
        if choice == 1:
            for suburb in suburb_list:
                print(suburb)
            input_suburb = input("\nPlease enter the suburb(or 'all'): ")
            while True:
                if input_suburb not in suburb_list and input_suburb != 'all':
                    print('Suburb not found, please enter again')
                    input_suburb = input('Please enter the suburb: ')
                else:
                    break
            Suburb.suburb_summary(df, input_suburb)
            avg_land_size = Suburb.avg_land_size(df, input_suburb)
            print('-'*30)
            print('Average land size:', avg_land_size,'m^2')
            print('-'*30)
            choice_visual = input('Do you want to the distribution(Y/N)?')
            while True:
                if choice_visual == 'Y':
                    print(currency_list)
                    user_currency = input('Please enter the currency: ')
                    if user_currency.upper() not in currency_list:
                        print('Currency not found, use AUD as default')
                    Graphy.prop_val_distribution(df, input_suburb, user_currency.upper())
                    break
                elif choice_visual == 'N':
                    break
                else:
                    print('Invalid input, please enter again')
        elif choice == 2:
            Graphy.sales_trend(df)
        elif choice == 3:
            print('Input the suburb name and price to find a property')
            suburb = input('Please enter the suburb: ')
            while True:
                if suburb not in suburb_list:
                    print('Suburb not found, please enter again')
                    suburb = input('Please enter the suburb: ')
                else:
                    break
            price = input('Please enter the price: ')
            while True:
                if price.isdigit():
                    break
                else:
                    print('Invalid input, please enter again')
                    price = input('Please enter the price: ')
            if Suburb.locate_price(price, df, suburb):
                print('Found a property in', suburb, 'with price', price)
            else:
                print('Not found a property in', suburb, 'with price', price)
        elif choice == 4:
            break


if __name__ == '__main__':
    main()