%define _version %(date +"%Y%m%d")

Name:           primus-vk
Version:        %{_version}
Release:        1%{?dist}
Summary:        Primus-Vk Nvidia Vulkan offloading for Bumblebee
License:        BSD
Group:          Hardware/Other
Url:            https://github.com/felixdoerre/primus_vk
Source0:        primus_vk-master.zip
Source1:        pvkrun

# Patch for makefile to use provided compiler flags
Patch0:         makefile.patch

# Patch to compile on Fedora 29
Patch1:         fedora29.patch

# Patch to compile on Fedora COPR for EPEL-7 where vulkan_xcb.h header is not available
Patch2:         epel_vulkan.patch

# Temporary patch
#Patch3:         gcc48.patch

BuildRequires:  gcc-c++
BuildRequires:  vulkan-devel
BuildRequires:  libxcb-devel
BuildRequires:  mesa-libGL-devel
%if 0%{?fedora} >= 29
BuildRequires:  vulkan-validation-layers-devel
%endif

Requires:       vulkan-filesystem
Requires:       bumblebee
Requires:       %{name}-libs

%description
This Vulkan layer can be used to do GPU offloading. Typically you want to display an image rendered on a more powerful GPU on a display managed by an internal GPU.
It is basically the same as Primus for OpenGL (https://github.com/amonakov/primus). However it does not wrap the Vulkan API from the application but is directly integrated into Vulkan as a layer (which seems to be the intendend way to implement such logic).

%package libs
Version:        %{_version}
Release:        1%{?dist}
Summary:        Primus-Vk libraries
License:        BSD

%description libs
%{summary}

%prep
%setup -q -n primus_vk-master
%patch0 -p1
%if 0%{?fedora} >= 29
%patch1 -p1
%endif
%if 0%{?rhel}
%patch2 -p1
%endif
#%if 0%{?fedora} <= 28 || 0%{?epel} == 7
#%patch3 -p1
#%endif

%build
%if 0%{?rhel}
export CXXFLAGS="%{optflags} -I."
%else
export CXXFLAGS="%{optflags}"
%endif
make %{?_smp_mflags}

%install
install -D "libnv_vulkan_wrapper.so" "%{buildroot}%{_libdir}/libnv_vulkan_wrapper.so"
install -D "libprimus_vk.so" "%{buildroot}%{_libdir}/libprimus_vk.so"
install -Dm 755 "primus-vk-diag" "%{buildroot}%{_bindir}/primus-vk-diag"
install -Dm 755 "%{SOURCE1}" "%{buildroot}%{_bindir}/pvkrun"
install -D "primus_vk.json" "%{buildroot}%{_sysconfdir}/vulkan/implicit_layer.d/primus_vk.json"

%post
if [ -f /etc/vulkan/icd.d/nvidia_icd.json ]; then
	if [ ! -f /etc/vulkan/icd.d/nvidia_icd.json.primus-vk ]; then
		cp /etc/vulkan/icd.d/nvidia_icd.json /etc/vulkan/icd.d/nvidia_icd.json.primus-vk
		sed -i "s/libGLX_nvidia.so.0/libnv_vulkan_wrapper.so/g" /etc/vulkan/icd.d/nvidia_icd.json
	fi
fi
if [ -f /usr/share/vulkan/icd.d/nvidia_icd.json ]; then
	if [ ! -f /usr/share/vulkan/icd.d/nvidia_icd.json.primus-vk ]; then
		cp /usr/share/vulkan/icd.d/nvidia_icd.json /usr/share/vulkan/icd.d/nvidia_icd.json.primus-vk
		sed -i "s/libGLX_nvidia.so.0/libnv_vulkan_wrapper.so/g" /usr/share/vulkan/icd.d/nvidia_icd.json
	fi
fi

%postun
if [ $1 == 0 ]; then
	if [ -f /etc/vulkan/icd.d/nvidia_icd.json.primus-vk ]; then
		mv /etc/vulkan/icd.d/nvidia_icd.json.primus-vk /etc/vulkan/icd.d/nvidia_icd.json
	fi
	if [ -f /usr/share/vulkan/icd.d/nvidia_icd.json.primus-vk ]; then
		mv /usr/share/vulkan/icd.d/nvidia_icd.json.primus-vk /usr/share/vulkan/icd.d/nvidia_icd.json
	fi
fi

%files
%defattr(-,root,root)
%doc LICENSE README.md
%{_bindir}/primus-vk-diag
%{_bindir}/pvkrun
%{_sysconfdir}/vulkan/implicit_layer.d/primus_vk.json

%files libs
%{_libdir}/libnv_vulkan_wrapper.so
%{_libdir}/libprimus_vk.so


%changelog
* Tue Oct 16 2018 Leonid Maksymchuk <leonmaxx@4menteam.com>
- update scripts
- include primus-vk-diag

* Sat Oct 13 2018 Leonid Maksymchuk <leonmaxx@4menteam.com>
- first attemp on rpm packaging
