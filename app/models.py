from django.db import models
from django.contrib.auth import get_user_model
user= get_user_model ()

# Create your models here.
class category(models.Model):
    ctgname=models.CharField(max_length=100)

class Books(models.Model):
    book_name=models.CharField(max_length=255)
    author_name=models.CharField(max_length=255)
    genere=models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    summary=models.TextField()
    quantity=models.IntegerField()
    price=models.IntegerField()
    rent=models.IntegerField()
    image=models.ImageField(upload_to="image/",null=True)
    date=models.DateField(auto_now_add=True)
    publisherid=models.TextField(null=True)

class issue(models.Model):
    buser=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Books,on_delete=models.CASCADE,null=True)
    from_date=models.DateField(auto_now_add=True)
    to_date=models.DateField(auto_now_add=True)
    total=models.IntegerField()

class bag(models.Model):
    book=models.ForeignKey(Books,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=1)
    def total_price(self):
        if self.book:
            return self.quantity*self.book.price
        return 0

class rented(models.Model):
    book=models.ForeignKey(Books,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    fromdate=models.TextField()
    todate=models.TextField()
    total=models.TextField(max_length=255)
    fine=models.TextField(max_length=255)
    finestatus=models.TextField(max_length=255,null=True)
    returns=models.TextField(max_length=255,null=True)
    rdate=models.DateField(null=True)

class userdata(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    gender=models.TextField(max_length=255)
    address=models.TextField(max_length=255)
    phone=models.TextField(max_length=255)
    image=models.ImageField(upload_to="image/",null=True)

class lostdata(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Books,on_delete=models.CASCADE,null=True)
    price=models.PositiveIntegerField(null=True)
    fine=models.PositiveIntegerField(null=True)
    date=models.DateField(null=True)
  
class purchase(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Books,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    quantity=models.PositiveIntegerField(null=True)
    price=models.PositiveIntegerField(null=True)