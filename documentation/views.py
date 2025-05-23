from django.shortcuts import render

# Create your views here.

def ShowDocumentation(request):
    return render(request,"output.html")
