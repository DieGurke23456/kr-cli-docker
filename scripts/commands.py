import os
import sys
import re
n = str(sys.argv[1])
if (len(sys.argv) > 2):
    reportFileName = str(sys.argv[2])
else:
    reportFileName = "testbericht"
os.chdir(n)
path = os.getcwd()
testlist = []
countP = 0
countF = 0
for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(".html")):
            testlist.append(os.path.join(file))
if not os.path.exists("reports"):
    os.makedirs("reports")
for x in testlist:
    os.system('kr-cli run firefox ' + x + ' -rp "reports" --data "userdaten.csv"')
we shall store all the file names in this list
filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(".log")):
            filelist.append(os.path.join(root,file))
    
def filterFile(filename):
    global countP
    global countF            
    helper = []
    errors = []
    linenum = 0
    previousSuite = ()
    previousCase = ()
    passed = "Test case passed"
    failed = "Test case failed"
    testcase = "Playing test case:"
    testsuite = "Found test suite:" 
    pattern1 = re.compile("Found test suite: | Playing test case: | Test case failed", re.IGNORECASE)  # Compile a case-insensitive regex
    pattern2 = re.compile("Test case passed", re.IGNORECASE)
    pattern3 = re.compile("Test case failed", re.IGNORECASE)
    with open (filename, 'rt') as myfile:    
        for line in myfile:
            linenum += 1
            if (pattern1.search(line)):    # If a match is found 
                helper.append((linenum, line.rstrip('\n')))
            if (pattern2.search(line)):
                countP+=1
            if (pattern3.search(line)):
                countF+=1
    #print(str(countP) + " Passsed")
    #print(str(countF) + " Failed")
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
        with open(reportFileName, 'a') as f:
            f.write(err[1] + "\n")

for name in filelist:
    filterFile(name)
with open(reportFileName, 'a') as x:
        x.write(str(countP) + " Tests Passed \n")
        x.write(str(countF) + " Tests Failed \n")