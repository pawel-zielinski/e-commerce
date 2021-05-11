from django.shortcuts import render
from django.views.generic import ListView, DetailView
from Shop_API.models import Product, Category


class Home(ListView):
    model = Product
    template_name = 'Shop_API/home.html'
