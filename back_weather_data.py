from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime as dt

import geocoder as gc, csv, sys, datetime
import front_weather_data as front_end
import os.path

# Tied to Update data button, it gathers data of the area specified by the address provided by the user.
# Takes an address and goes through a geocoder to gather the zip code. The current system is limited
# to the United States. Also, if the weather.com html structure changes, it will fail to gather the data
# properly. 
def gather_data():
	ui.updateButton.setEnabled(False)
	address_str = str(ui.addressBox.text())
	postal_zip = gc.google(address_str)
	zip_code = str(postal_zip.postal)	

	if(zip_code != "None"):
		url = 'https://weather.com/weather/hourbyhour/l/' + zip_code + ':4:US'

		uClient = uReq(url)
		page_html = uClient.read()
		page_soup = soup(page_html, "html.parser")
		time_containers = page_soup.findAll("div", {"class":"hourly-time"})
		containers = page_soup.findAll("td", {"class":"temp"})
		precip_containers = page_soup.findAll("td", {"class":"precip"})
		humid_containers = page_soup.findAll("td", {"class":"humidity"})
		wind_containers = page_soup.findAll("td", {"class":"wind"})

		today = datetime.date.today().strftime("%Y-%m-%d")
		length = len(time_containers)
		mylist = [[] for i in range(length)]
		x = 0

		for container in containers:

			wind_dir = ''.join([i for i in wind_containers[x].text if not i.isdigit()])
			wind_speed = ''.join([i for i in wind_containers[x].text if not i.isalpha()])

			if(time_containers[x].span.text == "12:00 am"):
				today = datetime.date.today() + datetime.timedelta(days=1)
				today = today.strftime("%Y-%m-%d")

			mylist[x].extend((today, time_containers[x].span.text, container.text[:-1], precip_containers[x].text[:-1],
								humid_containers[x].text[:-1], wind_dir[:-5].strip(), wind_speed.strip()))
			x += 1

		write_mode = file_check(file_path)

		write_csv(mylist, write_mode)

	else:
		invalid_address()

	ui.updateButton.setEnabled(True)

# Warning message for users that provide addresses with not enough information for google to 
# find the zip code.
def invalid_address():
	warningMsg = QMessageBox()        
	warningMsg.setIcon(QMessageBox.Warning)       
	warningMsg.setWindowIcon(QtGui.QIcon("assets\icon.png"))
	warningMsg.setText("The address provided in the text box is invalid." + 
					   "\nPlease try again with more detail.") 
	warningMsg.setWindowTitle("Invalid Address") 
	warningMsg.setStandardButtons(QMessageBox.Ok)       
	warningMsg.setEscapeButton(QMessageBox.Close)
	warningMsg.exec_() 

# Warning message that program doesn't have any weather data to analyze yet.
def missing_data(path):
	warningMsg = QMessageBox()        
	warningMsg.setIcon(QMessageBox.Warning)       
	warningMsg.setWindowIcon(QtGui.QIcon("assets\icon.png"))
	warningMsg.setText("The program cannot find " + path + " in the folder." + 
					   "\nPlease try again with data gathered from the update data\nbutton.") 
	warningMsg.setWindowTitle("Missing Weather Data") 
	warningMsg.setStandardButtons(QMessageBox.Ok)       
	warningMsg.setEscapeButton(QMessageBox.Close)
	warningMsg.exec_() 

# Informs user that the weather has successfully been gathered.
def update_success(char):
	successMsg = QMessageBox()        
	successMsg.setWindowIcon(QtGui.QIcon("assets\icon.png"))
	successMsg.setIcon(QMessageBox.Information)      

	if(char == 'w'):
		msg = 'created.'
	else:
		msg = 'updated.'

	successMsg.setText("The file named weather_data.csv has been successfully " + msg) 
	successMsg.setWindowTitle(msg.capitalize()[:-1] + " Weather Data") 
	successMsg.setStandardButtons(QMessageBox.Ok)       
	successMsg.setEscapeButton(QMessageBox.Close)
	successMsg.exec_() 

# Informs user that the weather has successfully been analyzed and put in a .csv report file.
# The report shows the averages of the weather at each particular time. The idea is that
# we can neatly see what the average temperature has been lately at any given time along 
# with all the other details.
def created_report():
	successMsg = QMessageBox()        
	successMsg.setWindowIcon(QtGui.QIcon("assets\icon.png"))
	successMsg.setIcon(QMessageBox.Information)      
	name = str(ui.nameBox.text())
	successMsg.setText("The file named " + name + ".csv has been successfully created.") 
	successMsg.setWindowTitle("Created Weather Report") 
	successMsg.setStandardButtons(QMessageBox.Ok)       
	successMsg.setEscapeButton(QMessageBox.Close)
	successMsg.exec_() 

