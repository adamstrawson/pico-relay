import time
from machine import Pin
import socket
import network
import schedule

led = Pin("LED", Pin.OUT)
led.on()

ssid = "CHRISTMAS_AP"
password = "santa123"

relay = Pin(6, Pin.OUT)

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while not ap.active():
    pass

print(ap.ifconfig())

def html(relay_status):
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Christmas Tree</h1>
            <p>Lights are currently: {relay_status}</p>
            <form action="/toggle" method="get">
                <button type="submit" name="toggle" value="on">Turn On</button>
                <button type="submit" name="toggle" value="off">Turn Off</button>
            </form>
        </body>
    </html>
    """

def web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        toggle_on = "toggle=on" in request
        toggle_off = "toggle=off" in request
        print(request)
        if toggle_on:
            light_toggle("on")
        elif toggle_off:
            light_toggle("off")

        relay_status = "On" if relay.value() else "Off"
        response = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + html(relay_status)
        conn.send(response)
        conn.close()

def light_toggle(power):
    print(f"Turning lights {power}...")
    if power == "on":
        relay.value(1)
    elif power == "off":
        relay.value(0)
    else:
        print("Unknown toggle option")

schedule.every().day.at("16:00").do(light_toggle, power="on")
schedule.every().day.at("22:00").do(light_toggle, power="off")

web_server()
