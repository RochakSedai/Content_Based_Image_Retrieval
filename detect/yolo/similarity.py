import cv2
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

x1 = cv2.imread("/home/sandeep/Desktop/major/yolo/yolov5/photos/image1.jpg")
x2 = cv2.imread("/home/sandeep/Desktop/major/yolo/yolov5/photos/image1.jpg")

x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2GRAY)
x2 = cv2.cvtColor(x2, cv2.COLOR_BGR2GRAY)
print(x1.shape)
print(x2.shape)

from skimage.transform import resize
x2 = resize(x2, (x1.shape[0], x1.shape[1]), anti_aliasing=True, preserve_range=True)
x1 = resize(x1, (x1.shape[0], x1.shape[1]), anti_aliasing=True, preserve_range=True)

print(x1.shape)
print(x2.shape)
absdiff = cv2.absdiff(x1, x2)
cv2.imwrite("home/sandeep/Desktop/major/yolo/yolov5/photos/imagediff.jpg", absdiff)

diff = cv2.subtract(x1, x2)
result = not np.any(diff)
print("this is ",result)

m = mse(x1, x2)
s = ssim(x1, x2)

print (m,s)
