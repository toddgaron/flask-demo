from flask import Flask, render_template, request, redirect
from requests import get
from simplejson import loads
from pandas import DataFrame
from numpy import array, datetime64
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method=='GET':
		return render_template('stockinfo.html')
	else:
		app.vars['Name']=request.form['name']
		app.vars['Method']=request.form['method']
		try:
			w=get('https://www.quandl.com/api/v3/datasets/WIKI/{}/data.json'.format(app.vars['Name'])).text
			w=loads(w)
			w=DataFrame(w['dataset_data']['data'],columns=w['dataset_data']['column_names'])
			p=figure(width=800,height=400,x_axis_type="datetime")
			p.line(array(w['Date'],dtype=datetime64),list(w[app.vars['Method']]))
			script, div = components(p)
			#return render_template('outpage.html',name=app.vars['Name'])
			print 'here'
			return render_template('outpage.html',name=app.vars['Name'].toUpper(),s=script,d=div)
		except:
			return render_template('errorpage.html')

if __name__ == '__main__':
  app.run(port=33507)
