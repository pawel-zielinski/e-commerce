from django.shortcuts import render
from django.views.generic import ListView, DetailView
from Shop_API.models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(ListView):
    model = Product
    template_name = 'Shop_API/home.html'

class ProductDetail(DetailView):
    model = Product
    template_name = 'Shop_API/product_detail.html'
