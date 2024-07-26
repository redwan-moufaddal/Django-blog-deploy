from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuid.django_fields import ShortUUIDField
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=35, null=True,blank=True)
    last_name = models.CharField(max_length=35, null=True,blank=True)
    gender = models.CharField(max_length=20, null=True,blank=True)
    city = models.CharField(max_length=100, null=True,blank=True)
    country = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField(db_index=True,unique=True,max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'





class Article(models.Model):
    aid = ShortUUIDField(unique=True,primary_key=True, length=10, max_length=30, prefix="art", alphabet="redwanmoufdl12345")
    title = models.TextField()
    image_url_video_url = models.TextField()
    category = models.CharField(max_length=100)
    sub_description = models.TextField()
    content = models.TextField()
    date = models.CharField(max_length=15)
    keywords = models.TextField()
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    def __str__(self):
        return f"{self.email} subject:{self.subject}"

class BlogReview(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


