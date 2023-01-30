import cv2
import numpy as np
from skimage import io
import imutils
import pandas as pd 
import os


# compare similarity of images using SIFT library
def sift_similarity(imageA, imageB):
    # convert both images to size 1000x1000
    imageB = cv2.resize(imageB, (1000, 1000))

    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(imageA, None)
    kp_2, desc_2 = sift.detectAndCompute(imageB, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []
    ratio = 0.75
    for m, n in matches:
        if m.distance < ratio*n.distance:
            good_points.append(m)
            #print(len(good_points))
    result = cv2.drawMatches(imageA, kp_1, imageB, kp_2, good_points, None)

    # Define how similar they are
    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)
    
    match_percentage = len(good_points) / number_keypoints * 100
    # print("Keypoints 1ST Image: " + str(len(kp_1)))
    # print("Keypoints 2ND Image: " + str(len(kp_2)))

    # print("GOOD Matches:", len(good_points))
    # print("How good it's the match: ", len(good_points) / number_keypoints * 100, "%")

    return match_percentage

def check_similar():
    # load the two input images

    imageA = io.imread(r"D:\Major Project on CBIR and Recommendation\CBIR\media\photos\products\shoes.jpg")

    imageA = cv2.resize(imageA, (1000, 1000))
        
    similarities = []

    for filename in os.listdir(r"D:\Major Project on CBIR and Recommendation\CBIR\Json_response_images"):
        if filename.endswith(".jpg"):
            # Read the image
            img = cv2.imread(os.path.join(r"D:\Major Project on CBIR and Recommendation\CBIR\Json_response_images", filename))
            s1 = sift_similarity(imageA, img)
            #print(filename +" "+ str(s1))
            similarities.append((filename, s1))

    # Sort the similarity values in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities


