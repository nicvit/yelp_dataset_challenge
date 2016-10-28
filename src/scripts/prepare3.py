#!/usr/bin/env python
# a stacked bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

data = [[1, 2, 15, 1], [2, 5, 18, 2], [3, 2, 10, 2], [4, 2, 8, 6], [5, 3, 10, 3], [6, 3, 8, 12], [7, 5, 7, 5], [8, 2, 12, 6], [9, 5, 15, 3], [10, 3, 7, 4], [11, 3, 9, 2], [12, 5, 6, 5], [13, 3, 8, 5], [14, 5, 7, 2], [15, 1, 5, 7], [16, 3, 11, 9], [17, 1, 7, 3], [18, 1, 4, 6], [19, 4, 7, 7], [20, 4, 8, 6], [21, 0, 6, 5], [22, 2, 5, 4], [23, 1, 3, 2], [24, 1, 4, 5], [25, 2, 6, 2], [26, 4, 9, 8], [27, 1, 7, 3], [28, 3, 4, 7], [29, 4, 4, 3], [30, 1, 8, 5], [31, 3, 8, 2], [32, 8, 10, 4], [33, 3, 7, 5], [34, 1, 2, 7], [35, 3, 3, 6], [36, 1, 0, 3], [37, 0, 4, 5], [38, 4, 6, 8], [39, 1, 8, 9], [40, 2, 6, 3], [41, 4, 9, 3], [42, 4, 8, 3], [43, 1, 12, 8], [44, 4, 12, 2], [45, 6, 14, 5], [46, 5, 5, 3], [47, 4, 13, 7], [48, 1, 4, 10], [49, 0, 7, 10], [50, 1, 6, 4], [51, 1, 11, 10], [52, 4, 10, 6], [53, 5, 7, 5], [54, 3, 5, 4], [55, 2, 4, 10], [56, 4, 13, 11], [57, 1, 13, 14], [58, 4, 6, 6], [59, 6, 9, 6], [60, 5, 9, 8], [61, 2, 7, 2], [62, 3, 3, 0]]

data = data[0:5]
N = len(data)

print data

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

"""

Data Schema:

[[Month #, #negatives, #neutrals, #positives],
...]

"""


months = []

negatives = []
neutrals = []
positives = []

for i in data:
	months.append(i[0])
	negatives.append(i[1])
	neutrals.append(i[2])
	positives.append(i[3])



ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, negatives, width, color='r')
p2 = plt.bar(ind, neutrals, width, color='w', bottom=negatives)
p2 = plt.bar(ind, positives, width, color='g', bottom=negatives+neutrals)

plt.ylabel('Review Number')
plt.title('Review Statistics')
#plt.xticks(ind + width/2., ('G1', 'G2', 'G3', 'G4', 'G5'))
#plt.yticks(np.arange(0, 81, 10))
#plt.legend((p1[0], p2[0]), ('Men', 'Women'))

plt.show()

