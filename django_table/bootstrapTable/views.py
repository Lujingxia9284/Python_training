import json
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request,"index.html")

def getData(request):
    
    filename = "D:/repo/Python_training/django_table/static/tableData.json"
    with open(filename,encoding='utf-8') as f:
        movie_json = json.load(f)
    # print('-------------',type(list(movie_json)))
    return HttpResponse(movie_json)

