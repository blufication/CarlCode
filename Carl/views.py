from django.shortcuts import render
from .forms import ChatForm
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.cleaned_data.get('chat', None)
            message = form.cleaned_data.get('message', None)
            print('Name:'+ chat,'SSN:'+ message)
    name = "Welcome"
    return render(request, "Carl.html", {"name": name})


