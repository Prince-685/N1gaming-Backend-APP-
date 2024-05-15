# from django.test import TestCase

# Create your tests here.
# from datetime import datetime

# current_time = datetime.now()

# # Calculate the recent time with minute rounded down to the nearest multiple of 15
# recent_minute = current_time.minute // 15 * 15

# # Format the current time in 12-hour format with the recent minute
# recent_time_str = current_time.replace(minute=recent_minute).strftime("%I:%M %p")

from datetime import datetime


print(datetime.now().replace(microsecond=0) )