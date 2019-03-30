import csv
from sys import argv, exit
from multiprocessing import Process, Queue

queue = Queue()


class Args():
    """命令行参数类"""

    def __init__(self):
        """获取命令行参数"""
        if len(argv) != 7:
            print('Wrong parameter.')
            exit()
        else:
            self.args = argv[1:]

    def get_path(self, parm):
        """根据参数获取所需文件路径"""
        path = self.args[self.args.index(parm) + 1]
        return path

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


class Config():
    """配置文件类"""

    def __init__(self):
        self._config = {}
        self.cfg_value = self.open_cfg_file()

    def open_cfg_file(self):
        """获取配置文件并得到相应参数的字典"""
        try:
            with open(args.cfg_path) as f_obj:
                for line in f_obj.readlines():
                    list1 = line.split('=')
                    self._config[list1[0].strip()] = list1[1].strip()
            return self._config
        except FileNotFoundError:
            print('Can not find "%s".' % (args.cfg_path))
            exit()

    def get_cfg(self, key):
        """获取字典中的值"""
        try:
            self.value = float(self.cfg_value[key])
            return self.value
        except KeyError:
            print('Cfg key: "%s" was wrong.' % (key))
            exit()
        except ValueError:
            print('Cfg key: "%s"\'s value was wrong.' % (key))
            exit()

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
            print(k)
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
                '%.2f' % real_wage
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
                self.save_data(item)
            except:
                return


userdata = UserData(queue)
incometax = IncomeTax(queue)


userdata.start()
incometax.start()

userdata.join()
incometax.join()
