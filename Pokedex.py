from microbit import *
import radio
import random
import music

#------------------LCD FUNCTIONS----------------------------------

# pin connections
rs = pin0
enable = pin1
datapins = [pin8, pin12, pin2, pin13]

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00


def InitDisplay():
    # at least 50ms after power on
    sleep(50)
    # send rs, enable low - rw is tied to GND
    rs.write_digital(0)
    enable.write_digital(0)
    write4bits(0x03)
    sleep(5)
    write4bits(0x03)
    sleep(5)
    write4bits(0x03)
    sleep(2)
    write4bits(0x02)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(5)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(2)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(2)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(2)
    send(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF,0)
    clear()
    send(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT,0)
     
# high level commands    
def clear():
    send(LCD_CLEARDISPLAY,0)
    sleep(2)

def home():
    send(LCD_RETURNHOME,0)
    sleep(2)

def setCursor(col, row):
    orpart = col
    if row>0:
        orpart = orpart + 0x40
    send(LCD_SETDDRAMADDR | orpart, 0)

def showText(t):
    for c in t:
        send(ord(c), 1)

# mid and low level commands        
def send(value, mode):
    rs.write_digital(mode)
    write4bits(value>>4)
    write4bits(value)
    
def pulseEnable():
    enable.write_digital(0)
    sleep(1)
    enable.write_digital(1)
    sleep(1)
    enable.write_digital(0)
    sleep(1)

def write4bits(value):
    for i in range(0,4):
        datapins[i].write_digital((value>>i) & 0x01)
    pulseEnable()

#----------------END OF LCD FUNCTIONS------------------------------------------------------------------    
    
InitDisplay()
radio.on()
radio.config(channel=16)
radio.config(queue=2)
start_up = 0

#Start Screen
while True:
    msg = radio.receive()
    if msg == 'msg':
        clear()
        break
    elif msg:
        while start_up == 0:
            showText(msg)
            setCursor(0, 1)
            showText("to Start")
            start_up += 1
        while start_up == 1:
            msg = radio.receive()
            if msg:
                clear()
                showText("Loading...")
                start_up += 1

clear()
while True:
    #Finding Pokemon Section
    while start_up == 2:
        sleep(2000)
        msg = radio.receive()
        pkm = msg
        if msg:
            clear()
            showText("A wild ")
            showText(msg)
            setCursor(0, 1)
            showText("has appeared!")
            sleep(4000)
            start_up = 3
        else:
            clear()
            showText('Finding')
            setCursor(0,1)
            showText('Pokemon...')
            sleep(500)
            continue

    #Pokemon level and "Shake to Catch"
    while start_up == 3:
        radio.send(msg)
        clear()
        display.clear()
        lvl = str(random.randrange(2, 8))
        showText(msg + ':' + lvl)
        pkdx = msg + ':' + lvl
        setCursor(0, 1)
        showText('Shake to catch')
        radio.send(msg)
        start_up = 4
    
    #Pokemon Caught Status and Pokedex Update
    while start_up == 4:
        catch_succesful = radio.receive()
        if catch_succesful == msg:
            clear()
            showText(msg)
            setCursor(0, 1)
            showText('has been caught!')
            sleep(2000)
            radio.send(pkdx)
            catch_succesful = ""
            start_up += 1
            while start_up == 5:
                update = radio.receive()
                if update == 'updated':
                    clear()
                    showText('Your Pokedex has')
                    setCursor(0, 1)
                    showText('been updated')
                    msg = None
                    start_up = 2
                    continue
        if catch_succesful == 'fled':
            clear()
            showText(msg)
            setCursor(0, 1)
            showText('has fled!')
            sleep(1500)
            start_up = 2 
            continue