# Checks path to see if it exists to determine if the header line needs to be added along
# with some small wording details.
def file_check(file_path):
	if(os.path.exists(file_path)):
		return 'a'
	else:
		return 'w'

# Method for writing data to csv file.
def write_csv(list_data, mode):
	with open('weather_data.csv', mode, newline='') as myfile:
	    wr = csv.writer(myfile, delimiter=',', quoting=csv.QUOTE_NONE)
	    if(mode == 'w'):
	    	wr.writerow(('date', 'time', 'temp', 'precip', 'humid', 'wind dir', 'wind spd'))
	    for row in list_data:
	    	wr.writerow(row)
	if(mode == 'w'):
		print("Created data file: weather_data.csv")
	else:
		print("Added data file to weather_data.csv")
		
	update_success(mode)

	myfile.close()

# Method for analyzing all the data gathered in the form of averages and most commonly directed winds.
def analyze_data():
	if(file_check(file_path) == 'a'):
		file = open(file_path, newline='')
		reader = csv.reader(file)
		header = next(reader)

		data = []
		temp_total = 0

		for row in reader:
			date, time = dt.strptime(row[0], '%Y-%m-%d'), dt.strptime(row[1], '%I:%M %p').time()
			temp, precip, humid, wind_spd = int(row[2]), int(row[3]), int(row[4]), int(row[6])
			data.append([date, time, temp, precip, humid, row[5], wind_spd])

		file.close()
		
		report_name = str(ui.nameBox.text()) + ".csv"
		file = open(report_name, 'w', newline='')
		writer = csv.writer(file)
		writer.writerow(["Time", "Temp", "Precip", "Humid", "Wind Dir", "Wind Spd", "Sample Size"])

		sum_temp, sum_precip, sum_hum, cnt_wdir, sum_wspd, cnt_time = {}, {}, {}, {}, {}, {}
		date_reference = []

		wind_directions = ['N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW', 'NNE', 'ENE', 'ESE', 'SSE', 'SSW', 'WSW' , 'WNW', 'NNW']

		for i in range(len(data)):
			sum_temp[data[i][1]] = 0
			sum_precip[data[i][1]] = 0
			sum_hum[data[i][1]] = 0
			sum_wspd[data[i][1]] = 0
			cnt_time[data[i][1]] = 0
			cnt_wdir[data[i][1]] = {}
			for j in range(16):
				cnt_wdir[data[i][1]][wind_directions[j]] = 0

		for i in range(len(data)):
			current_row = data[i]
			current_date, current_time, current_temp  = current_row[0], current_row[1], current_row[2]
			current_precip, current_hum, current_wdir  = current_row[3], current_row[4], current_row[5]
			current_wspd = current_row[6]

			if((current_date, current_time) not in date_reference):
				sum_temp[current_time] += current_temp
				sum_precip[current_time] += current_precip
				sum_hum[current_time] += current_hum
				cnt_wdir[current_time][current_wdir] += 1
				sum_wspd [current_time] += current_wspd
				cnt_time[current_time] += 1 
				date_reference.append((current_row[0], current_time))
		for i in range(len(sum_wspd)):
			current_row = data[i]
			current_time = current_row[1]
			str_time, counted_time = current_time, cnt_time[current_time]
			avg_temp, avg_precip = sum_temp[str_time]/counted_time, sum_precip[str_time]/counted_time
			avg_humid, avg_wspd = sum_hum[str_time]/counted_time, sum_wspd[str_time]/counted_time
			mst_cmn_wdir = max(cnt_wdir[str_time], key=cnt_wdir[str_time].get)

			writer.writerow([current_time, avg_temp, avg_precip, avg_humid, mst_cmn_wdir, avg_wspd, counted_time])

		file.close()
		created_report()
	else:
		missing_data(file_path)

# Check to see if the default texts is still there in order to clear it on click if that is the case.
def clear_address():
	if(str(ui.addressBox.text()) == "Enter your address for a weather update"):
		ui.addressBox.setText('')
def clear_file_name():
	if(str(ui.nameBox.text()) == "Enter a name for the weather report file"):
		ui.nameBox.setText('')

# Main method for connecting buttons to methods, setting up the graphical user interface, etc.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main_window = front_end.QtWidgets.QApplication(sys.argv)
    form = front_end.QtWidgets.QWidget()

    ui = front_end.Ui_Form()
    ui.setupUi(form)

    ui.createButton.clicked.connect(analyze_data)
    ui.updateButton.clicked.connect(gather_data)

    ui.addressBox.returnPressed.connect(gather_data)
    ui.nameBox.returnPressed.connect(analyze_data)	

    ui.addressBox.clicked.connect(clear_address)
    ui.nameBox.clicked.connect(clear_file_name)	

    file_path = 'weather_data.csv'

    ui.createButton.setFocus() # Makes default focus not visible.
    form.show()
    sys.exit(app.exec_())
