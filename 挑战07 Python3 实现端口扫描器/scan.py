import re
from socket import socket
from sys import argv
from sys import exit


def port_scanner(host, port):
    try:
        s = socket()
        s.settimeout(0.1)
        s.connect((host, port))
        print('%s open' % port)
    except:
        print('%s closed' % port)
    finally:
        s.close()


def get_args(regex_port, regex_host, message):
    if len(argv) != 5:
        print(message)
        exit()
    elif argv[1] != '--host' and argv[3] != '--port':
        print(message)
        exit()

    try:
        host = regex_host.search(argv[2]).group()
    except AttributeError:
        print(message)
        exit()

    if '-' in argv[4]:
        try:
            mo = regex_port.search(argv[4])
            port1 = int(mo.group(1))
            port2 = int(mo.group(2))
        except ValueError:
            print(message)
            exit()
        else:
            return [host, port1, port2]
    else:
        try:
            mo = regex_port.search(argv[4])
            port = int(mo.group())
        except ValueError:
            print(message)
            exit()
        else:
            return [host, port]


def main():
    regex_port = re.compile(r'(\d+)-{,1}(\d*)')
    regex_host = re.compile(r'^\d+\.{1}\d+\.{1}\d+\.{1}\d+$')
    # 如需通过挑战需要将下面的 message 内容改成 'Parameter Error'
    message = '''
        Usage
        =====
        python3 scan.py [options] --host <host> --port <port>
                    
        <host> example 1.1.1.1
        <port> example 20 or 20-40
        '''
    args = get_args(regex_port, regex_host, message)
    if len(args) == 2:
        port_scanner(args[0], args[1])
    else:
        for i in range(args[1], args[2] + 1):
            port_scanner(args[0], i)


if __name__ == '__main__':
    main()
