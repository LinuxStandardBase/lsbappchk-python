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
URL: http://www.linuxbase.org/test
#Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root
AutoReqProv: no
BuildArch: noarch
Requires: lsb-tet3-lite lsb-python

%description
This is the official package version of the LSB Python Application Test.
Heavy lifting is done by Python's modulefinder module, using some ideas
from http://www.tarind.com/depgraph.html.
 
#==================================================
%prep
%setup -q

#==================================================
%build
# nothing to do here

#==================================================
%install

rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{basedir}/bin
mkdir -p ${RPM_BUILD_ROOT}%{basedir}/lib/appchk
mkdir -p ${RPM_BUILD_ROOT}%{basedir}/share/appchk
cp -p source/lsbappchk.py ${RPM_BUILD_ROOT}%{basedir}/bin
cp -p %{SOURCE1} ${RPM_BUILD_ROOT}%{basedir}/lib/appchk
cp -p lists/lsb-python-modules.list ${RPM_BUILD_ROOT}%{basedir}/share/appchk

# VERSION file for the journal
cat > VERSION.lsbappchk.py << EOF
%{name} %{version}-%{rel} (noarch)
EOF
cp VERSION.lsbappchk.py ${RPM_BUILD_ROOT}%{basedir}/share/appchk

# license file
install -d ${RPM_BUILD_ROOT}%{basedir}/doc/%{name}
cp source/Artistic ${RPM_BUILD_ROOT}%{basedir}/doc/%{name}

#==================================================
%clean
if [ ! -z "${RPM_BUILD_ROOT}"  -a "${RPM_BUILD_ROOT}" != "/" ]; then 
    rm -rf ${RPM_BUILD_ROOT}
fi

#==================================================
%files
%defattr(-,root,root)

/opt/lsb/bin/lsbappchk.py
%dir /opt/lsb/lib/appchk
/opt/lsb/lib/appchk/*
%dir /opt/lsb/share/appchk
/opt/lsb/share/appchk/*
%dir /opt/lsb/doc/%{name}
/opt/lsb/doc/%{name}/*

#==================================================
%changelog
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

