# XXX We should play the usual tricks defining stuff here and building
# XXX a specfile from this info, but not yet: for now keep in sync
PACKAGE=lsb-appchk-python
VERSION=5.0.0
BUILDNO=1
# default version we will test against - change as needed
LSBVERSION=5.0

# for getting the module list from the lsb db
DBOPTS=-N -h $$LSBDBHOST -u $$LSBUSER --password=$$LSBDBPASSWD

# Derive date string for daily snapshots
ISO_DATE=$(shell date +"%Y%m%d")
PWD=$(shell pwd)

FULL_PACKAGE_NAME=$(PACKAGE)-$(VERSION)
DOC_DIR=/opt/lsb/test/doc
RPM_BINARY_NAME=$(FULL_PACKAGE_NAME)-$(RELEASE).$(RPM_BUILD_ARCH).rpm
RPM_SOURCE_NAME=$(FULL_PACKAGE_NAME)-$(RELEASE).src.rpm

SOURCE1 = $(PACKAGE)-$(VERSION).tar.gz
TETJ = tetj.py
MODULE_LIST = lsb-python-modules.list

# Temporary build directory
TMP_BUILD_DIR=/tmp/$(FULL_PACKAGE_NAME)

# Handle different version generation for snapshots than for official builds
# OFFICIAL_RELEASE should be set to the tag to extract from CVS
ifdef OFFICIAL_RELEASE
# EXPORT_TAG should be set to the cvs tag to use
RELEASE=$(BUILDNO)
EXPORT_TAG=-r $(OFFICIAL_RELEASE)
else
RELEASE=0.$(ISO_DATE).$(BUILDNO)
EXPORT_TAG=-D now
endif

# Determine whether to use rpm or rpmbuild to build the packages
ifeq ($(wildcard /usr/bin/rpmbuild),)
	RPM_BUILD_CMD=rpm
else
	RPM_BUILD_CMD=rpmbuild 
endif

# Get RPM configuration information
# NOTE THAT RPM_TMP_BUILD_DIR IS DELETED AFTER THE RPM BUILD IS COMPLETED
# The rpmrc file translates targets where there are multiple choices per
# architecture. On build, the derived RPM_BUILD_ARCH is given as the target
RCFILELIST="/usr/lib/rpm/rpmrc:./rpmrc"
MACROFILELIST="/usr/lib/rpm/macros:/etc/rpm:~/.rpmmacros:./rpmmacros"
RPM_TMP_BUILD_DIR=$(HOME)/tmp/rpm-build
# noarch package
#RPM_BUILD_ARCH=$(shell rpm --rcfile ${RCFILELIST} --eval=%{_target_cpu})
#RPM_BINARY_DIR=$(RPM_TMP_BUILD_DIR)/RPMS/$(RPM_BUILD_ARCH)
RPM_BUILD_ARCH=noarch
RPM_BINARY_DIR=$(RPM_TMP_BUILD_DIR)/RPMS/noarch
RPM_SRPM_DIR=$(RPM_TMP_BUILD_DIR)/SRPMS

# Override this on the command line to use a different repo
BZRTREES?=http://bzr.linuxfoundation.org/lsb/devel
BZR_MODULE=lsbappchk-python
TETJ_MODULE=misc-test

# Default target
ifndef BUILD_NO_DEB
all: rpm_package deb_package
else
all: rpm_package
endif

clean:
	@rm -f *.rpm *.deb *.tar.gz tetj.py $(PACKAGE).spec

gensrc:
	mysql $(DBOPTS) $$LSBDB < get_python_modules.sql > $(MODULE_LIST)

tarball: $(SOURCE1) $(TETJ)

# Specfile generation rule
%.spec : %.spec.sed
	sed -e "s#@LSBVERSION@#`echo $(LSBVERSION)`#" -e "s#@VERSION@#`echo $(VERSION)`#" -e "s#@RELEASE@#`echo $(RELEASE)`#" < $< > $@

deb_package: rpm_package
	@fakeroot alien -cdk $(RPM_BINARY_NAME)

rpm_package: $(RPM_BINARY_NAME) $(RPM_SOURCE_NAME) 

list_uploadable:
	@echo $(RPM_BINARY_NAME)
ifndef BUILD_NO_DEB
	@ls *.deb
endif

$(RPM_BINARY_NAME) $(RPM_SOURCE_NAME): $(PACKAGE).spec $(SOURCE1) $(TETJ) 
	@mkdir -p $(RPM_TMP_BUILD_DIR)/BUILD
	@mkdir -p $(RPM_TMP_BUILD_DIR)/RPMS
	@mkdir -p $(RPM_TMP_BUILD_DIR)/SRPMS
ifdef SIGN_PACKAGES
	@expect -c 'set timeout -1' -c 'spawn $(RPM_BUILD_CMD) --sign --rcfile ${RCFILELIST} --macros=$(MACROFILELIST) --define=_sourcedir\ $(PWD) --define=_topdir\ $(RPM_TMP_BUILD_DIR) --define=_target_cpu\ $(RPM_BUILD_ARCH) -ba $(PACKAGE).spec' -c 'expect -ex "Enter pass phrase:"' -c 'send "\n"' -c 'expect "Executing(%clean)"' -c 'expect "exit 0"' -c 'send "\n"'
else
	@$(RPM_BUILD_CMD) --rcfile ${RCFILELIST} --macros=$(MACROFILELIST) --define="_sourcedir $(PWD)" --define="_topdir $(RPM_TMP_BUILD_DIR)" --define="_target_cpu $(RPM_BUILD_ARCH)" -ba $(PACKAGE).spec
endif
	@mv $(RPM_SRPM_DIR)/$(RPM_SOURCE_NAME) .
	@mv $(RPM_BINARY_DIR)/$(RPM_BINARY_NAME) .
	@rm -rf $(RPM_TMP_BUILD_DIR)

$(SOURCE1):
	bzr export $(SOURCE1) $(BZRTREES)/$(BZR_MODULE)

$(TETJ):
	bzr cat $(BZRTREES)/$(TETJ_MODULE)/tetj/tetj.py > tetj.py

.PHONY : tarball rpm_package
