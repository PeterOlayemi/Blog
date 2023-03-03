from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, DetailView

from .models import * 
from .forms import *

@login_required
def ReplyEditView(request, pk, id, uuid):
    replies = Comment.objects.get(uuid = uuid)
    comment = Comment.objects.get(id=id)
    post = Post.objects.get(id=pk)
    if request.method != 'POST':
        form = CommentForm(instance=replies)
    else:
        form = CommentForm(request.POST, instance=replies)
        if form.is_valid:
            data = form.save(commit=False)
            data.writer = request.user
            data.parent=comment
            data.save()
            return redirect(reverse('detailview', args=[post.pk]))
    return render(request, 'writer/reply.html', {'form':form})

class ReplyComView(DetailView):
    queryset = Post.objects.all()
    context_object_name = 'post'
    template_name= 'writer/reply.html'

    def get_success_url(self):
        id = self.kwargs.get('pk')
        return reverse('detailview', kwargs={'pk':id})

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        comment = Comment.objects.filter(post=self.get_object())
        data['comment'] = comment
        data['form'] = CommentForm()
        return data

    def post(self , request , *args , **kwargs):
        id = self.kwargs.get('id')
        comment = Comment.objects.filter(post=self.get_object()).get(id=id)
        if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                parent = form.cleaned_data['parent']
            new_comment = Comment(content=content , writer = self.request.user , post=self.get_object() , parent=comment)
            new_comment.save()
            return redirect(self.get_success_url())

class PostDeleteView(DeleteView):
    queryset = Post.objects.all()
    context_object_name = 'post'
    template_name = 'writer/delete.html'
    success_url = '/'

@login_required
def PostView(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.writer = request.user
            obj.save()
            return redirect('index')
    return render(request, 'writer/post.html', {'form':form})
    
@login_required
def PostUpdateView(request, pk):
    post = Post.objects.get(id=pk)
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.writer = request.user
            obj.save()
        return redirect(reverse('detailview', args=[post.pk]))
    return render(request, 'writer/post.html', {'form':form})

def WriterSignUpView(request):
    if request.method != 'POST':
        form = WriterSignUpForm()
    else:
        form = WriterSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    context = {'form': form, 'user_type':'writer'}
    return render(request, 'registration/signup.html', context)