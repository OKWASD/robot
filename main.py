#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait

#Initialize EV3sensors and ev3brick
robot = EV3Brick()
grip = Motor(Port.A)
arm = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
base = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
base_touch = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)

#Reset and calibrate arm and grip
def calibrate():
    #Zero arm
    arm.run_time(-30, 1000)
    arm.run(15)
    while 0 < color_sensor.reflection() < 50:
        wait(15)
    arm.reset_angle(0)
    arm.hold()

    #Zero base
    base.run(-60)
    while not base_touch.pressed():
        wait(15)
    base.reset_angle(0)
    base.hold()

    #Zero grip
    grip.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    grip.reset_angle(0)
    grip.run_target(200, -90)

#US01 && US03
def pickup():
    "Pickups object and checks if object exist"
    arm.run_target(60, -40)
    grip.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    if grip.angle() > -3:
        grip.run_target(200, -90)
    arm.run_target(60, 0)

#US02
def drop():
    "Drops held object"
    arm.run_target(60, -40)
    grip.run_target(200, -90)
    arm.run_target(60, 0)

#US04
def check_color():
    "Checks color "
    color = color_sensor.color()
    robot.screen.print(color)
    return color

calibrate()

while True:
    pressedButtons = robot.buttons.pressed()
    if(Button.DOWN in pressedButtons):
        drop()
        wait(100)
    elif(Button.UP in pressedButtons):
        pickup()
        wait(100)
    elif(Button.CENTER in pressedButtons):
        check_color()
        wait(100)
    
    if(Button.LEFT in pressedButtons):
        base.run(50)
    elif(Button.RIGHT in pressedButtons):
        base.run(-50)
    else:
        base.hold()
