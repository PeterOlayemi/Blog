from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from ckeditor.fields import RichTextField
from django.utils import timezone
from django_countries.fields import CountryField

from django.db import models
import uuid

class Admin(models.Model):
    first_name = models.CharField(max_length=49)
    last_name = models.CharField(max_length=49)
    age = models.CharField(max_length=2)
    email = models.EmailField(max_length=249, unique=True)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=249)
    qualification = models.CharField(max_length=29)
    bio = models.TextField()
    apply_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name + "'s Application"

class ContactModel(models.Model):
    facebook = models.CharField(max_length=249)
    whatsapp = models.CharField(max_length=249)
    instagram = models.CharField(max_length=249)
    twitter = models.CharField(max_length=249)
    github = models.CharField(max_length=249)

class Category(models.Model):
    area = models.CharField(max_length=19, unique=True)
    
    def __str__(self):
        return self.area

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
    )

STATE = (
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
    ('FCT', 'FCT'),
)

class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_writer = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)
    first_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)
    username = models.CharField(max_length=99, unique=True)
    email = models.EmailField(max_length=249, unique=True)
    picture = models.FileField(upload_to='images/', blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=9)
    country = CountryField(multiple=False)
    state = models.CharField(choices=STATE, max_length=49)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
QUAL = (
    ('B.Sc', 'B.Sc'),
    ('B.Tech', 'B.Tech'),
    ('MBBS', 'MBBS'),
    ('Others', 'Others')
    )
    
class Writer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    year_of_graduation = models.CharField(max_length=4, default = 2023)
    school = models.CharField(max_length=99)
    qualification = models.CharField(choices=QUAL, max_length=10)

    def __str__(self):
        return self.user.username
    
class Reader(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class Post(models.Model):
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=99, unique=True)
    post = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_like')
    dislikes = models.ManyToManyField(User, related_name='post_dislike')
    
    def __str__(self):
        return self.title + ' by ' + self.writer.username
    
    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_dislikes(self):
        return self.dislikes.count()

class Comment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering=['-date_updated']

    def __str__(self):
        return str(self.writer) + ' comments - ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    