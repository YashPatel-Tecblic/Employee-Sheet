from django.db import models

# Create your models here.
class User_data(models.Model):
    n= models.IntegerField(null=False,default=0)
    Employee_name = models.CharField(max_length=100,blank=False,default="name")
    Date_of_joining = models.DateField()
    Employee_code = models.IntegerField(null=False)
    Annual_salary = models.BigIntegerField(null= False)
    Monthly_CTC = models.IntegerField(null=False,default=0) 
    Present_day = models.IntegerField(null=True)
    Holiday = models.IntegerField(null=True)
    Absent_days = models.IntegerField(null=True)
    Weekly_off_days = models.IntegerField(null=False)
    Earn_leave = models.IntegerField(null=True)
    Leave_without_pay_day = models.IntegerField(null=True)
    TDS = models.IntegerField(null=True)

    def __str__(self):
        return self.Employee_name

class Add_User(models.Model):
    Emp_code = models.IntegerField()
    Emp_name = models.CharField(max_length=100)
    Annual_salary = models.IntegerField()

    def __str__(self):
        return self.Emp_name