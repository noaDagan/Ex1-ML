import math
import numpy as np
import scipy.io as sio
from scipy.spatial import distance
import matplotlib.pyplot as plt
from init_centroids import init_centroids
from scipy.misc import imread

# print function
def print_cent(cent):
    if type(cent) == list:
        cent = np.asarray(cent)
    if len(cent.shape) == 1:
        return ' '.join(str(np.floor(100*cent)/100).split()).replace('[ ', '[').replace('\n', ' ').replace(' ]',']').replace(' ', ', ')
    else:
        return ' '.join(str(np.floor(100*cent)/100).split()).replace('[ ', '[').replace('\n', ' ').replace(' ]',']').replace(' ', ', ')[1:-1]

# The function return the average of all the 3 color
def findAvg(A_norm, c, centroidArr):
    red = 0
    blue = 0
    green = 0
    count = 0
    avgColor = [0, 0, 0]
    lenA = len(A_norm)
    # run over all the pixle and calculate the average of the 3 color
    for pHeight in range(lenA):
        for pWidth in range(lenA):
            if (centroidArr[pHeight][pWidth] == c):
                red += A_norm[pHeight][pWidth][0]
                blue += A_norm[pHeight][pWidth][1]
                green += A_norm[pHeight][pWidth][2]
                count = count + 1
    # div by zero, calculate the the average of all one
    # return arr[3]
    if (count != 0):
        avgColor[0] = red / count
        avgColor[1] = blue / count
        avgColor[2] = green / count
    return avgColor


# function find min of centroid and return the index
def findMin(temp):
    lenOfArr = len(temp)
    min = temp[0]
    index = 0
    for i in range(lenOfArr):
        if (temp[i] <= min):
            min = temp[i]
            index = i
    return index

def createImgByK(k):
    # data preperation (loading, normalizing, reshaping)
    path = 'dog.jpeg'
    A = imread(path)
    A_norm = A.astype(float) / 255.
    img_size = A_norm.shape
    X = A_norm.reshape(img_size[0] * img_size[1], img_size[2])
    # size of A_norm is 128
    lenA = len(A_norm)
    # centroid arr
    centroid = init_centroids(X, k)
    # initialize the copy arry of index
    centroidArr = [[0] * lenA for i in range(lenA)]
    lenCent = len(centroid)
    # run over all the centroid in iteration 0 and print
    print("iter 0 :", end="")
    iter = 0
    for indK in centroid:
        print(print_cent(indK), end = "")
        if (iter < lenCent - 1):
            print(", ", end="")
            iter += 1
    print("")
    # run over all the pixle with 10 iteration
    for i in range(10):
        for pHeight in range(lenA):
            for pWidth in range(lenA):
                temp = []
                for l in range(lenCent):
                    temp.append(0)
                for kIndex in range(lenCent):
                    temp[kIndex] = distance.euclidean(A_norm[pHeight][pWidth], centroid[kIndex])
                centroidArr[pHeight][pWidth] = findMin(temp)
        print("iter", i + 1, ":", end="")
        # run over all the centroid and update them
        for c in range(len(centroid)):
            centroid[c] = findAvg(A_norm, c, centroidArr)
        # run over all the centroid in all the iteration and print
        iter = 0
        for num in centroid:
            print(print_cent(num), end = "")
            if (iter < lenCent - 1):
                print(", ",end = "")
                iter += 1
        print("")
    # run over all the pixle in A_norm and update
    for a in range(lenA):
        for b in range(lenA):
            A_norm[a][b] = centroid[centroidArr[a][b]]

# main function run over the function with k = 2,4,8,16
def main():
    print("k = 2:")
    createImgByK(2)
    print("k = 4:")
    createImgByK(4)
    print("k = 8:")
    createImgByK(8)
    print("k = 16:")
    createImgByK(16)


# call to main function
main()
