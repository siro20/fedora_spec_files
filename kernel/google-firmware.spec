# spec file for package google-firmware-drivers
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

%define srcname google-firmware-drivers-dkms

Name:             %{srcname}
Version:          5.0.9
Release:          1%{?dist}
Summary:          Google Firmware Drivers, Kernel modules for memconsole and coreboot tables
License:          GPLv2
URL:              https://www.kernel.org/
Source0:          https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
Group:            Applications/Tools

BuildRequires:  redhat-rpm-config
BuildRequires:  sed

Requires:       memconsole-coreboot-dkms == %{version}
Requires:       coreboot-table-dkms == %{version}

%define desc These firmware drivers are used by Google's servers. They are only useful if you are working directly on one of their proprietary servers.

%description
%desc

%global debug_package %{nil}

%prep -n %{srcname}
%autosetup -n linux-%{version}

%build -n %{srcname}
%install

%undefine srcname
%define srcname memconsole-coreboot

# Load kernel module on boot
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/modules-load.d/
echo "%{srcname}" > $RPM_BUILD_ROOT/%{_sysconfdir}/modules-load.d/%{srcname}.conf

# Create DKMS folder
mkdir -p $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/

# Install dkms.conf
echo "MAKE=\"make -C . KERNELDIR=/lib/modules/\${kernelver}/build MACHINE=%{_arch}\"
CLEAN=\"make clean -C . KERNELDIR=/lib/modules/\${kernelver}/build MACHINE=%{_arch}\"
BUILT_MODULE_NAME=%{srcname}
BUILT_MODULE_LOCATION=.
PACKAGE_NAME=%{srcname}
DEST_MODULE_LOCATION=\"/extra\"
PACKAGE_VERSION=%{version}
REMAKE_INITRD=no
AUTOINSTALL=yes" > $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/dkms.conf

# Just copy files for DKMS
cp drivers/firmware/google/* $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/

# Install Makefile
echo "%{srcname}-y := memconsole.o memconsole-coreboot.o
obj-m=%{srcname}.o

all: %{srcname}

check_kernel_dir:
	@if [ ! -d \$(KERNELDIR) ]; then \
		echo \"Unable to find the Linux source tree.\"; \
		exit 1; \
	fi

%{srcname}: check_kernel_dir clean
	make -C \$(KERNELDIR) M=\${CURDIR} modules
clean: check_kernel_dir
	make -C \$(KERNELDIR) M=\${CURDIR} clean
" > $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/Makefile



%undefine srcname
%define srcname coreboot-table

# Create DKMS folder
mkdir -p $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/

# Install dkms.conf
echo "MAKE=\"make -C . KERNELDIR=/lib/modules/\${kernelver}/build MACHINE=%{_arch}\"
CLEAN=\"make clean -C . KERNELDIR=/lib/modules/\${kernelver}/build MACHINE=%{_arch}\"
BUILT_MODULE_NAME=%{srcname}
BUILT_MODULE_LOCATION=.
PACKAGE_NAME=%{srcname}
DEST_MODULE_LOCATION=\"/extra\"
PACKAGE_VERSION=%{version}
REMAKE_INITRD=no
AUTOINSTALL=yes" > $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/dkms.conf

# Just copy files for DKMS
cp drivers/firmware/google/* $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/

# Install Makefile
echo "%{srcname}-y := coreboot_table.o
obj-m=%{srcname}.o 

all: %{srcname}

check_kernel_dir:
	@if [ ! -d \$(KERNELDIR) ]; then \
		echo \"Unable to find the Linux source tree.\"; \
		exit 1; \
	fi

%{srcname}: check_kernel_dir clean
	make -C \$(KERNELDIR) M=\${CURDIR} modules
clean: check_kernel_dir
	make -C \$(KERNELDIR) M=\${CURDIR} clean
" > $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/Makefile



%files

%undefine srcname
%define srcname coreboot-table


%package -n %{srcname}-dkms

Version:        %{version}
Release:        %{?dist}
URL:            https://www.kernel.org/
Summary:        Google Firmware coreboot tables
License:        GPLv2
Group:          System Environment/Kernel
Requires:       dkms

Requires:       kernel-devel >= %{version}
Requires:       kernel >= %{version}

%description -n %{srcname}-dkms
%desc

%post -n %{srcname}-dkms
dkms add -m %{srcname} -v %{version} -q --rpm_safe_upgrade
for i in `rpm -q --queryformat '%%{VERSION}-%%{RELEASE}.%%{ARCH} ' kernel-devel`;
do
  dkms build -m %{srcname} -v %{version} -k $i > /dev/null
  dkms install -m %{srcname} -v %{version} -k $i > /dev/null
done

%preun -n %{srcname}-dkms
dkms remove -m %{srcname} -v %{version} --all -q --rpm_safe_upgrade

%files -n %{srcname}-dkms
%{_usrsrc}/%{srcname}-%{version}




%undefine srcname
%define srcname memconsole-coreboot


%package -n %{srcname}-dkms

Version:        %{version}
Release:        %{?dist}
URL:            https://www.kernel.org/
Summary:        Google Firmware memconsole
License:        GPLv2
Group:          System Environment/Kernel
Requires:       dkms

Requires:       kernel-devel >= %{version}
Requires:       kernel >= %{version}
Requires:       coreboot-table-dkms == %{version}

%description -n %{srcname}-dkms
%desc

%post -n %{srcname}-dkms
dkms add -m %{srcname} -v %{version} -q --rpm_safe_upgrade
for i in `rpm -q --queryformat '%%{VERSION}-%%{RELEASE}.%%{ARCH} ' kernel-devel`;
do
  dkms build -m %{srcname} -v %{version} -k $i > /dev/null
  dkms install -m %{srcname} -v %{version} -k $i > /dev/null
done

%preun -n %{srcname}-dkms
dkms remove -m %{srcname} -v %{version} --all -q --rpm_safe_upgrade

%files -n %{srcname}-dkms
%{_usrsrc}/%{srcname}-%{version}
%{_sysconfdir}/modules-load.d/%{srcname}.conf





%changelog
* Tue Sep 17 2019 Patrick Rudolph <patrick.rudolph@9elements.com> Patchlevel 2:
- Updated to kernel 5.0

* Mon Feb 05 2018 Patrick Rudolph <patrick.rudolph@9elements.com> Patchlevel 1:
- Initial release


