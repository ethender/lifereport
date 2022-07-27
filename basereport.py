from datetime import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt



'''
    Need to do 
    1. Process the step
    2. Generate the sources
    3. In corporate into HTML
    4. Schedule the Apache Air flow for every month.
'''
class BaseReport:

    def __init__(self):
        self.url = 'http://aarambh.tech:3000/api/life'
        (self.startDate,self.endDate) = self.getStartEndDateString()
        self.fetchedData = {}
        self.process()


    def process(self):
        params = {'from':self.startDate,'to':self.endDate}
        self.fetchedData['credits'] = self.fetchCredit(params)
        self.fetchedData['expense'] = self.fetchExpenses(params)
        self.fetchedData['investment'] = self.fetchInvestment(params)
        self.fetchedData['investmengained'] = self.fetchInvestmentGained(params)
        self.fetchedData['loanemi'] = self.fetchLoanEmi(params)
        self.dropLastModified()
        self.changeDateTypes()


    def dropLastModified(self):
        for key,value in self.fetchedData.items():
            if 'lastmodified' in value.columns:
                value.drop(columns=['lastmodified'],axis=1,inplace=True)
            else:
                value.drop(columns=['lastModified'], axis=1, inplace=True)
            self.fetchedData[key] = value

    def changeDateTypes(self):
        for key,value in self.fetchedData.items():
            if key == 'credits':
                value['cdate'] = pd.to_datetime(value['cdate']).dt.date
                value.rename(columns={'cdate': 'date'}, inplace=True)
            elif key  == 'expense':
                value['mdate'] = pd.to_datetime(value['mdate']).dt.date
                value.rename(columns={'mdate': 'date'}, inplace=True)
            elif key == 'investment':
                value['startdate'] = pd.to_datetime(value['startdate']).dt.date
                value['enddate'] = pd.to_datetime(value['enddate']).dt.date
            elif key == 'investmengained':
                value['idate'] = pd.to_datetime(value['idate']).dt.date
                value.rename(columns={'idate': 'date'}, inplace=True)
            elif key == 'loanemi':
                value['emidate'] = pd.to_datetime(value['emidate']).dt.date
                value.rename(columns={'emidate': 'date'}, inplace=True)
            else:
                pass
            self.fetchedData[key] = value

    def fetchExpenses(self,params=None):
        req = self.fetchUrl(extendurl='/month/expense')
        try:
            return pd.DataFrame(req.json())
        except ValueError:
            return pd.DataFrame()

    def fetchCredit(self,params=None):
        req = self.fetchUrl(extendurl='/credit')
        try:
            return pd.DataFrame(req.json())
        except ValueError:
            return pd.DataFrame()

    def fetchInvestment(self,params=None):
        req = self.fetchUrl(extendurl='/investment')
        try:
            return pd.DataFrame(req.json())
        except ValueError:
            return pd.DataFrame()

    def fetchInvestmentGained(self,params=None):
        req = self.fetchUrl(extendurl='/investmentgained')
        try:
            return pd.DataFrame(req.json())
        except ValueError:
            return pd.DataFrame()

    def fetchLoans(self,params=None):
        req = self.fetchUrl(extendurl='/loans')
        try:
            return pd.DataFrame(req.json())
        except ValueError:
            return pd.DataFrame()

    def fetchLoanEmi(self,params=None):
        req = self.fetchUrl(extendurl='/loanemi')
        try:
            return pd.DataFrame(req.json())
        except ValueError:
            return pd.DataFrame()

    def fetchUrl(self,extendurl,params=None):
        if params is None:
            startDate, endDate = self.getStartEndDateString()
            params = {'from': startDate, 'to': endDate}
        req = requests.get(self.url+extendurl, params=params)
        return req

    def getStartEndDate(self):
        month = datetime.today().month
        year = datetime.today().year
        startDate = datetime(year,month,1)
        endDate = datetime(year,month,self.getMonthBoundaries(month))
        return (startDate,endDate)

    def getStartEndDateString(self):
        startDate,endDate=self.getStartEndDate()
        firstDate  = f'{startDate.year}-{self.formatMonth(startDate.month)}-{startDate.day}'
        endDate   = f'{endDate.year}-{self.formatMonth(endDate.month)}-{endDate.day}'
        return (firstDate,endDate)

    def formatMonth(self,month):
        if month < 10:
            return f"0{month}"
        else:
            return month

    def getMonthBoundaries(self,month,isLeapYear=False):
        if month==1:
            return 31
        elif month==2:
            if isLeapYear:
                return 29
            else:
                return 28
        elif month==3:
            return 31
        elif month==4:
            return 30
        elif month==5:
            return 31
        elif month==6:
            return 30
        elif month==7:
            return 31
        elif month==8:
            return 31
        elif month==9:
            return 30
        elif month==10:
            return 31
        elif month==11:
            return 30
        else:
            return 31

    def getData(self):
        return self.fetchedData

    def __str__(self):
        return self.fetchedData




if __name__ == "__main__":
    print("***")
    re = BaseReport()
    print(re.__str__())
