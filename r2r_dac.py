import RPi.GPIO as GPIO
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        max_number = 2 ** len(self.gpio_bits) - 1

        if not isinstance(number, int):
            print("Число на выход ЦАП должно быть целым")
            return

        if number < 0 or number > max_number:
            print(f"Число выходит за диапазон ЦАП (0 - {max_number})")
            return 
        
        bits = [int(bit) for bit in bin(number)[2:].zfill(len(self.gpio_bits))]
        GPIO.output(self.gpio_bits, bits)

        if self.verbose:
            print(f"Число на вход ЦАП: {number}, биты {bits}")

    def set_voltage(self, voltage):
        max_number = 2 ** len(self.gpio_bits) - 1

        if voltage < 0 or voltage > self.dynamic_range:
            print(f"НАпряжение выходит за динамический диапазон ЦАП "
                f"(0.00 - {self.dynamic_range:.2f} B)"
                )
            return
        
        number = int(voltage / self.dynamic_range * max_number)
        self.set_number(number)

if __name__ == "__main__":
    dac = None
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)

        while True:
            try:
                voltage = float(input("Ввудите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")


    finally:
        if dac is not None:
            dac.deinit()