from django.shortcuts import render,Http404, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Place, Category, Feedback, Contact
from blog.models import Post
from django.contrib import messages
from .forms import FeedBackForm
from django.core.mail import send_mail
from datetime import datetime
from django.template.loader import render_to_string

# Create your views here.

class PlaceListView(ListView):
    model = Place
    query_pk_and_slug = True
    template_name = 'index.html'
    context_object_name = 'places'
    paginate_by = 6
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all().order_by('-id'),
            'feedbacks': Feedback.objects.all().order_by('-id'),
            'posts': Post.objects.all().order_by('-date_stamp')[:3] 
        }) 
        return context
    def get_queryset(self):
        return Place.objects.filter(featured=True).order_by('-id')

class ListingView(ListView):
    model = Place
    query_pk_and_slug = True
    template_name = 'listings.html'
    context_object_name = 'places'
    ordering = ['-id']
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all()
        }) 
        return context

class PlaceDetailView(DetailView):
    model = Place
    template_name = 'listings-single.html'
    context_object_name = 'place'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'feedbacks': Feedback.objects.all().order_by('-id'),
            'places': Place.objects.all().order_by('-id')[:5]
        }) 
        return context

class PlaceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Place
    success_url = '/listings'

    def test_func(self):
        place = self.get_object()
        if self.request.user == place.author:
            return True
        return False

class PlaceCreateView(LoginRequiredMixin, CreateView):
    model = Place
    fields = ['name', 'image', 'description', 'address', 'location', 'category']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PlaceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Place
    fields = ['name', 'image', 'description', 'address', 'location', 'category']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        place = self.get_object()
        if self.request.user == place.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user.place_set.get(slug=self.kwargs.get('slug')),
        })  
        return context

class UserPlaceListView(ListView):
    model = Place
    template_name = 'user_place.html'
    context_object_name = 'places'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'posts': Place.objects.all().order_by('-date_stamp')[:5] 
        })  
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Place.objects.filter(author=user).order_by('-date_stamp')

class CategoryList(ListView):
    model = Place
    template_name = 'category_place.html'
    context_object_name = 'places'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'feedbacks': Feedback.objects.all().order_by('-id'),
            'posts': Post.objects.all().order_by('-date_stamp')[:3] 
        })  
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Place.objects.filter(category=category).order_by('-date_stamp')

def feedback(request):
    if request.method=='POST':
        form = FeedBackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your feedback has been received. Thank you!')
            return redirect('index')
    else:
        form = FeedBackForm()
    return render(request, 'feedback.html', {'form':form})


def search(request):
    name = request.GET['name']
    location = request.GET['location']
    cat = request.GET['category']
    places = Place.objects.filter(name__icontains=name)|Place.objects.filter(location__icontains=name)
    objects = Place.objects.filter(location__icontains=location)|Place.objects.filter(name__icontains=location)
    categories = Category.objects.get(name=cat)
    category = categories.places.all().order_by('-id')
    print(category)

    ca = Category.objects.all()
    return render(request, 'search.html', {'places':places,'category':category,'ca':ca, 'objects':objects, 'cat':cat,'location':location, 'name':name})



def about(request):
    	return render(request, 'about.html', {})

def contact(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        date_stamp = datetime.now()

        contact = Contact.objects.create(
            fname=fname,
            lname=lname, 
            email=email, 
            subject=subject, 
            message=message,
            date_stamp=date_stamp
            )
        contact.save()

        messages.success(request, 'Your message has been successfully sent! Thanks for reaching out.')

        context = {
            'fname':fname,
            'lname':lname,
            'email':email,
            'message':message
        }

        body = render_to_string('contact.txt', context)
        send_mail('Contact Form: {}'.format(subject), body, 'rasholayemi@gmail.com', ['rasholayemi@gmail.com'])

    return render(request, 'contact.html', {})