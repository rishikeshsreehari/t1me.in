from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
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
        return redirect(url_for('show_time', time=time_str, zone=zone))

    return 'Invalid URL format. Please use HHMMIST format.'

@app.route('/time')
def show_time():
    time_str = request.args.get('time', '')
    zone = request.args.get('zone', '')

    # Set timezone for the input time to IST explicitly
    ist_tz = pytz.timezone('Asia/Kolkata')
    time_obj = datetime.strptime(time_str, '%H%M')

    common_time_zones = pytz.common_timezones
    time_zones = {}
    for tz in common_time_zones:
        try:
            tz_obj = pytz.timezone(tz)
            localized_time_obj = ist_tz.localize(time_obj.replace(tzinfo=None), is_dst=None)
            converted_time = localized_time_obj.astimezone(tz_obj).strftime('%H:%M')
            time_zones[tz] = converted_time
        except Exception as e:
            print(f"Error occurred for timezone '{tz}': {e}")

    return render_template('time.html', time_val=time_obj, time_zones=time_zones, zone=zone)


if __name__ == '__main__':
    app.run()
