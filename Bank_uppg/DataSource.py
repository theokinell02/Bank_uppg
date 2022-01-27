#!/usr/bin/env python
# coding: utf-8

# In[31]:


path = "D:\\School\\Bank_uppg_mockdata.txt"

class DataSource:
    def datasource_conn():
        text_file = open(path)
        if(text_file.readable):
            text_file.close()
            return [True, "Connection successful"]
        text_file.close()
        return[False, "Connection unsuccessful"]
    
    def get_all(self):
        text_file = open(path)
        customer_list = text_file.readlines()
        text_file.close()
        return customer_list
    
    def update_by_id(self, id, target, input):
        flag = True
        customer_list = self.get_all()
        i = 0
        out_customer = ""
        for customer in customer_list:
            if(customer[0:customer.index(":")] == str(id)):
                start_index = customer.index(":")
                if(target == "name"):
                    customer = customer[0:start_index + 1] + input +  customer[customer.index(":", start_index + 1):]
                    flag = False
                    out_customer = customer
                elif(target == "pnr"):
                    start_index = customer.index(":", start_index + 1)
                    customer = customer[0:start_index + 1] + str(input) +  customer[customer.index(":", start_index + 1):]
                    flag = False
                    out_customer = customer
                elif(target == 0):
                    for x in range(4):
                        start_index = customer.index(":", start_index + 1)
                    customer = customer[0:start_index + 1] + str(input)
                    flag = False
                    out_customer = customer
                else:
                    for x in range(0,target):
                        start_index = customer.index("#", start_index + 1)
                    start_index = customer.index(":", start_index + 1)
                    start_index = customer.index(":", start_index + 1)
                    customer = customer[0:start_index + 1] + str(input) + customer[customer.index(":", start_index + 1):]
                    flag = False
                    out_customer = customer
            customer_list[i] = customer
            i += 1
        if(flag):
            return -1
        text_file = open(path, "w")
        for customer in customer_list:
            text_file.write(customer)
        text_file.close()
        return out_customer
            
    def find_by_id(self, id):
        customer_list = self.get_all()
        for customer in customer_list:
            if(customer[:customer.index(":")] == str(id)):
                return customer
        return -1
    
    def find_by_pnr(self, pnr):
        customer_list = self.get_all()
        start_index = 0
        for customer in customer_list:
            start_index = customer.index(":", start_index + 1)
            start_index = customer.index(":", start_index + 1)
            if(customer[start_index + 1:customer.index(":", start_index + 1)] == str(pnr)):
                return customer
            start_index = 0
                
    def remove_by_id(self, id):
        text_file = open(path, "r")
        customer_list = text_file.readlines()
        text_file.close()
        i = 0
        for customer in customer_list:
            if(customer[0:customer.index(":")] == str(id)):
                del customer_list[i]
            i += 1
        text_file = open(path, "w")
        for customer in customer_list:
            text_file.write(customer)
        text_file.close()
    
    def add_customer(self, id, name, pnr, acc_id):
        customer = str(id) + ":" + name + ":" + str(pnr) + ":" + str(acc_id) + ":debit account:0.0\n"
        customer_list = self.get_all()
        customer_list.append(customer)
        text_file = open(path, "w")
        for customer in customer_list:
            text_file.write(customer)
        text_file.close()
        
    def add_account(self, id, acc_id):
        customer = self.find_by_id(id)
        temp_customer = customer
        customer = customer[:len(customer) - 1] + "#" + str(acc_id) + ":debit account:0.0\n"
        customer_list = self.get_all()
        i = 0
        for x in customer_list:
            if(x == temp_customer):
                customer_list[i] = customer
                break
            i += 1
        text_file = open(path, "w")
        for customer in customer_list:
            text_file.write(customer)
        text_file.close()
        
    def remove_account(self, id, acc_id):
        customer = self.find_by_id(id)
        start_index = 0
        for x in range(3):
            start_index = customer.index(":", start_index + 1)
        if(customer.find(str(acc_id), start_index, customer.index(":", start_index + 1)) != -1):
            if("#" in customer):
                customer = customer[:start_index] + ":" + customer[customer.index("#") + 1:]
            else:
                self.remove_by_id(id)
        elif("#" in customer[customer.index("#" + str(acc_id), customer.index("#")) + len(str(acc_id)) + 1:]):
            start_index = customer.index("#" + str(acc_id), customer.index("#"))
            customer = customer[:start_index] + customer[customer.index("#", start_index + 1):]
        elif(customer[customer.rindex("#") + 1: customer.index(":", customer.rindex("#"))] == str(acc_id)):
            customer = customer[:customer.rindex("#")] + "\n"
        else:
            return -1
        i = 0
        customer_list = self.get_all()
        for temp_customer in customer_list:
            if(temp_customer[0:temp_customer.index(":")] == str(id)):
                break
            i += 1
        customer_list[i] = customer
        text_file = open(path, "w")
        for customer in customer_list:
            text_file.write(customer)
        text_file.close()


# In[ ]:




