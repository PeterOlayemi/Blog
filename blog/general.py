from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import *

class AdminApplSuccessView(TemplateView):
    template_name = 'general/success.html'

class AdminApplView(CreateView):
    model = Admin
    form_class = AdminApplForm
    template_name = 'general/adminapply.html'
    success_url = 'success'

def LoginView(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                msg = 'Invalid Email or Password'
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})

class ContactView(ListView):
    queryset = ContactModel.objects.all()
    context_object_name = 'obj'
    template_name = 'general/contact.html'

class AboutView(TemplateView):
    template_name= 'general/about.html'

@login_required
def PostLikerView(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    context = {'number_of_likes':post.number_of_likes(), 'post_is_liked':liked, 'post':post}
    return render(request, 'general/liker.html', context)

@login_required
def PostDisLikerView(request, pk):
    post = get_object_or_404(Post, id=pk)
    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        disliked = True
    context = {'number_of_dislikes':post.number_of_dislikes(), 'post_is_disliked':disliked, 'post':post}
    return render(request, 'general/disliker.html', context)

@login_required
def PostLikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(reverse('detailview', args=[post.pk]))

@login_required
def PostDisLikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return redirect(reverse('detailview', args=[post.pk]))

@login_required
def LikeInLikerView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(reverse('liker', args=[post.pk]))

@login_required
def DisLikeInDisLikerView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return redirect(reverse('disliker', args=[post.pk]))

@login_required
def CategoryView(request):
    cat = Category.objects.all()
    catcount = Category.objects.all().count()
    context = {
        'cat':cat,
        'catcount':catcount
    }
    return render(request, 'general/category.html', context)

@login_required
def ProfileView(request, pk):
    user = User.objects.get(id=pk)
    if user.is_writer == True:
        writer = Writer.objects.filter(user=user).get(id=pk)
        context = {'writer':writer, 'user':user, 'user_type':'Writer'}
        return render(request, 'general/profile.html', context)
    else:
        reader = Reader.objects.filter(user=user).get(id=pk)
        context1 = {'reader':reader, 'user':user, 'user_type':'Reader'}
        return render(request, 'general/profile.html', context1)

@login_required
def EditProfileView(request, pk):
    user = User.objects.filter(email=request.user).get(id=pk)
    if user.is_writer == True:
        writer = Writer.objects.filter(user=user).get(id=pk)
        if request.method != 'POST':
            form1 = UserForm(instance=user)
            form2 = WriterForm(instance=writer)
        else:
            form1 = UserForm(request.POST, request.FILES, instance=user)
            form2 = WriterForm(request.POST, instance=writer)
            if form1.is_valid() and form2.is_valid():
                form1.save() and form2.save()
                return redirect(reverse('profile', args=[user.pk]))
        context = {'form1': form1, 'form2': form2, 'user_type':'Writer'}
        return render(request, 'registration/editprofile.html', context)
    else:
        reader = Reader.objects.filter(user=user).get(id=pk)
        if request.method != 'POST':
            form1 = UserForm(instance=user)
            form2 = ReaderForm(instance=reader)
        else:
            form1 = UserForm(request.POST, request.FILES, instance=user)
            form2 = ReaderForm(request.POST, instance=reader)
            if form1.is_valid() and form2.is_valid():
                form1.save() and form2.save()
                return redirect(reverse('profile', args=[user.pk]))
        context1 = {'form1': form1, 'form2': form2, 'user_type':'Reader'}
        return render(request, 'registration/editprofile.html', context1)

class PostDetailView(DetailView):
    queryset = Post.objects.all()
    context_object_name = 'post'
    template_name= 'general/detail.html'

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        comment = Comment.objects.filter(post=self.get_object()).order_by('-date_updated')
        com_count = comment.count()
        
        #like_feature
        obj = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if obj.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = obj.number_of_likes()
        data['post_is_liked'] = liked
        
        #dislike_feature
        obj = get_object_or_404(Post, id=self.kwargs['pk'])
        disliked = False
        if obj.dislikes.filter(id=self.request.user.id).exists():
            disliked = True
        data['number_of_dislikes'] = obj.number_of_dislikes()
        data['post_is_disliked'] = disliked
        
        data['comment'] = comment
        data['com_count'] = com_count
        data['form'] = CommentForm()
        return data

    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                try:
                    parent = form.cleaned_data['parent']
                except:
                    parent=None
            new_comment = Comment(content=content , writer = self.request.user , post=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)

@login_required
def EditCommentView(request, pk, id):
    post = Post.objects.get(id = pk)
    comment = Comment.objects.filter(post = post).order_by('-date_updated')
    com_count = Comment.objects.filter(post = post).count()
    com = Comment.objects.get(id=id)
    
    obj = get_object_or_404(Post, id=pk)
    liked = False
    if obj.likes.filter(id=request.user.id).exists():
        liked = True
        
    #like_feature
    rat = get_object_or_404(Comment, id=id)
    cliked = False
    if rat.likes.filter(id=request.user.id).exists():
        cliked = True
    
    form = CommentForm(request.POST or None, instance=com)
    if request.method == 'POST':
        if form.is_valid:
            data = form.save(commit = False)
            data.writer = request.user
            data.post = post
            data.save()
            return redirect(reverse('detailview', args=[post.pk]))
    return render(request, 'general/detail.html', {'no_of_likes': rat.number_of_likes(), 'comment_is_liked':cliked, 'post':post, 'comment':comment, 'com_count':com_count, 'form':form, 'number_of_likes':obj.number_of_likes(), 'post_is_liked':liked })

@login_required
def CommentDeleteView(request, pk, id):
    post = Post.objects.get(id=id)
    com = Comment.objects.get(id=pk)
    if request.method == "POST":
        com.delete()
        return redirect(reverse('detailview', args=[post.id]))
    return render(request, 'general/comdelete.html', {'com':com, 'post':post})

def IndexView(request):
    cat = Category.objects.all()
    paginator = Paginator(cat, 5)
    page = request.GET.get('page')
    try:
        cat = paginator.page(page)
    except PageNotAnInteger:
        cat = paginator.page(1)
    except EmptyPage:
        cat = paginator.page(paginator.num_pages)
    pc = Post.objects.all().count()
    catcount = Category.objects.all().count()
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    post = Post.objects.filter( Q(writer__username__icontains=q) | Q(title__icontains=q) | Q(post__icontains=q) | Q(category__area__icontains=q)).order_by('-date_updated')
        
    context = {
        'post':post,
        'cat':cat,
        'pc':pc,
        'catcount':catcount,
    }
    return render(request, 'general/index.html', context)

@login_required
def CategoryDetailView(request, cat):
    post = Post.objects.filter(category__area=cat).order_by('-date_updated')
    context = {
        'post':post,
        'cat':cat
    }
    return render(request, 'general/categorydetail.html', context)
