import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup as soup
import os
import re
import json
import collections
from bson import json_util

#from lxml.html.soupparser import fromstring
#from urllib.request import urlopen as uReq
#def pastclasses(profname):


client = MongoClient()
db = client.coursedb
#courses = db.courses

#fall17 = '../UD_DB/fall17.html'
#summer18 = '../UD_DB/spring17.html' ["Fall 2014", '../UD_DB/fall14.html'],
coursefiles = [["Spring 2015", '../UD_DB/spring15.html'],
 ["Fall 2015", '../UD_DB/fall15.html'],["Spring 2016", '../UD_DB/spring16.html'],
 ["Fall 2016", '../UD_DB/fall16.html'],["Spring 2017", '../UD_DB/spring17.html'], 
 ["Fall 2017", '../UD_DB/fall17.html'],["Spring 2018", '../UD_DB/spring18.html']]

for f in coursefiles:

    mysoup= soup(open(f[1], encoding='utf-8'), "html.parser")
    semester = f[0]
    breaks = mysoup.findAll("span")

    for i in range(len(breaks)):
        if "Instructor" in breaks[i].text or "Leader" in breaks[i].text : 
            courseid = ""
            coursename = ""
            time = ""
            preptime = ""
            description = ""
            limit = "no limit"
            tocontinue = False
            instructors = []
            front =  breaks[i].text
            if len(breaks[i-2].text) == 4:
                courseid = breaks[i-2].text.strip('\n')
                cour = breaks[i-1].text
                for s in cour.split('\n'):
                    coursename += " " + s
                coursename = re.sub(' +',' ',coursename)
                coursename.lstrip()
                if courseid[1:3].isdigit():
                    tocontinue = True
            elif len(breaks[i-2].text.split(" ")[0]) == 3:
                courseid = breaks[i-2].text.split(" ")[0]
                cour = breaks[i-2].text[4:] + " " + breaks[i-1].text
                for s in cour.split('\n'):
                    coursename += s
                coursename = re.sub(' +',' ',coursename)
                coursename.lstrip()
                if courseid[1:3].isdigit():
                    tocontinue = True
                    
            lines = front.split("\n")
            multinst = False
            if tocontinue:
                if "**" in coursename:
                    preptime = "2+ hours"
                    coursename = coursename[:coursename.index("*")]
                elif "*" in coursename:
                    preptime = "1-2 hours"
                    coursename = coursename[:coursename.index("*")]   
                else:
                    preptime = "0-1 hours"
                #print(coursename)    
                for line in lines:
                    if "a.m." in line or "p.m." in line:
                        time = line
                        #print(time)
                    elif "Leader" in line or "Instructor" in line:
                        if "," in line:
                            try:
                                ins = line[line.index(":")+2:].split(",")
                                for i in ins:
                                    instructors.append(i.strip())
                                    #print(ins)
                            except:
                                print("e")
                                pass
                        else:
                            try:
                                instructors.append(line[line.index(":")+2:].strip())
                                print(instructors)
                            except:
                                print("e")
                                pass
                    else:
                        description += " " + line
                description.lstrip()
                #print(description)
            
                      
                for n in range(1,3):
                    try:
                        if "Limited" in breaks[i+n].text:
                            limit = breaks[i+n].text.strip('\n')
                    except:
                        pass
                try:
                    course = {
                        'coursename': coursename,
                        'instructors': instructors,
                        'coursenum': courseid,
                        'semesters': [semester],
                        'category': courseid[0],
                        'time': [time],
                        'prep time': preptime,
                        'limited to': limit,
                        'description': description
                    }
                    print(course)
                    if db.courses.find({'coursename': coursename}).count() > 0:
                        db.courses.update({'coursename': coursename}, 
                            { '$push': {'semesters': semester,
                                        'time': time}

                            })
                    else:
                        db.courses.update({'coursename': coursename}, course, upsert=True)
                    
                except:
                    print("e")
                    pass
                
            



