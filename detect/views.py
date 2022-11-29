from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProductForm, Product
import requests
import urllib
import os
import glob
from .yolo.call2 import calling
from .comment_classifier import get_responses
from .similarity_2 import check_similar
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
import cv2
from PIL import Image
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')


def video_upload(request):
    
    video_capture = cv2.VideoCapture(0)

    # setting up the width and height of the video window
    video_capture.set(3, 640)  # 3 -> width
    video_capture.set(4, 480)  # 4 -> width

    while True:
        ret, img = video_capture.read()


        dir_path = r'D:\Major Project on CBIR and Recommendation\CBIR\media\photos\products'
        basename = 'shoes'
        base_path = os.path.join(dir_path, basename)
        ext = 'jpg'

        n = 0
        if ret:
            cv2.imwrite('{}.{}'.format(base_path, ext), img)

        cv2.imshow('Real time face detection', img)

        
        # we wait for a key to be pressed - press 'ESC' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        
        

    # destroy and release the camera etc
    video_capture.release()
    cv2.destroyAllWindows()

    calling()

    # reading the content of file and again deleting that content from file
    with open(r"D:\Major Project on CBIR and Recommendation\CBIR\test.txt", 'r+') as f:
        keyword=f.readline()
        f.truncate(0)
    print(keyword)

    # getting data from api
    responses = requests.get(f'http://shoeasy.me/shoEasy-api/?search={keyword}').json()
    

    if responses == []:
        keyword = keyword.rsplit(' ', 1)[0]
        keyword = keyword.rsplit(' ', 1)[0]
        responses = requests.get(f'http://shoeasy.me/shoEasy-api/?search={keyword}').json()
       
        if responses == []:
            keyword = keyword.rsplit(' ', 1)[0]
            keyword = keyword.rsplit(' ', 1)[0]
            responses = requests.get(f'http://shoeasy.me/shoEasy-api/?search={keyword}').json()

    print(responses)

    # review rating analysis
    df_product=list(get_responses(responses))
    img_lst=[]
    for item in df_product:
        img_lst.append(item+".jpg")
    print(img_lst)

    # removing files from directory
    removing_files = glob.glob('Json_response_images\*')
    for i in removing_files:
        os.remove(i)

    # downloading the images in the directory
    for response in responses:
        #print(response)
        name = response['product_name'] 
        print(name)
        url = response['images']
        print(url)
        testImage = urllib.request
        testImage.urlretrieve(url, f'D:\Major Project on CBIR and Recommendation\CBIR\Json_response_images\{name}.jpg')

    # checking the image similarity
    img_lst=check_similar(img_lst)
    print(img_lst)

    for i in range(len(img_lst)):
        for j in range(len(responses)):
            img = os.path.splitext(img_lst[i])[0]
            if responses[j]['product_name'] == img:
                response = responses[i]
                responses[i] = responses[j]
                responses[j] = response

    
    context = {
        'responses': responses,
    }

    return render(request, 'output.html', context)

def upload(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

               
    calling()

    # reading the content of file and again deleting that content from file
    with open(r"D:\Major Project on CBIR and Recommendation\CBIR\test.txt", 'r+') as f:
        keyword=f.readline()
        f.truncate(0)
    print(keyword)

    # getting data from api
    responses = requests.get(f'http://shoeasy.me/shoEasy-api/?search={keyword}').json()
    

    if responses == []:
        keyword = keyword.rsplit(' ', 1)[0]
        keyword = keyword.rsplit(' ', 1)[0] 
        responses = requests.get(f'http://shoeasy.me/shoEasy-api/?search={keyword}').json()
        
       
        if responses == []:
            keyword = keyword.rsplit(' ', 1)[0]
            keyword = keyword.rsplit(' ', 1)[0]
            responses = requests.get(f'http://shoeasy.me/shoEasy-api/?search={keyword}').json()

    print(responses)

    # review rating analysis
    df_product=list(get_responses(responses))
    img_lst=[]
    for item in df_product:
        img_lst.append(item+".jpg")
    print(img_lst)

    # removing files from directory
    removing_files = glob.glob('Json_response_images\*')
    for i in removing_files:
        os.remove(i)

    # downloading the images in the directory
    for response in responses:
        #print(response)
        name = response['product_name'] 
        print(name)
        url = response['images']
        print(url)
        testImage = urllib.request
        testImage.urlretrieve(url, f'D:\Major Project on CBIR and Recommendation\CBIR\Json_response_images\{name}.jpg')

    # checking the image similarity
    img_lst=check_similar(img_lst)
    print(img_lst)

    for i in range(len(img_lst)):
        for j in range(len(responses)):
            img = os.path.splitext(img_lst[i])[0]
            if responses[j]['product_name'] == img:
                response = responses[i]
                responses[i] = responses[j]
                responses[j] = response

    
    context = {
        'responses': responses,
    }

    return render(request, 'output.html', context)
    


def contactView(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            from_name = form.cleaned_data["from_name"]
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ["sedairochak@gmail.com"],)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, 'Success! Thank you for your message.')
            return redirect("success")
    return render(request, "home.html", {"form": form}) 

def successView(request):
    return render(request, 'home.html')
    
    #return HttpResponse("Success! Thank you for your message.")