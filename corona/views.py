from django.shortcuts import render
import requests
import bs4


def get_html_data(url):
    data = requests.get(url)
    return data


def get_country_data(name):
    url = ''
    if name != 'Global':
        url = 'https://www.worldometers.info/coronavirus/country/'+name
    else:
        url = 'https://www.worldometers.info/coronavirus/'
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text,'html.parser')
    
    info_div = bs.find('div',class_='content-inner').findAll("div",id="maincounter-wrap")
    
    all_data = []

    for block in info_div:
        text = block.find('h1',class_=None).get_text()
        count = block.find('span',class_ = None).get_text()

        all_data.append(count)
    
    return all_data

def reload():
    new_data = get_covid_data()
    mainLabel['text'] = new_data


def get_covid_data(request):
    # data = {}
    # for c in countries:
    #     data[c] = get_country_data(c) 
    data = []
    all_data = {}
    if request.method == 'POST':
        data = get_country_data(request.POST['country'])
        all_data['country'] = request.POST['country'] 
    if len(data) == 0:
        data = get_country_data('Global')
        all_data['country'] = 'Global'
    all_data['Cases'] = data[0]
    all_data['Deaths'] = data[1]
    all_data['Recovered'] = data[2]
    print(all_data)
    # url = 'https://www.worldometers.info/coronavirus/'
    # html_data = get_html_data(url)
    # bs = bs4.BeautifulSoup(html_data.text,'html.parser')
    # info_div = bs.find('div',class_='content-inner').findAll("div",id="maincounter-wrap")
    # all_data = ''
    # for block in info_div:
    #     text = block.find('h1',class_=None).get_text()
    #     count = block.find('span',class_ = None).get_text()
    #     all_data += text+" "+count+"\n"

    # return all_data
    return render(request, 'corona/tracker.html', {'data': all_data})
