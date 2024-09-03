from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    has_children = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',  
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.name

    def get_ancestry(self):
        ancestry = []
        category = self
        while category.parent:
            ancestry.insert(0, category.parent)  # Insert at the beginning to maintain order from top-level to the current category
            category = category.parent
        return ancestry

    def get_full_path(self):
        """Get the full path of categories as a string."""
        ancestry = self.get_ancestry()
        return ' > '.join([category.name for category in ancestry] + [self.name])


class Part(models.Model):
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    part = models.CharField(max_length=200,null=False)
    part_description = models.TextField(blank=True)

    @property
    def category_path(self) -> str :
        return self.category.get_full_path()

    def __str__(self):
        return f' {self.part} => {self.category.get_full_path()}'

class PartImage(models.Model):
    part = models.ForeignKey(Part,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="part-images")

    def __str__(self) -> str:
        return f' {self.part.category} {self.part.part}'


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.client}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    part = models.ForeignKey(Part,on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.part.part} - {self.quantity}"
