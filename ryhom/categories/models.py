import itertools

from django.db import models
from django.utils.text import slugify

#from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(blank=True, upload_to='category-icons/')
    description = models.TextField(max_length=300, default='', blank=True)
    slug = models.SlugField(unique=True, null=False, default='', blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_categories',
    )

    class Meta:
        unique_together = ('slug', 'parent',)
        #indexes = [models.Index(fields=['slug', 'parent'])]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    # @property
    # def children(self):
    #     return self.category_set.all().order_by("title") <-- RESEARCH MORE OR USE A MODEL MANAGER!


    def _generate_slug(self):
        name = self.name
        unique_slug = slug = slugify(name) # Same value to 2 variables

        for num in itertools.count(1):
            if not Category.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '{}-{}'.format(slug, num)

        self.slug = unique_slug


    def save(self, *args, **kwargs):

        if not self.pk:
            self._generate_slug()

        if self.id and self.parent and self.id == self.parent.id:
            self.parent = None

        super().save(*args, **kwargs)


    # def get_absolute_url(self):
    #     return reverse("categories:category", kwargs={'slug': self.slug})


    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])


#-----------------------------------------------------------------------------

"""
views.py...

VERSION 1
"""

# def show_category(request, hierarchy):
#     category_slugs = hierarchy.split('/')
#     categories = []

    # REPLACE WITH 'try/except' IF ALL OF THIS WORKS!

#     for slug in category_slugs:
#         if not categories:
#             parent = None
#         else:
#             parent = categories[-1]
#         category = get_object_or_404(Category, slug=slug, parent=parent)
#         categories.append(category)


"""
views.py...

VERSION 2 --> with breadcrumbs
"""


# def show_category(request,hierarchy= None):
#     category_slug = hierarchy.split('/')
#     category_queryset = list(Category.objects.all())
#     all_slugs = [ x.slug for x in category_queryset ]
#     parent = None
#     for slug in category_slug:
#         if slug in all_slugs:
#             parent = get_object_or_404(Category,slug=slug,parent=parent)
#         else:
#             instance = get_object_or_404(Post, slug=slug)
#             breadcrumbs_link = instance.get_cat_list()
#             category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
#             breadcrumbs = zip(breadcrumbs_link, category_name)
#             return render(request, "postDetail.html", {'instance':instance,'breadcrumbs':breadcrumbs})

#     return render(request,"categories.html",{'post_set':parent.post_set.all(),'sub_categories':parent.children.all()})

#-----------------------------------------------------------------------------
