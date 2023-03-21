import json, logging
from typing import List
import datetime
import time

class TimingParser:
   def __init__(self):
      self.logger = logging.getLogger(__name__)
      self._timing_maps = {
         'S1': self._parse_time_duration_seconds,
         'S2': self._parse_time_duration_seconds,
         'S3': self._parse_time_duration_seconds,
         'Diff': self._parse_time_duration_seconds,
         'Gap': self._parse_time_duration_seconds,
         'Best': self._parse_time_duration_minutes,
         'Last': self._parse_time_duration_minutes,
         #'scrape_timestamp': 'absolute_time',
         #'date': 'absolute_date'
      }

   def _get_timing_map(self, key):
      return self._timing_maps.get(key, self._do_not_parse)
   
   def _parse_time_duration_seconds(self, timing: str):
      timing  = float(timing)
      return timing
   
   def _parse_time_duration_minutes(self, timing: str):
      timing = time.strptime(timing,'%M:%S.%f')
      seconds = datetime.timedelta(hours=timing.tm_hour,minutes=timing.tm_min,seconds=timing.tm_sec).total_seconds()
      return seconds
   
   def _do_not_parse(self, timing: str):
      return timing


   def parse_message(self, message):
      for key in message:
         parse_method = self._get_timing_map(key)
         value = parse_method(message[key])
         message[key] = value
      return message


   

