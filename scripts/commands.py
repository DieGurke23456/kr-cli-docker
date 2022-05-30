import os
import io
import sys
import re
import time
import subprocess
import signal
import psutil
import csv
TIMEOUT_DURATION = 20 # the amount of seconds to wait for kr-cli to open another firefox-tab before we check if they have been opened
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
def run_test(testpath):
    try :
        proc = subprocess.Popen(["kr-cli", "run", "firefox", testpath, "-rp", "reports", "--data","userdaten.csv"])
        time.sleep(TIMEOUT_DURATION)  
        children = getChildProcesses(proc.pid)
        print(len(getOnlyWithNameFromList(children, "Web Content")))
        if (len(getOnlyWithNameFromList(children, "Web Content")) < 4):
            kill_proc_tree(proc.pid)
            raise subprocess.TimeoutExpired(testpath, TIMEOUT_DURATION)
        else:
            proc.wait()
    except subprocess.TimeoutExpired:
        print("Test timeout expired!")
        print(proc.pid)

def get_tests_in_dir(path):
    testlist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith(".html")):
                testlist.append(os.path.join(file))
    return testlist
def run_tests(testdir):
    oldpath = os.getcwd()
    os.chdir(testdir)
    testlist = get_tests_in_dir(os.getcwd())
    if not os.path.exists("reports"):
        os.makedirs("reports")
    for test in testlist:
        run_test(test)
        #pid = os.fork()
        #if n : 
            #pass
        #sys.exit()
    os.chdir(oldpath)
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
    

#main program
n = str(sys.argv[1])
if (len(sys.argv) > 2):
    reportFileName = str(sys.argv[2])
else:
    reportFileName = "testbericht"
    
print("running tests...")
run_tests(n)
oldpath = os.getcwd()
os.chdir(oldpath)
print("combining logs...")

csvFiles = get_test_csv_files(n)
combined_csv = read_and_combine_csv_files(csvFiles)
suites = suites_from_combined_csv(combined_csv)
write_suites(suites, reportFileName)
