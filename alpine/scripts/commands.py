import os
import io
import sys
import re
import time
import subprocess
import signal
import psutil
import csv
from threading import Timer
import time
import getopt
from junit_xml import TestSuite, TestCase

TIMEOUT_DURATION = 350 
def print_usage():
    print("usage: test.py [-h] [-o OUT_FILENAME] [-r RETRIES] IN_DIR")
def getConfigFromCli(argv):
    argsListNoFileName = argv[1:]

    optionsString = "ho:r:"
    options, posArgs = getopt.getopt(argsListNoFileName, optionsString)
    
    if len(posArgs) != 1:
        raise getopt.GetoptError
    
    headless = False
    if ('-h', '') in options:
        headless = True
        print("headless")
    
    reportFileName = "reportFile"
    if any(x[0] == '-o' for x in options):
        reportFileName = [x for x in options if x[0] == '-o' ][0][1]
    
    retries = 0
    if any(x[0] == '-r' for x in options):
        retries = [x for x in options if x[0] == '-r' ][0][1]
        try:
            retries = int(retries)
        except:
            
            raise getopt.GetoptError
    return [headless, reportFileName, posArgs[0], retries]

def getChildProcesses(pid):
    children= []
    try: 
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return 
    children = parent.children(recursive=True)
    return children
def getOnlyWithNameFromList(processes, name):
    return [x for x in processes if x.name() == name]
def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,timeout=None, on_terminate=None):
    assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        try:
            p.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=timeout,
                                    callback=on_terminate)
    return (gone, alive)
def check_enough_firefox_windows(proc):
    children = getChildProcesses(proc.pid)
    if (len(getOnlyWithNameFromList(children, "Web Content")) < 4):
        kill_proc_tree(proc.pid)
        raise subprocess.TimeoutExpired(testpath, TIMEOUT_DURATION)
    else:
        proc.wait()    
        
def kill_stuff():
    subprocess.run(["killall", "xvfb"]) # kill xvfb runtime blocking display :99
    subprocess.run(["killall","node"]) # kill node-runtime blocking port :3500
    subprocess.run(["killall","firefox"])
def run_test(path, test, headless=False):
    try:
        command = []
        if headless:
            command = ["xvfb-run","-a","--server-args=-screen 0, 1920x1080x24"]
        
        command = command + ["kr-cli", "run", "firefox", test, "-rp", path + "/reports", "--data",path + "/userdaten.csv"]
        subprocess.run(command, timeout=TIMEOUT_DURATION)    
        return 1
        #t = Timer(TIMEOUT_DURATION, check_enough_firefox_windows,[proc])
        #t.start()
        #proc.wait()
        ##proc.wait()
        ##time.sleep(TIMEOUT_DURATION)  
        #children = getChildProcesses(proc.pid)
        ##print(len(getOnlyWithNameFromList(children, "Web Content")))
        #if (len(getOnlyWithNameFromList(children, "Web Content")) < 4):
            #kill_proc_tree(proc.pid)
            #raise subprocess.TimeoutExpired(testpath, TIMEOUT_DURATION)
        #else:
            #proc.wait()
    except subprocess.TimeoutExpired:
        print("Test timeout expired!")
        kill_stuff()
        # print(proc.pid)
        return -1

def get_tests_in_dir(path):
    testlist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith(".html")):
                testlist.append(os.path.join(file))
    return testlist
def run_tests(testdir, headless=False, retries=1):
    oldpath = os.getcwd()
    testlist = get_tests_in_dir(testdir)
    curTest = 0
    for test in testlist:
        retval = run_test(testdir, testdir + "/" + test, headless=headless)
        retriesDone = 0
        while retval == -1 and retriesDone < retries:
            retval = run_test(testdir, testdir + "/" + test) #retry once 
            retriesDone = retriesDone + 1
        
        #print("%i OUT OF %i" %(len(testlist)) %curTest)
        curTest = curTest + 1
    os.chdir(oldpath)
def remove_logs(path):
    for root, dirs, files in os.walk(path+ "/reports"):
        for file in files:
            try:
                os.remove(os.path.join(root,file))
            except OSError as error:
                print(error)
                print("File '%s' can not be removed" %file)
        for dir in dirs:
            try:
                os.rmdir(os.path.join(root, dir))
            except OSError as error:
                print("Directory '%s' can not be removed" %dir)
def get_test_log_files(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith(".log")):
                filelist.append(os.path.join(root,file))
    return filelist
def get_test_csv_files(path):
    filelist = []
    filenamePattern = re.compile("kr_execution.csv",re.IGNORECASE)
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith(".csv") and filenamePattern.search(file)):
                filelist.append(os.path.join(root,file))
    return filelist
