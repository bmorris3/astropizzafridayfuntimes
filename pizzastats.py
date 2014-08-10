# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:30:16 2014

@author: bmorris
"""

import numpy as np
from matplotlib import pyplot as plt
import datetime
months = range(1,13)

pizzadatafile = open('pizzadata.csv','r').read().splitlines()
dates = []
pizzasordered = []
pizzasleft = []

for i in range(1,len(pizzadatafile)):
    # Parse the dates, written in MM/DD/YY format, make datetime objects
    splitline = pizzadatafile[i].split(',')
    mm, dd, yearminus2000 = map(int,splitline[0].split('/'))
    year = int(2000 + yearminus2000)
    dates.append(datetime.datetime(year, mm, dd))
    
    pizzasordered.append(float(splitline[1]))
    pizzasleft.append(float(splitline[2]))

## Put in chronological order
dateorder = np.argsort(dates)
dates = np.array(dates)[dateorder].tolist()
pizzasordered = np.array(pizzasordered)
pizzasleft = np.array(pizzasleft)
pizzasordered = pizzasordered[dateorder]
pizzasleft = pizzasleft[dateorder]

## Get the month of each recorded order
months = np.array([date.month for date in dates])
ind = range(len(dates))

# Get the monthly medians of the pizzas ordered and pizzas left
median_ordered = np.zeros(12, dtype=float)
median_left = np.zeros(12, dtype=float)
median_ideal = np.zeros(12, dtype=float)
Norderspermonth = np.zeros(12, dtype=float)
for i in range(12):
    month = i + 1
    Norderspermonth[i] = sum(months == month)
    if Norderspermonth[i] > 0:
        median_ordered[i] = np.median(pizzasordered[months == month])
        median_left[i] = np.median(pizzasleft[months == month])
        median_ideal[i] = np.median(pizzasordered[months == month] - pizzasleft[months == month])

fig, ax = plt.subplots(1, 2, figsize=(16, 8))
ax[0].plot(ind, pizzasordered, label='Pies Ordered')
ax[0].plot(ind, pizzasleft, label='Pies Left')
ax[0].plot(ind, pizzasordered-pizzasleft, label='Ideal #')

ax[0].set_title('Pizza Order History')
ax[0].set_xlabel('Historical Order Index')
ax[0].set_ylabel('Number of Pies')

monthrange = range(1,13)
ax[1].plot(monthrange, median_ordered, label='Pies Ordered')
ax[1].plot(monthrange, median_left, label='Pies Left')
ax[1].plot(monthrange, median_ideal, label='Ideal #')
ax[1].plot(monthrange, Norderspermonth/2, label='(# orders)/2')

ax[1].set_title('Monthly Order Medians')
ax[1].set_xlabel('Month')
ax[1].set_ylabel('Number of Pies')
ax[1].set_xticks(monthrange)
ax[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', \
                    'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax[1].set_xlim([0.5, 12.5])
ax[1].legend(numpoints=1, loc='center right')
ax[1].set_ylim([0, 6.5])


### Annotate with the number of orders per month:
#ax[1].set_ylim([0, 7])
#ax[1].annotate('Numer of orders per month:', xy=(0.7, 6.8), \
#            xycoords='data', ha='left',\
#            va='bottom', size=12)
#for i in monthrange:
#    annotation = str(int(Norderspermonth[i-1]))
#    ax[1].annotate(annotation, xy=(i, 6.5), \
#                xycoords='data', ha='center',\
#                va='bottom', size=12)

plt.show()