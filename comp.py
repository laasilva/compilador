# -*- coding: utf-8 -*-

               
c = open("code.txt", "r")

if c.mode == "r":
    content = c.readlines()
    if "_START_" in content:
        print ("start of code")