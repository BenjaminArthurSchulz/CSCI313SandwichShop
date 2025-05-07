from django.db import models

# Create your models here.
class Bread(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Protein(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vegetarian = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Cheese(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Vegetable(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Condiment(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Extra(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Sandwich(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    proteins = models.ManyToManyField(Protein, blank=True)
    cheeses = models.ManyToManyField(Cheese, blank=True)
    vegetables = models.ManyToManyField(Vegetable, blank=True)
    condiments = models.ManyToManyField(Condiment, blank=True)
    extras = models.ManyToManyField(Extra, blank=True)
    toasted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_price(self):
        price = self.bread.price
        
        for protein in self.proteins.all():
            price += protein.price
            
        for cheese in self.cheeses.all():
            price += cheese.price
            
        for vegetable in self.vegetables.all():
            price += vegetable.price
            
        for condiment in self.condiments.all():
            price += condiment.price
            
        for extra in self.extras.all():
            price += extra.price
            
        return price
    
    def __str__(self):
        if self.name:
            return self.name
        return f"Custom Sandwich #{self.id}"
    

