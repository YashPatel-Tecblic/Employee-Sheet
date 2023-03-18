from django.shortcuts import render

# Create your views here.
import gspread 
import pandas as pd
from django.http import HttpResponse,JsonResponse
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .models import *
from rest_framework.response import Response
from .serializers import EmployeeSerializer,AddSerializer
from rest_framework import status
from rest_framework.views import APIView
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file('sheet-pandas-de0631f40a71.json', scopes=scopes)
credentials1 = Credentials.from_service_account_file('adddata-gsheet-90cef70844bf.json',scopes=scopes)

gc = gspread.authorize(credentials1)
gc1 = gspread.authorize(credentials)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# open a google sheet
gs = gc.open_by_key('1R6ciVIw9-NXvJdtvEEx7Ll7qpON5iz9hcjs0_6N7BzI')
gs1 = gc1.open_by_key('1VgUm8fEhD_ccBTpnNsVA2fRKZqbDT-HbsNQ2v2K3-N4')
# gs = gc.open_by_key('1R6ciVIw9-NXvJdtvEEx7Ll7qpON5iz9hcjs0_6N7BzI')
# select a work sheet from its name
worksheet = gs.worksheet('Sheet1')
worksheet1 = gs1.worksheet('Sheet2')

# worksheet1.update('B1', 'Bingo!')

class DetailsAPI(APIView):
    
    def get(self,request,pk=None,format =None):
        id =pk
        if id is not None:
          stu = User_data.objects.get(id=id)
          serializer =EmployeeSerializer(stu) 
         #  worksheet1.update_cell(3,2,Date_of_joining)   
          return Response(serializer.data)

        stu = User_data.objects.all()
        serializer = EmployeeSerializer(stu,many =True)
        return Response(serializer.data,status=status.HTTP_200_OK) 
    
    def post(self,request,format=None):
         i = request.data["i"]
         Employee_name = request.data["Employee_name"]
         worksheet1.update_cell(i,1,Employee_name)

         Date_of_joining = request.data["Date_of_joining"]
         worksheet1.update_cell(i,2,Date_of_joining)

         Employee_code = request.data["Employee_code"]
         worksheet1.update_cell(i,3,Employee_code)

         Annual_salary = request.data["Annual_salary"]
         worksheet1.update_cell(i,4,Annual_salary)

         Monthly_CTC = Annual_salary / 12
         worksheet1.update_cell(i,5,Monthly_CTC)

         Basic = int(Monthly_CTC*50)/100
         worksheet1.update_cell(i,6,Basic)
       
         HRA = int(Basic*40)/100
         worksheet1.update_cell(i,7,HRA)

         Conveyance = int(Monthly_CTC*10)/100
         worksheet1.update_cell(i,8,Conveyance)

         Special_allowance = int(Basic*40)/100
         worksheet1.update_cell(i,9,Special_allowance)

         Other_allowance = 0
         worksheet1.update_cell(i,10,Other_allowance)

         Total_Gross_Salary = Monthly_CTC
         worksheet1.update_cell(i,11,Total_Gross_Salary)

         temp =request.data["temp"]
         Per_Day_Salary = Total_Gross_Salary /temp
         worksheet1.update_cell(i,12,Per_Day_Salary)

         Present_day = request.data["Present_day"]
         worksheet1.update_cell(i,13,Present_day)

         Holiday = request.data["Holiday"]
         worksheet1.update_cell(i,14,Holiday)

         Absent_days= request.data["Absent_days"]
         worksheet1.update_cell(i,15,Absent_days)

         Weekly_off_days = request.data["Weekly_off_days"]
         worksheet1.update_cell(i,16,Weekly_off_days)

         Earn_leave = request.data["Earn_leave"]
         worksheet1.update_cell(i,17,Earn_leave)

         Leave_without_pay_day = request.data["Leave_without_pay_day"]
         worksheet1.update_cell(i,18,Leave_without_pay_day)
      
         Actual_Salary = Total_Gross_Salary
         worksheet1.update_cell(i,20,Actual_Salary)

         SDBOL = (Leave_without_pay_day*Per_Day_Salary)
         worksheet1.update_cell(i,21,SDBOL)

         Rate_pay = Actual_Salary - SDBOL
         worksheet1.update_cell(i,22,Rate_pay)

         Professional_tax = 200
         worksheet1.update_cell(i,23,Professional_tax)

         if Rate_pay>30000 or Rate_pay==30000:
            v = Rate_pay - 15000
            worksheet1.update_cell(i,24,v) 
         elif Rate_pay<30000:
            v = Rate_pay / 2
            worksheet1.update_cell(i,24,v) 
         elif Rate_pay < 12000:
            v = Rate_pay   
            worksheet1.update_cell(i,24,v)

         Employee_pf1 = Basic *13 /100
         worksheet1.update_cell(i,25,Employee_pf1)

         Employee_pf2 = Basic * 12/100
         worksheet1.update_cell(i,26,Employee_pf2)

         ESIC_1 = (Rate_pay*3.25/100)
         worksheet1.update_cell(i,27,ESIC_1)

         ESIC_2 =  (Rate_pay*0.75/100)
         worksheet1.update_cell(i,28,ESIC_2)

         TDS = request.data["TDS"]
         worksheet1.update_cell(i,29,TDS)
         
       
         serializer = EmployeeSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()   

            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk,format=None):
       id=pk
       stu =User_data.objects.get(pk=id) 
       serializer =EmployeeSerializer(stu,data=request.data) 
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data,status = status.HTTP_200_OK)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk,format=None):
       id =pk
       stu = User_data.objects.get(pk=id)
       stu.delete()
       return Response({'msg':'data Deleted'})


