#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

__author__ = 'otger'


class Relay(object):
    def __init__(self, bcm_out_pin):
        self._pin = bcm_out_pin

        self._setup()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.OUT)

    def enable(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self._pin, GPIO.HIGH)

    def disable(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self._pin, GPIO.LOW)

    def clear(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup(self._pin)


class RelaysArray(object):
    def __init__(self, bcm_pins=[]):
        self._pins = bcm_pins
        self._relays = []
        self._setup()

    def _setup(self):
        self._relays = []
        for r in self._pins:
            if not isinstance(r, int):
                raise Exception('BCM pin must be an integer')
            self._relays.append(Relay(r))

    def enable(self, channel):
        if not isinstance(channel, int):
            raise Exception('Channel must be an integer')
        if channel >= len(self._relays):
            raise Exception("Unknown channel")
        self._relays[channel].enable()

    def disable(self, channel):
        if not isinstance(channel, int):
            raise Exception('Channel must be an integer')
        if channel >= len(self._relays):
            raise Exception("Unknown channel")
        self._relays[channel].disable()

    def clear(self, channel):
        if not isinstance(channel, int):
            raise Exception('Channel must be an integer')
        if channel >= len(self._relays):
            raise Exception("Unknown channel")
        self._relays[channel].clear()
