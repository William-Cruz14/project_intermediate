from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Product
from .forms import ContactForm, ProductModelForm

def index(request):
    context = {"products": Product.objects.all()}
    return render(request, 'index.html', context)

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.send_mail()
            messages.success(request, f"message sent successfully")
            form = ContactForm()
    else:
        messages.error(request, "Please fill out the form")


    context = {'form': form}
    return render(request, 'contact.html', context)

def product(request):
    print(f"User: {request.user}")
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProductModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, f"Product saved successfully")
                form = ProductModelForm()
            else:
                messages.error(request, "Error saving product")

        else:
            form = ProductModelForm()

        context = {'form': form}
        return render(request, 'product.html', context)
    else:
        return redirect('index')