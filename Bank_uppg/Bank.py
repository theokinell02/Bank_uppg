#!/usr/bin/env python
# coding: utf-8

# In[8]:


import DataSource as data_source
import Customer as Customer

class Bank:
    customer_list = []
    gl_customer_id = 1000
    gl_acc_id = 1000
    gl_transaction_id = 0
    
    def load(self):
        self.customer_list.clear()
        ds = data_source.DataSource()
        customer_list_str = ds.get_all()
        start_index = 0
        for customer in customer_list_str:
            customer_id = int(customer[:customer.index(":")])
            start_index = customer.index(":", start_index + 1) + 1
            customer_name = customer[start_index:customer.index(":", start_index + 1)]
            start_index = customer.index(":", start_index + 1) + 1
            customer_pnr = int(customer[start_index:customer.index(":", start_index + 1)])
            start_index = customer.index(":", start_index + 1) + 1
            customer_acc_list_str = customer[start_index:len(customer) - 1]
            if(customer_acc_list_str.find("#") != -1):
                last_acc_id = int(customer_acc_list_str[customer_acc_list_str.rindex("#") + 1: customer_acc_list_str.index(":", customer_acc_list_str.rindex("#"))])
            else:
                last_acc_id = int(customer_acc_list_str[:customer_acc_list_str.index(":")])
            if(self.gl_acc_id < last_acc_id):
                    self.gl_acc_id = last_acc_id
            self.customer_list.append(Customer.Customer(customer_id, customer_name, customer_pnr, self.gl_transaction_id, customer_acc_list_str))
            start_index = 0
        self.gl_acc_id += 1
        self.gl_customer_id = customer_id + 1
    
    def get_customers(self):
        customer_list = []
        for customer in self.customer_list:
            customer_list.append([customer.name, customer.pnr])
        return customer_list
    
    def add_customer(self, name, pnr):
        ds = data_source.DataSource()
        customer_list = self.get_customers()
        for customer in customer_list:
            if(customer[1] == pnr):
                return False
        ds.add_customer(self.gl_customer_id, name, pnr, self.gl_acc_id)
        self.customer_list.append(Customer.Customer(self.gl_customer_id, name, pnr, self.gl_transaction_id, "", self.gl_acc_id))
        self.gl_acc_id += 1
        return True
    
    def get_customer(self, pnr):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        if(customer_str == None):
            return -1
        for customer in self.customer_list:
            if(customer.id == int(customer_str[0:customer_str.index(":")])):
                acc_info = []
                for acc in customer.acc_list:
                    acc_info.append([acc.acc_id, acc.acc_type, acc.balance])
                return [customer.name, customer.pnr, acc_info]
    
    def change_customer_name(self, name, pnr):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        result = ds.update_by_id(customer_str[0: customer_str.index(":")], "name", name)
        if(result == -1):
            return False
        for customer in self.customer_list:
            if(customer.id == int(customer_str[0:customer_str.index(":")])):
                customer.name = name
        return True
    
    def remove_customer(self, pnr):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        if(customer_str == None):
            return -1
        balance = 0
        customer_info = self.get_customer(pnr)
        for acc in customer_info[2]:
            balance += acc[2]
        customer_info.append(balance)
        ds.remove_by_id(customer_str[:customer_str.index(":")])
        i = 0
        for customer in self.customer_list:
            if(customer.id == int(customer_str[0:customer_str.index(":")])):
                del self.customer_list[i]
            i += 1
        i = 0
        return customer_info
    
    def add_account(self, pnr):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        if(customer_str == None):
            return -1
        ds.add_account(customer_str[0: customer_str.index(":")], self.gl_acc_id)
        self.load()
        customer_str = ds.find_by_pnr(pnr)
        return int(customer_str[customer_str.rindex("#") + 1: customer_str.index(":", customer_str.rindex("#"))])
    
    def get_account(self, pnr, account_id):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        for customer in self.customer_list:
            if(customer.id == int(customer_str[0:customer_str.index(":")])):
                for acc in customer.acc_list:
                    if(acc.acc_id == account_id):
                        return "konto nummer: " + str(acc.acc_id) + ", saldo: " + str(acc.balance) + ", konto typ: " + acc.acc_type
        return -1
    
    def deposit(self, pnr, account_id, amount):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        for customer in self.customer_list:
            if(customer.id == int(customer_str[0:customer_str.index(":")])):
                i = 0
                for acc in customer.acc_list:
                    if(acc.acc_id == account_id):
                        acc.balance += amount
                        ds.update_by_id(customer.id, i, acc.balance)
                        customer.add_transaction(account_id, amount)
                        i = 0
                        return True
                    i += 1
        return False
                    
    def withdraw(self, pnr, account_id, amount):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        for customer in self.customer_list:
            if(customer.id == int(customer_str[0:customer_str.index(":")])):
                i = 0
                for acc in customer.acc_list:
                    if(acc.acc_id == account_id):
                        acc.balance -= amount
                        ds.update_by_id(customer.id, i, acc.balance)
                        customer.add_transaction(account_id, float("-" + str(amount)))
                        i = 0
                        return True
                    i += 1
        return False
    
    def close_account(self, pnr, account_id):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        if(customer_str == None):
            return -1
        balance = float(customer_str[customer_str.rindex(":") + 1: len(customer_str) - 1])
        result = ds.remove_account(customer_str[0:customer_str.index(":")], account_id)
        if(result == -1):
            return -1
        self.load()
        return balance
    
    def get_all_transactions_by_pnr_acc_nr(self, pnr, acc_nr):
        ds = data_source.DataSource()
        customer_str = ds.find_by_pnr(pnr)
        transaction_list = []
        for customer in self.customer_list:
            if(customer.id == int(customer_str[0:customer_str.index(":")])):
                for acc in customer.acc_list:
                    if(acc.acc_id == acc_nr):
                        for transaction in customer.transaction_list:
                            if(acc_nr == transaction.acc_id):
                                transaction_list.append([transaction.id, transaction.customer_id, transaction.acc_id, transaction.date, transaction.amount])
                        return transaction_list
                return -1
        return -1


# In[ ]:




