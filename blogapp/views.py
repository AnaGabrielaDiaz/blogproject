from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Avg

# Registrar usuario
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blogapp:blog_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

# Mensaje de credenciales incorrectas
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)


class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'

    # Promedio de reseñas en la lista de blogs
    def get_queryset(self):
        return Blog.objects.annotate(promedio_rating=Avg('reviews__rating'))


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'

    # Cálculo de promedio de reseñas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        promedio = self.object.reviews.aggregate(promedio=Avg('rating'))['promedio']
        context['promedio_rating'] = round(promedio, 2) if promedio else None
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})


class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        blog_id = self.kwargs['pk']
        if Review.objects.filter(blog_id=blog_id, reviewer=request.user).exists():
            messages.warning(request, "Ya has dejado una reseña para este blog.")
            return redirect('blogapp:blog_detail', pk=blog_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})
