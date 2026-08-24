Væksthus

A 2nd semester school project, a small automated greenhouse system built with a Raspberry Pi, made to keep a chili plant alive with minimal manual care.

What it does

The system monitors soil moisture and light levels, and automatically controls a water pump and an LED grow light based on the readings. Sensor data is logged to a database so conditions can be tracked over time.

How it works

- `soil.py` — reads soil moisture from the sensor
- `ldr.py` — reads light levels
- `pumpe.py` — controls the water pump based on soil moisture readings
- `led.py` — controls the LED grow light based on light levels
- `database.py` — handles storing sensor readings
- `app.py` — main application, ties the sensors and controls together

Built with

- Python
- Raspberry Pi
- Basic electronics (soil moisture sensor, LDR light sensor, relay-controlled pump, LED)

Team project

Built together — a shared effort with no fixed role split.
