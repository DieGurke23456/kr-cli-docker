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
for x in testlist:
    os.system('npx kr-cli run firefox ' + x + ' -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "benutzer.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "kunde.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "projekt.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "textbausteine.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "anwesenheit.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "ausgabe.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "feiertage.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "pausen-und arbeitszeitregelung.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "stundenkorrektur.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "zeiteintrag.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "arbeitszeitmodell.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "unternehmensstruktur.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "abwesenheitssichtbarkeit.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "benutzerrechte.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "dienstplan.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "terminplan.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "abwesenheiten.html" -rp "reports" --data "userdaten.csv"')
#os.system('npx kr-cli run firefox "abwesenheitstypen.html" -rp "reports" --data "userdaten.csv"')
#--os.system('npx kr-cli run firefox "aufgabenplanung.html" -rp "reports" --data "userdaten.csv"')
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
        with open('testbericht.txt', 'a') as f:
            f.write(err[1] + "\n")

for name in filelist:
    filterFile(name)