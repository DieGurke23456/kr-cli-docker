import os
import sys
import re
n = str(sys.argv[1])
os.chdir(n)
path = os.getcwd()
testlist = []
for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(".html")):
            testlist.append(os.path.join(file))
if not os.path.exists("reports"):
    os.makedirs("reports")
for x in testlist:
    os.system('kr-cli run firefox ' + x + ' -rp "reports" --data "userdaten.csv"')
#we shall store all the file names in this list
filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(".log")):
            filelist.append(os.path.join(root,file))
    
def filterFile(filename):
                
    helper = []
    errors = []
    linenum = 0
    previousSuite = ()
    previousCase = ()
    failed = "Test case failed"
    testcase = "Playing test case:"
    testsuite = "Found test suite:" 
    pattern1 = re.compile("Found test suite: | Playing test case: | Test case failed", re.IGNORECASE)  # Compile a case-insensitive regex
    with open (filename, 'rt') as myfile:    
        for line in myfile:
            linenum += 1
            if (pattern1.search(line)):    # If a match is found 
                helper.append((linenum, line.rstrip('\n')))
    
    for i in helper:
        if (testsuite in str(i[1])):
            previousSuite = i
        if (testcase in str(i[1])):
            previousCase = i
        if (failed in str(i[1])):
            errors.append(previousSuite)
            errors.append(previousCase)
            errors.append(i)
    for err in errors:                            # Iterate over the list of tuples
        with open('testlog', 'a') as f:
            f.write(err[1] + "\n")

for name in filelist:
    filterFile(name)
