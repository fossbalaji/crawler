from django.db import models

# Create your models here.


class Domain(models.Model):
    """
        author:fossbalaji@gmail.com,
        purpose: to store unique domain names
    """
    name = models.CharField(unique=True, blank=False, null=False, max_length=255)
    created_on = models.DateTimeField(auto_now=True)


class Crawledpages(models.Model):
    """
        author: fossbalaji@gmail.com
        purpose: store every crawled page and links in it
    """
    domain_id = models.IntegerField(null=False, blank=False, db_index=True)
    url = models.URLField(null=False, blank=False)
    is_seed_url = models.BooleanField(default=False, db_index=True)
    content = models.TextField(null=True)
    page_links = models.TextField(null=True)
    image_links = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now=True)