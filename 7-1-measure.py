import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

dac    = [26, 19, 13,  6, 5, 11,  9, 10]
leds   = [21, 20, 16, 12, 7,  8, 25, 24]
comp   = 4
troyka = 17

MAX_VOLTAGE    = 3.3
HIGHER_VOLTAGE = MAX_VOLTAGE * 0.9
LOWER_VOLTAGE  = MAX_VOLTAGE * 0.1
BITS           = 8
LEVELS         = 2 ** BITS

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)


def d2b(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc_sar():
    value = 0

    for i in range(7, -1, -1):
        step   = 2 ** i
        value += step

        GPIO.output(dac, d2b(value))
        time.sleep(0.0005)
        
        if GPIO.input(comp) == GPIO.LOW:
            value -= step

    return value


def get_troyka_voltage(digit):
    return digit / LEVELS * MAX_VOLTAGE

def set_troyka_power(value):
    GPIO.output(troyka, value)
        
def light_leds(digit):
    GPIO.output(leds, d2b(digit))

def transform(digit):
    return (1 << round(digit * BITS / LEVELS)) - 1


try:
    voltages = []
    exp_start = time.time()
    troyka_voltage = 0
    digit = 0

    set_troyka_power(1)

    while troyka_voltage < HIGHER_VOLTAGE:
        digit = adc_sar()
        print("Voltage: {:.2f}V, digit: ".format(digit * MAX_VOLTAGE / LEVELS), digit)
        light_leds(digit)
        troyka_voltage = get_troyka_voltage(digit)
        voltages.append(troyka_voltage)

    charge_duration = time.clock() - exp_start

    set_troyka_power(0)

    while troyka_voltage > LOWER_VOLTAGE:
        digit = adc_sar()
        print("Voltage: {:.2f}V, digit: ".format(digit * MAX_VOLTAGE / LEVELS), digit)
        light_leds(digit)
        troyka_voltage = get_troyka_voltage(digit)
        voltages.append(troyka_voltage)

    exp_duration = time.time() - exp_start


    plt.plot(voltages)
    plt.show()

    voltages_str = [str(item) for item in voltages]

    with open("data.txt", "w") as file:
        file.write("\n".join(voltages_str))

    with open("settings.txt", "w") as file:
        file.write("discret: {} s\nquant: {:.5f} V\n".format(exp_duration / len(voltages), 3.3 / 256))
        file.write("experiment time: {:.3f} s\n".format(exp_duration))


finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()