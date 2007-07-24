#!/opt/lsb/appbat/bin/python
# prototype application to check python applications
# for LSB compliance
# derived from ideas at http://www.tarind.com/depgraph.html
# Copyright GPL, Stew Benedict <stewb@linux-foundation.org>

import sys
import os
# modulefinder does all the heavy lifting
import modulefinder
sys.path.append('/opt/lsb/lib/appchk')
import tet

# re-define the report class for our needs
class lsbmf(modulefinder.ModuleFinder):
    def report(self):
        return self.modules 

# compare the found modules to the LSB list and report
# if the import uses a /opt path, just warn
def check_modules(journal, modules, lsb_modules, syspath_org):
    twarn = ' is used from nonstandard path '
    tfail = ' is used, but is not part of LSB'
    keys = modules.keys()
    keys.sort()
    tcount = 0;
    for key in keys:
        jresult = 'PASS'
        tcount = tcount + 1
        if journal:
            tet.istart(tcount)
            tet.info(tcount, 'Check ' + key)
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
                    jresult = 'UNRESOLVED'
                else:
                    tresult = key + tfail
                    jresult = 'FAIL'
                print tresult
                if journal:                
                    tet.info(tcount, tresult)
        if journal:
            tet.result(tcount, jresult)        
            tet.iend(tcount)
        
def main(argv):
    if len(argv) == 1:
        print 'Usage: ' + argv[0] + ' [-j] some_program.py'
        sys.exit(1)

    # drop our path to the tet module and preserve a pristine sys.path
    syspath_org = sys.path[:-1]

    sharepath = '/opt/lsb/share/appchk'

    journal = 0
    if '-j' in argv:
        journal = 1
        testapp = argv[2]
        jsuffix = os.path.basename(testapp)
    else:
        testapp = argv[1]

    try:
        f = file(testapp, 'r')
    except:
        print 'Failed to open ' + testapp
        sys.exit(1)
    f.close

    # prep the journal header
    if journal:
        myname = os.path.basename(argv[0])
        journal_file = tet.open_journal('journal.' + myname + '.' + jsuffix)
        tet.write_header(journal_file)
        vfile = sharepath + '/VERSION.' + myname
        tet.write_version(journal_file,vfile)
        tet.file_info(journal_file, testapp)

    path = sys.path[:]
    debug = 0
    exclude = []
    
    # get the 'blessed' LSB module list
    lsb_modules = []
    modfile = open(sharepath + '/lsb-python-modules.list', 'r')
    line = modfile.readline()
    line = line.rstrip()
    while line:
        if line[0] != '#':
            lsb_modules.append(line)
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

    print testapp + ":"
    if journal:
        tet.tstart(testapp)
    modules = mf.report()
    check_modules(journal, modules, lsb_modules, syspath_org)

if __name__=='__main__':
    main(sys.argv)
