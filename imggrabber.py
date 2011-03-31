import urllib2
import urllib
import random

class imggrab:
        def __init__(self,url, name, ext,  path, retry):
                self.path = path
                self.retry = retry
                #self.checkhd = checkhd
                self.url = url 
                self.name = name
                self.ext = ext 
        def useragent(self):
               uagen = []
               uagen = [
                       'Mozilla/4.0 (compatible; MSIE 2.0; Windows NT 5.0; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)', 
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25', 
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre'
               ]
               return uagen[random.randrange(0, len(uagen)-1)]
        
        def progress_callback(self, blocks, block_size, total_size):
               downloaded = float(blocks) * float(block_size)
               percent = (downloaded/float(total_size))*100
               size = (float(total_size) / 8)/1024
               block_sizes = (float(block_size) /8)/1024 
               print "Downloaded %i of %fKB size file with %s blockes sized %fKB each" % (int(percent), size,  blocks, block_sizes)
        
        def imagevarify(self, file):
                from PIL import Image
                from StringIO import StringIO
                
                try:
                        im = Image.open(file)
                        im.verify()
                        print "varified", im.format, "%dx%d" % im.size, im.mode
                        size = "[%dx%d]" % im.size
                        filename = self.name+size+self.ext
                        fullpath = self.path+filename
                        print fullpath 
                        s = Image.open(file)
                        s.save(fullpath)
                        print filename
                except Exception as e: 
                        print e
                        raise 
                        
        def get_image(self):
                while(self.retry >0):
                        try:
                                #headers = { 'User-Agent' : self.useragent()}
                                #req = urllib2.Request(self.url,None, headers)
                                #print "headers set %s" % headers
                                #response = urllib2.urlopen(req)
                                #print "Response set"
                                (file, headers) = urllib.urlretrieve(self.url,self.name, self.progress_callback)
                                print "downloaded binary object %s Passing to pil for varification" % headers
                                self.imagevarify(file)
                                break
                        except Exception as e: 
                                print e
                                print "Retying [%i]" % self.retry
                                self.retry -=1 
def getcsv(csvfilename, path, retry):
        import csv
        csvreader = csv.reader(open(csvfilename,'rb'), delimiter=    ';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in csvreader:
                url = row[0]
                name = row[1]
                ext = row[3]
                try:
                        img = imggrab(url, name, ext, path, retry)
                        img.get_image()
                        print "saved file"
                except Exception as e: 
                        print e 



if __name__ == '__main__':
        csvfile = 'files.csv'
        path = "/home/nash/Pictures/"
        retry = 1
        getcsv(csvfile, path, retry)
