# Create your views here.
from django.shortcuts import  render, redirect
from .forms import NewUserForm, SearchForm
from django.contrib.auth import login, authenticate,  logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.contrib import messages #import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Article
from django.contrib.auth.models import User
from django.db.models import Q

def registerview(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/')
	form = NewUserForm
	return render (request=request, template_name="register.html", context={"register_form":form})
def loginview(request):
	if request.method == "POST":
		form=AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username=form.cleaned_data.get('username')
			password=form.cleaned_data.get('password')
			user=authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('/welcome')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

class Dashboardview(LoginRequiredMixin, ListView):
	model = Article
	template_name ='dashboard.html'
	context_object_name = "articles"
	ordering = ["-created_on"]
	def get_queryset(self):
		return Article.objects.filter(author=self.request.user)
	def get_context_data(self, **kwargs):
		context = super(Dashboardview, self).get_context_data(**kwargs)
		context['search_form']=SearchForm()
		return context

class CreateArticleview(LoginRequiredMixin, CreateView):
	model = Article
	fields = ["articlename","photo", "description", "visibility"]
	template_name = "create_article.html"
	success_url='/welcome'
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class SearchResview(LoginRequiredMixin, ListView):
	model = Article
	template_name ='searchresults.html'
	context_object_name = "articles"
	ordering = ["-created_on"]
	def get_queryset(self):
		query=self.request.GET.get('user', '')
		user_id=User.objects.get(username=query)
		return Article.objects.filter(Q(author=user_id.id) & Q(visibility=True))
	def get_context_data(self, **kwargs):
		context = super(SearchResview, self).get_context_data(**kwargs)
		context['user']=self.request.GET.get('user', '')
		return context

def logoutview(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("http://127.0.0.1:8000/")