#!/usr/bin/env python


# Fade up to Orange and hold there.

from array import array
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE,  DMX_UNIVERSE_SIZE

__author__ = 'Alexander McKinney'

"""
Fade up to Orange on tree lights.
"""


UPDATE_INTERVAL = 25  # In ms, this comes about to ~40 frames a second
FINISH_TIME = 10000    # In ms, when the fade should be done.
DMX_DATA_SIZE = 100
UNIVERSE = 1
R_TREE_LIGHTS_CH = [1, 5, 9, 13, 17, 101, 105, 109, 113, 117]
G_TREE_LIGHTS_CH = [2, 6, 10, 14, 18, 102, 106, 110, 114, 118]

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
    # Create 2 faders: one to 255 (Red) and one to 165 (Green).
    r_wrapper = ClientWrapper()
    r_controller = SimpleFadeController(UNIVERSE, UPDATE_INTERVAL, r_wrapper, R_TREE_LIGHTS_CH, 0, 255,
                                        FINISH_TIME/UPDATE_INTERVAL)
    g_wrapper = ClientWrapper()
    g_controller = SimpleFadeController(UNIVERSE, UPDATE_INTERVAL, g_wrapper, G_TREE_LIGHTS_CH, 0, 165,
                                        FINISH_TIME/UPDATE_INTERVAL)
    # Set things to stop after the number of steps.
    #g_wrapper.AddEvent(SHUTDOWN_INTERVAL, g_wrapper.Stop)
    #r_wrapper.AddEvent(SHUTDOWN_INTERVAL, r_wrapper.Stop)
    r_wrapper.Run()
    g_wrapper.Run()

    print "Done"
