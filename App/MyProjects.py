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
	print app.config['DATABASE']
	conn=sqlite3.connect(app.config['DATABASE'])
	return conn

@app.route('/')
def Hello():
	return app.config['DATABASE']

@app.route('/WaterLevel')
def WaterLevel():
	
	conn=connect_db()
	c = conn.cursor();
	sqlstr = "SELECT DateAndTime, Pressure " \
			"FROM PressureSensor "\
			"ORDER BY rowid DESC LIMIT 280"
		
	
	data = c.execute(sqlstr)				 
	data = data.fetchall();
	print(data)
	
	WaterLevel=[]
	timeoffset=-5  # 5 hour difference
	n=0
	for row in data:
		
		dstr =str(row[0]).strip()
		d=datetime.strptime(dstr,'%m/%d/%y %H:%M:%S')+ timedelta(hours=timeoffset)	
		dstr=d.strftime('%m/%d/%y %H:%M:%S');
		print(dstr)
		WaterLevel.append([dstr,row[1]])
		n=n+1
	
	conn.close()


	#ChartData=[{'data' : WaterLevel, 'name' :'Water Level '}]
	return render_template('WaterLevel_Graph.html', WaterLevel=WaterLevel)



@app.route('/ChristmasTreeLights',methods=['GET'] )
def ToggleLights():

	writeoutput = False
	loc=4;
	
	
	if request.method =='GET':
		lights = request.args.get('light')


	if lights == 'on':
		outstr ='{0} ON'
		writeoutput = True

	elif lights =='off':    
		outstr ='{0} OFF'
		writeoutput = True

	else:
		lights ='Bad Request : {}  - not processed'.format(lights)

	if writeoutput:
		fname = os.path.join(app.root_path,'GPIO','GPIOHandShake.txt')

		with open(fname, 'w') as f:
			f.write(outstr.format(loc))
		


	return render_template('ChristmasTreeLights.html', lights=lights)

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0')
