from PIL import Image
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import sys,os
import PIL.ImageOps  
from skimage import measure
try:
    from skimage import filters
except ImportError:
    from skimage import filter as filters

def count_white(image):
    #counts white value of gray scale image, is it all white?
    im = array(PIL.ImageOps.invert(image).convert('L'))
    
    grayscale_value = 0
    for i in im[0]:
        grayscale_value += i
    return (grayscale_value/len(im[0]))**2

def segment_vertically(filename):
    image = Image.open(filename)
    im = array(image.convert('L'))
    columns = list()
    for i in im:
        for j in range(len(i)):
            try:
                columns[j].append(i[j])
            except IndexError:
                columns.append(list())
                columns[j].append(i[j])
            
    colsums = [sum(x)**2 for x in columns] #colsums contain sums of white values
    colsumsa = array(colsums)
    maximas = argrelextrema(colsumsa, np.greater)
    maximas = [i for i in maximas[0]]
    maximas.insert(0, 0)
    maximas.append(image.width-1)

    out_path = "./%s" % (filename.split(".")[0])
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    os.chdir(out_path)

    for i in range(len(maximas)-1):
        left = maximas[i]
        top = 0
        width = maximas[i+1] - maximas[i]
        height = image.height
        box = (left, top, left+width, top+height)
        area = image.crop(box)
        
        area.save("%s_%s" % (i, filename),"JPEG")
        
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    colnum = list(range(len(colsums)))
    ax.bar(colnum,colsums)
    plt.show()
    
def segment_horizontally(filename):
    # read image to array, convert it to grayscale
    image = Image.open(filename)
    im = array(image.convert('L'))

    ### get sum squared of each line row, higher values are mostly white
    ### will separate this later with either a hardcoded threshold or better
    ### a sigmoid function that will segment the image into rows of text

    ### OPTIONAL FOR NOW: you could also do this horizontally to segment the text lines
    ### into either individual letters or words.

    #get sums of each row (pixel values grayscale)
    rowsums = [sum(x)**2 for x in im] #rowsums contain sums of white values
    rowsumsa = array(rowsums)
    maximas = argrelextrema(rowsumsa, np.greater)
    maximas = [i for i in maximas[0]]
    maximas.insert(0, 0)
    maximas.append(image.height-1)

    out_path = "./%s" % (filename.split(".")[0])
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    os.chdir(out_path)

    save_counter = 0
    for i in range(len(maximas)-1):
        left = 0
        top = maximas[i]
        width = image.width
        height = maximas[i+1] - maximas[i]
        box = (left, top, left+width, top+height)
        area = image.crop(box)
        if count_white(area) <= 20:
            continue
        area.save("%s_%s" % (save_counter, filename),"JPEG")
        save_counter += 1
        
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    rownum = list(range(len(rowsums)))
    ax.bar(rownum,rowsums)
    plt.show()


def segment_letters(nfilename):
    image = Image.open(nfilename)
    inverted_image = PIL.ImageOps.invert(image)
    filename = 'p' + nfilename
    inverted_image.save(filename)
    # Init values
    n = 2
    img = Image.open(filename)
    data = np.array(img)
    xlen = len(data[:,0])
    ylen = len(data[0,:])

    # Finds tha max and min value from the array
    maxv = max(data.flatten())
    minv = min(data.flatten())

    # Data segmentation process
    data = filters.gaussian(data, sigma = 1/n)
    blobs = data > 0.8*(data.mean()) # Also play with this value
    labels = measure.label(blobs)
    setL = set(filter(lambda a : a !=0, labels.flatten()))
    arrLab = []
    lstPath=[]

    # output dir
    out_path = filename.split('.')[0] + "/"
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    # Binarization of the image
    for i in range(1,len(setL),1):
        data2 = labels.astype('uint8')
        data2[data2 != i] = minv
        data2[data2 == i] = maxv
        arrLab.append(data2)

    # Size limit Play with this value
    limit = 100

    # Write the value of the array
    for ik in range(0,len(arrLab),1):
        ev = arrLab[ik]
        flat = list(filter(lambda a:a!=0,ev.flatten()))
        mide = len(flat)

        # If the image is smaller than the size of the image then wirte the image.
        if mide >= limit:
            lout = Image.fromarray(ev)
            lout.save(out_path + "%s_%s.jpg"%(filename, ik))

segment_horizontally("bench2.jpg")
