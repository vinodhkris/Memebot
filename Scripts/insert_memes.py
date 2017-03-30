#!/usr/bin/python

import sys, getopt
import tesseroc as admitit
import tensorflowretraining as thatguy
from db import MongoObj
import os
import string

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
	maps = {}
	descriptions = []
	actors = []
	image_names = []
	db = MongoObj()
	files = os.listdir(root_directory)
	for filename in files:
		if "jpg" not in filename:
			continue
		admitit.convert_to_greyscale(root_directory,filename)

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
		#get labels from tensorflow
		actor = tf_actors[filename]
		#insert_many in mongoob
		descriptions.append(description)
		actors.append(actor)
		image_names.append(filename)
		print filename,'done. Description:',description
	db.insert_bulk(descriptions,actors,image_names)
	print 'All memes inserted. Vanakkam Mahan.'
		