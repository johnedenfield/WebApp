# -*- coding: utf-8 -*-
#!/usr/bin/python2.7

# Create Temperature Logging Database
import sqlite3 , subprocess, threading
from datetime import datetime
from time import sleep

def Createdb():
    # Create database in RAM
    
    conn = sqlite3.connect('TemperatureData');
    
    c = conn.cursor();
    c.execute( ''' CREATE TABLE IF NOT EXISTS CPUTemperature (date text , temperature real) ''');
    
    conn.commit();
    conn.close();

def getTemperature():
    # Gets CPU Temperature
    # Returns the temperature in degrees C”
    s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"]);
    return float(s.split('=')[1][:-3]);
    
    

def LogTemperature():
    # Log CPU temperature
    conn = sqlite3.connect('TemperatureData');
    tempC = getTemperature();
    tempF =tempC*9/5+32;
    
    # Get Time
    d=datetime.now();
    dstr=d.strftime('%m/%d/%y %H:%M:%S');
      
    
    c = conn.cursor();
    c.execute('INSERT INTO CPUTemperature VALUES (?, ?)' , (dstr,tempF));
    
    conn.commit();
    conn.close();
    threading.Timer(5,LogTemperature).start();


def ReturnData(conn):
    # Check Data
    
    # conn = sqlite3.connect('TemperatureData');
    c = conn.cursor();
    
    data = c.execute('SELECT * FROM CPUTemperature ')
    
    return data.fetchall();
    
    conn.close();

def StartLogging():
    # Create database
    Createdb();
    #Log Data
    LogTemperature()
    
    

if __name__ =='__main__':
    print "Started Logging"
    StartLogging();
    
