from sys import argv
from sys import exit


def calc(wage):
    '''基于挑战1，增加rate（社保费率）
       返回结果是实际到手工资
    '''
    rate = 0.08 + 0.02 + 0.005 + 0.06
    num = wage - wage * rate - 5000
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

    return format(wage - wage * rate - tax, '.2f')


if __name__ == '__main__':
    try:
        for arg in argv[1:]:
            info = arg.split(':')
            wage = float(info[1])
            print(info[0] + ':' + calc(wage))
    # 判断工资是否为数字
    except ValueError:
        print('Wrong parameter.')
        exit()
    # 判断参数格式是否是（工号:工资)
    except IndexError:
        print('Wrong parameter.')
        exit()
