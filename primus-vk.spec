Name:           primus-vk
Version:        %{_version}
Release:        1%{?dist}
Summary:        Nvidia Vulkan offloading for Bumblebee
License:        BSD
Group:          Hardware/Other
Url:            https://github.com/felixdoerre/primus_vk
Source0:        %{name}-master.zip
Source1:        pvkrun
Patch0:         makefile.patch
Patch1:         gcc48.patch
Patch2:         driver_path.patch

BuildRequires:  gcc-c++
BuildRequires:  vulkan-devel

Requires:       vulkan-filesystem
Requires:       bumblebee

%description
This Vulkan layer can be used to do GPU offloading. Typically you want to display an image rendered on a more powerful GPU on a display managed by an internal GPU.
It is basically the same as Primus for OpenGL (https://github.com/amonakov/primus). However it does not wrap the Vulkan API from the application but is directly integrated into Vulkan as a layer (which seems to be the intendend way to implement such logic).

%prep
%setup -q -n primus_vk-master
%patch0 -p1
%if 0%{?rhel} || 0%{?fedora} < 26
%patch1 -p1
%endif
sed -i 's#__DRIVER_PATH__#\"%{_driverpath}\"#g' %{PATCH2}
%patch2 -p1

%build
export CXXFLAGS="%{optflags}"
make %{?_smp_mflags}

%install
install -D "libnv_vulkan_wrapper.so" "%{buildroot}%{_libdir}/libnv_vulkan_wrapper.so"
install -D "libprimus_vk.so" "%{buildroot}%{_libdir}/libprimus_vk.so"
install -m 755 -D "%{SOURCE1}" "%{buildroot}%{_bindir}/pvkrun"
install -D "primus_vk.json" "%{buildroot}%{_sysconfdir}/vulkan/implicit_layer.d/primus_vk.json"

%post
if [ ! -f /etc/vulkan/icd.d/nvidia_icd.json.primus-vk ]; then
    cp /etc/vulkan/icd.d/nvidia_icd.json /etc/vulkan/icd.d/nvidia_icd.json.primus-vk
    sed -i "s/libGLX_nvidia.so.0/libnv_vulkan_wrapper.so/g" /etc/vulkan/icd.d/nvidia_icd.json
fi

%postun
if [ $1 == 0 ] && [ -f /etc/vulkan/icd.d/nvidia_icd.json.primus-vk ]; then
    mv /etc/vulkan/icd.d/nvidia_icd.json.primus-vk /etc/vulkan/icd.d/nvidia_icd.json
fi

%files
%defattr(-,root,root)
%doc LICENSE README.md
%{_libdir}/libnv_vulkan_wrapper.so
%{_libdir}/libprimus_vk.so
%{_bindir}/pvkrun
%{_sysconfdir}/vulkan/implicit_layer.d/primus_vk.json

%changelog
* Sat Oct 13 2018 Leonid Maksymchuk <leonmaxx@4menteam.com>
- first attemp on rpm packaging
