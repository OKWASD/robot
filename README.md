# PA1473 - Software Development: Agile Project

## Template information
This template should help your team write a good readme-file for your project. (The file is called README.md in your project directory.)
You are of course free to add more sections to your readme if you want to.

Readme-files on GitHub are formatted using Markdown. You can find information about how to format using Markdown here: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Your readme-file should include the following sections:


## Introduction
A sorting robot written in python using pybricks.

How the robot should look like:
![robot image](/IMG_6790.jpg)

## Getting started
1. Clone this repository 
2. Install VS code and install the ev3 extension
3. Open the folder to your cloned repository

## Building and running
### Running the project
1. Connect the robot
2. Press download and run

The server and client robots should be paired before running and the server should be launched before the client.

If you want to run only one robot use main.py instead of client.py & server.py

### Instructions:
Moving the arm when calibrating use the arrow buttons
press the center button to confirm the position.

1. Wait for the robot to calibrate
2. First set how many drop-offzones with right and left arrow and press center to confirm
3. Set pick up zone first
4. Then set shared zone where the robots will share the drop-off zone (If running server & client)
5. Set remaining zones
6. Let the program run

## Tests 
https://docs.google.com/document/d/1GjgFoYxHxjOlEtBsgi7YkAAaRv6gSJomERTnEkErh2c/edit

## Features

- [x] US01B: As a customer, I want the robot to pick up items from a designated position. 
- [x] US02B: As a customer, I want the robot to drop items off at a designated position.
- [x] US03: As a customer, i want the robot to be able to determine if an item is present at a given location
- [x] US04B: As a customer, I want the robot to tell me the color of an item at a designated position.
- [x] US05: As a customer, I want the robot to drop items off at different locations based on the color of the item.
- [x] US06: As a customer, I want the robot to be able to pick up items from elevated positions.
- [x] US08B: As a customer, I want to be able to calibrate items with three different colors and drop the items off at a specific drop-off zones based on color
- [x] US09: As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived
- [] US10: As a customer, I want the robot to sort items at a specific time
- [x] US11: As a customer, I want the robot to communicate and work together on items sorting without colliding with each other
- [x] US12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones.
