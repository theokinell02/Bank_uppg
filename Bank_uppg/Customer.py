#!/usr/bin/env python
# coding: utf-8

# In[34]:


import Account as Acc
import Transaction as transaction

class Customer:
    id = -1
    name = ""
    pnr = 0
    acc_list = []
    transaction_list = []
    gl_transaction_id = 0
    
    def __init__(self, id, name, pnr, gl_transaction_id, acc_list_str="", account_id=900):
        self.id = id
        self.name = name
        self.pnr = pnr
        self.gl_transaction_id = gl_transaction_id
        self.acc_list = []
        self.transaction_list = []
        if(acc_list_str == ""):
            self.acc_list.append(Acc.Account(account_id))
        else:
            if("#" in acc_list_str):
                temp_acc_list_str = acc_list_str
                for acc in range(acc_list_str.count("#")):
                    acc_str = temp_acc_list_str[:temp_acc_list_str.index("#")]
                    acc_id = int(acc_str[:acc_str.index(":")])
                    acc_balance = float(acc_str[acc_str.rindex(":") + 1:])
                    self.acc_list.append(Acc.Account(acc_id, acc_balance))
                    temp_acc_list_str = temp_acc_list_str[temp_acc_list_str.index("#") + 1:]
                    
                acc_id = int(acc_list_str[acc_list_str.rindex("#") + 1:acc_list_str.index(":", acc_list_str.rindex("#") + 1)])
                acc_balance = float(acc_list_str[acc_list_str.rindex(":") + 1:])
                self.acc_list.append(Acc.Account(acc_id, acc_balance))
            else:
                acc_id = int(acc_list_str[:acc_list_str.index(":")])
                acc_balance = float(acc_list_str[acc_list_str.rindex(":") + 1:])
                self.acc_list.append(Acc.Account(acc_id, acc_balance))
    
    def add_transaction(self, acc_id, amount):
        self.transaction_list.append(transaction.Transaction(self.gl_transaction_id, self.id, acc_id, amount))
        self.gl_transaction_id += 1
         

# In[ ]:




