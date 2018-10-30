#!/usr/bin/env python


# Fade up to Orange and hold there.

from array import array
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE,  DMX_UNIVERSE_SIZE
import math
import time
import random

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

class RandomBreath(object):
    def __init__(self, lights, low, high):
        self._lights = lights
        self._low = low
        self._high = high
        NewBreath()

    def NewBreath(self)
        # Calculate a random duration.
        self._up_dir = True
        self._num_steps = random.randint(500/UPDATE_INTERVAL, 5000/UPDATE_INTERVAL)
        self._cur_step = 0
        self._R = (self._num_steps * math.log10(2))/(math.log10(abs(self._high-self._low)));

    def UpdateLights(self, data, cur_step):
        """
        This function gets called periodically based on UPDATE_INTERVAL
        """
        for light in self._lights:
            data[light-1] = int(self.low_value + 2**(self._cur_step / self._R) - 1);
        if self._up_dir:
            self._cur_step += 1
            if self._cur_step >= self._num_steps:
                self._up_dir = False
        else:
            self._cur_step -= 1
            if self._cur_step <= 0:
                NewBreath()

    def GetLights(self):
        return self._lights


class CopyFader(object):
    """
    This class is a fader tha follows another fader. The 2 faders need to be
    the same length.
    """
    def __init__(self, lights, fader, scale):
        self._lights = lights
        self._fader = fader
        self._scale = scale

    def UpdateLights(self, data, cur_step):
        # This fader just copies the specified fader and applies the multiplier to each value.
        lights = self._fader.GetLights()
        for light in self._lights:
            data[light-1] = lights[light-1] * self._scale


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
    for r_light,g_light in zip(R_TREE_LIGHTS_CH, G_TREE_LIGHTS_CH):
        r_fader = RandomBreath(r_light, 10, 165)
        g_fader = CopyFader(g_light, r_fader, 0.5)
        faders.append(r_fader, g_fader)

    wrapper = ClientWrapper()
    while True:
        controller = DMXUpdater(UNIVERSE, UPDATE_INTERVAL, wrapper, faders, FINISH_TIME/UPDATE_INTERVAL)
        wrapper.Run()

    print "Done"
