from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    info = models.TextField(blank=True)
    category = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='images/', max_length=250)
    additional_image = models.ForeignKey(
        'AdditionalImage', null=True, blank=True, related_name='projects', on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        # Generate the slug only if the name has been changed or the project is being saved for the first time.
        if not self.slug or self.name != self._original_name:
            self.slug = slugify(self.name)
            counter = 1
            original_slug = self.slug

            while Project.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self._original_name = self.name


class AdditionalImage(models.Model):
    project = models.ForeignKey(
        Project, null=True, blank=True, related_name='additionalimages', on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.name
