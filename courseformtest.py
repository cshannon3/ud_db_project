import sys
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup as soup

client = MongoClient()
db = client.coursedb
courses = db.courses

	

	
	#form = '../../../../Downloads/Standard_Course Proposal_Form_2018_Fall.html'
form = './courseform.html'

fsoup = soup(open(form , encoding='utf-8'), "html.parser")
#Go Through each span line
shouldprint = False
for eachcourse in courses.find({'semesters':{'$all':["Spring 2018", "Fall 2017", "Spring 2017"]}}):
#eachcourse = courses.find_one()
    coursenametext = ''
    for key, value in eachcourse.items():
        #print(value)
        if key == 'instructors':
            for inst in range(len(value)):
                if inst == 0:
                    instructoronediv =  fsoup.find("input", {"id": "instructor1name"})
                    dvl = fsoup.new_tag("input", type="text", id="instructor1name", value=value[inst], size="40")
                    instructoronediv.replace_with(dvl)
                elif inst == 1:
                    instructortwodiv =  fsoup.find("input", {"id": "instructor2name"})
                    dvl = fsoup.new_tag("input", type="text", id="instructor2name", value=value[inst], size="40")
                    instructortwodiv.replace_with(dvl)
        elif key == 'coursename':
            coursenametext = value
            coursename = fsoup.find("input", {"id": "coursename"})
            dvl = fsoup.new_tag("input", type="text", id="coursename", value=value, size="80")
            coursename.replace_with(dvl)
        elif key == 'semesters':
            previousSem = ''
            for s in value:
                previousSem += s + " "
            sval = fsoup.find("input", {"id": "lasttaught"})
            dvl = fsoup.new_tag("input", type="text", id= "lasttaught", value= previousSem, size="80")
            sval.replace_with(dvl)
        elif key == 'category':
            try:
                sval = fsoup.find("input", {"id": value})
                dvl = fsoup.new_tag("input", type="checkbox", id=value, checked="")
                sval.replace_with(dvl)
            except:
                pass
        elif key == 'time':
            timeinfo = ''
            for t in value:
                if t not in timeinfo:
                    timeinfo+= t + ", "
            sval = fsoup.find("input", {"id": "timeinfo"})
            dvl = fsoup.new_tag("input", type="text", id= "timeinfo", value= timeinfo, size="80")
            sval.replace_with(dvl)
        elif key == 'prep time':
            if value == "1-2 hours":
                print(value)
                sval = fsoup.find("input", {"id": "onestar"})
                dvl = fsoup.new_tag("input", type="checkbox", id="onestar", checked="")
                sval.replace_with(dvl)
            elif value == "2+ hours":
                print(value)
                sval = fsoup.find("input", {"id": "twostar"})
                dvl = fsoup.new_tag("input", type="checkbox", id="twostar", checked="")
                sval.replace_with(dvl)
            else:
                sval = fsoup.find("input", {"id": "nostar"})
                dvl = fsoup.new_tag("input", type="checkbox", id="nostar", checked="")
                sval.replace_with(dvl)
        elif key == 'limited to':
            maxen =  fsoup.find("input", {"id": "max_enrollment"})
            newinst2 = fsoup.new_tag("input", type="text", id="max_enrollment", value=value)
            maxen.replace_with(newinst2)
        elif key == 'description':
            des = fsoup.find("textarea", {"id": "description"})
            des.string = value

           
       
    html = fsoup.prettify("utf-8")
    filename = "outputs/" + coursenametext + ".html"
    with open(filename, "wb") as file:
        file.write(html)
    fsoup = soup(open(form , encoding='utf-8'), "html.parser")