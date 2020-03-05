from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.views.generic import (
         ListView,
         DetailView,
         CreateView,
         UpdateView,
         DeleteView
         )

#def home(request):
    #context = {'posts' : Post.objects.all() }
    #return render(request, 'blog/home.html', context)

# use of class views instead of function views
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

        #messages.success(request, f'Post updated successfully!')
        #return redirect ('home')
        # class AuthorCreate(SuccessMessageMixin, CreateView):
        # 	 	model = Author
        # 		success_url = '/success/'
        # 		success_message = "Updated successfully"

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
        return render(request, 'blog/about.html', {'title':'About Us'})

def most_recent_posts(request):
        recent = Post.objects.all().order_by('-date_posted')[:5]
        return render(request, 'blog/base.html', {'recent': recent})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post-detail', pk = post.pk)
    else:
        form = CommentForm()
    return render (request, 'blog/add_comment_to_post.html', {'form':form, 'title': 'Comments'})

# class CommentCreateView(LoginRequiredMixin, CreateView):
#     	model = Comment
# 		fields = ['author', 'text']

# 	def form_valid(self, form):
# 		form.instance.author = self.request.user		
# 		return super().form_valid(form)

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)