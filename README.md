# Primus-vk-rpm
RPM packaging script for [Primus-vk](https://github.com/felixdoerre/primus_vk).  
  
Just run: `./create-package.sh`  
Created packages will be in RPMs sub directory.
  
After packages is installed run your vulkan application:
```shell
pvkrun vkapp
```

# Builds
Builds availale on [Releases](https://github.com/leonmaxx/primus-vk-rpm/releases) page, and on [Fedora COPR](https://copr.fedorainfracloud.org/coprs/leonmaxx/primus-vk-rpm/).

# Installing
Just install `primus-vk` package. On 64-bit OS also install 32-bit libs package:
```
dnf install primus-vk primus-vk-libs.i686
```

# Issues
Issues with running Vulkan applications should be reported to [Primus-vk](https://github.com/felixdoerre/primus_vk) repository.  
In this repository report only packaging issues.
