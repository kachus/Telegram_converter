
import requests
import json
currencies = {'USD': 'USDT',
              'EUR' : 'EUR',
              'RUB': 'RUB'


}

crypto_currencies = {'BTC': 'BTC',
                     'ETH': 'ETH',
                     'SAT': 'SAT'


}


def create_ans():
     #открыть файл с тремя переменными, обработать, вызвать с ними функцию, импортнуть файл в исходный код.
     # Выдать результат в логе
     #удалить инфу из файла
    with open("/Users/Evgenia/Desktop/data.txt", 'r') as f:
        cur_inp_from, value, cur_inp_to = f.read().strip().split()
        value = int(value)
        template = "{} {} = {} {}"
        ans = count_ans(cur_inp_from, value, cur_inp_to)
    return template.format(value, cur_inp_from, ans, cur_inp_to)

def count_ans(currency_from, value, currency_to):
    try:
        if currency_to == 'SAT':
            currency_to = 'BTC'
            ans = count_ans(currency_from, value, currency_to) * 10**8
            return ans
        currency_from = currencies[currency_from]
        currency_to = crypto_currencies[currency_to]
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={currency_to}{currency_from}"
        r = requests.get(url)
        data = json.loads(r.text)
        try:
            currency_rate = float(data['price'])
            return value/currency_rate
        except KeyError:
            print('No such URL')
    except KeyError:
        print('No such key in dict')
    except TypeError:
         print('Value must be float, not string')




# if __name__ == "__main__":
#     print('nothing')
# execute func only when it is not main
