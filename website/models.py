from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse


class Pins(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    collection = models.ForeignKey('Collections', on_delete=models.SET_NULL, null=True)
    video = models.FileField(upload_to='videos/%Y/%m/%d/', null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('pin', kwargs={'pin_id': self.pk})

    def comments_count(self):
        return self.comment_set.count()


class Likes(models.Model):
    liked_by = models.ForeignKey('Profile', on_delete=models.CASCADE)
    pin = models.ForeignKey('Pins', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    pin = models.ForeignKey('Pins', on_delete=models.CASCADE)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content}'


class Collections(models.Model):
    title = models.CharField(max_length=18)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    collection_image = models.ImageField(upload_to='collections/', default='collections/favorites.jpg')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('collection', kwargs={'collection_id': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    about = models.TextField(max_length=255, null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_id': self.pk})


class Follow(models.Model):
    follower = models.ForeignKey('Profile', related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey('Profile', related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} -> {self.following}'


class Report(models.Model):
    post = models.ForeignKey('Pins', on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"'{self.post.title}' {self.reporter.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        Collections.objects.create(title='Избранное',
                                   author=profile,
                                   collection_image='collections/favorites.jpg')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
