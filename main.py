#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait

robot = EV3Brick()
grip = Motor(Port.A)
arm = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
base = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
base_touch = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
ZONES = []

def move(location, angle, armFirst = False):
    if armFirst:
        arm.run_target(60, angle)
        base.run_target(60, location)
    else:
        base.run_target(60, location)
        arm.run_target(60, angle)

def calibrate():
    grip.run_target(200, -90)
    grip.hold()

    arm.run_until_stalled(-30, Stop.COAST, 50)
    arm.run(15)
    while 0 < color_sensor.reflection() < 50:
        wait(15)
    arm.run_time(-20, 300)
    arm.reset_angle(0)
    arm.hold()

    base.run(-60)
    while not base_touch.pressed():
        wait(15)
    base.reset_angle(0)
    base.hold()

    grip.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    grip.reset_angle(0)
    grip.run_target(200, -90)


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

def calibrate_zones():
    colorIndex = 1
    PICKUPZONE = None
    robot.screen.print("Set pick-up zone")
    while len(ZONES) < 2:
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
                robot.screen.print("Set\nSet pick-up zone" + str(colorIndex))
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
                robot.screen.print("Set\nSet drop-off zone " + str(colorIndex))
            wait(1000)
    robot.screen.clear()
    return PICKUPZONE


if __name__ == "__main__":
    calibrate()
    PICKUPZONE = calibrate_zones()
    print(PICKUPZONE)
    print(ZONES)
    
    move(PICKUPZONE[0], 0)

    while True:
        wait(5000)
        if pickup(PICKUPZONE[0], PICKUPZONE[1]):
            robot.screen.clear()
            wait(500)
            color = get_color()
            robot.screen.print(color[0])
            drop(color[2], color[3])
            move(PICKUPZONE[0], 0)
