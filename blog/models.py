from django.conf import settings
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        """__str__ method """
        return self.name

    def get_absolute_url(self):
        return reverse('post_list')  # what is this? check!


class Post(models.Model):
    """ Post - basic Post object"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=255, default='none')
    
    def publish(self):
        """Post.publish() method"""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        """__str__ method """
        return self.title + ' | ' + str(self.author) + ' | ' + self.category


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "images/%s-%s" % (slug, filename)  


class Image(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')
