#!/usr/bin/python

import sys, getopt
import tesseroc as admitit
import tensorflowretraining as thatguy
from db import MongoObj
import os
import string
import re
import cv2
import numpy as np
#import cv
#from PIL import Image

def DetectFace(image, faceCascade, returnImage=False):
    # Detect the faces
    faces = faceCascade.detectMultiScale(image, 1.3, 5)
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
	file_maps = {}      #will contain all info for a file name
	db = MongoObj()
	#db.clear_db()
	#create cropped and grayscale images
	files = os.listdir(root_directory)
	for filename in files:
		if "jpg" not in filename:
			continue
		im1 = admitit.convert_to_greyscale(root_directory,filename)
		faceCascade = cv2.CascadeClassifier('/Users/vinodhkris/Desktop/Pet_Projects/Memebot/Scripts/faceDetection/haarcascade_frontalface_default.xml')
        faces=DetectFace(im1,faceCascade)
        n = 0 
        for (x,y,w,h) in faces:
            crop_img = im1[y:y+h, x:x+w] # Crop from x, y, w, h -> 100, 200, 300, 400
            cv2.imwrite( root_directory+"/"+filename.split(".jpg")[0]+"_crop"+str(n)+".jpg", crop_img )
            n+=1

	#Run tensorflow on all images directly
	tf_actors = thatguy.run_inference_on_images(root_directory)
	print 'Finished running tf on all images'
	files = os.listdir(root_directory)
	#get all descriptions and actors for images
	for filename in files:
		if "jpg" not in filename:
			continue
		#run tesseract
		description = admitit.get_text(root_directory,filename)
		description = description.strip()
		description = out = "".join(c for c in description if c not in ('!','.',':',',',"'"))
		description = description.lower().replace('\n',' ')
		#insert_many in mongoob
	    #get labels from tensorflow
		actor = tf_actors[filename]
		#do not insert multiple entries 
		#for grayscale versions of same file. Just append to the existing entry
		f = filename.replace("_grayscale","").replace("_crop\d","")
		if f in file_maps:
			file_maps[f]["actor"] = file_maps[f]["actor"] +" "+actor
			file_maps[f]["description"] = file_maps[f]["description"] +" "+description
		else:
			file_maps[f] = {}
			file_maps[f]["actor"] = actor
			file_maps[f]["description"] = description

		if 'grayscale' in filename or "crop" in filename:
			os.remove(root_directory + filename)

		print filename,'done. Description:',description

	descriptions = []
	actors = []
	image_names = []
	#update the lists to be inserted
	for filename in file_maps:
		image_names.append(filename)
		actors.append(file_maps[filename]["actor"])
		descriptions.append(file_maps[filename]["description"])

	db.insert_bulk(descriptions,actors,image_names)
	print 'All memes inserted. Vanakkam Mahan.'
		
