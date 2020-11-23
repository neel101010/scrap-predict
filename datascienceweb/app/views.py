from django.http import HttpResponse
from django.shortcuts import render
from .controller import infoGet, closingGet, companyGet


# Home Page
def index(request):
    return render(request, 'main_page.html')


# Analyse page
def analyse(request):
    company_list = companyGet()
    return render(request, 'analyse.html', company_list)


# Analyse page
def info(request, company):
    info = infoGet(company)
    return render(request, 'company.html', info)


# Predicted Closing Price Calculation
def cal(request, company):
    x = request.GET.get('opening')
    info = closingGet(x, company)
    return render(request, 'predict.html', info)


# About page
def about(request):
    return render(request, 'about.html')


# Methodology Page
def methodology(request):
    return render(request, 'methodology.html')

