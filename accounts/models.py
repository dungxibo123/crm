from django.db import models
MAX_LENGTH = 200
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, null=True)
    phone = models.CharField(max_length=MAX_LENGTH, null=True)
    email = models.CharField(max_length=MAX_LENGTH, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )
    name = models.CharField(max_length=MAX_LENGTH, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=MAX_LENGTH, null=True, choices=CATEGORY)
    description = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=MAX_LENGTH, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)



class Tag(models.Model):
	name = models.CharField(max_length=MAX_LENGTH, null=True)

	def __str__(self):
		return self.name
