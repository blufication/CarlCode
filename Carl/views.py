from django.shortcuts import render

# Create your views here.
def home(request):
	name = "Welcome"
	return render(request, "Carl.html", {"name": name})

