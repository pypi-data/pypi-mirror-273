"""
Written by our favorite chat bot.
"""
# The function to be tested (save as convert_to_seconds.py)
import re

def convert_to_seconds(time_str):
    if not time_str:
        raise ValueError("Invalid time format")

    pattern = re.compile(r'(?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?')
    match = pattern.fullmatch(time_str)
    
    if not match:
        raise ValueError("Invalid time format")

    time_dict = match.groupdict(default='0')
    days = int(time_dict['days'])
    hours = int(time_dict['hours'])
    minutes = int(time_dict['minutes'])
    seconds = int(time_dict['seconds'])

    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    return total_seconds
