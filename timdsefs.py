from datetime import datetime, timedelta

# Starting time
start_time = datetime.strptime('01:05:00', '%H:%M:%S')

# Loop to decrement the time by one second until it reaches 00:60:00 (which is essentially 01:00:00)
while start_time > datetime.strptime('00:59:59', '%H:%M:%S'):
    formatted_time = start_time.strftime('%H:%M:%S')

    # If time is 01:00:00, change it to 60:00
    if formatted_time == '01:00:00':
        formatted_time = '60:00'

    print(formatted_time)

    start_time -= timedelta(seconds=1)
