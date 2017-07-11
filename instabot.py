import requests, urllib
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import simplejson

'''This program uses Instagram API to handle accounts'''

# Token Owner: gaur_abhishek
# Insta Users: vivek3273, vivekkumarsingh3075, streethustler_1, vikas__mittal

'''For security reasons, the Access Token is stored on the local machine'''

with open('token.txt') as file:
    APP_ACCESS_TOKEN = file.read()

BASE_URL = 'https://api.instagram.com/v1/'

# The main menu of the application

main_menu = ['Welcome to your main menu. Here are your options',
                 '1. My details',
                 '2. Details of other users',
                 '3. My recent post',
                 '4. Post I Liked',
                 '5. Recent post of other users',
                 '6. Like a post',
                 "7. Get list of people who've liked a post",
                 '8. Comment on a post',
                 '9. Get list of comment(s) on a post',
                 '10. Hashtag Analysis on matplotlib',
                 '11. Create WordCloud',
                 '12. Exit']

hashtag_counts = []
wordcloud_data = []

# Function to get the details of the token owner


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % APP_ACCESS_TOKEN
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function to get user id of the sandbox users


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

# Function to get details of the token owner


def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

# Function to download a post on the local machine


def download_post(request_url):
    media = requests.get(request_url).json()

    if media['meta']['code'] == 200:
        if len(media['data']):

            # To check if the media is image or not
            if media['data'][0]['type'] == 'image':
                image_name = media['data'][0]['id'] + '.jpeg'
                image_url = media['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print 'The post  has been downloaded!'

            # To check if the media is a video or not
            elif media['data'][0]['type'] == 'video':
                video_name = media['data'][0]['id'] + '.mp4'
                video_url = media['data'][0]['videos']['standard_resolution']['url']
                urllib.urlretrieve(video_url, video_name)
                print 'The post has been downloaded'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function to get the latest post of the token owner


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % APP_ACCESS_TOKEN
    download_post(request_url)

# Function to get the latest post of the sandbox users


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    download_post(request_url)

# Function to get the post id of the media


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

# Function to like a post


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % media_id
    payload = {"access_token": APP_ACCESS_TOKEN}
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

# Function to post a comment


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % media_id

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

# Function to get the list of comments on a post


def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    comment_list = requests.get(request_url).json()
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print 'The comment(s) are'
            for i in range(0, len(comment_list['data'])):
                print comment_list['data'][i]['text']

# Function to get the list of people who've liked the post


def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    like_list = requests.get(request_url).json()
    if like_list['meta']['code'] == 200:
        if len(like_list['data']):
            print 'This post is liked by'
            for i in range(0, len(like_list['data'])):
                print like_list['data'][i]['username']

# Function to get the post liked by the token owner


def get_liked_post():
    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % APP_ACCESS_TOKEN
    download_post(request_url)

# To get hashtags from user and plot them on matplotlib


def get_hashtags(hashtag_number):
    i = 1
    while i <= hashtag_number:
        i = i + 1
        tag_name = raw_input('Enter the tag you want to search for:\n'
                             "No need to put '#'. Just enter the keyword\n")
        request_url = (BASE_URL + 'tags/search?q=%s&access_token=%s') % (tag_name, APP_ACCESS_TOKEN)
        tag_list = requests.get(request_url).json()
        count = tag_list['data'][0]['media_count']
        hashtag_counts.append(count)
        print hashtag_counts
        plt.plot([i-1], [count], 'gs')
        plt.axis([0, hashtag_number + 1, 0, 200000000])
    else:
        plt.show()

# To create a wordcloud based on a user's data


def get_wordcloud(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    text = requests.get(request_url).json()
    for i in range(0, len(text['data'])):
        wordcloud_data.append(text['data'][i]['text'])
    f = open('raw_data.txt', 'w')
    simplejson.dump(wordcloud_data, f)
    with open('raw_data.txt') as file:
        string = file.read()
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white',width=1200, height=1000).generate(string)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

menu_functions = [self_info, get_user_info, get_own_post, get_liked_post, get_user_post, like_a_post,
                    get_like_list, post_a_comment, get_comment_list, get_hashtags,get_wordcloud, exit]

accepted_values = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

# Function to start the bot


def start_bot():
    while True:
        for elem in main_menu:
            print elem

        select_from_menu = int(raw_input('What do you want to do ?\n'
                                         'Please enter a value from (1-11)\n'))

        while select_from_menu not in accepted_values:
            print 'Invalid Input'
            select_from_menu = int(raw_input('What do you want to do ?\n'
                                         'Please enter a value from (1-11)\n'))

        get_menu_option = select_from_menu - 1
        if get_menu_option == 0 or get_menu_option == 3 or get_menu_option == 11:
            menu_functions[get_menu_option]()

        elif get_menu_option == 9:
            hashtag_number = int(raw_input('Enter the number of hashtags you want to analyze'))
            menu_functions[get_menu_option](hashtag_number)
        else:
            insta_username = raw_input('Enter the name of user\n')
            menu_functions[get_menu_option](insta_username)

start_bot()