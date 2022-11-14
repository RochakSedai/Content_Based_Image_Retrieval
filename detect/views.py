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

# Create your views here.
def home(request):
    return render(request, 'home.html')

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
            return redirect("success")
    return render(request, "home.html", {"form": form}) 

def successView(request):
    return HttpResponse("Success! Thank you for your message.")