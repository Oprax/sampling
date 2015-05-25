#!/usr/bin/env python3
# coding: utf-8

from sampling import Sampling

fluct = Sampling()
print(fluct.intervalFluctuation(10000, 1/1000))
print(fluct.valideSample(15, 10000, 1/1000))

print(fluct.intervalEstimate(22, 100))
print(fluct.intervalEstimate(22, 100, strict=True))

print('====================================')

fluct = Sampling(precision=15)
print(fluct.intervalFluctuation(10000, 1/1000))
print(fluct.valideSample(15, 10000, 1/1000))

print(fluct.intervalEstimate(22, 100))
print(fluct.intervalEstimate(22, 100, strict=True))
