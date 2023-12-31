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
    df_main = LoadData.extract_property_info('property_information.csv')
    suburb_list = df_main['suburb'].unique()
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
            Suburb.suburb_summary(df_main, input_suburb)

            avg_land_size = Suburb.avg_land_size(df_main, input_suburb)
            if avg_land_size != None:
                print('-'*30)
                print('Average land size:', avg_land_size,'m^2')
                print('-'*30)
                question = 'Do you want to see the distribution of '+suburb+'(Y/N)?'
            else:
                question = 'Do you want to see the distribution of all suburbs(Y/N)?'

            while True:
                choice_visual = input(question)
                if choice_visual.isalpha() and choice_visual.upper() == 'Y':
                    print(currency_list)
                    user_currency = input('Please enter the currency: ')
                    if user_currency.upper() not in currency_list:
                        print('Currency not found, use AUD as default')
                    Graphy.prop_val_distribution(df_main, input_suburb, user_currency.upper())
                    print('-'*30)
                    print('Graph generated successfully!')
                    print('-'*30)
                    break
                elif choice_visual.isalpha() and choice_visual.upper() == 'N':
                    break
                else:
                    print('Invalid input, please enter again')
        elif choice == 2:
            Graphy.sales_trend(LoadData.extract_property_info('property_information.csv'))
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
            if Suburb.locate_price(price, df_main, suburb):
                print('Found a property in', suburb, 'with price', price)
            else:
                print('Not found a property in', suburb, 'with price', price)
        elif choice == 4:
            break


if __name__ == '__main__':
    main()