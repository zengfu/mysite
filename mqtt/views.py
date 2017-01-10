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
    color = {'red': 0, 'green': 0, 'blue': 0}
    if request.method=="POST":
        form=colorform(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            red=cd['red']
            green=cd['green']
            blue=cd['blue']

            data = {
                'led_r': 1023-red,
                'led_g': 1023-green,
                'led_b': 1023-blue
            }
            color['red']=red
            color['green']=green
            color['blue']=blue
            mqtt.client.publish('/mytopic', json.dumps(data))
        return render(request, 'index.html', {'form': form,'color':color})
    else:
        form=colorform()
        print form
        return render(request,'index.html',{'form':form,'color':color})