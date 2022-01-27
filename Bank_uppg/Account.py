#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Account:
    balance = 0.0
    acc_type = "debit account"
    acc_id = -1
    
    def __init__(self, acc_id, balance=0.0):
        self.balance = balance
        self.acc_id = acc_id


