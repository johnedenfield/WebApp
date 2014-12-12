# -*- coding: utf-8 -*-
#!/usr/bin/python2.7

import sqlite3, chartkick, os

from datetime import datetime, timedelta
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash


app=Flask(__name__,static_folder=chartkick.js(), static_url_path='/static')
# configuration
DATABASE= os.path.join(app.root_path, 'db/SensorData.db')
DEBUG = True
SECRET_KEY = 'Montana'
USERNAME = 'admin'
PASSWORD = 'default'


#app=Flask(__name__,static_folder=chartkick.js(), static_url_path='/static/js/')
app.config.from_object(__name__)
app.jinja_env.add_extension("chartkick.ext.charts")


def connect_db():
	#print app.config['DATABASE']
	conn=sqlite3.connect(app.config['DATABASE'])
	return conn

@app.route('/')
def Hello():
	return 'Apps up and running'

@app.route('/WaterLevel')
def WaterLevel():
	
	conn=connect_db()
	c = conn.cursor();
	sqlstr = "SELECT DateAndTime, Pressure " \
			"FROM PressureSensor "\
			"ORDER BY rowid DESC LIMIT 432"
		
	
	data = c.execute(sqlstr)				 
	data = data.fetchall();
		
	WaterLevel=[]
	timeoffset=-5  # 5 hour difference
	n=0
	for row in data:
		
		dstr =str(row[0]).strip()
		d=datetime.strptime(dstr,'%m/%d/%y %H:%M:%S')+ timedelta(hours=timeoffset)	
		dstr=d.strftime('%m/%d/%y %H:%M:%S');
		
		WaterLevel.append([dstr,row[1]])
		n=n+1
	
	conn.close()


	#ChartData=[{'data' : WaterLevel, 'name' :'Water Level '}]
	return render_template('WaterLevel_Graph.html', WaterLevel=WaterLevel, CurrentLevel = WaterLevel[0])



@app.route('/ChristmasTreeLights',methods=['GET'] )
def ToggleLights():

	writeoutput = False
	loc=4;
	
	fname=os.path.join(app.root_path,'GPIO','GPIOHandShake.txt')

	if request.method =='GET':
		lights = request.args.get('light')


	if lights == 'on':
		outstr ='{0} ON'
		writeoutput = True
		status=1

	elif lights =='off':    
		outstr ='{0} OFF'
		writeoutput = True
		status=0
	else:
		with open(fname,'r') as f:
			status= f.read()
		lights=status.split()[1]
		
		if lights =='ON':
			status=1
		else:
			status=0


	if writeoutput:

		with open(fname, 'w') as f:
			f.write(outstr.format(loc))
		


	return render_template('ChristmasTreeLights.html', lights=lights, status=status)

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0')
