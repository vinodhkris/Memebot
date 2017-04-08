#downloads images for training set and augments it with crops of the face and grayscale images.
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json
import cv2
import numpy as np
import sys
#import cv
#from PIL import Image

def DetectFace(image, faceCascade, returnImage=False):
    # Detect the faces
    faces = faceCascade.detectMultiScale(image, 1.3, 5)
    if returnImage:
        return image
    else:
        return faces

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def convert_to_greyscale(directory,filename):
    img = cv2.imread( directory+"/"+filename )
    img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
    cv2.imwrite( directory+"/"+filename.split(".jpg")[0]+"_grayscale.jpg", img )
    return img

def create_other_images(directory):
    files = os.listdir(directory)
    pathname = os.path.dirname(sys.argv[0])  
    faceCascade = cv2.CascadeClassifier(pathname+'/faceDetection/haarcascade_frontalface_default.xml')
    for filename in files:
        if "jpg" not in filename:
            continue
        im1 = convert_to_greyscale(root_directory,filename)
        faces= DetectFace(im1,faceCascade)
        n = 0 
        for (x,y,w,h) in faces:
            crop_img = im1[y:y+h, x:x+w] # Crop from x, y, w, h -> 100, 200, 300, 400
            cv2.imwrite( root_directory+"/"+filename.split(".jpg")[0]+"_crop"+str(n)+".jpg", crop_img )
            n+=1
    print 'Created grayscale and face cropped images.'

def download_images(actors,root_directory):
    if len(actors) == 0:
        print 'Please provide a comma seperated list of actors you wish to create the training set for (like ajith, sivakarthikeyan, ...).'
    for actor in actors:
        url="https://www.google.co.in/search?q="+actor+"&source=lnms&tbm=isch"
        DIR=root_directory
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = get_soup(url,header)
        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))

        print 'Downloading',len(ActualImages),'from',url,'to',root_directory+actor

        #Creating folders
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        DIR = os.path.join(DIR, actor.split()[0])
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        ###print images
        for i , (img , Type) in enumerate( ActualImages):
            try:
                req = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(req).read()

                cntr = len([i for i in os.listdir(DIR)]) + 1
                if len(Type)==0:
                    f = open(os.path.join(DIR , str(cntr)+".jpg"), 'wb')
                else :
                    f = open(os.path.join(DIR , str(cntr)+"."+Type), 'wb')
                f.write(raw_img)
                f.close()
            except Exception as e:
                print "could not load : "+img
                print e

        ###Convert to grayscale
        create_other_images(DIR)
        print 'Finished training set creation for '+actor

if __name__ == "__main__":
    actors = []
    #get root_directory
    root_directory = get_args(sys.argv[1:])
    if root_directory is None or root_directory == '':
        print 'please enter a valid path. usage: python image_dowloader.py -i <root_directory>'
        sys.exit(2)
    if not root_directory.endswith("/"):
        root_directory += "/"

    #get actors
    query = raw_input("Enter your comma separated actor list: ") # you can change the query for the image  here
    query= query.split(',')
    for arg in query:
        arg = arg.strip()
        args = arg.split()
        actors.append('+'.join(args))

    #create training set
    download_images(actors,root_directory)
   