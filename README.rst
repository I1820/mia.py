I1820-RPi
==============================================================================
- `Introduction`_
- `SubProjects`_

Introduction
------------------------------------------------------------------------------
.. figure:: http://aolab.github.io/documentation/architecture/I1820-Plug.jpg
   :alt: I1820-Plug in AoLab IoT Architecture
   :align: center

Improved 18.20 Raspberry Pi Plugin. You can use it in order to create I1820 Applications
for your IoT environment that runs on Raspberry Pi platform.

SubProjects
------------------------------------------------------------------------------
Goldoon
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Author: Iman Tabrizian

This project provides soild humidity measurement with I1820.
ESP sends it's data to RPi and RPi acts as a gateway and sends
the data to I1820 brain.

Green House
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Author: Behnaz Sadat Motevali

This project controls your green house water and humdity with zigbees.
zigbees send their data to RPi and RPi acts as a gateway and sends
the data to I1820 brain.

AoLab
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Author: Field Team of AoLab.

This project is a our main goal of creating this platform.
In this project we connect the RPi to nRF network and it acts like
a gateway and we can control the lamps or read the sensors.

Presenter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Author: Reza Jahani

This project is a presentation controller for RPi, with this project you can
control your presentation with I1820 platform.
