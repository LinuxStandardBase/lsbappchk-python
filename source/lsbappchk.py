#!/usr/bin/python
# prototype application to check python applications
# for LSB compliance
# derived from ideas at http://www.tarind.com/depgraph.html
# Artistic license, Stew Benedict <stewb@linuxfoundation.org>

import sys
import os
import string
# modulefinder does all the heavy lifting
sys.path.append('/opt/lsb/lib/appchk')
import lsb_modulefinder
import tetj

# re-define the report class for our needs
class lsbmf(lsb_modulefinder.ModuleFinder):
    def report(self):
        return self.modules 

def sumfile(fname):
    cmd = 'md5sum %s' % (fname)
    for m in os.popen(cmd).readlines():
        md5sum = string.split(m)[0]
    return md5sum
      
def file_info(journal, tfile):
    fsize = os.path.getsize(tfile)
    wstr = "FILE_SIZE %d" % (fsize)
    journal.purpose_start('File information')
    journal.testcase_info(1,0,0,wstr)
    md5sum = sumfile(tfile)
    wstr = "BINARY_MD5SUM %s" % (md5sum)
    journal.testcase_info(0,0,0,wstr)
    journal.result(tetj.TETJ_PASS)        
    journal.purpose_end()

# compare the found modules to the LSB list and report
# if the import uses a /opt path, just warn
def check_modules(journal, modules, lsb_modules, syspath_org, lsb_version):
    twarn = ' is used from nonstandard path '
    tfail = ' is used, but is not part of LSB'
    tappeared = ' did not appear until LSB '
    twithdrawn = ' was withdrawn in LSB '
    keys = modules.keys()
    keys.sort()
    tcount = 0;
    for key in keys:
        jresult = tetj.TETJ_PASS
        tcount = tcount + 1
        if journal:
            journal.purpose_start('Check ' + key)

        if key in lsb_modules:
            appeared = lsb_modules[key][0]
            withdrawn = lsb_modules[key][1]
            #print appeared, withdrawn
            if withdrawn != "NULL":
                if float(withdrawn) < float(lsb_version):
                    tresult = key + twithdrawn + withdrawn
                    jresult = tetj.TETJ_FAIL              
                    print tresult
                    if journal:                
                        journal.testcase_info(0,0,0,tresult)
            if float(appeared) > float(lsb_version):
                tresult = key + tappeared + appeared
                jresult = tetj.TETJ_FAIL              
                print tresult
                if journal:                
                    journal.testcase_info(0,0,0,tresult)

        if key not in lsb_modules:
            if key != '__main__' and key != '__builtin__':
                # warn if we're getting modules from outside sys.path
                m = modules[key]
                #print m
                if m.__file__:    
                    #print 'file:' + m.__file__
                    mdir = os.path.dirname(m.__file__)
                else:
                    # no __file__ attribute - just give it one to move on
                    mdir = syspath_org[0]
                if mdir not in syspath_org:
                    tresult = key + twarn + mdir
                    jresult = tetj.TETJ_UNRESOLVED
                else:
                    tresult = key + tfail
                    jresult = tetj.TETJ_FAIL
                print tresult
                if journal:                
                    journal.testcase_info(0,0,0,tresult)

        if journal:
            journal.result(jresult)        
            journal.purpose_end()
        
def main(argv):
    lsb_version = '4.0'
    if len(argv) == 1:
        print 'Usage: ' + argv[0] + ' [-j] [-v N.N (LSB version to test for, default is ' + lsb_version + ')] some_program.py'
        sys.exit(1)

    # drop our path to the tet module and preserve a pristine sys.path
    syspath_org = sys.path[:-1]

    sharepath = '/opt/lsb/share/appchk'

    journal = 0
    if '-j' in argv:
        journal = 1
    if '-v' in argv:
        vloc = string.index(argv, "-v")
        lsb_version = argv[vloc + 1]
        try:
            float(lsb_version)
        except:
            print 'Invalid LSB_VERSION: ' + lsb_version
            sys.exit(1)
        if float(lsb_version) < 1.0 or float(lsb_version) > 20:
            print 'Invalid LSB_VERSION: ' + lsb_version
            sys.exit(1)

    testapp = argv[len(argv)-1]
    jsuffix = os.path.basename(testapp)
    fullargs = string.join(argv, ' ')

    try:
        f = file(testapp, 'r')
    except:
        print 'Failed to open ' + testapp
        sys.exit(1)
    f.close

    # prep the journal header
    if journal:
        myname = os.path.basename(argv[0])
        journal = tetj.Journal('journal.' + myname + '.' + jsuffix, fullargs)
        journal.add_config("VSX_NAME=lsb-tetjtest.py 0.1 (%s)" % journal.machine)
        journal.config_end()

    path = sys.path[:]
    debug = 0
    exclude = []
    
    # get the 'blessed' LSB module list
    lsb_modules = {}
    modfile = open(sharepath + '/lsb-python-modules.list', 'r')
    line = modfile.readline()
    line = line.rstrip()
    while line:
        if line[0] != '#':
            module, appeared, withdrawn = string.split(line)
            exclude.append(module)
            lsb_modules[module] = appeared, withdrawn
        line = modfile.readline()
        line = line.rstrip()
    modfile.close()
    #print lsb_modules

    mf = lsbmf(path,debug,exclude)

    # see if target is really a python script and run it
    try:
        mf.run_script(testapp)
    except:
        print 'Cannot analyse ' + testapp + ' (is it a python app?)'
        sys.exit(1)

    print testapp + " tested against LSB " + lsb_version + ":"
    if journal:
        journal.testcase_start(testapp)
        file_info(journal, testapp)

    modules = mf.report()
    check_modules(journal, modules, lsb_modules, syspath_org, lsb_version)
    if journal:
        journal.testcase_end(testapp)
        journal.close()

if __name__=='__main__':
    main(sys.argv)
