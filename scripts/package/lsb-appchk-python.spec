%define basedir /opt/lsb
# %{version}, %{rel} are provided by the Makefile
Summary: LSB Python Application Checker
Name: lsb-appchk-python
Version: %{version}
Release: %{rel}
License: Artistic 
Group: Development/Tools
Source: %{name}-%{version}.tar.gz
Source1: tetj.py
Source2: lsb-python-modules.list
URL: http://www.linuxbase.org/test
#Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root
AutoReqProv: no
BuildArch: noarch

%description
This is the official package version of the LSB Python Application Test.
Heavy lifting is done by Python's modulefinder module, using some ideas
from http://www.tarind.com/depgraph.html.

This package bundles a modified version of modulfinder named lsb_modulefinder,
as well as a modified dis.py and copies of opcode.py and types.py from Python
2.4.
 
#==================================================
%prep
%setup -q
# (sb) set the default version we'll test against (from the Makefile)
sed -i "s|lsb_version = '4.0'|lsb_version = '%{lsbversion}'|g" source/lsbappchk.py

#==================================================
%build
# nothing to do here

#==================================================
%install

rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{basedir}/bin
mkdir -p ${RPM_BUILD_ROOT}%{basedir}/share/appchk
cp -p source/lsbappchk.py ${RPM_BUILD_ROOT}%{basedir}/bin
cp -p source/lsb_modulefinder.py ${RPM_BUILD_ROOT}%{basedir}/share/appchk
for module in modulefinder dis opcode types; do
  cp -p source/lsb_$module.py ${RPM_BUILD_ROOT}%{basedir}/share/appchk
done
cp -p %{SOURCE1} ${RPM_BUILD_ROOT}%{basedir}/share/appchk
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}%{basedir}/share/appchk

# VERSION file for the journal
cat > VERSION.lsbappchk.py << EOF
%{name} %{version}-%{rel} (noarch)
EOF
cp VERSION.lsbappchk.py ${RPM_BUILD_ROOT}%{basedir}/share/appchk

# license files
install -d ${RPM_BUILD_ROOT}%{basedir}/doc/%{name}
for license in Artistic LICENSE.txt; do
  cp source/$license ${RPM_BUILD_ROOT}%{basedir}/doc/%{name}
done

# man page
install -d ${RPM_BUILD_ROOT}%{basedir}/man/man1
cp doc/lsbappchk.py.1 ${RPM_BUILD_ROOT}%{basedir}/man/man1

# bug 2509 - unpackaged .pyc/.pyo files on some build platforms
find ${RPM_BUILD_ROOT}%{basedir} -name '*.pyc' | xargs rm -f
find ${RPM_BUILD_ROOT}%{basedir} -name '*.pyo' | xargs rm -f

#==================================================
%clean
if [ ! -z "${RPM_BUILD_ROOT}"  -a "${RPM_BUILD_ROOT}" != "/" ]; then 
    rm -rf ${RPM_BUILD_ROOT}
fi

#==================================================
%files
%defattr(-,root,root)

/opt/lsb/bin/lsbappchk.py
%dir /opt/lsb/share/appchk
/opt/lsb/share/appchk/*
%dir /opt/lsb/doc/%{name}
/opt/lsb/doc/%{name}/*
/opt/lsb/man/man1/lsbappchk.py.1

#==================================================
%changelog
* Tue Feb 03 2009 Stew Benedict <stewb@linux-foundation.org>
- drop lsb-tet3-lite requires

* Fri Dec 19 2008 Stew Benedict <stewb@linux-foundation.org>
- add manpage

* Wed Jul 02 2008 Stew Benedict <stewb@linux-foundation.org>
- Lose /opt/lsb/lib to co-exist with multiversion sdk

* Wed Jun 04 2008 Stew Benedict <stewb@linux-foundation.org>
- add multiversion support (bug 2098)

* Tue Apr 15 2008 Stew Benedict <stewb@linux-foundation.org>
- package/use lsb_modulefinder based on modulefinder (bug 1881)
- make lsbappchk.py LSB compliant (drop md5 module, use system python)
- make lsb_modulefinder LSB compliant:
  replace "new" with "types", drop getopt dependency
  bundle modified lsb_opcode, lsb_types, lsb_dis
- include Python LICENSE.txt for our borrowed modules

* Mon Feb 18 2008 Stew Benedict <stewb@linux-foundation.org>
- We generate lsb-python-modules.list from the specdb now

* Mon Dec 03 2007 Stew Benedict <stewb@linux-foundation.org>
- Add license file

* Sat Dec  1 2007 Mats Wichmann <mats@linux-foundation.org>
- renamed package to lsb-appchk-python from lsbappchk-python (convention)

* Tue Nov 27 2007 Stew Benedict <stewb@linux-foundation.org>
- fix journal issues (bug 1782)
- use tetj.py from misc-test

* Tue Jul 10 2007 Stew Benedict <stewb@linux-foundation.org>
- _foo -> foo, add os, re, string
- bump to release 2

* Tue Jun 03 2007 Stew Benedict <stewb@linux-foundation.org>
- initial packaging

