from os import curdir
from django.shortcuts import redirect, render
from django.http import HttpResponse


def login(request):
	return render(request, 'index.html')
