#Currency Converter (using request lib. to get upated real time exchange rates from URL)

from msilib.schema import SelfReg
import re
from tkinter.font import BOLD
import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

class RealTimeCurrencyConverter():
    def __init__(self,url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'USD' :    
            amount = amount / self.currencies[from_currency] 

        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.resizable(0,0)
        self.title("Currency Converter")
        self.title = 'Currency Converter'
        self.currency_converter = converter

        self.configure(background = '#a1d1ae')
        self.geometry("500x200")
        
        #header
        heading = Label(self, text = 'Currency Converter' , font ='arial 17 bold', bg='#a1d1ae').pack()        
        body = Label(self, text = 'Use this calculator to convert any \n amount of money from one currency to another!', font ='arial 11 bold', bg='#a1d1ae').pack()
        instruc = Label(self, text = 'Enter an amount, then press "Convert"', font ='arial 10 bold', fg = 'RED', bg='white').pack()
        
        #fields
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self,bd = 1, relief = FLAT, justify = tk.CENTER,validate='key', validatecommand=valid)
        self.converted_amount_field_label = Label(self, bd = 1, text = '', fg = 'black', bg = 'white', relief = FLAT, justify = tk.CENTER, width = 17, borderwidth = 3)

        #Dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("CAD") # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD") # default value
        font = ("Courier", 12, "bold")
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)

        #positsions
        self.from_currency_dropdown.place(x = 30, y= 120)
        self.amount_field.place(x = 38, y = 150)
        self.to_currency_dropdown.place(x = 340, y= 120)
        self.converted_amount_field_label.place(x = 348, y = 150)
        
        # Convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", font = BOLD, command = self.perform) 
        self.convert_button.config(font=('Courier', 12, 'bold'))
        self.convert_button.place(x = 215, y = 125)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text = str(converted_amount))
    
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'   #exchange api / base is USD
    converter = RealTimeCurrencyConverter(url)

    App(converter)
    mainloop()

