from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta

import csv

# Create your views here.
def index(request):
    date = datetime.today().date()
    date = datetime(2024, 8, 19).date()
    weekDay = date.strftime("%A")
    holiday = False
    dueTo = None
    
    
    if weekDay == "Sunday" or weekDay == "Saturday":
        holiday = True
        dueTo = weekDay
    else:
        holiday, dueTo = sageHoliday(date)

    return render(request, "isholiday/index.html", {
        "isholiday": holiday,
        "dueTo": dueTo,
        "weekDay": weekDay
    })

def sageHoliday(curr_date):
    dueTo = None
    with open("isholiday/holidays_in_sage.csv", "r") as f:
        
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            
            if is_range(row[0]):
                
                start, end = row[0].split(" to ")
                
                start = datetime.strptime(start, "%d.%m.%Y").date()
                end = datetime.strptime(end, "%d.%m.%Y").date()
                
                while start <= end:
                    if start == curr_date:
                        return (True, row[2])
                    start += timedelta(days=1)

            else:
                date = datetime.strptime(row[0], str("%d.%m.%Y")).date()
                if curr_date == date:
                    return (True, row[2])
    
    return (False, dueTo)


def is_range(date:str):
    if 'to' in date:
        return True
    else:
        return False