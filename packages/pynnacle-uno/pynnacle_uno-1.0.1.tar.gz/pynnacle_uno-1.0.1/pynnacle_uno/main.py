'''
    The Pynnacle-Uno provides an Arduino-like programming experience in Python for beginners (see full description below).

    Copyright (C) 2024 Rafael Red Angelo M. Hizon, Jenel M. Justo, and Serena Mae C.S. Lee

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This module was built on top of Pymata4 by Alan Yorinks - <https://github.com/MrYsLab/pymata4/>
'''


'''
    The pynnacle-uno module was originally created for the readers of the book 'Bot Adventures: Discovering the Mysteries of Robotics' authored by
    Team Pinnacle. This simple module was built on top of Pymata4, and it was designed to provide beginners with robotics coding experience in
    Python that's relatively close to the Arduino's programming language. This is to hopefully provide them with easier transition once they
    start learning Arduino's programming language which is relatively more challenging to learn than Python. Lastly, this was mainly created
    for Arduino UNO. Although this might work for some boards to some extent, it is highly recommended that you use Arduino UNO for this module.

    DISCLAIMER:
        Some functions were changed by the book authors to cause a slightly different effect from the original Arduino's programming language.
        This was done to align with the mission of the book to teach and expose absolute beginners in the field of robotics in a simple way.

    TEAM PINNACLE:
        1. Red Hizon
        2. Jenel Justo
        3. Serena Lee
'''

# Import statements
from pymata4 import pymata4
from time import sleep
import re

# CONSTANTS

# States
HIGH = 1
LOW = 0

# Modes
OUTPUT = 'O'
INPUT = 'I'
INPUT_PULLUP = 'IP'

# Maximum number of digital pins on the Arduino UNO
DIGITAL_PINS_COUNT = 14

# Analog Pins on Arduino UNO. Add more if you want to 
A0 = 'A0'
A1 = 'A1'
A2 = 'A2'
A3 = 'A3'
A4 = 'A4'
A5 = 'A5'

# Notes and their corresponding frequencies
# reference: <https://docs.arduino.cc/built-in-examples/digital/toneMelody/>
NOTE_B0 = 31
NOTE_C1 = 33
NOTE_CS1 = 35
NOTE_D1 = 37
NOTE_DS1 = 39
NOTE_E1 = 41
NOTE_F1 = 44
NOTE_FS1 = 46
NOTE_G1 = 49
NOTE_GS1 = 52
NOTE_A1 = 55
NOTE_AS1 = 58
NOTE_B1 = 62
NOTE_C2 = 65
NOTE_CS2 = 69
NOTE_D2 = 73
NOTE_DS2 = 78
NOTE_E2 = 82
NOTE_F2 = 87
NOTE_FS2 = 93
NOTE_G2 = 98
NOTE_GS2 = 104
NOTE_A2 = 110
NOTE_AS2 = 117
NOTE_B2 = 123
NOTE_C3 = 131
NOTE_CS3 = 139
NOTE_D3 = 147
NOTE_DS3 = 156
NOTE_E3 = 165
NOTE_F3 = 175
NOTE_FS3 = 185
NOTE_G3 = 196
NOTE_GS3 = 208
NOTE_A3 = 220
NOTE_AS3 = 233
NOTE_B3 = 247
NOTE_C4 = 262
NOTE_CS4 = 277
NOTE_D4 = 294
NOTE_DS4 = 311
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_FS4 = 370
NOTE_G4 = 392
NOTE_GS4 = 415
NOTE_A4 = 440
NOTE_AS4 = 466
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_CS5 = 554
NOTE_D5 = 587
NOTE_DS5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_FS5 = 740
NOTE_G5 = 784
NOTE_GS5 = 831
NOTE_A5 = 880
NOTE_AS5 = 932
NOTE_B5 = 988
NOTE_C6 = 1047
NOTE_CS6 = 1109
NOTE_D6 = 1175
NOTE_DS6 = 1245
NOTE_E6 = 1319
NOTE_F6 = 1397
NOTE_FS6 = 1480
NOTE_G6 = 1568
NOTE_GS6 = 1661
NOTE_A6 = 1760
NOTE_AS6 = 1865
NOTE_B6 = 1976
NOTE_C7 = 2093
NOTE_CS7 = 2217
NOTE_D7 = 2349
NOTE_DS7 = 2489
NOTE_E7 = 2637
NOTE_F7 = 2794
NOTE_FS7 = 2960
NOTE_G7 = 3136
NOTE_GS7 = 3322
NOTE_A7 = 3520
NOTE_AS7 = 3729
NOTE_B7 = 3951
NOTE_C8 = 4186
NOTE_CS8 = 4435
NOTE_D8 = 4699
NOTE_DS8 = 4978

_board = None

