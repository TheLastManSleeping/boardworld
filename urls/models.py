from allauth.account.views import email
from django.core import mail
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.db.backends import postgresql
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from faker.providers import address

from SaveMe.settings import EMAIL_HOST


class CommonInfo(models.Model):
    name = models.CharField("Название", max_length=50, db_index=True)

    class Meta:
        abstract = True



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    picture = models.ImageField("Картинка", upload_to="urls/", default='te2.jpg')
    # other fields...


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Categories(models.Model):
    """Категории гамесов"""
    name = models.CharField("Категория", max_length=50, db_index=True)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Publisher(CommonInfo):
    name = models.CharField("Название", max_length=50, db_index=True)
    description = models.TextField("Описание")
    picture = models.ImageField("Картинка", upload_to="urls/")

    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"



class Games(CommonInfo):
    categories = models.ManyToManyField(Categories, verbose_name="категория")
    description = models.TextField("Описание")
    picture = models.ImageField("Картинка", upload_to="urls/")
    publisher = models.ManyToManyField(Publisher, verbose_name="издатель", related_name="creator")
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("game_detail", kwargs={"slug": self.url})


class Reviews(models.Model):
    name = models.CharField("Имя", max_length=50, db_index=True)
    text = models.TextField("Сообщение", max_length=50)
    picture = models.ImageField("Картинка", upload_to="urls/")
    game = models.ForeignKey(Games, verbose_name="игра", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.game}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class LostMail(object):

    def __init__(self):
        temp = models.CharField("Текст", max_length=400)
        send_mail.queue.put(temp)

    def __del__(self):
        send_mail(EMAIL_HOST, [address], False)


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=MetaSingleton):
    connection = None

    def __init__(self):
        self.cursorobj = self.connection.cursor()

    def connect(self):
        if self.connection is None:
            self.connection = postgresql.connect("postgresql")
        return self.cursorobj

