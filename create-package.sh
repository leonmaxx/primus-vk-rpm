#!/bin/bash
# Author: LeonMaxx
# This script downloads Primus-VK master branch from github and creates RPM package from it.

spec_file="primus-vk.spec"
work_dir="$PWD/work"
rpm_dir="$PWD/RPMs"
datestamp=`date +%Y%m%d`
#release=1

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Downloading...${NC}"
wget -q -O primus-vk-master.zip https://github.com/felixdoerre/primus_vk/archive/master.zip || exit 1

#nvvulkan64=`find /usr/lib64/ -name "libGLX_nvidia.so.0"`
#nvvulkan32=`find /usr/lib/ -name "libGLX_nvidia.so.0"`

#if [ -z "$nvvulkan64" ]; then
#        echo -e "${RED}WARNING: 64-bit Nvidia Vulkan driver not found! Using default path.${NC}"
#        nvvulkan64="/usr/lib64/nvidia/libGLX_nvidia.so.0"
#fi

#if [ -z "$nvvulkan32" ]; then
#        echo -e "${RED}WARNING: 32-bit Nvidia Vulkan driver not found! Using default path.${NC}"
#        nvvulkan32="/usr/lib/nvidia/libGLX_nvidia.so.0"
#fi

mkdir -p $work_dir/SOURCES
mkdir -p $rpm_dir

cp primus-vk-master.zip $work_dir/SOURCES/
cp pvkrun $work_dir/SOURCES/
cp *.patch $work_dir/SOURCES/

echo -e "${GREEN}Building 64-bit package...${NC}"
rpmbuild -bb "$spec_file" --define "_topdir $work_dir" --define "_rpmdir $rpm_dir" --define "_version $datestamp" 
#--define "_driverpath $nvvulkan64"

#cp *.patch $work_dir/SOURCES/

echo -e "${GREEN}Building 32-bit package...${NC}"
rpmbuild -bb "$spec_file" --target=i686 --define "_topdir $work_dir" --define "_rpmdir $rpm_dir" --define "_version $datestamp" 
#--define "_driverpath $nvvulkan32"

exit 0