# Text styles for the info function
class _Style:
    __BOLD = '\033[1m'
    __ITALIC = '\033[3m'
    __UNDERLINE = '\033[4m'
    __COLOR_BLUE = '\033[94m'
    __COLOR_RED = '\033[91m'
    __RESET = '\033[0m'  # Reset to default

    @staticmethod
    def info():
        print("\n")
        formatted_text = (
            f"\n{_Style.__COLOR_BLUE}{_Style.__BOLD}THE PYNNACLE-UNO{_Style.__RESET}\n\n"
            f"This module is tailored for beginners in robotics and programming,\n"
            f'originally for readers of "{_Style.__COLOR_BLUE}{_Style.__ITALIC}Bot Adventures: Discovering the Mysteries of Robotics{_Style.__RESET}" by {_Style.__BOLD}{_Style.__COLOR_BLUE}Team Pinnacle{_Style.__RESET}.\n'
            f"Based on {_Style.__ITALIC}Pymata4{_Style.__RESET}, it offers a Python-based robotics coding experience resembling Arduino's language.\n"
            f"Its main goal is easing the transition for learners, bridging the gap between Python's simplicity\n"
            f"and Arduino's complexity, known for its steep learning curve.\n\n"
            f"{_Style.__ITALIC}This work requires attribution if you modify and distribute it and its derivatives.\nYou can find the attribution requirement towards the end of the license document.{_Style.__RESET}\n\n"
            f"{_Style.__COLOR_BLUE}{_Style.__BOLD}Copyright (c) 2024 {_Style.__RESET}{_Style.__COLOR_BLUE}{_Style.__UNDERLINE}Rafael Red Angelo M. Hizon{_Style.__RESET}, {_Style.__COLOR_BLUE}{_Style.__UNDERLINE}Jenel M. Justo{_Style.__RESET}, {_Style.__COLOR_BLUE}{_Style.__UNDERLINE}Serena Mae C.S. Lee\n{_Style.__RESET}"
        )
        print(formatted_text)

    @staticmethod
    def print_error_message():
        error_prompt = f"\n{_Style.__BOLD}{_Style.__COLOR_RED}Error:{_Style.__RESET} There was an issue with instantiating the board."
        possible_causes = [
            "1. Check the board connection.",
            "2. Ensure the board is properly powered.",
            "3. Verify that the board is compatible with your system.",
            "4. Check for any hardware failures or conflicts."
        ]
        print(error_prompt)
        print("\nPossible Causes:")
        for cause in possible_causes:
            print(f"  {cause}")

# Board instantiation
try:
    _board = pymata4.Pymata4()
    _Style.info()
except:
    _Style.info()
    _Style.print_error_message()




# In Arduino's pinMode function, there are only 3 modes:
#   1. INPUT
#   2. OUTPUT
#   3. INPUT_PULLUP
# See more at: https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/
def pinMode(pin, mode):
    # Check if pin is an integer only. If so, it must be a digital pin.
    if re.match(r'^\d+$', str(pin)):
        if mode == INPUT:
            _board.set_pin_mode_digital_input(pin)
        elif mode == OUTPUT:
            _board.set_pin_mode_digital_output(pin)
        elif mode == INPUT_PULLUP:
            _board.set_pin_mode_digital_input_pullup(pin)
        else:
            raise Exception('Not a valid pin mode.')

    # Else if pin starts with an 'A', then it must be an analog pin.
    # Analog pins are usually used for analog inputs, but they can also be used as digital pins for input and output devices.
    # See more at:
    # 1. <https://docs.arduino.cc/learn/microcontrollers/analog-input/>
    # 2. <https://mryslab.github.io/pymata4/pin_modes/#set_pin_mode_analog_input>
    elif pin.startswith('A'):
        integer_only = int(pin[1:])
        if mode == INPUT:
            _board.set_pin_mode_analog_input(integer_only)

        else:
            digital_pin_equivalent = DIGITAL_PINS_COUNT + integer_only
            if mode == OUTPUT:
                _board.set_pin_mode_digital_output(digital_pin_equivalent)

            elif mode == INPUT_PULLUP:
                _board.set_pin_mode_digital_input_pullup(digital_pin_equivalent)

            else:
                raise Exception('Not a valid pin mode.')
    else:
        raise Exception('Wrong parameter in pinMode.')


# This simulates the Arduino's delay function.
# In Arduino, the said function takes a delay time in milliseconds.
# It is implemented here using the sleep method.
def delay(ms):
    sleep(ms / 1000)  # The sleep method takes a delay time in seconds so we divide by 1000.


# This function accepts a pin as a parameter.
# This function converts the analog pin to its digital pin equivalent.
# It returns the calculated digital pin equivalent.
def analogToDigital(pin):
    integer_only = int(pin[1:])
    pin = DIGITAL_PINS_COUNT + integer_only
    return pin


