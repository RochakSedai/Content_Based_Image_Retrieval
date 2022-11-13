import pandas as pd
import numpy as np
from textblob import TextBlob
import re
import urllib.request
from PIL import Image

def cleantxt(text):
    text = re.sub(r'@[A-Za-z0-9]+','',text) # Remove mentions
    text = re.sub(r'#','',text) # Remove #
    text = re.sub(r'RT[\s]+','',text) # Remove RTs
    text = re.sub(r'https?:\/\/\S+','',text) # Remove hyperlink
    text = re.sub(r'\n','',text)  # remove \n
    return text
    # Clean the text
    

def getPolarity(text):
    return TextBlob(text).sentiment.polarity
# JSON file

def get_responses(responses):
    # Get Combined review and rating for a product from different comments
    #responses= [{'product_name': 'Goldstar black sports shoes', 'description': 'very very good product', 'price': 1699, 'images': 'http://shoeasy.me/media/photos/products/Goldstar_Black___Grey_Sports_Shoes_For_Men___G10_G305.jpg', 'category': {'category_name': 'Sports'}, 'reviews': ['Very nice product but delivery time was very slow , 3.50', 'bad product late delivery , 0.50']}, {'product_name': 'Goldstar Black Sports Shoe G11', 'description': 'Goldstar Black Sports Shoe G11', 'price': 1299, 'images': 'http://shoeasy.me/media/photos/products/Goldstar_Black_Sports_Shoes_For_Men_-_G10_G902.jpg', 'category': {'category_name': 'Sports'}, 'reviews': ['Good Product , 4.50', 'It doesnot fit on my foot and color goes after washing , 1.50']}, {'product_name': 'GoldStar Black Sports Shoe G766', 'description': 'GoldStar Black Sports Shoe G766', 'price': 1599, 'images': 'http://shoeasy.me/media/photos/products/Goldstar_Shoes_For_Men_G10_701_Black_Goldstar_Sports_Shoe.jpg', 'category': {'category_name': 'Sports'}, 'reviews': ['Good product durable but seller response was slow , 3.50', 'Nice product , 5.00']}]
    #responses= [{'product_name': 'Goldstar black sports shoes', 'description': 'very very good product', 'price': 1699, 'images': 'http://shoeasy.me/media/photos/products/Goldstar_Black___Grey_Sports_Shoes_For_Men___G10_G305.jpg', 'category': {'category_name': 'Sports'}, 'reviews': ['Very nice product but delivery time was very slow , 3.50', 'bad product late delivery , 0.50']}, {'product_name': 'Goldstar Black Sports Shoe G11', 'description': 'Goldstar Black Sports Shoe G11', 'price': 1299, 'images': 'http://shoeasy.me/media/photos/products/Goldstar_Black_Sports_Shoes_For_Men_-_G10_G902.jpg', 'category': {'category_name': 'Sports'}, 'reviews': ['Good Product , 4.50', 'It doesnot fit on my foot and color goes after washing , 1.50']}, {'product_name': 'GoldStar Black Sports Shoe G766', 'description': 'GoldStar Black Sports Shoe G766', 'price': 1599, 'images': 'http://shoeasy.me/media/photos/products/Goldstar_Shoes_For_Men_G10_701_Black_Goldstar_Sports_Shoe.jpg', 'category': {'category_name': 'Sports'}, 'reviews': ['Good product durable but seller response was slow , 3.50', 'Nice product , 5.00']}]
    print(responses)
    
    overall_review,overall_rating = [],[]
    l = len(responses)
    df = pd.DataFrame(columns=['product_name','description','price','images','category','review','rating'])
    for i in range(l):
        rating, review = [], []
        x = len(responses[i]['reviews'])
        for j in range(x):
            rating.append(responses[i]['reviews'][j].split('~$')[1])
            review.append(responses[i]['reviews'][j].split('~$')[0])
        p = len(rating)
        ints = [float(item) for item in rating]
        mean_rating = sum(ints)/p
        overall_rating.append(mean_rating)

        ans = ' '
        for t in review:

            ans = ans+ ' '+ t
        overall_review.append(ans)

    # Create a new column with the results

    df = pd.DataFrame(responses)
    df['Rating'] = overall_rating
    df['Review'] = overall_review
    df.drop('reviews',axis=1,inplace=True)
    df['Review'] = df['Review'].apply(cleantxt)

    # Create a function to get the polarity
    

    # max price for shoes
    fixed_max = 20000

    df['Score'] = df.Review.apply(getPolarity)
    df['Normalized_Price'] = (fixed_max - df['price'])/fixed_max
    df['Overall_Score'] = df['Score']*0.4 + df['Rating']*0.2 + df['Normalized_Price']*0.4
    df.sort_values(by=['Overall_Score'], inplace=True, ascending=False)
    #print(df)
    return df['product_name']

    
