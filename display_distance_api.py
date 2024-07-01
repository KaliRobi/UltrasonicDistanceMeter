from flask import Flask, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    
    #if the signal is too weak this just loops to the infinte and beyond

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime

    '''
    multiply with the speed of sound (34300 cm/s) 
    and divide by 2, ( there and back)

    could be more accurate with temperature and humidity meter to define
    that should be  
    x = 331.3 * sqrt(1 + (T/273.15)) * sqrt(RH/100)
    T =temperature in celsius (sensor)
    RH =  relative humidity in %

    Sensor will be:  DHT11 - Okystar
    '''

    distance = (TimeElapsed * 34300) / 2

    return distance

@app.route('/distance', methods=['GET'])
def get_distance():
    dist = distance()
    return jsonify({'distance': dist})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Measurement stopped")
        GPIO.cleanup()
