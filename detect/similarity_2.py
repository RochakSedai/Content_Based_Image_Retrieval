import cv2
import glob
import os
from os import listdir
import pandas as pd
import numpy as np
from skimage.metrics import structural_similarity as ssim
from copy import deepcopy
from skimage.transform import resize

def mse(imageA, imageB):
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

# def diff_remove_bg(img0, img, img1):
#     d1 = diff(img0, img)
#     d2 = diff(img, img1)
#     return cv2.bitwise_and(d1, d2)


def check_similar(img_lst):

   
    img_lst=deepcopy(img_lst)
    x1 = cv2.imread("media\photos\products\shoes.jpg")
    x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2GRAY) 
    print("this is inside check",img_lst)
    
    #folder_dir = "Json_response_images"
    mse_lst=[]
    ssim_lst=[]
    for i in img_lst:
        print("this is i",i)
        x2 = cv2.imread(f"Json_response_images\{i}")
        print("this is image",f"Json_response_images\{i}")
        x2 = cv2.cvtColor(x2, cv2.COLOR_BGR2GRAY)
        x2 = resize(x2, (x1.shape[0], x1.shape[1]), anti_aliasing=True, preserve_range=True)
        x1 = resize(x1, (x1.shape[0], x1.shape[1]), anti_aliasing=True, preserve_range=True)
        #absdiff = cv2.absdiff(x1, x2)
        diff = cv2.subtract(x1, x2)
        result = not np.any(diff)
        print("this is ",result)

        m = mse(x1, x2)
        mse_lst.append(m)
        s = ssim(x1, x2)
        ssim_lst.append(s)

        print ("This is final result",result,m,s)

    for i in range(len(ssim_lst)):
        for j in range(i + 1, len(ssim_lst)):

            if ssim_lst[i] < ssim_lst[j]:
                ssim_lst[i], ssim_lst[j] = ssim_lst[j], ssim_lst[i]
                img_lst[i], img_lst[j] = img_lst[j], img_lst[i]

    
    return img_lst


