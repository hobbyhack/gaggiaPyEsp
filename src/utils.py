import socket

import machine


def print_file(filename):
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        print(line)


def stream_socket(
    host: str = "towel.blinkenlights.nl", port: int = 23, format: str = "utf8"
):
    addr_info = socket.getaddrinfo(host, port)
    addr = addr_info[0][-1]
    s = socket.socket()
    s.connect(addr)

    while True:
        data = s.recv(500)
        print(str(data, format), end="")


def http_get(url: str = "http://micropython.org/ks/test.html", format: str = "utf8"):
    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), format))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, format), end="")
        else:
            break
    s.close()


def pin_http_server():
    pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

    html = """<!DOCTYPE html>
    <html>
        <head> <title>Pins</title> </head>
        <body> <h1>Pins</h1>
            <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
        </body>
    </html>
    """

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("listening on", addr)

    while True:
        cl, addr = s.accept()
        print("client connected from", addr)
        cl_file = cl.makefile("rwb", 0)
        while True:
            line = cl_file.readline()
            if not line or line == b"\r\n":
                break
        rows = ["<tr><td>%s</td><td>%d</td></tr>" % (str(p), p.value()) for p in pins]
        response = html % "\n".join(rows)
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()


def scale_mode(scale, oled):
    tare = scale.read_average(10)
    while True:
        weight = round(((scale.read_average(10) - tare) / 427.77925))
        oled.fill(0)
        oled.show()
        oled.text(str(weight), 0, 0)
        oled.show()


def scale_temp(scale, temp, oled):
    time.sleep(1)
    tare = scale.read_average(20)
    oled.flip()
    while True:
        temperature = temp.temperature
        weight = round(((scale.read_average(10) - tare) / 427.77925))
        oled.fill(0)
        oled.show()
        oled.text(str(weight), 0, 0)
        oled.text(str(temperature), 0, 10)
        oled.show()
