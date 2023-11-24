from django.shortcuts import render

from django.shortcuts import render

def home(request):
    return render(request,'layout/index.html')
def main(request):
    return render(request,'layout/main.html')
    
