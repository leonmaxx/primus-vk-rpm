# Primus-vk-rpm
RPM packaging script for [Primus-vk](https://github.com/felixdoerre/primus_vk).  
  
Just run: `./create-package.sh`  
Created packages will be in RPMs sub directory.
  
After packages is installed run your vulkan application:
```shell
pvkrun vkapp
```

## Builds
Builds availale on [Releases](https://github.com/leonmaxx/primus-vk-rpm/releases) page, and on [Fedora COPR](https://copr.fedorainfracloud.org/coprs/leonmaxx/primus-vk-rpm/).

## Installing COPR .repo on Fedora
Fedora COPR doesn't support *multilib*, so to be able to install 32-bit libraries on 64-bit OS, please replace `.repo` file contents with:
```
[leonmaxx-primus-vk-rpm-i386]
name=Copr repo for primus-vk-rpm owned by leonmaxx
baseurl=https://copr-be.cloud.fedoraproject.org/results/leonmaxx/primus-vk-rpm/fedora-$releasever-i386/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/leonmaxx/primus-vk-rpm/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1

[leonmaxx-primus-vk-rpm-x86_64]
name=Copr repo for primus-vk-rpm owned by leonmaxx
baseurl=https://copr-be.cloud.fedoraproject.org/results/leonmaxx/primus-vk-rpm/fedora-$releasever-x86_64/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/leonmaxx/primus-vk-rpm/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1
```

## Installing
Just install `primus-vk` package. On 64-bit OS also install 32-bit libs package:
```
dnf install primus-vk primus-vk-libs.i686
```

## Issues
Issues with running Vulkan applications should be reported to [Primus-vk](https://github.com/felixdoerre/primus_vk) repository.  
In this repository report only packaging issues.
