# [MiA](https://github.com/I1820/mia) Python SDK

## Introduction

Middleware in Action (MiA) python sdk which can be used to write agents in python.
Agents pings MiA periodically for registering themselves and their things. The logic
for adding or remove things is written into agent and depends on the scenario.

## SubProjects

Following projects are written with mia.py.

### Goldoon

- Author: Iman Tabrizian

This project provides soild humidity measurement with MiA.
ESP sends its data to RPi and RPi acts as a gateway and sends
the data to MiA brain.

### Green House

- Author: Behnaz Sadat Motevali

This project controls your green house water and humdity with Zigbees.
zigbees send their data to RPi and RPi acts as a gateway and sends
the data to MiA brain.

### AoLab

- Author: Field Team of AoLab.

This project is a our main goal of creating this platform in 2016.
In this project we connect the RPi to nRF network and it acts like
a gateway and we can control the lamps or read the sensors for providing Smart Campus at Amirkabir University.

### Presenter

- Author: Reza Jahani

This project is a presentation controller for RPi, with this project you can
control your presentation with MiA platform.

### Car

- Author: Roya Taheri

This project is a smart car monitoring system.
