from django.db import models
from django.urls import reverse
from django.conf import settings

class Product(models.Model):
    title = models.CharField(max_length = 100 , default = "Name Not Set")
    photo = models.ImageField(upload_to='pics', default='defaultProduct.jpg')
    maker = models.ForeignKey(
        # 'auth.User',
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        
    )
    price = models.CharField(max_length=10, default = "Price Not Set")
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    