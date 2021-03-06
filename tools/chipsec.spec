# spec file for package chipsec
#
# Copyright (c) 2018 siro@das-labor.org
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

%define srcname chipsec
%define realversion 1.5.0
%define dkmsversion 1.5.0
%global dkms_name %{srcname}

Name:             %{srcname}
Version:          %{realversion}
Release:          1%{?dist}
Summary:          CHIPSEC is a framework for analyzing the security of PC platforms; see https://github.com/chipsec/chipsec
License:          GPLv2
URL:              https://github.com/chipsec/chipsec
Source0:          https://github.com/chipsec/chipsec/archive/%{version}.tar.gz
Group:            Applications/Tools

BuildRequires:  redhat-rpm-config
BuildRequires:  python
BuildRequires:  python3-devel
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  gcc

Requires:       %{srcname}-doc = %{realversion}
Requires:       python3-%{srcname} = %{realversion}

%define desc CHIPSEC is a framework for analyzing the security of PC platforms including hardware, system firmware (BIOS/UEFI), and platform components. It includes a security test suite, tools for accessing various low level interfaces, and forensic capabilities.

%description
%desc

%global debug_package %{nil}

%prep
%autosetup -n chipsec-%{version}

%build
%py3_build "--skip-driver"

%install
%py3_install

#find $RPM_BUILD_ROOT/%{python3_sitearch}/ -type f -name '*.py' -delete
find $RPM_BUILD_ROOT/%{python3_sitearch}/ -type f -name '*.pyo' -delete

mkdir -p $RPM_BUILD_ROOT/%{_usrsrc}/%{dkms_name}-%{version}
cp -r drivers/linux/* $RPM_BUILD_ROOT/%{_usrsrc}/%{dkms_name}-%{version}/

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/doc/chipsec/
mv $RPM_BUILD_ROOT/%{_prefix}/chipsec-manual.pdf $RPM_BUILD_ROOT/%{_prefix}/share/doc/chipsec/chipsec-manual.pdf

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/modules-load.d
echo "chipsec
" > $RPM_BUILD_ROOT/%{_sysconfdir}/modules-load.d/chipsec.conf

echo 'MAKE="export KERNEL_SRC_DIR=${kernel_source_dir} && make -C ."
CLEAN="export KERNEL_SRC_DIR=${kernel_source_dir} && make clean -C ."
BUILT_MODULE_NAME=chipsec
BUILT_MODULE_LOCATION=.
PACKAGE_NAME=chipsec
DEST_MODULE_LOCATION="/extra"
PACKAGE_VERSION=%{version}
REMAKE_INITRD=no
AUTOINSTALL=no' > $RPM_BUILD_ROOT/%{_usrsrc}/%{dkms_name}-%{version}/dkms.conf

%files
%{_bindir}/chipsec_main
%{_bindir}/chipsec_util

%package -n %{srcname}-doc
Summary:          Documentation for CHIPSEC.
Version:          %{version}
Release:          1%{?dist}
License:          GPLv2
URL:              https://github.com/chipsec/chipsec

BuildArch:        noarch

%description -n %{srcname}-doc
%desc
Documentation.

%files -n %{srcname}-doc
%{_prefix}/share/doc/chipsec/chipsec-manual.pdf


%package -n python3-%{srcname}
Summary:          The python tools for CHIPSEC.
Version:          %{version}
Release:          1%{?dist}
License:          GPLv2
URL:              https://github.com/chipsec/chipsec

Requires:       %{dkms_name}-dkms = %{version}

%description -n python3-%{srcname}
%desc

%files -n python3-%{srcname}
%{python3_sitearch}/*

%package -n %{srcname}-dkms

Version:        %{realversion}
Release:        1%{?dist}
URL:            https://github.com/chipsec/chipsec
Summary:        DKMS kernel module for CHIPSEC
License:        GPLv2
Group:          System Environment/Kernel
Requires:       dkms
Requires:       nasm
Requires:       make
Requires:       gcc
Requires:       flex
Requires:       bison
Supplements:    python3-%{srcname}

%if "%{version}" == "1.3.5"
Requires:       kernel-devel < 4.15.0
Requires:       kernel < 4.15.0
%else
Requires:       kernel-devel < 5.7.0
Requires:       kernel < 5.7.0
%endif

%description -n %{srcname}-dkms
%desc

%post -n %{srcname}-dkms
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade
for i in `rpm -q --queryformat '%%{VERSION}-%%{RELEASE}.%%{ARCH} ' kernel-devel`;
do
  if [ $(echo $i|cut -d. -f1) -gt 5 ]; then continue; fi
  if [ $(echo $i|cut -d. -f2) -gt 6 ]; then continue; fi
  dkms build -m %{dkms_name} -v %{version} -q -k $i --kernelsourcedir=/usr/src/kernels/$i --config=/usr/src/kernels/$i/.config > /dev/null
  dkms install -m %{dkms_name} -v %{version} -q -k $i --kernelsourcedir=/usr/src/kernels/$i > /dev/null
done


%preun -n %{srcname}-dkms
dkms remove -m %{dkms_name} -v %{version} --all -q --rpm_safe_upgrade
if [ -e "/lib/modules/$(uname -r)/extra/chipsec.ko" ]; then
  rm "/lib/modules/$(uname -r)/extra/chipsec.ko"
fi

%files -n %{srcname}-dkms
%{_usrsrc}/%{dkms_name}-%{version}
%{_sysconfdir}/modules-load.d/chipsec.conf

%changelog
* Mon Oct 14 2019 Patrick Rudolph <patrick.rudolph@9elements.com> Patchlevel 2:
- Updated to 1.4.2
* Mon Feb 05 2018 Patrick Rudolph <patrick.rudolph@9elements.com> Patchlevel 1:
- Initial release