# This function sets (writes) a digital pin's state into HIGH or LOW.
# This function takes in 2 parameters:
#   1. pin
#   2. state (HIGH or LOW)
def digitalWrite(pin, state):
    if isinstance(pin, str) and pin.startswith('A'):
        pin = analogToDigital(pin)  # convert analog pin to digital pin equivalent
    _board.digital_write(pin, state)


# This function allows users to write PWM wave (analog value) to a pin.
# This function takes in 2 parameters:
#   1. pin
#   2. val (ranges from 0-255)
# In Arduino, the analogWrite function does not require the programmer to
# invoke pinMode in order to set the pin as OUTPUT. We simulate this effect
# using the set_pin_mode_pwm_output method before calling pwm_write.
# See more at: <https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/>
def analogWrite(pin, val):
    if isinstance(pin, str) and pin.startswith('A'):
        pin = analogToDigital(pin)  # convert analog pin to digital pin equivalent
    _board.set_pin_mode_pwm_output(pin)  # set the pin's mode as a pwm output pin
    _board.pwm_write(pin, val)  # write an output value


# This function accepts a pin as a parameter.
# This function allows to read a digital pin's state whether HIGH or LOW.
# It returns a list with two values:
#   1. last value change
#   2. time_stamp
# See more at: <https://mryslab.github.io/pymata4/pin_changes/#digital_read>
def digitalRead(pin):
    if isinstance(pin, str) and pin.startswith('A'):
        pin = analogToDigital(pin)  # convert analog pin to digital pin equivalent
        _board.set_pin_mode_digital_input(pin)  # set the pin's mode as a digital input pin
    val = _board.digital_read(pin)  # read the digital value
    return val


# This function accepts a pin as a parameter.
# This function allows to read the value from an analog pin.
# It returns a list with two values:
#   1. last value change
#   2. time_stamp
# See more at: <https://mryslab.github.io/pymata4/pin_changes/#analog_read>
def analogRead(pin):
    if isinstance(pin, str) and pin.startswith('A'):
        pin = int(pin[1:])
    val = _board.analog_read(pin)  # read the analog value
    return val


# That pin will then be set for ultrasonic operations.
# This accepts 2 parameters:
#   1. trigger_pin
#   2. echo_pin
# See more at: <https://mryslab.github.io/pymata4/pin_modes/#set_pin_mode_sonar>
# This function is not part of the original programming language of Arduino.
# It is added here for educational purposes in line with the authors' book.
def ultrasonicAttach(trigger_pin, echo_pin):
    _board.set_pin_mode_sonar(trigger_pin, echo_pin)


# This function accepts a trigger_pin as a parameter.
# This function retrieves ping data from the ultrasonic (HC-SR04 type).
# This returns a list with 2 values:
#   1. last value
#   2. raw time_stamp
# See more at: <https://mryslab.github.io/pymata4/pin_changes/#sonar_read>
# This function is not part of the original programming language of Arduino.
# It is added here for educational purposes in line with the authors' book.
def ultrasonicRead(trigger_pin):
    val = _board.sonar_read(trigger_pin)
    return val


# That pin will then be set for servo operations.
# This accepts 3 parameters:
#   1. pin of the servo
#   2. min pulse width in ms. (if no value was passed, value is 544)
#   3. max pulse width in ms. (if no value was passed, value is 2400)
# See more at:
#   1. <https://www.arduino.cc/reference/en/libraries/servo/attach/>
#   2. <https://mryslab.github.io/pymata4/pin_modes/#set_pin_mode_servo>
def servoAttach(pin, min_pulse=544, max_pulse=2400):
    _board.set_pin_mode_servo(pin)


# This function controls the shaft of the servo according to the position parameter.
# This accepts 2 parameters:
#   1. pin of the buzzer
#   2. frequency
# See more at:
#   1. <https://www.arduino.cc/reference/en/libraries/servo/write/>
#   2. <https://mryslab.github.io/pymata4/device_writes/#servo_write>
def servoWrite(pin, position):
    _board.servo_write(pin, position)


# This function accepts a pin as a parameter.
# That pin will then be set for tone operations.
# See more at: <https://mryslab.github.io/pymata4/pin_modes/#set_pin_mode_tone>
# This function is not part of the original programming language of Arduino.
# It is added here for educational purposes in line with the authors' book.
def buzzerAttach(pin):
    _board.set_pin_mode_tone(pin)


# This function plays a sound based on the frequency passed as a parameter.
# This accepts 3 parameters:
#   1. pin of the buzzer
#   2. frequency
#   3. duration (if no value was passed, tone will be played continuously)
# See more at:
#   1. <https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/>
#   2. <https://mryslab.github.io/pymata4/device_writes/#play_tone>
def tone(pin, frequency, duration=None):
    if duration is None:
        _board.play_tone_continuously(pin, frequency)
    else:
        _board.play_tone(pin, frequency, int(duration))


# This function accepts a pin as a parameter.
# This function turns off the tone being played on the pin that was passed as a parameter.
def noTone(pin):
    _board.play_tone_off(pin)
