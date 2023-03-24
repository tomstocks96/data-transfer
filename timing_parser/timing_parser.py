import json, logging
from typing import List
from datetime import datetime
from datetime import timedelta
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
      method = self._timing_maps.get(key, self._do_not_parse)
      self.logger.debug(f'returning method {method.__name__} for key {key}')
      return method
   
   def _parse_time_duration_seconds(self, timing: str):
      try:
         self.logger.debug(f'converting second timing {timing} into seconds')
         timing  = float(timing)
         return timing
      
      except ValueError as e:
         try:
            self.logger.debug(f'also trying converting minute timing {timing} into seconds')
            timing = self._parse_time_duration_minutes(timing=timing)
            return timing
         except Exception as e:
            self.logger.warn(f'conversion failed with error {e}')
            return None

      except Exception as e: 
         self.logger.warn(f'conversion failed with error {e}')
         return None

   def _parse_time_duration_minutes(self, timing: str):
      try:
         self.logger.debug(f'converting minute timing {timing} into seconds')
         timing = datetime.strptime(timing,'%M:%S.%f')
         seconds = timedelta(minutes=timing.minute,seconds=timing.second,microseconds=timing.microsecond).total_seconds()
         return seconds
      except Exception as e: 
         self.logger.warn(f'conversion failed with error {e}')
         return None

   
   def _do_not_parse(self, timing: str):
      return timing


   def parse_message(self, message):
      for key in message:
         self.logger.debug(f'for key: {key}')
         parse_method = self._get_timing_map(key)
         self.logger.debug(f'initial value was {message[key]}')
         value = parse_method(message[key])
         self.logger.debug(f'method returned {value}')
         message[key] = value

      lap_message = {k: v for k, v in message.items() if v is not None}
      
      return lap_message


   

