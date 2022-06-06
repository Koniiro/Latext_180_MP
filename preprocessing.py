from PIL import Image
from pylab import *
import matplotlib.pyplot as plt
# read image to array, convert it to grayscale
im = array(Image.open('bench.jpg').convert('L'))

### get sum squared of each line row, higher values are mostly white
### will separate this later with either a hardcoded threshold or better
### a sigmoid function that will segment the image into rows of text

### OPTIONAL FOR NOW: you could also do this horizontally to segment the text lines
### into either individual letters or words.

#get sums of each row (pixel values grayscale)
rowsums = [sum(x)**2 for x in im]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
rownum = list(range(len(rowsums)))
ax.bar(rownum,rowsums)
plt.show()
