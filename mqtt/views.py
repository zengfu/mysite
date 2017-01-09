from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
import json
from . import mqtt
# Create your views here.


class colorform(forms.Form):
    red=forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':'0', 'max':'1023'}))
    green = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '1023'}))
    blue = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '1023'}))
    #red = forms.RegexField(max_length=1023)
    #green = forms.RegexField(max_length=1023)
    #blue = forms.RegexField(max_length=1023)

def index(request):
    if request.method=="POST":
        form=colorform(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            red=cd['red']
            green=cd['green']
            blue=cd['blue']
            print red
            print green
            print blue
            data = {
                'led_r': red,
                'led_g': green,
                'led_b': blue
            }
            mqtt.client.publish('/mytopic', json.dumps(data))

    else:
        form=colorform()
    return render(request,'index.html',{'form':form,'book':'sbth'})