import requests

with open('token.txt') as file:
    APP_ACCESS_TOKEN = file.read()

BASE_URL = 'https://api.instagram.com/v1/'

'''Function declaration to get your own info '''


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

self_info()
