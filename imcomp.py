import os
import sys
import time
from PIL import Image
from datetime import datetime

# --- Global section ---
# verbose mode flag
VERBOSE = True

# log file location 
LOGFILE = r"C:\Users\dbretschneider\Desktop\imcomp_log.log"

# minimal file size
MIN_FILE_SIZE = 150000


def log(msg):
    """
    Prints msg to console and logs in logfile 
    """
    if VERBOSE == True:
        print(msg)
         
    file = open(LOGFILE, "a+")
    ts = datetime.now()
    file.write("[" + str(ts) + "]: " + msg + "\n")
    file.close()


def CompressImage(file):
    """
    Compress image

    compress image by factor 25
    """
    filepath = os.path.abspath(file)
    oldsize = os.stat(filepath).st_size
    picture = Image.open(filepath)
    dim = picture.size

    # set quality= to the preferred quality. 
    picture.save(file, "JPEG", optimize=True, quality=25)

    newsize = os.stat(file).st_size
    percent = (oldsize - newsize) / float(oldsize) * 100
    if (VERBOSE):
        log("File: " + filepath +  " compressed from {0} to {1} or {2}%".format(oldsize, newsize, percent))
    return percent


def checkDate(file):
    """
    Check if file is older than half a year.

    returns True if older than half a year
    returns False if not older older than one year
    """
    # todays date
    today = datetime.today()
    
    # date of creation
    t = os.stat(file)[8]

    # total filetime
    filetime = datetime.fromtimestamp(t) - today
    log(str(filetime))

    # Check if file is older than half a year
    if (filetime.days <= -182):
        log("File with name '" + file + "' is older than half a year.")
        return True
    else:
        log("File with name '" + file + "' is not older than half a year.")
        return False


def main():
    """
    main method

    """

    # time stamp to measure duration of p.execution
    starttime = time.time()

    # checks for verbose flag
    if (len(sys.argv) > 1):
        if (sys.argv[1].lower() == "-v"):
            VERBOSE = True
            log("Verbose mode turned on!")

    # start node
    # path = str(r"" + input("Enter start node: "))     # WENN DER BENUTZER DEN PFAD SELBST ANGEBEN MÖCHTE DANN HIER AUSKOMMENTIEREN
    path = str(r"" + sys.argv[1])                       # übernimmt pfad als CMD-Argument
    log("User entered: " + path)
    fname = []
    total = 0
    num = 0

    
    # walks recursively through start directory
    # finds all .jpg-files and compress them
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            try: 
                filename = os.path.join(root, f)
                log("Checking if file is older than a year.")
                if ((filename.endswith(".jpg") or filename.endswith(".jpeg"))):         # and checkDate(filename) == True
                    if os.stat(filename).st_size > MIN_FILE_SIZE:
                        log("compressing: " + filename)
                        fname.append(os.path.join(root, f))
                        num += 1
                        total += CompressImage(filename)
                    else:
                        log("WARNING: File size smaller than 300kb, not compressing.")
            except:
                log("ERROR: An error occured compressing image with name: " + str(filename))

    # end 
    if num != 0:
        print("Average Compression: %d" % (float(total) / num))
    print("Done")
    print("--- %s seconds ---" % (time.time() - starttime))


#
# start of program
#
if __name__ == "__main__":
    main()
