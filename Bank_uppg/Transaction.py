#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime

class Transaction:
    id = 0
    customer_id = 0
    acc_id = 0
    date = ""
    amount = 0
    
    def __init__(self, id, customer_id, acc_id, amount):
        self.id = id
        self.customer_id = customer_id
        self.acc_id = acc_id
        self.date = str(datetime.datetime.now())
        self.amount = amount

