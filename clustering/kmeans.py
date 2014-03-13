from PIL import Image
import numpy
import math

#Open the two images and import them into numpy arrays
in_image = Image.open("mandrill-small.tiff")
in_large = Image.open("mandrill-large.tiff")
A = numpy.asarray(in_image).astype(float)
A_large = numpy.asarray(in_large)

#This function calculates the Euclidean distance given an 
#RGB array and the cluster center
def euclid(pixel, mi):
    return math.sqrt((float(pixel[0]) - float(mi[0]))**2 + (float(pixel[1]) - float(mi[1]))**2 + (float(pixel[2]) - float(mi[2]))**2)

#This function takes a pixel and the list of cluster centers 
#and returns the index of the cluster with the smallest
#Euclidean distance from the pixel
def nearest_cluster(pixel, m):
    distance = -1
    index = 0
    for i,mi in enumerate(m):
    	d = euclid(pixel, mi)
	if distance < 0 or d < distance:
	    distance = d
	    index = i
    return index

#This function creates the new cluster center by
#computing the average RGB values of the pixels
#added to the cluster
def pixel_average(pixels):
    l = len(pixels)
    total = numpy.sum(pixels, axis=0)
    return numpy.true_divide(total, l)

def main():
    m = []
    global A_large
    #Create the array which will store the RGB values for the 
    #compressed image    
    output_array = numpy.zeros(A_large.shape, dtype=numpy.uint8)
    #First we create the initial cluster centers by taking 16
    #random pixels from the input image    
    for i in range(16):
    	m.append(A[tuple(numpy.random.random_integers(0,127,2).tolist()[0:2])])
    #Run through 30 times
    for j in range(30):
	C = [[] for i in range(16)]
        #For each pixel, add to its nearest cluster	
	for x in range(A.shape[0]):
	 for y in range(A.shape[1]):
	    index = nearest_cluster(A[x][y], m)
	    C[index].append(A[x][y])
	#Compute the new cluster centers
    	for i,value in enumerate(m):
	    m[i] = pixel_average(C[i])
    #Set each pixel in the output array to the value
    #of its nearest cluster center
    for x in range(A_large.shape[0]):
    	for y in range(A_large.shape[1]):
	    index = nearest_cluster(A_large[x][y], m)
	    output_array[x][y] = m[index].astype(numpy.uint8)
    out_image = Image.fromarray(output_array, "RGB")
    out_image.save("output-mandrill.tiff")

if __name__ == "__main__":
	main()
