from flask import Flask, request, render_template, redirect, send_file
from werkzeug.utils import secure_filename
import os
import mysql.connector
#estaiblish the connection
conn=mysql.connector.connect(host='localhost',user='root',password='', database='proj')
#responsible data 
cursor = conn.cursor()

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/getdata' , methods=['post'])
def getdata():
	if request.method == 'POST':
		file = request.files['img']
		filename = secure_filename(file.filename)
		ext = filename.rsplit('.', 1)[1].lower()
		if ext=="jpeg" or ext=="png" or ext=="jpg":
			path = '../desktop/'
			fullpath = os.path.join(path, filename)
			file.save(fullpath)
			q="INSERT INTO imageupload VALUES(null, %s, %s, NOW(), NOW())"
			cursor.execute(q, (filename, fullpath))
			conn.commit()
			return redirect('/view')
		return "Error occured!"
	else:
		return "Error occured!"	

@app.route('/view')
def view():
	q="SELECT * FROM imageupload"
	cursor.execute(q)
	result=cursor.fetchall()
	return render_template('view.html', result=result)



@app.route('/delete')
def delete():
	row_id=request.args['id']
	path=request.args['path']
	q="DELETE FROM imageupload WHERE id="+row_id
	cursor.execute(q)
	conn.commit()
	os.remove(path)
	return redirect('/view')

@app.route('/download')
def download():
	path=request.args['path']
	return send_file(path, as_attachment=True)


app.run(debug=True)