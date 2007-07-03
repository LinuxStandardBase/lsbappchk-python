# basic python source TET functions
# used to avoid using /opt/lsb-tet3-lite/lib/python/pytet.py
# which relies on a binary shared library tied to python-2.4

import os
import sys
import time
import md5

def open_journal(jfile):
    global journal_file
    journal_file = open(jfile, 'w')
    return journal_file

def close_journal():
    global journal_file
    journal_file.close

def write_version(journal, vfile):
    version_file = open(vfile, 'r')
    version = '30||VSX_NAME=' + version_file.read()
    version_file.close
    journal.write(version)

def write_header(journal):
    tdate = time.strftime("%H:%M:%S %Y%m%d", time.localtime(time.time()))
    user = os.environ['USER']
    caller = sys.argv[0]
    journal.write('0|3.7-lite ' + tdate + '|User: ' + user + ', Command line:' + caller + '\n')
    uname = os.popen('uname -snrvm').readlines()
    journal.write('5|' + uname[0][:-1] + '|System Information\n')

def sumfile(fobj):
    m = md5.new()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def file_info(journal,tfile):
    fsize = os.path.getsize(tfile)
    wstr = "520|0 1 0 0 0|FILE_SIZE %d\n" % (fsize)
    journal_file.write(wstr)
    f = file(tfile, 'rb')
    md5sum = sumfile(f)
    f.close()
    wstr = "520|0 1 0 0 0|BINARY_MD5SUM %s\n" % (md5sum)
    journal_file.write(wstr)

def start(tcount, test):
    ttime = time.strftime("%H:%M:%S", time.localtime(time.time()))
    journal_file.write('10|0 ' + test + '|TC Start\n')
    wstr = "400|0 %d %d %s|IC StartFILE_SIZE\n" % (tcount, tcount, ttime)
    journal_file.write(wstr)
    wstr = "200|0 %d %d %s|TP Start\n" % (tcount, tcount, ttime)
    journal_file.write(wstr)

def tstart(test):
    ttime = time.strftime("%H:%M:%S", time.localtime(time.time()))
    journal_file.write('10|0 ' + test + '|TC Start\n')

def istart(tcount):
    ttime = time.strftime("%H:%M:%S", time.localtime(time.time()))
    wstr = "400|0 %d %d %s|IC Start\n" % (tcount, tcount, ttime)
    journal_file.write(wstr)

def info(tcount, infotext):
    ttime = time.strftime("%H:%M:%S", time.localtime(time.time()))
    wstr = "520|0 %d %s|%s\n" % (tcount, ttime, infotext)
    journal_file.write(wstr)

def iend(tcount):
    ttime = time.strftime("%H:%M:%S", time.localtime(time.time()))
    wstr = "410|0 %d %d %s|IC End\n" % (tcount, tcount, ttime)
    journal_file.write(wstr)

def result(tcount, result):
    rcodes = {'PASS': 0, 'FAIL': 1, 'UNRESOLVED': 2, 'NOTINUSE':3, 
            'UNSUPPORTED':4, 'UNTESTED':5, 
            'UNINITIATED':6, 'NORESULT':7}
    tcode = rcodes[result]
    ttime = time.strftime("%H:%M:%S", time.localtime(time.time()))
    wstr = "220|0 %d %d %s|%s\n" % (tcount, tcode, ttime, result)
    journal_file.write(wstr)



