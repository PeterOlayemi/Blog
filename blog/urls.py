from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .general import *
from .reader import *
from .writer import *

urlpatterns = [
        
#general

    path('', IndexView, name='index'),
    path('login/', LoginView, name='login'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detailview'),
    path('post/like/<int:pk>/', PostLikeView, name='post_like'),
    path('post/inlike/<int:pk>/', LikeInLikerView, name='like_liker'),
    path('post/liker/<int:pk>/', PostLikerView, name='liker'),
    path('post/dislike/<int:pk>/', PostDisLikeView, name='post_dislike'),
    path('post/indislike/<int:pk>/', DisLikeInDisLikerView, name='dislike_disliker'),
    path('post/disliker/<int:pk>/', PostDisLikerView, name='disliker'),
    path('comment/edit/<int:pk>/<int:id>/', EditCommentView, name='edit_comment'),
    path('comment/del/<int:pk>/<int:id>/', CommentDeleteView, name='comment_delete'),
    path('user/<int:pk>/', ProfileView, name='profile'),
    path('user/edit/<int:pk>/', EditProfileView, name='edit_profile'),
    path('all/category/', CategoryView, name='category'),
    path('<cat>/', CategoryDetailView, name='category_detail'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('apply/admin/', AdminApplView.as_view(), name='admin_apply'),
    path('apply/admin/success/', AdminApplSuccessView.as_view(), name='success'),
    
#reader

    path('portal/reader_register', ReaderSignUpView, name='reader_register'),

#writer

    path('portal/writer_register', WriterSignUpView, name='writer_register'),
    path('w/post', PostView, name='post'),
    path('post/update/<int:pk>', PostUpdateView, name='post_update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('reply/<int:pk>/<int:id>', ReplyComView.as_view(), name='reply_view'),
    path('reply/edit/<int:pk>/<int:id>/<uuid:uuid>/', ReplyEditView, name='reply_edit'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
