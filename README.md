crashlibrary
============

crashspace library code exists for three different systems.

There is Arduino code to read the state of the door (from a magnetic reed switch) and weight of the shelf (pressure sensor) within the library. The Arduino sends this data over a serial connection and controls the light inside the library.

There is a laptop running some python. This python reads the serial data from the Arduino (sensor data) and sends it over the internet to a cloud data repo (currently xively).

There is python and perl scripts that can read and process the data from the cloud data repo.

enjoy!
