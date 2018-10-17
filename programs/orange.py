#!/usr/bin/env python


# Fade up to Orange and hold there.

from array import array
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE,  DMX_UNIVERSE_SIZE
import math

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

class LinearFade(object):
    def __init__(self, lights, start_value, end_value, num_steps):
        self._lights = lights
        self._start_value = start_value
        self._end_value = end_value
        self._num_steps = num_steps
        # Calculate linearizing factor: https://diarmuid.ie/blog/pwm-exponential-led-fading-on-arduino-or-other-platforms/
        self._R = (num_steps * math.log10(2))/(math.log10(end_value-start_value));

    def UpdateLights(self, data, cur_step):
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """
        for light in self._lights:
            data[light-1] = int(self._start_value + 2**(cur_step / self._R) - 1);
            #data[light-1] = int((self._end_value - self._start_value)*1.0/steps * cur_step)


class DMXUpdater(object):
  def __init__(self, universe, update_interval, client_wrapper,
               progs, steps):
    self._universe = universe
    self._update_interval = update_interval
    self._data = array('B', [DMX_MIN_SLOT_VALUE] * 150)
    self._progs = progs
    self._steps = steps
    self._cur_step = 0
    self._wrapper = client_wrapper
    self._client = client_wrapper.Client()
    self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)
    print len(self._data)

  def UpdateDmx(self):
    """
    This function gets called periodically based on UPDATE_INTERVAL
    """
    for prog in self._progs:
        prog.UpdateLights(self._data, self._cur_step)
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
    # Setup to Faders.
    r_fader = LinearFade(R_TREE_LIGHTS_CH, 10, 255, FINISH_TIME/UPDATE_INTERVAL)
    g_fader = LinearFade(G_TREE_LIGHTS_CH, 5, 165, FINISH_TIME/UPDATE_INTERVAL)

    progs = [ r_fader, g_fader ]

    wrapper = ClientWrapper()
    controller = DMXUpdater(UNIVERSE, UPDATE_INTERVAL, wrapper, progs, FINISH_TIME/UPDATE_INTERVAL)
    # Set things to stop after the number of steps.
    #g_wrapper.AddEvent(SHUTDOWN_INTERVAL, g_wrapper.Stop)
    #r_wrapper.AddEvent(SHUTDOWN_INTERVAL, r_wrapper.Stop)
    wrapper.Run()

    print "Done"
