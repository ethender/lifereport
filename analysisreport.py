from basereport import BaseReport as base
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

class AnalysisReport:


    def __init__(self):
        self.base = base()
        self.defaultCurrency = '£'

    def checkCurrenciesAmount(self,df, currencyLabel='currency', amountLabel='amount'):
        temp = {}
        if not df.empty:
            for currency in df[currencyLabel].unique():
                amount = df[df[currencyLabel] == currency][amountLabel].sum()
                temp[currency] = amount
        return temp

    def getSummary(self):
        data = self.base.getData()
        summary = {}
        summary['Credits'] = self.checkCurrenciesAmount(data['credits'])
        summary['Expense'] = self.checkCurrenciesAmount(data['expense'])
        summary['Investment'] = self.checkCurrenciesAmount(data['investment'],currencyLabel='investcurrency',amountLabel='investamount')
        summary['Investment Gained'] = self.checkCurrenciesAmount(data['investmengained'])
        summary['Loan Emi'] = self.checkCurrenciesAmount(data['loanemi'])
        return pd.DataFrame(summary).fillna(0).T

    def getSummaryPlot(self,currency=None):
        summary = self.getSummary()
        t = io.BytesIO()
        plt.figure(figsize=(10,10))
        if currency is None:
            data = summary.loc[:,self.defaultCurrency]
        else:
            data = summary.loc[:,currency]
        #return data
        plt.pie(data, labels=data.index, autopct='%1.1f%%')
        plt.title('Summary')
        plt.savefig(t, format='png')
        return base64.b64encode(t.getvalue()).decode("utf-8").replace("\n", "")






    def getTestPlot(self):
        image = io.BytesIO()
        x = np.linspace(0, 10)
        y = np.sin(x)
        plt.plot(x, y)
        plt.savefig(image, format='png')
        return base64.b64encode(image.getvalue()).decode("utf-8").replace("\n","")

if __name__ == "__main__":
    print("***")
    re = AnalysisReport()
    print(re.getSummaryPlot())