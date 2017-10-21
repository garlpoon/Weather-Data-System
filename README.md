# Weather-Data-System
An application for scraping and mining weather data from weather.com in Python.
It has a very simple user interface and gathers its data from Weather.com
The graphical user interface was designed using Qt Designer. The program requires PyQt5, 
bs4, and geocoder modules installed to your copy of Python. Also, Python must be version 3.6.2.

# Instructions
To gather weather data, type an address in the upper text box. 
Afterwards, press enter or press the button titled "Update data".
This creates a .csv file named weather_data.csv in the folder containing the code.

With the weather data gathered, type in a file name in the lower text box.
Then, press enter or press the button titled "Create Report".
This creates a .csv file named after the name that was typed on the lower text box 
in the folder containing the code.

# Use
The user should gather data day by day to provide more data for the program.
The report generates average values based on times of the day to provide a 
general idea of the temperature at any time.
