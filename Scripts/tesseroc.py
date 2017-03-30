import tesserocr
from PIL import Image
import os
import cv2

def convert_to_greyscale(directory,filename):
	print directory,filename
	img = cv2.imread( directory+"/"+filename )
	img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
	cv2.imwrite( directory+"/"+filename.split(".jpg")[0]+"_grayscale.jpg", img )

def text_bounding(directory,file_name ):
    img  = cv2.imread(directory+"/"+file_name)

    #img_final = cv2.imread(file_name)
    img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray , img2gray , mask =  mask)
    ret, new_img = cv2.threshold(image_final, 180 , 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    '''
            line  8 to 12  : Remove noisy portion 
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3 , 3)) # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more 
    dilated = cv2.dilate(new_img,kernel,iterations = 9) # dilate , more the iteration more the dilation

    _, contours, _ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
    index = 0 
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        #Don't plot small false positives that aren't text
        if w < 35 and h<35:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)

        '''
        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = img_final[y :y +  h , x : x + w]

        s = file_name + '/crop_' + str(index) + '.jpg' 
        cv2.imwrite(s , cropped)
        index = index + 1

        '''
    # write original image with added contours to disk  
    cv2.imwrite(directory+"/"+file_name, img)

def get_text(directory,filename):
	image = Image.open(directory+"/"+filename)
	return tesserocr.image_to_text(image) 


if __name__ == "__main__":
	root_directory = "/Users/vinodhkris/Desktop/Pet_Projects/Memer/actors/"
	actors = ["training"]
	for actor in actors:
		directory = root_directory + actor
        files = os.listdir(directory)
        for filename in files:
            convert_to_greyscale(directory,filename)

        for filename in os.listdir(directory):
			if "jpg" not in filename:
				continue
			key = actor + ":"+filename
			image = Image.open(directory+"/"+filename)
			print tesserocr.image_to_text(image) 