def read_and_combine_csv_files(files):
    data = []
    for filename in files: 
        with io.open(filename, 'r', encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            newRows = []
            for row in reader: 
                newRows.append(row)
            data =data + newRows[1:]
    return data
def suites_from_combined_csv(data):
    def get_name_from_row(row):
        return row[0]
    def case_from_row(row):
        case = {
            "name":row[1],
            "trace":[],
            "result":row[2].upper()
            }
        return case
    suites = []
    suiteNames = list(set(list(map(get_name_from_row, data))))
    for name in suiteNames:
        newSuite = {
            "name":name,
            "cases":[],
            "summary":{"passed":0, "failed":0}
        }
        caseRows = list(x for x in data if x[0] == name)
        newSuite["cases"] = list(map(case_from_row, caseRows))
        newSuite["summary"]["passed"] = len(list(x for x in newSuite["cases"] if x["result"] == "PASSED"))
        newSuite["summary"]["failed"] = len(list(x for x in newSuite["cases"] if x["result"] == "FAILED"))
        suites.append(newSuite)
    return suites
def filterFile(filename, reportFileName):
    suite = {
        "name":"",
        "cases":[]
    }
    startSuitePattern = re.compile("Found test suite:",re.IGNORECASE)
    startCasePattern = re.compile("Playing test case:",re.IGNORECASE)
    passedPattern = re.compile("Test case passed",re.IGNORECASE)
    failedPattern = re.compile("Test case failed",re.IGNORECASE)
    
    with io.open(filename, 'rt',encoding="utf-8") as myfile:
        startSuite = False
        startCase = False
        def newCase():
            return {"name":"","trace":[],"result":""}
        testCase = newCase()
        for line in myfile: 
            if (not startSuite and startSuitePattern.search(line)):
                startSuite = True 
                suite["name"] = str(line.rstrip('\n')).split(":")[-1] 
            if (startSuite and not startCase and startCasePattern.search(line)):
                startCase = True
                testCase["name"] = str(line.rstrip('\n')).split(":")[-1]
            if (startCase):
                if(passedPattern.search(line) or failedPattern.search(line)):
                    startCase = False
                    testCase["result"] = "PASSED" if passedPattern.search(line) else "FAILED"
                    suite["cases"].append(testCase)
                    testCase = newCase()
                else:
                    testCase["trace"].append(str(line.rstrip('\n')))
    return suite
def string_from_test_suite(suiteElement):
    def case_text(case):
        return "        " + case["result"] + " " + case["name"]
    def summary_text(suite):
        return "    TOTAL PASSED: " + str(suite["summary"]["passed"]) +" OUT OF " + str(suite["summary"]["failed"]+suite["summary"]["passed"])  
    caseTexts = "\n".join((list(map(case_text, suiteElement["cases"]))))
    return "\n".join(["   " +suiteElement["name"], caseTexts, summary_text(suiteElement)])
def get_summary_from_test_suite(suite):
    failedCount = len([x for x in suite["cases"] if x["result"] == "FAILED"])
    passedCount = len([x for x in suite["cases"] if x["result"] == "PASSED"])
    return {"failed" : failedCount, "passed":passedCount}
def get_summary_string(suiteElements):
    def single_summary(suite):
        return suite["name"] +"\n"+ str(suite["summary"]["passed"]) +" OUT OF " + str(suite["summary"]["failed"]+suite["summary"]["passed"])+"\n---------------------" 
    def passed(suite):
        return suite["summary"]["passed"]
    def failed(suite):
        return suite["summary"]["failed"]
    passedTotal = sum(list(map(passed, suiteElements)))
    failedTotal = sum(list(map(failed, suiteElements)))
    totalSummary = "TOTAL " + str(passedTotal) +" OUT OF "+ str(passedTotal + failedTotal) 
    
    returnElements = list(map(single_summary, suiteElements))
    return "\n".join(returnElements) + "\n" + totalSummary
def combine_logs(fileList, reportFileName):
    def f(filename):
        suite = filterFile(filename, reportFileName)
        suite["summary"] = get_summary_from_test_suite(suite)
        return suite
    
    suiteElements = list(map(f, fileList))
    summaryString = get_summary_string(suiteElements)
    with io.open(reportFileName, 'w',encoding="utf-8") as x:
        x.write("TEST SUITES:\n")
        for e in suiteElements: 
            x.write(string_from_test_suite(e) + "\n-----------------------------------------------------------------\n")
        x.write(summaryString)
def write_suites(suites, reportFileName):
    summaryString = get_summary_string(suites)
    with io.open(reportFileName, 'w', encoding="utf-8") as x:
        x.write("TEST SUITES:\n")
        for e in suites:
            x.write(string_from_test_suite(e) + "\n------------------------------------------------\n")
        x.write(summaryString)
def update_file_owner(newOwner, filename, recursive=False):
    recString = "-R" if recursive else ""
    os.system("chown {recString} {newOwner} {filename}".format(recString=recString, newOwner=newOwner, filename=filename))
def write_suites_XML(suites, outFileName):
    testSuites = list(map(suite_to_JSU_testsuite, suites))
    with io.open(outFileName, 'w', encoding="utf-8") as x:
        x.write(TestSuite.to_xml_string(testSuites))
def case_to_JSU_testcase(case):
    test_case = TestCase(case["name"], 'some.class.name',10, case["result"],"")
    if case["result"] == 'FAILED':
        test_case.add_failure_info("FAILED")
    return test_case
def suite_to_JSU_testsuite(suite):
    return TestSuite(suite["name"], list(map(case_to_JSU_testcase, suite["cases"])))
#main program
try:
    headless, reportFileName, inputFileName, retries = getConfigFromCli(sys.argv)
except:
    print("error!")
    print_usage()
    exit()
print("running tests...")
#run_tests(inputFileName, headless=headless, retries=retries)
#oldpath = os.getcwd()
#os.chdir(oldpath)
print("combining logs...")

csvFiles = get_test_csv_files(inputFileName)
combined_csv = read_and_combine_csv_files(csvFiles)
suites = suites_from_combined_csv(combined_csv)
write_suites(suites, reportFileName)
write_suites_XML(suites, "suiteResult.xml")

print('checking user')
print(os.environ['LOG_OUPUT_OWNER'])
if os.environ['LOG_OUPUT_OWNER']:
    print("updating permissions...")
    update_file_owner(os.environ['LOG_OUPUT_OWNER'], n + "/reports",recursive=True)
    update_file_owner(os.environ['LOG_OUPUT_OWNER'], reportFileName)
