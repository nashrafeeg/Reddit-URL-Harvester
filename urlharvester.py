#!/usr/bin/python
#
# Copyright (C) 2011  Nashath Rafeeq.
#   Reddit Url Harvester  V.0.0.1
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'nash.rafeeg@gmail.com (Nash Rafeeg)'


import os.path
import os
import urllib
from urlparse import urlparse

def dir_list2(dir_name, *args):
        #look into the current working directory and append all files to and array and return it 
        fileList = []
        for file in os.listdir(dir_name):
                dirfile = os.path.join(dir_name, file)
                if os.path.isfile(dirfile):
                        if len(args) == 0:
                                fileList.append(dirfile)
                        else:
                                if os.path.splitext(dirfile)[1][1:] in args:
                                        fileList.append(dirfile)
        
        """
        elif os.path.isdir(dirfile):
        print "Accessing directory:", dirfile
        fileList += dir_list2(dirfile, *args)
        """
        return fileList
def graburlsfiles(fileList):
        #method to look for files that end in urls
        urlfileList = []
        for file in fileList:
            s = os.path.splitext(file)
            if s[1] == ".urls":
                    urlfileList.append(file)
        return urlfileList

def validurls(dirtyurl):
        #try to see if the url grabed is a valid url 
        try: 
                urllib.urlopen(dirtyurl)        #this is very inefficent way of checking if its a valid url if reddit 404 or 502 will show up as a bad url if this happens re run the script
                print "validated %s" %dirtyurl
                return True
        except IOError:
                print "%s seem to be bad url" %dirtyurl
                return False

def graburls(urlfiles):
        #grab urls from .urls files and return it 
        cleanurls = []
        for ufiles in urlfiles: 
                file = open(ufiles, "r")
                dirty_urls = file.readlines()
                for url in dirty_urls:
                        print "validating"
                        if validurls(url):
                                cleanurls.append(url)
        return cleanurls

def findeimagelinks(url):
        import urllib2
        import json
        import csv
        import hashlib
        import datetime
        
        try: 
                
                downloadfile = csv.writer(open('files.csv', 'w'), delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL) #open csv file for writing will overwrite previouse file
                u = urllib2.urlopen(url) #open the url and get .JSON file
        
                objects = json.load(u)['data']                                                                  #look for the element 'data'
                children = objects['children']                                                                  #look for element children inside data 
                for c in children:             
                        keys = c.get("data")                                                                    #look for a data keys 
                        imgsrc =  keys.get("url")                                                               #the link 
                        imgname = keys.get("title")                                                             #post titile
                        urlparts = urlparse(keys.get("url"))
                        ext = os.path.splitext(urlparts.path)[1]                                                #try to get extention of the file 
                        hash = hashlib.sha224(imgsrc).hexdigest()                                               #future use hash the url genrate unique keys 
                        adddate = datetime.datetime.now()                                                       #the date and time addeed 
                        downloaddate = ""                                                                       #futur use 
                        flag = "tbd"                                                                            #futue use 
                        csvobj = [imgsrc, imgname.encode('ascii','ignore'), keys.get("domain"), ext, hash, adddate, downloaddate, flag] #creat csv object 
                        downloadfile.writerow(csvobj)                                                           #write csv object to file
        except IOError:
                pass 




if __name__ == '__main__':
        fileList = dir_list2('/home/nash/picdownloader')                                                        #path to dir containing the .urls change this 
        urlfiles = graburlsfiles(fileList)
        urls = graburls(urlfiles)
        for ur in urls:
                findeimagelinks(ur)
                print "Havested urls from %s" %ur
