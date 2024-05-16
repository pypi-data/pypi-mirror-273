"""!@package base
Abstract base classes for Juham IoT based home automation framework. 

This package represents the most low level layer in the framework. 
Most notably, it defines two essential abstractions on which communcation 
between various IoT nodes and the data tracking is based on:

1. jmqtt - publish-subscriber model data transmission 

2. jdatabase - interface to time series database used for data recording

3. jobject - base class of everything, from which all the objects in
the framework are derived.

"""

