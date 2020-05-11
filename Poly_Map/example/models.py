from django.db import models

# Create your models here.


class bill(models.Model):
	name = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	progress = models.CharField(max_length=100)
	link = models.CharField(max_length=100) 


	def __str__(self):
		return self.title





class congress(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	contact = models.CharField(max_length=400)
	party = models.CharField(max_length=50)
	district = models.IntegerField()
	state = models.CharField(max_length=50)
	house = models.BooleanField()
	website = models.CharField(max_length=150)
	imageLink = models.CharField(max_length=150)
	congress_num = models.IntegerField()

	bills = models.ManyToManyField(bill)




	def __str__(self):
		return (self.first_name + ' ' + self.last_name)


class committee(models.Model):
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(congress)
	location = models.CharField(max_length=50,default=0) # house senate special etc
	importance = models.IntegerField()					 # how we value the committee
	address = models.CharField(max_length=400,default=0)
	phone = models.CharField(max_length=20,default=0)

	bills = models.ManyToManyField(bill)
	
	def __str__(self):
		return self.name

class sub_committee(models.Model):
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(congress)
	committee = models.ForeignKey(committee,on_delete=models.CASCADE,null=True)
