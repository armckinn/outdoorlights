#!/usr/bin/env python


# Fade up to Orange and hold there.

from array import array
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE,  DMX_UNIVERSE_SIZE
import math
import time


__author__ = 'Alexander McKinney'

"""
Fade up to Orange on tree lights.
"""


UPDATE_INTERVAL = 25  # In ms, this comes about to ~40 frames a second
FINISH_TIME = 1000    # In ms, when the fade should be done.
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
        self._R = (num_steps * math.log10(2))/(math.log10(abs(end_value-start_value)));
        if end_value > start_value:
            self._up_dir = True
        else:
            self._up_dir = False

    def UpdateLights(self, data, cur_step):
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """
        for light in self._lights:
            if self._up_dir:
                data[light-1] = int(self._start_value + 2**(cur_step / self._R) - 1);
            else:
                data[light-1] = int(self._end_value + 2**((self._num_steps - cur_step) / self._R) - 1);
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
    r_fader_up = LinearFade(R_TREE_LIGHTS_CH, 10, 255, FINISH_TIME/UPDATE_INTERVAL)
    g_fader_up = LinearFade(G_TREE_LIGHTS_CH, 5, 165, FINISH_TIME/UPDATE_INTERVAL)
    progs_up = [ r_fader_up, g_fader_up ]
    r_fader_down = LinearFade(R_TREE_LIGHTS_CH, 255, 10, FINISH_TIME/UPDATE_INTERVAL)
    g_fader_down = LinearFade(G_TREE_LIGHTS_CH, 165, 5, FINISH_TIME/UPDATE_INTERVAL)
    progs_down = [ r_fader_down, g_fader_down ]

    wrapper = ClientWrapper()
    while True:
        controller = DMXUpdater(UNIVERSE, UPDATE_INTERVAL, wrapper, progs_up, FINISH_TIME/UPDATE_INTERVAL)
        wrapper.Run()

        time.sleep(2)

        controller = DMXUpdater(UNIVERSE, UPDATE_INTERVAL, wrapper, progs_down, FINISH_TIME/UPDATE_INTERVAL)
        wrapper.Run()

    print "Done"
