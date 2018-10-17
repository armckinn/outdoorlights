#!/usr/bin/env python


# Fade up to white and hold there.

from array import array
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE,  DMX_UNIVERSE_SIZE

__author__ = 'Alexander McKinney'

"""
Fade up to White on tree lights.
"""


UPDATE_INTERVAL = 25  # In ms, this comes about to ~40 frames a second
FINISH_TIME = 10000    # In ms, when the fade should be done.
DMX_DATA_SIZE = 100
UNIVERSE = 1
TREE_LIGHTS_CH = [4, 8, 12, 16, 20, 104, 108, 112, 116, 120]

class SimpleFadeController(object):
  def __init__(self, universe, update_interval, client_wrapper,
               lights, start_value, end_value, steps):
    self._universe = universe
    self._update_interval = update_interval
    self._data = array('B', [DMX_MIN_SLOT_VALUE] * max(lights))
    self._lights = lights
    self._start_value = start_value
    self._end_value = end_value
    self._steps = steps
    self._cur_step = 0
    self._wrapper = client_wrapper
    self._client = client_wrapper.Client()
    self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
    print max(lights)
    print len(self._data)

  def UpdateDmx(self):
    """
    This function gets called periodically based on UPDATE_INTERVAL
    """
    for light in self._lights:
        self._data[light-1] = int((self._end_value - self._start_value)*1.0/self._steps * self._cur_step)
    self._cur_step += 1;

    if self._cur_step <= self._steps:
        # Send the DMX data
        self._client.SendDmx(self._universe, self._data)
        # For more information on Add Event, reference the OlaClient
        # Add our event again so it becomes periodic
        self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
    else:
        self._wrapper.AddEvent(self._update_interval, self._wrapper.Stop)


if __name__ == '__main__':
    wrapper = ClientWrapper()
    controller = SimpleFadeController(UNIVERSE, UPDATE_INTERVAL, wrapper, TREE_LIGHTS_CH, 0, 255,
                                        FINISH_TIME/UPDATE_INTERVAL)
    # Set things to stop after the number of steps.
    #wrapper.AddEvent(SHUTDOWN_INTERVAL, r_wrapper.Stop)
    wrapper.Run()

    print "Done"
