import csv
from sys import argv, exit
from multiprocessing import Process, Queue
from configparser import ConfigParser
from datetime import datetime
from getopt import getopt

queue = Queue()


class Args():
    """命令行参数类"""

    def __init__(self):
        """获取命令行参数"""
        if len(argv) == 9:
            self.args = argv[1:]
        elif len(argv) == 2:  # and (argv[1] == '-h' or argv[1] == '--help'):
            self.get_usage()
        else:
            print(
                'Wrong parameter, if you need help, enter "calculator.py -h or --help".')
            exit()

    def usage(self):
        """使用说明"""
        print("========================")
        print("Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata")
        print("========================")
        exit()

    def get_usage(self):
        """获取使用说明"""
        try:
            options, s = getopt(argv[1:], '-h', ['help'])
        except:
            print('If you need help, enter "calculator.py -h or --help"')
            exit()
        for opt_name, opt_value in options:
            if opt_name in ('-h', '--help'):
                self.usage()
            else:
                print('If you need help, enter "calculator.py -h or --help"')
                exit()

    def get_path(self, parm):
        """根据参数获取所需文件路径"""
        path = self.args[self.args.index(parm) + 1]
        return path

    @property
    def get_city(self):
        """获取城市"""
        return self.get_path('-C')

    @property
    def cfg_path(self):
        """获取配置文件"""
        return self.get_path('-c')

    @property
    def wage_path(self):
        """获取用户工资文件"""
        return self.get_path('-d')

    @property
    def data_path(self):
        """计算完成数据保存路径"""
        return self.get_path('-o')


args = Args()
cfg = ConfigParser()


class Config():
    """配置文件类"""

    def __init__(self):
        self.cfg_value = self.read_cfg_file()

    def read_cfg_file(self):
        """读取配置文件参数"""
        return cfg.read(args.cfg_path, encoding='UTF-8')

    def get_cfg(self, key):
        """获取配置文件参数"""
        if args.get_city.upper() in cfg.sections():
            return float(cfg.get(args.get_city.upper(), key))
        else:
            return float(cfg.get('DEFAULT', key))

    @property
    def insurance_rate(self):
        """获取社保费率"""
        return sum([
            self.get_cfg('YangLao'),
            self.get_cfg('YiLiao'),
            self.get_cfg('ShiYe'),
            self.get_cfg('GongShang'),
            self.get_cfg('ShengYu'),
            self.get_cfg('GongJiJin')
        ])

    @property
    def jishul(self):
        """获取最低基数"""
        return self.get_cfg('JiShuL')

    @property
    def jishuh(self):
        """获取最高基数"""
        return self.get_cfg('JiShuH')


config = Config()


class UserData(Process):
    """用户工资类"""

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.user_data = self.open_wage_file()

    def open_wage_file(self):
        """获取用户工资数据"""
        self.user_dict = {}
        try:
            with open(args.wage_path) as f_obj:
                for line in f_obj.readlines():
                    list1 = line.split(',')
                    self.user_dict[list1[0]] = list1[1].strip()
            self.queue.put(self.user_dict)
            return self.user_dict
        except FileNotFoundError:
            print('Can not find "%s"' % (args.wage_path))
            exit()


class IncomeTax(Process):
    """工资计算类"""

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    @classmethod
    def clac_insurance(cls, wage):
        """计算应缴纳社保金额"""
        if wage <= config.jishul:
            insurance = config.jishul * config.insurance_rate
        elif wage >= config.jishuh:
            insurance = config.jishuh * config.insurance_rate
        else:
            insurance = wage * config.insurance_rate
        return insurance

    @classmethod
    def clac_tax(cls, wage, insurance):
        """计算个人所得税"""
        no_insurace = wage - insurance
        if no_insurace < 5000:
            tax = 0.00
        elif no_insurace - 5000 <= 3000:
            tax = (no_insurace - 5000) * 0.03
        elif no_insurace - 5000 <= 12000:
            tax = (no_insurace - 5000) * 0.1 - 210
        elif no_insurace - 5000 <= 25000:
            tax = (no_insurace - 5000) * 0.2 - 1410
        elif no_insurace - 5000 <= 35000:
            tax = (no_insurace - 5000) * 0.25 - 2660
        elif no_insurace - 5000 <= 55000:
            tax = (no_insurace - 5000) * 0.3 - 4410
        elif no_insurace - 5000 <= 80000:
            tax = (no_insurace - 5000) * 0.35 - 7160
        else:
            tax = (no_insurace - 5000) * 0.45 - 15160
        return tax

    @classmethod
    def clac_real_wage(cls, wage, insurance, tax):
        """计算到手工资"""
        real_wage = wage - insurance - tax
        return real_wage

    def save_data(self, item):
        """计算用户数据，并将数据写入文件"""
        result = []
        for k, v in item.items():
            wage = float(v)
            id = k
            insurance = self.clac_insurance(wage)
            tax = self.clac_tax(wage, insurance)
            real_wage = self.clac_real_wage(wage, insurance, tax)

            result.append([
                id,
                '%.2f' % wage,
                '%.2f' % tax,
                '%.2f' % insurance,
                '%.2f' % real_wage,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
        try:
            with open(args.data_path, 'w') as f_obj:
                csv.writer(f_obj).writerows(result)
        except FileNotFoundError:
            print('Path "%s" does not exist' % (args.data_path))

    def run(self):
        """获取数据"""
        while True:
            try:
                item = self.queue.get(timeout=1)
                # print(item)
                self.save_data(item)
            except:
                return


userdata = UserData(queue)
incometax = IncomeTax(queue)


userdata.start()
incometax.start()

userdata.join()
incometax.join()
