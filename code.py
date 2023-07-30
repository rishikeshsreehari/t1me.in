from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Time Zone Converter!'

@app.route('/<time_str>')
def convert_time(time_str):
    time_str = time_str.upper()
    if time_str.endswith('IST'):
        zone = time_str[-3:]
        time_str = time_str[:-3]
        return redirect(url_for('show_time', time=time_str,zone=zone))

    return 'Invalid URL format. Please use HHMMIST format.'

@app.route('/time')
def show_time():
    time_str = request.args.get('time', '')
    zone = request.args.get('zone', '')
    time_obj = datetime.strptime(time_str, '%H%M')
    ist_time = time_obj.strftime('%H:%M')
    
    #timezone = pytz.timezone('Asia/Calcutta')
    
    # gmt_time = gmt_time.strftime('%H:%M')

    # Convert IST time to other time zones
    time_zones = {
        'PST': time_obj - timedelta(hours=12),
        'EST': time_obj - timedelta(hours=9),
        'GMT': time_obj - timedelta(hours=5),
    }
    return render_template('time.html', ist_time=ist_time, time_zones=time_zones, zone=zone)


if __name__ == '__main__':
    app.run()