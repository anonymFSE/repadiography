import sys, os, string
import urllib
import zipfile
import subprocess
from optparse import OptionParser
import math
from PIL import Image
from random import randint


class Apk2Png:
    external = "https://github.com/scaruso/ToolAndroguard/files/2101469/tool.zip"

    def __init__(self):
        self.home = ''
        self.tool = ''
        self.outdir = ''
        self.apk_file_1 = ''
        self.apk_file_2 = ''
        self.project_name = ''
        self.report=''
        self.image = ''
        self.apk=''

    def _call(self, cmd, **kwargs):
        print('Running: {0}'.format(' '.join(cmd)))
        return subprocess.call(cmd, **kwargs)

    def _report(self, blocknr, blocksize, size):
        current = blocknr * blocksize
        sys.stdout.write("\rProgress: {0:.2f}%".format(100.0 * current / size) + " - {0:.1f} MB".format(
            current / 1024 / 1024) + "/{0:.1f} MB".format(size / 1024 / 1024))

    def _check_home(self, path):
        return os.path.isdir(path + "/tool")

    def _getunzipped(self, theurl, thedir, report):
        if not os.path.exists(thedir):
            os.mkdir(thedir)
        print("Downloading external tool... -> " + thedir + "/tool/")
        name = os.path.join(thedir, 'temp.zip')
        try:
            name, hdrs = urllib.request.urlretrieve(theurl, name, report)
        except IOError as e:
            print("Can't retrieve %r to %r: %s" % (theurl, thedir, e))
            return
        try:
            z = zipfile.ZipFile(name)
        except zipfile.error as e:
            print("Bad zipfile (from %r): %s" % (theurl, e))
            return
        for n in z.namelist():
            (dirname, filename) = os.path.split(n)
            perm = ((z.getinfo(n).external_attr >> 16) & 0x0777)
            if filename == '':
                # directory
                newdir = thedir + '/' + dirname
                if not os.path.exists(newdir):
                    os.mkdir(newdir)
            else:
                # file
                fd = os.open(thedir + "/" + n, os.O_CREAT | os.O_WRONLY, perm)
                os.write(fd, z.read(n))
                os.close(fd)
        z.close()
        os.unlink(name)
        print("")

    def check_tools(self, home):
        if self._check_home(home) == False:
            self._getunzipped(Apk2Png.external, home, self._report)
        self.home = home
        self.tool = os.path.join(self.home, 'tool/')

    def _print_header(self, text):
        block = "*********************************************"
        print(block)
        print('**' + text.center(len(block) - 4) + '**')
        print(block)

    def _androsim(self):
        f=open(self.project_name + ".txt", "w")
        self._print_header("Compare two 'apk'")
        os.chdir(self.tool)
        self._call(['python', 'androsim.py', '-i', self.apk_file_1, self.apk_file_2, '-c', 'ZLIB', '-n', '-d'], stdout=f)
        print('Done')

    def compare(self, file1, file2):
        if (os.path.splitext(file1)[-1] == '.apk') and (os.path.splitext(file2)[-1] == '.apk'):
            #os.chdir('/home/marianna/Scrivania/Image-Binary-Converter-master/Apk')
            #print("percorso corrente" + os.getcwd())
            self.apk=os.path.join(self.home , 'Apk/') 
            os.chdir(self.apk)
            #print("percorso corrente" + os.getcwd())
            self.apk_file_1 = self.apk + '/' + file1
            self.apk_file_2 = self.apk + '/' +file2
            os.chdir(self.home)
            self.report = os.path.join(self.home, 'Report')
            
            if not os.path.exists(self.report):
                    os.makedirs(self.report) 
            os.chdir(self.report)

            self.project_name= os.path.splitext(os.path.basename(file1))[0]+ "_" +os.path.splitext(os.path.basename(file2))[0]
            self.out = os.path.join(self.report, self.project_name)
            print self.out
            self._androsim()    

        else:
            raise Exception("You must select a valid APK file!")

    def getIdenticalMethods(self):
        os.chdir(self.report) 
        #print("percorso corrente" + os.getcwd()) 
        f=open(self.out + ".txt")
        output= open(self.project_name + "_i.txt", "w")
        s= set()
        #self.project_name = os.path.splitext(os.path.basename(file))[0].lower()
        #self.out = os.path.join(self.outdir, self.project_name)    
        for line in f:
            if line.strip()=='IDENTICAL methods:':
                break

        for line in f:
            if line.strip()=='NEW methods:':
                break 
            y= line.split('\t')[-1:]
            for el in y:
                y= el.split('; ')[1]
                x= y.split()[0]
                if 'values' not in x and '$' not in x and '<' not in x and len(x) != 1 and x[-1:] != '_' :
                    if x not in s:
                        s.add(x)                                
                        output.write(x + "\n")
        output.close()

    def getSimilarMethods(self):
        f=open(self.out + ".txt")
        output= open(self.project_name + "_s.txt", "w")   
        
        for line in f:
            if line.strip()=='SIMILAR methods:':
                break

        for line in f:
            if line.strip()=='IDENTICAL methods:':
                break
    
            if '-->' not in line:
                y2=line.split('\t')[-1]
                z2= y2.split(' (')[0]
                x2= z2.split('; ')[-1:][0]
                if 'values' not in x2 and '$' not in x2 and '<' not in x2 and len(x2) != 1 and x2[-1:] != '_' :
                    z2 = z2
            else:
                z= line.split(' (')
                x= z[0].split('--> ')[-1]
                y= x.split('; ')[-1:][0]
                if 'values' not in y and '$' not in y and '<' not in y and len(y) != 1 and y[-1:] != '_' :
                    t= (z[1].split('\n')[0]).split(' ')[-1]
                    output.write (z2 + " " + x + " " + t + "\n")

        output.close()

    def getNewMethods(self):
        f=open(self.out + ".txt")
        output= open(self.project_name + "_n.txt", "w")
        for line in f:
            if line.strip()=='NEW methods:':
                break

        for line in f:
            if line.strip()=='DELETED methods:':
                break
        
            x2= (line.split(' (')[0]).split('\t')[-1]
            if 'values' not in x2 and '$' not in x2 and '<' not in x2 and len(x2) != 1 and x2[-1:] != '_' :
                output.write(x2 + '\n')

        output.close() 
            
    def _capDimensions(self,width, height, maxPixels):
        imageSize = int(math.ceil(math.sqrt(maxPixels)))
        return (imageSize, imageSize)

    def getOriginalColors(self):
        apkOr= "/" + self.project_name
        f=open(self.report + apkOr + "_i.txt")
        num_methods_i=0
        num_methods_s=0
        index=0
        resultSet=[]
        binaryValues = []

        for line in f:
            first_c = ord(line[0])
            last_c = ord(line[-2])
            lenght_m = len(line)-1
            binaryValues.append(first_c)
            binaryValues.append(last_c)
            binaryValues.append(lenght_m)
            num_methods_i+=1

        while ((index+3)< len(binaryValues)):
            R = binaryValues[index]
            index = index + 1
            G = binaryValues[index]
            index = index + 1
            B = binaryValues[index]
            index = index + 1
            for i in range (0,3000):
                resultSet.append((R, G, B))
                
        f=open(self.report + apkOr + "_s.txt")
        for line in f:
            line = line.split('; ')[-1]
            m = line.split(' ')[0]
            first_c = ord(m[0])
            last_c = ord(m[-2])
            lenght_m = len(m)
            #print first_c, last_c, lenght_m
            binaryValues.append(first_c)
            binaryValues.append(last_c)
            binaryValues.append(lenght_m)
            num_methods_s+=1


        while ((index+3)< len(binaryValues)):
            R = binaryValues[index] - 100
            index = index + 1
            G = binaryValues[index] + 30
            index = index + 1
            B = binaryValues[index] + 120
            index = index + 1
            if num_methods_s < 10:
                for i in range (0,20000):
                    resultSet.append((R, G, B))
            else:
                for i in range (0,10000):
                    resultSet.append((R, G, B))

        if num_methods_s < 10:
            num_pixels= 3000* num_methods_i + 20000 * num_methods_s
        if num_methods_s > 10:
            num_pixels= 3000* num_methods_i + 10000 * num_methods_s
        
        height= 1000
        width= 1000

        #if(num_pixels< width*height):
        image = Image.new('RGB', self._capDimensions(width,height,num_pixels), "black")
        image.putdata(resultSet)
        """
        else:
            image = Image.new('RGB', self._capDimensions(2*width,2*height,num_pixels), "black")
            image.putdata(resultSet)
        """
        self.image = os.path.join(self.home, 'image')
            
        if not os.path.exists(self.image):
            os.makedirs(self.image) 

        os.chdir(self.image) 
        print('Making image...')
        print('Saving image...')
        image.save(self.project_name + "_1.png", "PNG")
        os.chdir(self.home)

    def getRepackedColors(self):
        apkOr= "/" + self.project_name
        f=open(self.report + apkOr + "_i.txt")

        num_methods_i=0
        num_methods_s=0
        num_methods_n=0
        index=0
        resultSet=[]
        binaryValues = []

        for line in f:
            first_c = ord(line[0])
            last_c = ord(line[-2])
            lenght_m = len(line)-1
            binaryValues.append(first_c)
            binaryValues.append(last_c)
            binaryValues.append(lenght_m)
            num_methods_i+=1

        while ((index+3)< len(binaryValues)):
            R = binaryValues[index]
            index = index + 1
            G = binaryValues[index]
            index = index + 1
            B = binaryValues[index]
            index = index + 1
            for i in range (0,3000):
                resultSet.append((R, G, B))


        f=open(self.report + apkOr + "_s.txt")

        for line in f:
            line = line.split('; ')[-1]
            m = line.split(' ')[0]
            similarity = (line.split(' ')[1])
            similarity_f = float(similarity.split('\n')[0])
            similarity_i = int(round(similarity_f, 2) * 100)
            similarity_p = int((255 * similarity_i)/100)
            #print similarity_p, similarity_i
            first_c = ord(m[0])
            last_c = ord(m[-2])
            lenght_m = len(m)
            #print first_c, last_c, lenght_m
            binaryValues.append(first_c)
            binaryValues.append(last_c)
            binaryValues.append(lenght_m)
            num_methods_s+=1
   
        while ((index+3)< len(binaryValues)):
            if similarity_p <90:
                R = binaryValues[index] -100- 5*similarity_p
                index = index + 1
                G = binaryValues[index] +30 - 5*similarity_p
                index = index + 1
                B = binaryValues[index] +120 - 5*similarity_p
                index = index + 1
                if num_methods_s < 10:
                    for i in range (0,20000):
                        resultSet.append((R, G, B))
                else:
                    for i in range (0,10000):
                        resultSet.append((R, G, B))
            elif similarity_p > 90:  
                R = binaryValues[index] -100- similarity_p
                index = index + 1
                G = binaryValues[index] +30 - similarity_p
                index = index + 1
                B = binaryValues[index] +120 - similarity_p
                index = index + 1
                if num_methods_s < 10:
                    for i in range (0,20000):
                        resultSet.append((R, G, B))
                else:
                    for i in range (0,10000):
                        resultSet.append((R, G, B))

        if(os.path.isfile(self.report + apkOr + "_n.txt")):
            f=open(self.report + apkOr + "_n.txt")

            for line in f:
                line = line.split('; ')[-1]
                m = line.split(' ')[0]
                first_c = ord(m[0])
                last_c = ord(m[-2])
                lenght_m = len(m)
                binaryValues.append(first_c)
                binaryValues.append(last_c)
                binaryValues.append(lenght_m)
                num_methods_n+=1

            while ((index+3)< len(binaryValues)):
                R = binaryValues[index] + 50
                index = index + 1
                G = binaryValues[index] - 100
                index = index + 1
                B = binaryValues[index] -100
                index = index + 1
                if num_methods_n < 10:
                    for i in range (0,10000):
                        resultSet.append((R, G, B))
                else:
                    for i in range (0,5000):
                        resultSet.append((R, G, B))

        if num_methods_s < 10:
            num_pixels= 3000* num_methods_i + 20000 * num_methods_s + 5000* num_methods_n
        if num_methods_n < 10:
            num_pixels= 3000* num_methods_i + 10000 * num_methods_s + 10000* num_methods_n
        if num_methods_s < 10 and num_methods_n < 10:
            num_pixels= 3000* num_methods_i + 20000 * num_methods_s + 10000* num_methods_n
        if num_methods_s > 10 and num_methods_n > 10:
            num_pixels= 3000* num_methods_i + 10000 * num_methods_s + 5000* num_methods_n
        
        height= 1000
        width= 1000


        image = Image.new('RGB', self._capDimensions(width,height,num_pixels), "black")
        image.putdata(resultSet)

        if not os.path.exists(self.image):
            os.makedirs(self.image) 

        os.chdir(self.image)
        
        print('Making image...')
        print('Saving image...')
        image.save(self.project_name + "_2.png", "PNG")
        os.chdir(self.home)

def main():
    # current working directory
    cwd = os.getcwd()
    # apk2java installation path
    home = os.path.dirname(os.path.realpath(sys.argv[0]))

    usage = "usage: %prog file [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("--java", action="store_true", dest="java", default=True,
                      help="select java source format [DEFAULT]")
    parser.add_option("-o", dest="outdir", default=cwd, help="specify the output directory "
                                                                   + "(if not specified the decomipled version will be store in a folder in the script directory)")
    (options, args) = parser.parse_args()

    app = Apk2Png()
    # check if tools are instaled in the script dir
    app.check_tools(home)

    # by default is cwd
    app.outdir = options.outdir

    if len(args) == 2:
        app.compare(args[0], args[1])
        app.getIdenticalMethods()
        app.getSimilarMethods()
        app.getNewMethods()
    else:
        parser.print_help()
    

# Script start Here
if __name__ == "__main__":
    main()
