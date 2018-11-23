#!/bin/bash
# Author: LeonMaxx
# This script downloads Primus-VK master branch from github and creates RPM package from it.

spec_file="primus-vk.spec"
work_dir="$PWD/work"
rpm_dir="$PWD/RPMs"
srpm_dir="$PWD/RPMs/src"
datestamp=`date +%Y%m%d`

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Downloading...${NC}"
wget -q -O primus_vk-master.zip https://github.com/felixdoerre/primus_vk/archive/master.zip || exit 1

mkdir -p $work_dir/SOURCES
mkdir -p $rpm_dir

cp primus_vk-master.zip $work_dir/SOURCES/
cp pvkrun $work_dir/SOURCES/
cp *.patch $work_dir/SOURCES/

echo -e "${GREEN}Building 64-bit package...${NC}"
rpmbuild -ba "$spec_file" --define "_topdir $work_dir" --define "_rpmdir $rpm_dir" --define "_srcrpmdir $srpm_dir"

echo -e "${GREEN}Building 32-bit package...${NC}"
rpmbuild -bb "$spec_file" --target=i686 --define "_topdir $work_dir" --define "_rpmdir $rpm_dir"

exit 0
