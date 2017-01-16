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
                'led_b': 1023-blue,
                'cmd':1
            }
            color['red']=red
            color['green']=green
            color['blue']=blue
            mqtt.client.publish('/mytopic', json.dumps(data))
        return render(request, 'index.html', {'form': form,'color':color})
    else:
        form=colorform()
        print 'get'
        return render(request,'index.html',{'form':form,'color':color})
def handle_led(request):
    if request.method == 'POST':
        red=request.POST['red']
        green=request.POST['green']
        blue=request.POST['blue']

        data = {
            'led_r': 1023 - int(red),
            'led_g': 1023 - int(green),
            'led_b': 1023 - int(blue),
            'cmd':0
        }
        print data
        mqtt.client.publish('/mytopic', json.dumps(data))

        return HttpResponse("ok")
    else:
        return HttpResponse("<h1>test</h1>")
def sb(th):
    b=2
    a=-1/1023.0
    return int(th*th*a+b*th)
def get_color(request):
    if request.method == 'POST':
        red = request.POST['red']
        green = request.POST['green']
        blue = request.POST['blue']
        print "red:%s,green:%s,blue:%s"%(red,green,blue)
        data = {
            'led_r': sb(1023 - int(int(red)*4)),
            'led_g': sb(1023 - int(int(blue)*4)),
            'led_b': sb(1023 - int(int(green)*4)),
            'cmd': 0
        }
        print data
        mqtt.client.publish('/mytopic', json.dumps(data))

        return HttpResponse("ok")
    else:
        return HttpResponse("<h1>test</h1>")

def test(request):
    return render(request, 'test.html')
