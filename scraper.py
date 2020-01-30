from multiprocessing import Process, Manager
from datetime import datetime
from bs4 import BeautifulSoup
import argparse
import requests
import sys
import re

SITE_URL = 'https://old.reddit.com/'
REQUEST_AGENT = 'Mozilla/5.0 Chrome/47.0.2526.106 Safari/537.36'


def createSoup(url):
    return BeautifulSoup(requests.get(url, headers={'User-Agent':REQUEST_AGENT}).text, 'lxml')

def getSearchResults(searchUrl):
    posts = []
    while True:
        resultPage = createSoup(searchUrl)
        posts += resultPage.findAll('div', {'class':'search-result-link'})
        footer = resultPage.findAll('a', {'rel':'nofollow next'})
        if footer:
            searchUrl = footer[-1]['href']
        else:
            return posts

def parseComments(commentsUrl):
    commentTree = {}
    commentsPage = createSoup(commentsUrl)
    commentsDiv = commentsPage.find('div', {'class':'sitetable nestedlisting'})
    comments = commentsDiv.findAll('div', {'data-type':'comment'})
    for comment in comments:
        numReplies = int(comment['data-replies'])
        tagline = comment.find('p', {'class':'tagline'})
        author = tagline.find('a', {'class':'author'})
        author = "[deleted]" if author == None else author.text
        commentId = comment.find('p', {'class':'parent'}).find('a')['name']
        content = comment.find('div', {'class':'md'}).text.replace('\n','')
        parent = comment.find('a', {'data-event-action':'parent'})
        parentId = parent['href'][1:] if parent != None else '       '
        parentId = '       ' if parentId == commentId else parentId
        print(commentId, 'reply-to:', parentId, 'num-replies:', numReplies, content[:63])
        commentTree[commentId] = {'author':author, 'reply-to':parentId, 'text':content, 'num-replies':numReplies}
        return commentTree
        
    

def parsePost(post, results, user):
    title = post.find('a', {'class':'search-title'}).text
    author = post.find('a', {'class':'author'}).text
    subreddit = post.find('a', {'class':'search-subreddit-link'}).text
    commentsTag = post.find('a', {'class':'search-comments'})
    url = commentsTag['href']
    numComments = int(re.match(r'\d+', commentsTag.text).group(0))
    if user!=None:
        print('\n',':',numComments,user,subreddit,title)
        author = user
    else:
        print('\n' + ':', numComments, author, subreddit, title)
    commentTree = {} if numComments == 0 else parseComments(url)
    results.append({'title':title, 'author':author, 'subreddit':subreddit, 'comments':commentTree})


def returnResults(searchUrl,keyword,subreddit,user):
    sys.setrecursionlimit(10000)
    product = {}
    posts = getSearchResults(searchUrl)
    product[keyword] = {}
    product[keyword]['subreddit'] = 'all' if subreddit == None else subreddit
    results = Manager().list()
    jobs = []
    for post in posts:
        job = Process(target=parsePost, args=(post, results, user))
        jobs.append(job)
        job.start()
    for job in jobs:
        job.join()
    product[keyword]['posts'] = list(results)
    postList = product[keyword]['posts']
    return postList    
