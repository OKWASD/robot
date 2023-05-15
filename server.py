#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from datetime import datetime

robot = EV3Brick()
grip = Motor(Port.A)
arm = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
base = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
base_touch = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
ZONES = []
LOGLEVEL = 2

def log(message, level, clearFirst=False):
    if level <= LOGLEVEL:
        if clearFirst:
            robot.screen.clear()
        
        print(message)
        robot.screen.print(message)


def move(location, angle, armFirst = False):
    if armFirst:
        arm.run_target(60, angle)
        base.run_target(60, location)
    else:
        base.run_target(60, location)
        arm.run_target(60, angle)

def calibrate():
    log("Calibrating...", 0, True)

    grip.run_target(200, -90)
    grip.hold()
    log("Grip is done closing", 2)

    arm.run_until_stalled(-30, Stop.COAST, 50)
    arm.run(15)
    while 0 < color_sensor.reflection() < 50:
        wait(15)
    arm.run_time(-20, 300)
    arm.reset_angle(0)
    arm.hold()
    log("Arm is done calibrating after color sensor", 2)

    base.run(-60)
    while not base_touch.pressed():
        wait(15)
    base.reset_angle(0)
    base.hold()
    log("Base is done calibrating", 2)

    grip.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    grip.reset_angle(0)
    grip.run_target(200, -90)
    log("Grip is done calibarting", 2)


def pickup(location=base.angle(), height=-40):
    isHolding = True
    move(location, height)
    grip.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    arm.run_target(60, 0)
    if not is_holding():
        isHolding = False
        grip.run_target(200, -90)

    return isHolding


def is_holding() -> bool:
    return grip.angle() < -18


def drop(location=base.angle(), height=-40):
    move(location, height)
    grip.run_target(200, -90)
    arm.run_target(60, 0)

def get_color():
    r,g,b = color_sensor.rgb()
    wait(100)
    ambient = color_sensor.ambient()
    r *= ambient
    g *= ambient
    b *= ambient

    bestIndex = 0
    distBestIndex = (r-ZONES[bestIndex][1][0])**2 +\
                    (g-ZONES[bestIndex][1][1])**2 +\
                    (b-ZONES[bestIndex][1][2])**2

    for index, color in enumerate(ZONES):
        distIndex = (r-ZONES[index][1][0])**2 +\
                    (g-ZONES[index][1][1])**2 +\
                    (b-ZONES[index][1][2])**2

        if distBestIndex > distIndex:
            bestIndex = index
            distBestIndex = distIndex

    return ZONES[bestIndex]

def calibrate_zones(nrOfZones):
    colorIndex = 1
    PICKUPZONE = None
    log("Set pick-up zone", 0, True)
    while len(ZONES) < nrOfZones:
        pressedButtons = robot.buttons.pressed()

        if Button.LEFT in pressedButtons:
            base.run(50)
        elif Button.RIGHT in pressedButtons:
            base.run(-50)
        elif Button.UP in pressedButtons:
            arm.run(50)
        elif Button.DOWN in pressedButtons:
            arm.run(-50)
        else:
            base.hold()
            arm.hold()

        if Button.CENTER in pressedButtons:
            if PICKUPZONE == None:
                PICKUPZONE = (base.angle(), arm.angle())
                log("Set\nSet drop-off zone" + str(colorIndex), 0, True)
            else:
                currentZone = (base.angle(), arm.angle())
                pickup(currentZone[0], currentZone[1])
                wait(500)
                color = color_sensor.rgb()
                wait(100)
                ambient = color_sensor.ambient()
                base.hold()
                ZONES.append(("COLOR " + str(colorIndex), (color[0] * ambient, color[1] * ambient, color[2] * ambient), currentZone[0], currentZone[1]))
                colorIndex += 1
                drop(currentZone[0], currentZone[1])
                log("Set\nSet drop-off zone" + str(colorIndex), 0, True)
            wait(1000)
    log("", 0, True)
    return PICKUPZONE

def input_number(min=0, max=10):
    number = None
    temp_number = 3
    log(str(temp_number), 0, True)
    while number is None:
        pressedButtons = robot.buttons.pressed()
        if Button.LEFT in pressedButtons:
            temp_number -= 1
            if temp_number < min:
                temp_number=min
            wait(200)
            log(str(temp_number), 0, True)
        elif Button.RIGHT in pressedButtons:
            temp_number += 1
            if temp_number > max:
                temp_number=max
            wait(200)
            log(str(temp_number), 0, True)
        elif Button.CENTER in pressedButtons:
            number = temp_number
            log("", 0, True)
            wait(500)

    return number

if __name__ == "__main__":
    #Set server
    server = BluetoothMailboxServer()
    mbox = TextMailbox("text", server)
    server.wait_for_connection()
    log("CONNECTED", 2)

    calibrate()
    nrOfZones = input_number()
    PICKUPZONE = calibrate_zones(nrOfZones)
    move(PICKUPZONE[0], 0)
    
    wait_for_time = True
    while wait_for_time:
        wait(1000)
        date = (datetime.now())
        time  = date.strftime("%H:%M")
        if time == "09:59":
            wait_for_time = False

    while True:
        wait(5000)
        if mbox.read() == "COLLISION":
            move(base.angle(), 70)
            mbox.send("DONE")
            mbox.wait()
        if pickup(PICKUPZONE[0], PICKUPZONE[1]):
            robot.screen.clear()
            wait(500)
            color = get_color()
            log(color[0], 0, True)
            move(base.angle(), 30)
            drop(color[2], color[3])
            move(base.angle(), 30)
            move(PICKUPZONE[0], 0)
        else:
            robot.speaker.beep()
            log("Nothing", 0, True)
