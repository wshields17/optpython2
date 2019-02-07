from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,QTableWidgetItem
#import openpyxl
##from binomamer import binomialCallAmerican as binAm
from optioncalc import Ui_MainWindow  # importing our generated file
import py_vollib.black_scholes_merton.implied_volatility as BSvol
import py_vollib.black_scholes_merton as BSprice
import py_vollib.black_scholes_merton.greeks.analytical as BSgreeks
import py_vollib.black_scholes_merton.greeks.numerical as BSgreeksN
import sys
import QuantLib as ql
import ameroptmodels as amodel
from datetime import date
import urllib
import re
import time
import sys
from iexfinance.stocks import Stock
from dateutil.parser import parse

def fetchstockquotes(symbol):
    #base_url = 'https://api.iextrading.com/1.0/stock/'
    #quote1 = urllib.request.urlopen(base_url + symbol +'/price').read()
        
    #return quote1.decode("utf-8")
    
    qqq = Stock(symbol)
    prc=qqq.get_price()   
    return prc

def multtex(tex1,tex2):
    return str((float(tex1)* float(tex2)))


       

class mywindow(QtWidgets.QMainWindow):

   def __init__(self):

      super(mywindow, self).__init__()

      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.ui.dividend.setText("0") 
      self.ui.intrate.setText("0.02")
      self.ui.corp.setText("c")
      #self.ui.Percentage.setText(".85") 

      self.ui.Compbutton_2.clicked.connect(self.btnClicked)
      self.ui.Compbutton.clicked.connect(self.btnClicked2)
      self.ui.actionExit.triggered.connect(self.testf)
      self.ui.actionOpen.triggered.connect(self.fd)
      #self.ui.table1.setColumnCount(4)
        
      #self.ui.table1.setRowCount(40)

      #self.ui.actionExit()=sys.exit(app.exec())
      #lvprice = si.get_live_price("qqq")
      lvprice = fetchstockquotes('qqq')
      self.ui.StPrice.setText(str(lvprice))  
      self.ui.Strike.setText('160')
      self.ui.intrate.setText('.02')
      self.ui.optprice.setText(str(2))
      self.ui.volatility.setText(str(.2))
      self.ui.Days.setText('2/15/2019')
   


   def testf(self):
       
      sys.exit()   

   def fd(self):
      options = QFileDialog.Options()
      options |= QFileDialog.DontUseNativeDialog
      fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Excel Files (*.xlsx)", options=options)
     
      #wb = openpyxl.load_workbook(fileName)
      #sheet = wb.active
      #for i in range (3,20):
      #   for j in range(2,5 ):   
      #       cellinfo = str(sheet.cell(row=i, column=j).value ) 
      #       curcell = QTableWidgetItem(cellinfo)
      #       self.ui.OutWeight.setText(cellinfo) 
     
      #       self.ui.table1.setItem(i,j-1,curcell)
      

   def btnClicked(self):
      
      price = float(self.ui.StPrice.toPlainText()) 
      strike = float(self.ui.Strike.toPlainText())
      expd = self.ui.Days.toPlainText()
      rate =  float(self.ui.intrate.toPlainText())
      divd =  float(self.ui.dividend.toPlainText())
      cp = self.ui.corp.toPlainText() 
       
      optprice1 = float(self.ui.optprice.toPlainText()) 
      calcdate = date.today()
      expdate1 = parse(expd)
      expdate = expdate1.date()
      days2 = expdate - calcdate
      days = days2.days/365
      
      vol = BSvol.implied_volatility(optprice1,price , strike, days, rate,divd, cp)
      delt = BSgreeksN.delta(cp,price,strike, days, rate,vol,divd)
      vega = BSgreeksN.vega(cp,price,strike, days, rate,vol,divd)
      gamma = BSgreeksN.gamma(cp,price,strike, days, rate,vol,divd)
      theta = BSgreeksN.theta(cp,price,strike, days, rate,vol,divd)
      self.ui.volatility.setText(str(vol))
      self.ui.Delta1.setText(str(delt))
      self.ui.Theta1.setText(str(theta))
      self.ui.Gamma1.setText(str(gamma))
      self.ui.Vega1.setText(str(vega)) 
      
      #stockprice = Stock('qqq').price()
      #self.ui.StPrice.setText(str(stockprice))

   def btnClicked2(self):
     
      price = float(self.ui.StPrice.toPlainText()) 
      strike = float(self.ui.Strike.toPlainText())
      #dayst = float(self.ui.Days.toPlainText())
      expd = self.ui.Days.toPlainText()
      #days = dayst/365.0
      
      rate =  float(self.ui.intrate.toPlainText())
      divd =  float(self.ui.dividend.toPlainText())
      cp = self.ui.corp.toPlainText() 
      calcdate = date.today() 
      vol = float(self.ui.volatility.toPlainText())
      expdate1 = parse(expd)
      expdate = expdate1.date()
      #expdate = date(2019, 2, 15)
      days2 = expdate - calcdate
      days3 = days2.days/365
      modelname = 'crr'
      steps = 500
      price1 = amodel.binomialmodels(price,strike,vol,rate,calcdate,expdate,divd,cp,modelname,steps)
      #price1 = BSprice.black_scholes_merton(cp,price,strike,days,rate,vol,divd)
      #price2 = binAm(price,strike,days,rate,vol,1000)
      delt = BSgreeksN.delta(cp,price,strike, days3, rate,vol,divd)
      vega = BSgreeksN.vega(cp,price,strike, days3, rate,vol,divd)
      gamma = BSgreeksN.gamma(cp,price,strike, days3, rate,vol,divd)
      theta = BSgreeksN.theta(cp,price,strike, days3, rate,vol,divd)
      self.ui.optprice.setText(str(price1))
      self.ui.Delta1.setText(str(delt))
      self.ui.Theta1.setText(str(theta))
      self.ui.Gamma1.setText(str(gamma))
      self.ui.Vega1.setText(str(vega))
      self.ui.Gamma1.setText(str(days2.days))
        

app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())
