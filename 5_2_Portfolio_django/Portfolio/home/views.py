from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("this is home page")
    context={
        "variable":"this is variable"
    }
    return render(request,"index.html",context)

def aboutme(request):
    return HttpResponse("this is about page")

def service(request):
    return HttpResponse("this is service page")