from django import forms

class ChatForm(forms.Form):

    chat = forms.CharField()
    message = forms.CharField()
