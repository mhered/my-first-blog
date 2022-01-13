from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Category, Post
from .forms import PostForm, ImageForm, CatForm
from django.shortcuts import redirect
from django.views.generic import CreateView


from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Image



# Create your views here.


def add_category(request):
    if request.method == "POST":
        form = CatForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_list')
    else:
        form = CatForm()
    return render(request, 'blog/add_category.html', {'form': form})


def category_show(request, cat_name):
    cat_posts = Post.objects.filter(category=cat_name)
    return render(request, 'blog/categories.html', 
                    {'cat_name': cat_name, 'cat_posts': cat_posts})


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
 
    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm, extra=3)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
    
        post_form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())
    
    
        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
    
            for item in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if item:
                    image = item['image']
                    photo = Image(post=post, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(post_form.errors, formset.errors)
    else:
        post_form = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'blog/post_edit.html',
                  {'form': post_form, 'formset': formset})



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
