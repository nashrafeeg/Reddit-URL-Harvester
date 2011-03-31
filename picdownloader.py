import os.path
import os
import urllib
from urlparse import urlparse
def dir_list2(dir_name, *args):
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
        urlfileList = []
        for file in fileList:
            s = os.path.splitext(file)
            if s[1] == ".urls":
                    urlfileList.append(file)
        return urlfileList
def validurls(dirtyurl):
        try: 
                urllib.urlopen(dirtyurl)
                print "validated %s" %dirtyurl
                return True
        except IOError:
                print "%s seem to be bad url" %dirtyurl
                return False

def graburls(urlfiles):
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
                
                downloadfile = csv.writer(open('files.csv', 'w'), delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                u = urllib2.urlopen(url)
        
                objects = json.load(u)['data']
                children = objects['children']
                for c in children: 
                        keys = c.get("data")
                        imgsrc =  keys.get("url")
                        imgname = keys.get("title")
                        urlparts = urlparse(keys.get("url"))
                        ext = os.path.splitext(urlparts.path)[1]
                        hash = hashlib.sha224(imgsrc).hexdigest()
                        adddate = datetime.datetime.now()
                        downloaddate = ""
                        flag = "tbd"
                        csvobj = [imgsrc, imgname.encode('ascii','ignore'), keys.get("domain"), ext, hash, adddate, downloaddate, flag]
                        downloadfile.writerow(csvobj)
        except IOError:
                pass 




if __name__ == '__main__':
        fileList = dir_list2('/home/nash/picdownloader')
        urlfiles = graburlsfiles(fileList)
        urls = graburls(urlfiles)
        for ur in urls:
                findeimagelinks(ur)
                print "Havested urls from %s" %ur
