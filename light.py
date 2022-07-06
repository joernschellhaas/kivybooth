import emulation
import time
import atexit
if not emulation.active():  
    import wiringpi


def set_brightness(value):
    if not emulation.active(): 
        wiringpi.pwmWrite(LIGHT_PIN, int(1024 * value))


if not emulation.active():  
    LIGHT_PIN = 1
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(LIGHT_PIN, wiringpi.PWM_OUTPUT)
    atexit.register(set_brightness, 0)


if __name__ == '__main__':
    # Test lights
    #for i in [*range(1024), *range(1024, 0, -1)]:
    #    wiringpi.pwmWrite(LIGHT_PIN, i)
    #    time.sleep(0.002)
    set_brightness(1)
    time.sleep(0.5)
    set_brightness(0)
