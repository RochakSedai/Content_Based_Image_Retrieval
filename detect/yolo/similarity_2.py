import cv2
import glob
import os
from os import listdir
import pandas as pd


import numpy as np
from skimage.metrics import structural_similarity as ssim


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err

def diff_remove_bg(img0, img, img1):
    d1 = diff(img0, img)
    d2 = diff(img, img1)
    return cv2.bitwise_and(d1, d2)

x1 = cv2.imread("/home/sandeep/Desktop/jutta_2.jpg")
#x2 = cv2.imread("/home/sandeep/Desktop/major/yolo/yolov5/photos/image1.jpg")
img_name=[]
img=[]
folder_dir = "/home/sandeep/Desktop/major/color/images/Grey"
for images in os.listdir(folder_dir):
    # check if the image ends with png
    if (images.endswith(".jpg")):
        img_name.append(images)
        m_path="/"+f"home/sandeep/Desktop/major/color/images/Grey/{images}"
        im=cv2.imread(m_path)
        img.append(im)
#images = [cv2.imread(file) for file in glob.glob("/home/sandeep/Desktop/major/color/images/Black/*.jpg")]
#print("image type is ",type(images))
#print(len(images))
m_lst=[]
s_lst=[]

x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2GRAY)
for i in range(len(img)):
    x2=img[i]
    x2 = cv2.cvtColor(x2, cv2.COLOR_BGR2GRAY)


    from skimage.transform import resize
    x2 = resize(x2, (x1.shape[0], x1.shape[1]), anti_aliasing=True, preserve_range=True)
    x1 = resize(x1, (x1.shape[0], x1.shape[1]), anti_aliasing=True, preserve_range=True)

    #print(x1.shape)
    #print(x2.shape)
    absdiff = cv2.absdiff(x1, x2)
    cv2.imwrite("home/sandeep/Desktop/major/yolo/yolov5/photos/imagediff.jpg", absdiff)

    diff = cv2.subtract(x1, x2)
    result = not np.any(diff)
    print("this is ",result)

    m = mse(x1, x2)
    m_lst.append(m)
    s = ssim(x1, x2)
    s_lst.append(s)

    print ("This is final result",i,m,s)

a= pd.Series(m_lst).idxmin()
b= pd.Series(s_lst).idxmax()
print(img_name[a],m_lst[a])
print(img_name[b],s_lst[b])

# get the path/directory


