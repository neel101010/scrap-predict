from django.http import HttpResponse
from django.shortcuts import render
from .controller import infoGet, closingGet, companyGet


# Home Page
def index(request):
    return render(request, 'main_page.html')


# Analyse page
def analyse(request):
    company_list_temp = companyGet()
    company_list_temp = zip(company_list_temp["name"], company_list_temp["last_price"], company_list_temp["change"],
                            company_list_temp["per_change"], company_list_temp["volume"], company_list_temp["link"])
    company_list = {"company_list": company_list_temp}
    return render(request, 'analyse.html', company_list)


# Analyse page
def info(request, company):
    info = infoGet(company)
    return render(request, 'company.html', info)


# Predicted Closing Price Calculation
def cal(request, company):
    x = request.GET.get('opening')
    y = request.GET.get('period')
    info = closingGet(x, y, company)
    return render(request, 'company.html', info)


# About page
def about(request):
    return render(request, 'about.html')


# Methodology Page
def methodology(request):
    return render(request, 'methodology.html')

