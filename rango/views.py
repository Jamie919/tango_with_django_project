from django.shortcuts import render
from rango.models import Category
from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
    context_dict = {'boldmessage': 'This tutorial has been put together by Jamie!'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
# Create a context dictionary which we can pass
# to the template rendering engine.
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
    if form.is_valid():
        form.save(commit=True)
# Now that the category is saved, we could confirm this. # For now, just redirect the user back to the index view.
        return redirect('rango')
    else:
# The supplied form contained errors -
# just print them to the terminal.
       print(form.errors)
# Will handle the bad form, new form, or no form supplied cases. # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
            category = None
# You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('rango')
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


