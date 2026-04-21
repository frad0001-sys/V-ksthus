from flask import Flask, render_template       # Flask (web framework)
from flask_socketio import SocketIO, emit      # SocketIO (real-time kommunikation)
import threading                               # Bruges til at køre loops parallelt
from time import sleep                         # Pause i loops
import os                                      # Bruges til kamera kommando

# -----------------------
# IMPORT FRA EGNE FILER
# -----------------------

from database import init_db, insert_soil, insert_light  
# -> database.py (opretter DB + gemmer data)

from soil import SoilSensor     
# -> soil.py (læser jordfugtighed)

from ldr import LDRSensor       
# -> ldr.py (måler lys + beregner red/blue PWM)

from pumpe import WaterPump     
# -> pumpe.py (styrer vandpumpe)

from led import LEDController   
# -> led.py (styrer LED via PWM)

# -----------------------
# FLASK SETUP
# -----------------------

app = Flask(__name__)           
# -> opretter webserver

socketio = SocketIO(app, async_mode="threading")  
# -> gør det muligt at sende live data til frontend

# -----------------------
# DATABASE INIT
# -----------------------

init_db()  
# -> kalder database.py og opretter tabeller hvis de ikke findes

# -----------------------
# SENSORER + AKTUATORER
# -----------------------

soil = SoilSensor()  
# -> objekt fra soil.py

ldr = LDRSensor()    
# -> objekt fra ldr.py

pump = WaterPump()   
# -> objekt fra pumpe.py

led = LEDController()  
# -> objekt fra led.py

# -----------------------
# CACHE (GLOBALE VARIABLER)
# -----------------------

soil_value = 0  
# -> gemmer seneste jordværdi

light_value = {
    "adc": 0,
    "red": 0,
    "blue": 0,
    "stage": "starter"
}
# -> gemmer seneste lysdata fra ldr.py

# -----------------------
# SOIL LOOP (THREAD 1)
# -----------------------

def soil_loop():
    global soil_value

    while True:
        soil_value = soil.get_moisture()  
        # -> kalder soil.py

        insert_soil(soil_value)  
        # -> gemmer i database.py

        # automatisk vanding
        if soil_value < 10:
            pump.water(3)  
            # -> kalder pumpe.py (tænder pumpe i 3 sek)

        sleep(2)

# -----------------------
# LIGHT LOOP (THREAD 2)
# -----------------------

def light_loop():
    global light_value

    while True:
        light_value = ldr.get_light()  
        # -> kalder ldr.py
        # -> returnerer adc + red + blue + stage

        # HER kobles LDR til LED
        led.set_pwm(
            light_value["red"],
            light_value["blue"]
        )
        # -> sender værdier til led.py
        # -> styrer fysisk LED

        insert_light(
            light_value["adc"],
            light_value["stage"]
        )
        # -> gemmer lysdata i database.py

        sleep(2)

# -----------------------
# KAMERA
# -----------------------

def take_picture():
    path = "static/images/latest.jpg"

    os.system(f"libcamera-still -o {path} -t 1 --nopreview")
    # -> kører Raspberry Pi kamera kommando

# -----------------------
# START THREADS
# -----------------------

threading.Thread(target=soil_loop, daemon=True).start()
# -> starter soil_loop i baggrunden

threading.Thread(target=light_loop, daemon=True).start()
# -> starter light_loop i baggrunden

# -----------------------
# SOCKET EVENTS (frontend ↔ backend)
# -----------------------

@socketio.on('connect')
def connect():
    emit('soil', {"value": soil_value})
    emit('light', light_value)
    # -> sender startdata til web UI

@socketio.on('get_soil')
def get_soil():
    emit('soil', {"value": soil_value})
    # -> sender soil data til frontend

@socketio.on('get_light')
def get_light():
    emit('light', light_value)
    # -> sender lys data til frontend

@socketio.on('water')
def water(data):
    seconds = int(data.get('seconds', 3))

    pump.water(seconds)  
    # -> kalder pumpe.py

    emit('pump_status', "Vander")

    sleep(seconds)

    emit('pump_status', "Slukket")

# -----------------------
# ROUTES (websider)
# -----------------------

@app.route("/")
def home():
    return render_template("home.html")  
    # -> templates/home.html

@app.route("/soil")
def soil_page():
    return render_template("soil.html")  
    # -> templates/soil.html

@app.route("/light")
def light_page():
    return render_template("light.html")  
    # -> templates/light.html

@app.route("/pump")
def pump_page():
    return render_template("pump.html")

@app.route("/camera")
def camera():
    take_picture()
    return render_template("camera.html")

# -----------------------
# START SERVER
# -----------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
    # -> starter webserver
