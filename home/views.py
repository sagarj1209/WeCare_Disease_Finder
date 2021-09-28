from django.shortcuts import render, HttpResponse
from .models import Contact
from django.contrib import messages
import pandas as pd
import numpy as np
from numpy.linalg import inv
from numpy import load
import re

def index(request):
    return render(request, 'home/index.html')

def welcome(request):
    return render(request, 'home/checkup/welcome.html')

def info(request):
    return render(request, 'home/checkup/info.html')

def checkup(request):
    return render(request, 'home/checkup/checkup.html')

def disease(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        symp = request.POST.getlist('sym')

        C = load("media/Data/C.npy")
        U,s,V=np.linalg.svd(C, full_matrices=False)
        S=np.diag(s)
        reductie=30
        S=S[0:reductie,0:reductie]
        iS=inv(S)
        US=np.dot(U[:,0:reductie],iS)
        US_df=pd.DataFrame(data=US)
        sym = pd.read_csv("media/Data/new_sym.csv")
        dia = pd.read_csv("media/Data/new_dia.csv")
        Qsym = pd.DataFrame()
        for s in symp:
            Qsym = pd.concat([Qsym, sym.loc[(sym['symptom'] == s)]], axis=0)   
        Qsym.index.name = 'eye'
        Qsym2 = pd.DataFrame({'eye': []})

        for xx in range(len(Qsym)):
            waa =abs(Qsym.iloc[xx, :].name)
            print(abs(float(waa-1)))
            Qsy = pd.DataFrame((pd.DataFrame(US_df.loc[abs(waa-1), :reductie-1]).T))
            Qsym2 = Qsym2.append(Qsy)
        del Qsym2['eye']

        Qtemp = Qsym2.sum()*2
        dise = (dia[dia['_id'] == 0])
        similQd = np.dot(Qtemp, V[0:reductie, :]) /np.dot(np.abs(Qtemp), np.abs(V[0:reductie, :]))*100
        for xyz in range(len(V)):
            if similQd[xyz] > 20:
                disname = dia.iloc[[xyz-1]]
                disname.loc[:, 'index'] = similQd[xyz]
                dise = dise.append(disname)
        if(len(dise) < 5):
            res_df = dise.sort_values(('index'), ascending=False)[['diagnose', 'index']]
        else:
            res_df = dise.sort_values(('index'), ascending=False)[['diagnose', 'index']].head()
        res_df = res_df.round(2)
        res_df.dropna(axis=0, inplace=True)
        params = {}
        str_lst = []
        per_lst = []
        mylist = []
        for diag in res_df.diagnose:
            res = re.findall(r'\w+', str(diag))
            res_str = ''
            for word in res:
                res_str = res_str + ' ' + word
            str_lst.append(res_str)
        per_lst = res_df.loc[:, 'index']
        params = {'lst': str_lst, 'per': per_lst} 
        mylist = zip(str_lst,per_lst)
        return render(request, 'home/checkup/disease.html', {'lst':mylist})
    else:
        return HttpResponse('Access Denied')
    
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
    return render(request, 'home/contact.html')

def about(request):
    return HttpResponse("About")