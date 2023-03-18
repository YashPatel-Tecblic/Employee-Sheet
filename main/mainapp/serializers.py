from rest_framework import serializers
from .models import User_data,Add_User

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_data
        fields = ['n','id','Employee_name','Date_of_joining','Employee_code','Annual_salary','Monthly_CTC','Present_day','Holiday','Absent_days','Weekly_off_days','Earn_leave','Leave_without_pay_day','TDS'] 

class AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_User
        fields = '__all__'

