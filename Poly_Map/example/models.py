from django.db import models

# Create your models here.


class bill(models.Model):
	name = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	progress = models.CharField(max_length=100)
	link = models.CharField(max_length=100)
	congress_num = models.IntegerField(default=0)
	chamber = models.CharField(max_length=100,default="")
	pdflink = models.CharField(max_length=100,default="")
	views = models.IntegerField(default=0)


	def __str__(self):
		return self.name





class congress(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	contact = models.CharField(max_length=400)
	party = models.CharField(max_length=50)
	district = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	house = models.BooleanField()
	website = models.CharField(max_length=150)
	imageLink = models.CharField(max_length=150)
	congress_num = models.IntegerField()
	congresslink = models.CharField(max_length=150,default='')
	served = models.CharField(max_length=150,default='')
	views = models.IntegerField(default=0)
	bills = models.ManyToManyField(bill)
	cosponsored = models.ManyToManyField(bill,related_name='cosponsored')




	def __str__(self):
		return (self.first_name + ' ' + self.last_name)


class committee(models.Model):
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(congress)
	location = models.CharField(max_length=50,default=0) # house senate special etc
	importance = models.IntegerField()					 # how we value the committee
	address = models.CharField(max_length=400,default=0)
	phone = models.CharField(max_length=20,default=0)
	link = models.CharField(max_length=200,default=0)

	bills = models.ManyToManyField(bill)
	
	def __str__(self):
		return self.name

class sub_committee(models.Model):
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(congress)
	committee = models.ForeignKey(committee,on_delete=models.CASCADE,null=True)
	link = models.CharField(max_length=200,default=0)
