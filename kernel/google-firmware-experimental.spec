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

%define srcname google-firmware-drivers-experimental-dkms

Name:             %{srcname}
Version:          ad7a47dee899db5687dcd5717b4e9b07d7f681ff
Release:          1%{?dist}
Summary:          Experimental google Firmware Drivers, Kernel modules for memconsole and coreboot tables
License:          GPLv2
URL:              https://github.com/9elements/linux
Source0:          https://github.com/9elements/linux/archive/ad7a47dee899db5687dcd5717b4e9b07d7f681ff.tar.gz
Group:            Applications/Tools

BuildRequires:  redhat-rpm-config
BuildRequires:  sed

Requires:       coreboot-memconsole-experimental-dkms == %{version}
Requires:       coreboot-table-experimental-dkms == %{version}

%define desc These firmware drivers are used by Google's servers. They are only useful if you are working directly on one of their proprietary servers.

%description
%desc

%global debug_package %{nil}

%prep -n %{srcname}
%autosetup -n linux-%{version}

%build -n %{srcname}
%install


# Shared Makefile
# Required as all modules need to be build at once to satisfy symvers
mkdir -p $RPM_BUILD_ROOT/%{_usrsrc}/
echo "coreboot-memconsole-experimental-y := memconsole.o memconsole-coreboot.o
obj-m+=coreboot-memconsole-experimental.o

coreboot-table-experimental-y := coreboot_table.o
obj-m+=coreboot-table-experimental.o 

coreboot-cbmem-experimental-y := cbmem-coreboot.o
obj-m+=coreboot-cbmem-experimental.o

all: check_kernel_dir
	make -C \$(KERNELDIR) M=\${CURDIR} clean
	make -C \$(KERNELDIR) M=\${CURDIR} modules

check_kernel_dir:
	@if [ ! -d \$(KERNELDIR) ]; then \
		echo \"Unable to find the Linux source tree.\"; \
		exit 1; \
	fi

clean: check_kernel_dir
	make -C \$(KERNELDIR) M=\${CURDIR} clean
" > $RPM_BUILD_ROOT/%{_usrsrc}/Makefile

%undefine srcname
%define srcname coreboot-memconsole-experimental

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
AUTOINSTALL=yes" > $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/dkms.conf

# Just copy files for DKMS
cp drivers/firmware/google/* $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/

# Install Makefile
cp $RPM_BUILD_ROOT/%{_usrsrc}/Makefile $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/Makefile


%undefine srcname
%define srcname coreboot-table-experimental

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
cp $RPM_BUILD_ROOT/%{_usrsrc}/Makefile $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/Makefile

echo "%{srcname}" > $RPM_BUILD_ROOT/%{_sysconfdir}/modules-load.d/%{srcname}.conf

%undefine srcname
%define srcname coreboot-cbmem-experimental

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
cp $RPM_BUILD_ROOT/%{_usrsrc}/Makefile $RPM_BUILD_ROOT/%{_usrsrc}/%{srcname}-%{version}/Makefile
echo "%{srcname}" > $RPM_BUILD_ROOT/%{_sysconfdir}/modules-load.d/%{srcname}.conf



# Remove Makefile template
rm -f $RPM_BUILD_ROOT/%{_usrsrc}/Makefile


%files

%undefine srcname
%define srcname coreboot-table-experimental


%package -n %{srcname}-dkms

Version:        %{version}
Release:        1%{?dist}
URL:            https://www.kernel.org/
Summary:        Experimental google Firmware coreboot tables
License:        GPLv2
Group:          System Environment/Kernel
Requires:       dkms

Requires:       kernel-devel >= %{version}
Requires:       kernel >= %{version}
Requires:       make
Requires:       gcc
Requires:       flex
Requires:       bison

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




%undefine srcname
%define srcname coreboot-memconsole-experimental


%package -n %{srcname}-dkms

Version:        %{version}
Release:        1%{?dist}
URL:            https://www.kernel.org/
Summary:        Experimental google Firmware memconsole
License:        GPLv2
Group:          System Environment/Kernel
Requires:       dkms

Requires:       kernel-devel >= %{version}
Requires:       kernel >= %{version}
Requires:       make
Requires:       coreboot-table-experimental-dkms == %{version}

%description -n %{srcname}-dkms
%desc
Exposes /sys/firmware/log which allows to read the boot log recorded by coreboot
on every boot.

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


%undefine srcname
%define srcname coreboot-cbmem-experimental


%package -n %{srcname}-dkms

Version:        %{version}
Release:        1%{?dist}
URL:            https://www.kernel.org/
Summary:        Experimental google Firmware cbmem
License:        GPLv2
Group:          System Environment/Kernel
Requires:       dkms

Requires:       kernel-devel >= %{version}
Requires:       kernel >= %{version}
Requires:       make
Requires:       coreboot-table-experimental-dkms == %{version}

%description -n %{srcname}-dkms
%desc
Exposes /sys/bus/coreboot/drivers/cbmem/

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
* Tue Mar 17 2020 Patrick Rudolph <patrick.rudolph@9elements.com> Patchlevel 3:
- Removed no longer existing kernel modules
- Switched to new branch

* Tue Sep 17 2019 Patrick Rudolph <patrick.rudolph@9elements.com> Patchlevel 2:
- Updated to kernel 5.0

* Mon Feb 05 2018 Patrick Rudolph <patrick.rudolph@9elements.com> Patchlevel 1:
- Initial release


