if __name__ == '__main__':
    shortCurrency = ['$', '€', '¢', '£', '¥', 'zl', '%']
    currencySymbol = ['usd', 'eur', 'crc', 'gbp', 'jpy', 'pln', 'per']
    Currency = ['usa dolar', 'euro', 'costa rican colon', 'british pound sterling', 'japanese yen', 'polish zloty',
                'percent']
    file = open('./Documents/Currencies.txt', 'w')
    for i in range(0, len(shortCurrency)):
        file.writelines(str(currencySymbol[i]) + '-' + str(shortCurrency[i]) + '-' + str(Currency[i]) +'\n')
    file.close()