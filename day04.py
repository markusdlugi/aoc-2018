import re
import datetime
from collections import defaultdict

# Read observations from input and sort them by timestamp
lines = [line.strip() for line in open("input/04.txt")]
observations = list(map(lambda x: (int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]), x[5]),
                        (re.findall(r'\[(\d*)-(\d*)-(\d*) (\d*):(\d*)\] (.*)', line)[0] for line in lines)))
observations.sort()

# Dicts for tracking minutes slept
total_sleep = defaultdict(int)
minutes_asleep = defaultdict(lambda: defaultdict(int))

# Calculate minutes asleep for each guard
current_guard = None
sleep_start = None
for year, month, day, hour, minute, text in observations:
    if text.startswith('Guard'):
        current_guard = int(re.findall(r'Guard #(\d*) begins shift', text)[0])
    elif text.startswith('falls'):
        sleep_start = datetime.datetime(year, month, day, hour, minute)
    else:
        sleep_end = datetime.datetime(year, month, day, hour, minute)
        sleep_duration = (sleep_end - sleep_start).total_seconds() / 60
        total_sleep[current_guard] += sleep_duration
        for i in range(sleep_start.minute, minute):
            minutes_asleep[current_guard][i] += 1

# Part A - Find guard with max total sleep
max_sleep_guard = max(total_sleep, key=total_sleep.get)
minutes = minutes_asleep[max_sleep_guard]
max_sleep_minute = max(minutes.keys(), key=lambda k: minutes[k])

print(max_sleep_guard * max_sleep_minute)

# Part B - Find guard with most sleep in same minute (= highest minute value)
max_minute = max((max(minutes.values()) for minutes in minutes_asleep.values()))
max_minute_guard = [k for k, v in minutes_asleep.items() if max_minute in v.values()][0]
minutes = minutes_asleep[max_minute_guard]
max_minute_minute = max(minutes.keys(), key=lambda k: minutes[k])

print(max_minute_guard * max_minute_minute)
