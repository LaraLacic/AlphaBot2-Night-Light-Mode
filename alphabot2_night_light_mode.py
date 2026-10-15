       
import RPi.GPIO as GPIO
import time


ADC_CS   = 5
ADC_ADDR = 24
ADC_DATA = 23
ADC_CLK  = 25


def setup_all():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(ADC_CS, GPIO.OUT)
    GPIO.setup(ADC_ADDR, GPIO.OUT)
    GPIO.setup(ADC_CLK, GPIO.OUT)
    GPIO.setup(ADC_DATA, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    
    GPIO.output(ADC_CS, GPIO.HIGH)

def read_adc(channel):
    _ = _perform_bit_bang(channel)
    return _perform_bit_bang(channel)

def _perform_bit_bang(channel):
    value = 0
    GPIO.output(ADC_CS, GPIO.LOW)
    for i in range(10):
        if i < 4:
            bit = (channel >> (3 - i)) & 0x01
            GPIO.output(ADC_ADDR, bit)
        
        GPIO.output(ADC_CLK, GPIO.HIGH)
        value <<= 1
        if GPIO.input(ADC_DATA):
            value |= 0x01
        GPIO.output(ADC_CLK, GPIO.LOW)
        
    GPIO.output(ADC_CS, GPIO.HIGH)
    time.sleep(0.0001) 
    return value

def get_sensors_average():
    totals = 0
    for channel in range(5):
        totals += read_adc(channel)
    return totals / 5

def calibrate_garage():
    print("\n--- STARTING CALIBRATION ---")
    
    # 1. Light Space Baseline
    print("1. Place the robot in the LIGHT space.")
    print("Capturing light levels in 5 seconds...")
    time.sleep(5)
    light_total = 0
    for _ in range(20):
        light_total += get_sensors_average()
        time.sleep(0.05)
    light_baseline = light_total / 20
    print(f"Caught LIGHT Baseline: {light_baseline:.2f}")
    print("-" * 35)

    # 2. Dark Space Baseline
    print("2. Move the robot completely into the DARK space (Garage).")
    print("Capturing dark levels in 5 seconds...")
    time.sleep(5)
    dark_total = 0
    for _ in range(20):
        dark_total += get_sensors_average()
        time.sleep(0.05)
    dark_baseline = dark_total / 20
    print(f"Caught DARK Baseline: {dark_baseline:.2f}")
    print("-" * 35)

    # 3. Midpoint Calculation
    calculated_threshold = (light_baseline + dark_baseline) / 2
    print(f"CALIBRATION COMPLETE. Midpoint Threshold: {calculated_threshold:.2f}")
    return calculated_threshold

def run_garage_light(calculated_threshold):
    print("\n--- LIVE MONITORING ONLINE (Ctrl+C to Stop) ---")
   
    try:
        while True:
            current_vals = [read_adc(channel) for channel in range(5)]
            
            is_dark = any(val > calculated_threshold for val in current_vals)
            
            if is_dark:
                print(1) # Lights should be ON
            else:
                print(0) # Lights should be OFF
            
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nShutting down safely...")
        GPIO.cleanup()

if __name__ == "__main__":
    setup_all()
    threshold = calibrate_garage()
    run_garage_light(threshold)