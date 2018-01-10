from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.company_name)

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])
    

class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    company_name = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return '%s' % (self.branch_name)

    def get_absolute_url(self):
        return reverse('branch-detail', args=[str(self.id)])

    def get_orders_sorted_by_date(self):
        return self.orders.order_by('Order_Date').reverse()


class Customer(models.Model):
    phone_number = models.IntegerField(null=True)
    customer_name = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        return '%s' % (self.customer_name)

    def get_absolute_url(self):
        return reverse('customer-detail', args=[str(self.id)])

    def get_order_count(self):
        return self.orders.count()
    
    def get_latest_order(self):
        latest_order = self.orders.latest('Order_Date')
        return latest_order

    def get_absolute_url(self):
        return reverse('customer-detail', args=[str(self.id)])  

    def get_orders_sorted_by_date(self):
        return self.orders.order_by('Order_Date').reverse()


class Occassion(models.Model):
    occassion_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return '%s' % (self.occassion_name)

    def get_absolute_url(self):
        return reverse('occassion-detail', args=[str(self.id)])

    def get_orders_sorted_by_date(self):
        return self.orders.order_by('Order_Date').reverse()


class Order(models.Model):
    Company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL, related_name='orders')
    Branch = models.ForeignKey(Branch, blank=True, null=True, on_delete=models.SET_NULL, related_name='orders')
    Customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL, related_name='orders')
    Occassion = models.ForeignKey(Occassion, blank=True, null=True, on_delete=models.SET_NULL, related_name='orders')
    Order_Date = models.DateField( blank=True, null=True)
    Order_No = models.IntegerField(null=True, blank=True)
    Total_Amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return 'for %s on %s' % (self.Total_Amount, self.Order_Date)

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def create_order(self, i, company_name):
        print('order received')
        print (i)
        self.Company, c0 = Company.objects.get_or_create(company_name = company_name)
        self.Order_No = i['Order_No']
        self.Order_Date = i['Order_Date']
        self.Total_Amount = i['Total_Amount']
        self.Customer, c1 = Customer.objects.get_or_create(
                            phone_number = i['Contact_No'],
                            customer_name = i['Customer_Name']
                            )
        self.Occassion, c2 = Occassion.objects.get_or_create(occassion_name = i['Occassion'])
        self.Branch, c3 = Branch.objects.get_or_create(branch_name = i['Branch'], company_name = self.Company )

        self.save()




class Document(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/%Y')




# CREATE USER PROFILE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s' % (self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()