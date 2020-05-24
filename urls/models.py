from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User



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


class Publisher(models.Model):
    name = models.CharField("Название", max_length=50, db_index=True)
    description = models.TextField("Описание")
    picture = models.ImageField("Картинка", upload_to="urls/")

    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"


class Games(models.Model):
    name = models.CharField("Название", max_length=50, db_index=True)
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