class AddInfoAPI(APIView):
   def get(self,request,pk=None,format =None):
        id =pk
        if id is not None:
          stu = Add_User.objects.get(id=id)
          serializer =AddSerializer(stu) 
         #  worksheet1.update_cell(3,2,Date_of_joining)   
          return Response(serializer.data)

        stu = Add_User.objects.all()
        serializer = AddSerializer(stu,many =True)
        return Response(serializer.data,status=status.HTTP_200_OK) 
   
   def post(self,request,format=None):
         i = request.data['i']
         Emp_code = request.data["Emp_code"]
         worksheet.update_cell(i,1,Emp_code)

         Emp_name = request.data["Emp_name"]
         worksheet.update_cell(i,2,Emp_name)

         Annual_salary = request.data["Annual_salary"]
         worksheet.update_cell(i,3,Annual_salary)

         serializer = AddSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()   

            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def put(self, request,pk,format=None):
       id=pk
       stu =Add_User.objects.get(pk=id) 
       serializer =AddSerializer(stu,data=request.data) 
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data,status = status.HTTP_200_OK)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self, request,pk,format=None):
       i = request.data["i"]
       id =pk
       stu = Add_User.objects.get(pk=id)
       worksheet.delete_row(i)
       stu.delete()
       return Response({'msg':'data Deleted'})


    

    # nSlides = n//4 + ceil((n/4)-(n//4))
    #     allProds.append([prod,range(1, nSlides), nSlides])
    # params = {'allProds': allProds}
    # print(allProds)
    # return render(request, 'shop/index.html', params)

# def Data(request):    
 
    # n= request.POST.get('n','')      
    # for i in range(2,n+2):
    #     Employee_name = request.POST.get('Employee_name','')
    #     Employee = Employee_data(Employee_name = Employee_name)
    #     Employee.save()
    #     worksheet1.update_cell(i,1,Employee_name)
    # return HttpResponse(request,'')
        # Date_of_joining = input("Enter Date:")
        # worksheet1.update_cell(i,2,Date_of_joining)
    
        # Employee_code = input("Enter the Employee code: ")  
        # worksheet1.update_cell(i,3,Employee_code)
    
        # Annual_salary = int(input("Enter Annual Salary: "))
        # worksheet1.update_cell(i,4,Annual_salary)
    
        # Monthly_CTC = Annual_salary / 12
        # worksheet1.update_cell(i,5,Monthly_CTC)
    
        # Basic = int(Monthly_CTC*50)/100
        # worksheet1.update_cell(i,6,Basic)
    
        # HRA = int(Basic*40)/100
        # worksheet1.update_cell(i,7,HRA)
    
        # Conveyance = int(Monthly_CTC*10)/100
        # worksheet1.update_cell(i,8,Conveyance)
    
        # Special_allowance = int(Basic*40)/100
        # worksheet1.update_cell(i,9,Special_allowance)
    
        # Other_allowance = 0
        # worksheet1.update_cell(i,10,Other_allowance)
    
        # Total_Gross_Salary = Monthly_CTC
        # worksheet1.update_cell(i,11,Total_Gross_Salary)
    
        # # n = int(input("Enter number:"))
        # temp =int(input("Enter total days of this month: "))
        # Per_Day_Salary = Total_Gross_Salary / temp
        # worksheet1.update_cell(i,12,Per_Day_Salary)
    
        # Present_day = int(input("Enter present Days of this month: "))
        # worksheet1.update_cell(i,13,Present_day)
    
        # Holiday = int(input("Enter this month holidays: "))
        # worksheet1.update_cell(i,14,Holiday)
    
        # Absent_days = int(input("Enter absent days of this month: "))
        # worksheet1.update_cell(i,15,Absent_days)
    
        # Weekly_off = int(input("Enter total weekly of days: "))
        # worksheet1.update_cell(i,16,Weekly_off)
    
        # Earn_leave = int(input("Enter Earn leave of this month: "))
        # worksheet1.update_cell(i,17,Earn_leave)
    
        # Leave_without_pay_day= int(input("Enter this month leave without pay days: "))
        # worksheet1.update_cell(i,18,Leave_without_pay_day)
    
        # Actual_Salary = Total_Gross_Salary
        # worksheet1.update_cell(i,20,Actual_Salary)
    
        # SDBOL = (Leave_without_pay_day*Per_Day_Salary)
        # worksheet1.update_cell(i,21,SDBOL)
    
        # Rate_pay = Actual_Salary - SDBOL
        # worksheet1.update_cell(i,22,Rate_pay)
    
        # Professional_tax = 200
        # worksheet1.update_cell(i,23,Professional_tax)

        # if Rate_pay>30000 or Rate_pay==30000:
        #     v = Rate_pay - 15000
        #     worksheet1.update_cell(i,24,v) 
        # elif Rate_pay<30000:
        #     v = Rate_pay / 2
        #     worksheet1.update_cell(i,24,v) 
        # elif Rate_pay < 12000:
        #     v = Rate_pay   
        #     worksheet1.update_cell(i,24,v)  

        # Employee_pf1 = Basic *13 /100
        # worksheet1.update_cell(i,25,Employee_pf1)
    
        # Employee_pf2 = Basic * 12/100
        # worksheet1.update_cell(i,26,Employee_pf2)

        # ESIC_1 = (Rate_pay*3.25/100)
        # worksheet1.update_cell(i,27,ESIC_1)

        # ESIC_2 =  (Rate_pay*0.75/100)
        # worksheet1.update_cell(i,28,ESIC_2)

        # TDS = int(input("Enter TDS Amount: "))
        # worksheet1.update_cell(i,29,TDS)

    
        # Final_salary = 



            # Final_salary 

        
            

        
        # print("      Enter New Employee Details:")


# Details()

# df = pd.DataFrame(worksheet1.get_all_records())
# print(df) 