from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post
from newsapi import NewsApiClient

all_articles = {}

# Create your views here.
def blogHome(request):
    api = NewsApiClient(api_key='91d0b0ff2efb41d18dc3138d8846facb')
    top_headlines = api.get_top_headlines(category='health', country='in')
    articles = top_headlines['articles']
    # print(len(articles))
    for article in  articles:
        all_articles[article['title']] = article
    # print(articles[0])
    allPosts = Post.objects.all()
    
    
    # print(allPosts)
    context = {'allPosts': articles}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    # print(slug)
    article = all_articles[slug]
    context = {'post': article}
    return render(request, 'blog/blogPost.html', context)