#!/usr/bin/python

import sys, getopt
import tesseroc as admitit
import tensorflowretraining as thatguy
from db import MongoObj
import os
import string
import re
#import cv
#from PIL import Image

def DetectFace(image, faceCascade, returnImage=False):
    # This function takes a grey scale cv image and finds
    # the patterns defined in the haarcascade function
    # modified from: http://www.lucaamore.com/?p=638

    #variables    
    min_size = (20,20)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0

    # Equalize the histogram
    cv.EqualizeHist(image, image)

    # Detect the faces
    faces = cv.HaarDetectObjects(
            image, faceCascade, cv.CreateMemStorage(0),
            haar_scale, min_neighbors, haar_flags, min_size
        )

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:
            # Convert bounding box to two CvPoints
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 5, 8, 0)

    if returnImage:
        return image
    else:
        return faces

def get_args(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
	except getopt.GetoptError:
		print 'insert_memes.py -i <inputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'insert_memes.py -i <inputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
	
	return inputfile

if __name__ == "__main__":
	root_directory = get_args(sys.argv[1:])
	if root_directory is None or root_directory == '':
		print 'please enter a valid path'
		sys.exit(2)
	if not root_directory.endswith("/"):
		root_directory += "/"
	maps = {}
	descriptions = []
	actors = []
	image_names = []
	db = MongoObj()
	db.clear_db()
	files = os.listdir(root_directory)
	for filename in files:
		if "jpg" not in filename:
			continue
		admitit.convert_to_greyscale(root_directory,filename)
#		faceCascade = cv.Load('/Users/Akshay/Desktop/classifier/meme_bot/opencv.git/branches/2.4/data/haarcascades/haarcascade_frontalface_default.xml')
#		pil_im=Image.open(root_directory + filename)
#       cv_im=pil2cvGrey(pil_im)
#        faces=DetectFace(cv_im,faceCascade)
#        if faces:
#            n=1
#            for face in faces:
#                croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
#                fname,ext=os.path.splitext(img)
#                croppedImage.save(root_directory + "faces/" + fname+'_crop'+str(n)+ext)
#                n+=1
#        else:
#            print 'No faces found:', img


	#Run tensorflow on all images directly
	tf_actors = thatguy.run_inference_on_images(root_directory)
	print 'Finished running tf on all images'
	for filename in os.listdir(root_directory):
		if "jpg" not in filename:
			continue
		#run tesseract
		description = admitit.get_text(root_directory,filename)
		description = description.strip()
		description = out = "".join(c for c in description if c not in ('!','.',':',',',"'"))
		description = description.lower().replace('\n',' ')

		non_grayscale_filename = re.sub('\_grayscale$','', filename)
		
		#insert_many in mongoob
	    #get labels from tensorflow
		actor = tf_actors[filename]
		#do not insert multiple entries for grayscale versions of same file. Just append to the existing entry
		if non_grayscale_filename in image_names:
			index = image_names.index(non_grayscale_filename)
			descriptions[index].append(description)
		else:
			descriptions.append(description)

		if 'grayscale' not in filename:
			actors.append(actor)
			image_names.append(non_grayscale_filename)
		else:
			os.remove(root_directory + filename)


		print filename,'done. Description:',description
	db.insert_bulk(descriptions,actors,image_names)
	print 'All memes inserted. Vanakkam Mahan.'
		