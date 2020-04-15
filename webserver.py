import re
from socket import *
from select import *


class HTTPServer:
    def __init__(self, host="0.0.0.0", port=80, path=None):
        self.host = host
        self.port = port
        self.path = path
        self.create_socket()

        self.rs = []
        self.ws = []
        self.xs = []

    def start(self):
        self.s.listen(3)
        self.rs.append(self.s)

        while True:
            try:
                rlist, wlist, xlist = select(self.rs, self.ws, self.xs)
                for r in rlist:
                    if r is self.s:
                        conndf, addr = r.accept()
                        print("Connect from", addr)
                        conndf.setblocking(False)
                        self.rs.append(conndf)
                    else:
                        self.response(r)
            except:
                self.s.close()

    def response(self, conndf):
        try:
            print("OKKKKK")
            data = conndf.recv(1024).decode()
            print("OKKKKK1")
            info = re.findall(r"GET (/\S*) HTTP", data)
            print(info)
        except Exception as e:
            print(e)
            self.rs.remove(conndf)
            conndf.close()
            return
        else:
            self.get_html(conndf, info[0])
            self.rs.remove(conndf)
            conndf.close()

    def create_socket(self):
        self.s = socket()
        self.s.setblocking(False)
        self.s.bind((self.host, self.port))

    def get_html(self, conndf, info):
        if info == "/":
            filename = self.path + "/index.html"
        else:
            filename = self.path + info
        try:
            f = open(filename, "rb")
        except:
            response_head = "HTTP1.1 404 NOT FOUND\r\n"
            response_head += "Content-Type:text/html\r\n"
            response_head += "\r\n"
            response_content = "<h1>Sorry...</h1>"
            response = response_head.encode() + response_content.encode()
        else:
            response_content = f.read()
            response_head = "HTTP1.1 200 OK\r\n"
            response_head += "Content-Type:text/html\r\n"
            response_head += "Content-Length:%d\r\n" % len(response_content)
            response_head += "\r\n"
            response = response_head.encode() + response_content
            f.close()
        finally:
            conndf.send(response)


if __name__ == '__main__':
    host = "192.168.0.171"
    port = 8841
    dir = "../static"

    wb = HTTPServer(host=host, port=port, path=dir)
    wb.start()

