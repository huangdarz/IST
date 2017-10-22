from microbit import *
import random
import radio

radio.on()
radio.config(channel=16)
radio.config(queue=2)

#List of pokemon
pokemon = ["Pikachu", "Squirtle", "Eevee", "Bulbasaur", "Pidgey", "Dragonite", "Charizard", "Unown", "Mewtwo", "Kylo Ren"]
pokedex = {}

#Loading Images
POKEBALL = Image('09990:90009:99399:90009:09990:')
INVERTED = POKEBALL.invert()

start_up = 0
start_time = 800
fled = 0


#Function for Pokemon appearances
def pkm_appearance(a_chance1, a_chance2, a_chance3, a_chance4, pkm_start1, pkm_end1, pkm_start2, pkm_end2):
    global start_up
    global msg
    appearance_chance = random.randrange(21) 
    if appearance_chance >= a_chance1 and appearance_chance <= a_chance2:
        pokemon_name = int (random.randrange(pkm_start1, pkm_end1))
        radio.send(pokemon[pokemon_name]) 
        start_up = 3
    elif appearance_chance >= a_chance3 and appearance_chance <= a_chance4 :
        pokemon_name = random.randrange(pkm_start2, pkm_end2)
        radio.send(pokemon[pokemon_name])
        start_up = 3
    else:
        wait_time = random.randrange(3000)
        sleep(wait_time)

#Function for Pokemon Catch Rate
def catch_rate(message, rate_start, rate_end):
    global start_up
    global fled
    catch_chance = random.randrange(101)
    if catch_chance >= rate_start and catch_chance <= rate_end:
        radio.send(message)
        fled = 1
    else:
        fled = 2
        sleep(2000)

#Function for adding to Dictionary Pokedex        
def dict_add(pkm, lvl):
    pokedex[pkm] = lvl

#Function to add Pokemon to Pokedex
def pokedex_update():
    global start_up
    while start_up == 4:
        pokemon_caught = radio.receive()
        parts = pokemon_caught.split(':')
        pkm = parts[0]
        lvl = parts[-1]
        if pokemon_caught:
            dict_add(pkm, lvl)
            radio.send('updated')
            sleep(200)
            start_up = 2

#Function for Shake action to catch            
def catch_action(message, rate1, rate2):
    global start_up
    global fled
    global msg
    while start_up == 3: 
        if accelerometer.was_gesture('shake'):
            catch_rate(message, rate1, rate2)
            if fled == 1:
                radio.send(msg)
                start_up = 4
                fled = 0
            if fled == 2:
                start_up  = 2
                fled = 0
            msg = None
#-----------------START OF PROGRAM---------------------------------
        
while True:
    #Start Screen
    while start_up == 0:
        if button_a.was_pressed():
            radio.send("Press A Button")
            start_up = 1

    #Loading Screen
    while start_up == 1:
        display.clear()
        if button_a.was_pressed():
            radio.send("clear")
            while start_time > 0:
                display.show(POKEBALL)
                sleep(start_time)
                display.show(INVERTED)
                sleep(start_time)
                start_time -= 50
        if start_time == 0:
            start_up = 2
            display.clear()
            radio.send("msg")
    
    #Compass Calibration
    if compass.is_calibrated:
        cmps = compass.heading()
    else:
        compass.calibrate()
        cmps = compass.heading()

    #Pokemon Zones
    while start_up == 2:
        display.scroll('2')
        sleep(3000)
        cmps = compass.heading()
        if cmps > 0 and cmps <= 90:
            pkm_appearance(0, 10, 18, 20, 0, 3, 7, 9)
            continue
        if cmps > 90 and cmps <= 180:
            pkm_appearance(0, 10, 15, 19, 0, 2, 5, 8)
            continue
        if cmps > 180 and cmps <= 270:
            pkm_appearance(0, 5, 10, 18, 0, 3, 3, 6)
            continue
        if cmps > 270 and cmps <= 0:
            pkm_appearance(0, 15, 18, 20, 0, 5, 9, 10)
            continue
    
    #Pokemon Catch Rate
    while start_up == 3:
        display.scroll('3')
        msg = radio.receive()
        if msg:
            if msg == pokemon[0]:
                catch_action(msg, 20, 100)
                msg = None
                continue
            elif msg == pokemon[1]:
                catch_action(msg, 20, 100)
                msg = None
                continue
            elif msg == pokemon[2]:
                catch_action(msg, 20, 100)
                msg = None
                continue
            elif msg == pokemon[3]:
                catch_action(msg, 20, 100)
                msg = None
                continue
            elif msg == pokemon[4]:
                catch_action(msg, 25, 100)
                msg = None
                continue
            elif msg == pokemon[5]:
                catch_action(msg, 50, 100)
                msg = None
                continue
            elif msg == pokemon[6]:
                catch_action(msg, 50, 100)
                msg = None
                continue
            elif msg == pokemon[7]:
                catch_action(msg, 75, 100)
                msg = None
                continue
            elif msg == pokemon[8]:
                catch_action(msg, 75, 100)
                msg = None
                continue
            elif msg == pokemon[9]:
                catch_action(msg, 85, 100)
                msg = None
                continue

    #Pokedex Entry
    while start_up == 4:
        msg = ""
        display.scroll('4')
        sleep(2000)
        pokedex_update()
        sleep(400)
        start_up = 2




    
        
        
    