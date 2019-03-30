from sys import argv
from sys import exit


def calc(wage):
    num = wage - 5000
    if num <= 0:
        tax = 0
    elif num <= 3000:
        tax = num * 0.03
    elif num <= 12000:
        tax = num * 0.1 - 210
    elif num <= 25000:
        tax = num * 0.2 - 1410
    elif num <= 35000:
        tax = num * 0.25 - 2660
    elif num <= 55000:
        tax = num * 0.3 - 4410
    elif num <= 80000:
        tax = num * 0.35 - 7160
    else:
        tax = num * 0.45 - 15160
    
    return format(tax, '.2f')

if __name__ == '__main__':
    if len(argv) > 2:
        print('Wrong parmmeter.')
        exit()
    try:
        wage = int(argv[1])
    except ValueError:
        print('Wrong parmmeter.')
        exit()
    else:
        print(calc(wage))
