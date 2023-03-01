---
title : 环境配置
categories : mtk
---


参考mtk服务器修改  
安装环境均为root权限，编译时使用普通用户  

##环境配置

####0.服务器联网
请按如下方法进行认证联网：

    curl -v -X POST http://10.101.18.1:8008/portal.cgi -H "X-Requested-With:XMLHttpRequest" -d "username=jyyin103&password=RmliZXJob21lMTIzLi4u&uplcyid=null&language=0&submit=submit"
用户名为邮箱名，密码为密码转换成base64，如结尾有=则替换成%3D，base64可以通过在线网页计算出来

####1.服务器系统信息：
	root@chgao-virtual-machine:/#cat /etc/os-release
	NAME="Ubuntu"
	VERSION="16.04 LTS (Xenial Xerus)"
	ID=ubuntu
	ID_LIKE=debian
	PRETTY_NAME="Ubuntu 16.04 LTS"
	VERSION_ID="16.04"
	HOME_URL="http://www.ubuntu.com/"
	SUPPORT_URL="http://help.ubuntu.com/"
	BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
	UBUNTU_CODENAME=xenial

####2.apt-get 换源，推荐使用阿里源

	cd /etc/apt
	cp sources.list sources.list.backup

	清华源：https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/
	deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
	deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
	deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
	deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse

	阿里源：https://www.cnblogs.com/Cqlismy/p/12848400.html
	deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
	deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
	deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
	deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
	deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
	deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
	deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
	deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
	deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
	deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse


	更换完成之后运行：apt-get update

	这里换源没有成功，恢复了原来的源，然后apt-get update

####3.安装make工具：
	apt-get install make

这里已经安装了，不用管

####4.安装rar 工具
没管

####5.工具链
	svn://fhbbssvn2.fiberhome.com:3703/dep_driver/public/thd_sdk/sdk_mtk/EN7529/toolchain
从svn下载了工具链，解压到/opt/trendchip

	root@chgao-virtual-machine:/opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr# ls -l
	total 28
	drwxrwxrwx  6 10067037 10067037 4096 12月  3  2020 arm-buildroot-linux-gnueabi
	drwxrwxrwx  2 10067037 10067037 4096 12月  4  2020 bin
	drwxrwxrwx  3 10067037 10067037 4096 12月  3  2020 i686-pc-linux-gnu
	drwxrwxrwx  4 10067037 10067037 4096 12月  3  2020 include
	drwxrwxrwx  6 10067037 10067037 4096 12月  3  2020 lib
	drwxrwxrwx  4 10067037 10067037 4096 12月  3  2020 libexec
	drwxrwxrwx 13 10067037 10067037 4096 12月  3  2020 share

	
PATH环境变量变更

	export PATH=$PATH:/opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr/

然后将此行代码复制到/etc/profile最后面，重启生效，可以很跟模块编译的2.编译报错一起处理


####6.修改默认的sh
	root@chgao-virtual-machine:/# ls -l /bin/sh
	lrwxrwxrwx 1 root root 4 10月 10  2018 /bin/sh -> dash
执行  

	sudo dpkg-reconfigure dash  
然后选择【No】

	root@chgao-virtual-machine:/# ls -l /bin/sh
	lrwxrwxrwx 1 root root 4 10月 10  2018 /bin/sh -> bash

####7.安装fakeroot  
××××注：避免出现编译报错3，建议使用SDK编译第3步中的方法安装fakeroot工具  ××××××

	apt-get install fakeroot

这里已安装

####8.安装gcc
	apt-get install gcc

这里已安装

####9.安装g++
	apt-get install g++

这里已安装

---------------------------------------------------------------

##SDK编译

####1.编译报错：ZLib.cpp:28:18: fatal error: zlib.h: No such file or directory
安装 Zlib	：https://blog.csdn.net/weixin_42108004/article/details/84890597  

	apt-get install zlib1g-dev

####2.编译报错：arm-buildroot-linux-gnueabi-gcc: Command not found
问题原因：64位服务器32位工具链问题  
解决方法：

	apt-get install lsb-core

安装完后仍然报错 

	root@chgao-virtual-machine:~# /opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr/bin/arm-buildroot-linux-gnueabi-gcc -h
	/opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr/bin/arm-buildroot-linux-gnueabi-gcc: error while loading shared libraries: libstdc++.so.6: cannot open shared object file: No such file or directory
 
解决方法

	sudo apt-get install libstdc++6 
	sudo apt-get install lib32stdc++6

####3.编译报错：ERROR: ld.so: object 'libfakeroot-sysv.so' from LD_PRELOAD cannot be preloaded (wrong ELF class: ELFCLASS64): ignored.
报错原因：64位服务器上apt-get 安装的fakeroot 运行有问题
解决方法：安装32位的fakeroot，或者安装sdk目录里的fakeroot

	apt-get purge fakeroot
	cd /home/intl_mtk/src/thd_code/thd_mtk_sdk_en752x/tools/fakeroot
	./configure --prefix=/usr/local/
	make
	make install


####4.编译报错：fatal error: openssl/conf.h: No such file or directory
	apt-get install libssl-dev

####5.编译报错：fatal error: sys/cdefs.h: No such file or directory
报错原因：64位的ubuntu系统，使用gcc想编译出32位的应用程序，需要使用gcc -m32选项，但是使用gcc -m32选项后，会报这个错误

	sudo apt-get update							报错不用管
	sudo apt-get install libc6-dev				已经安了
	sudo apt-get install libc6-dev-i386			主要安装这个

####6.sdk编译时间较长，参考方法把后面需要安装的都安装了

#####编译报错：/bin/sh: libtoolize: command not found  

安装libtool

	apt-get install libtool

#####编译报错：./autogen.sh: line 3: autoreconf: command not found  

安装 automake

	apt-get install automake

#####编译报错：
./configure: line 12769: syntax error near unexpected token `libnfnetlink,'

./configure: line 12769: `PKG_CHECK_MODULES(libnfnetlink, libnfnetlink >= 1.0,' 

安装 libnfnetlink-dev、libnfnetlink

	apt-get install libnfnetlink0
	apt-get install libnfnetlink-dev

#####编译报错：

configure: error: C compiler cannot create executables

config.log中报错：shared libraries: libz.so.1: cannot open shared object file: No such file or directory

安装 lib32z1

	apt-get install lib32z1

#####编译报错：

/bin/sh: bc: command not found

Kbuild:66: recipe for target 'include/generated/timeconst.h' failed

安装 bc

	apt-get install bc

#####编译报错：make: dos2unix: Command not found

安装 dos2unix

	apt-get install dos2unix

#####fatal error: curses.h: No such file or directory

	apt-get install libncurses5-dev

#####服务器不支持 mkfs.jffs2 命令

	apt-get install mtd-utils


####7.*** Error: No suitable bison/yacc found. ***
	apt-get install bison
	apt-get install libbison-dev

##模块编译
####1.编译报错：
/media/jiny5707_60027/TY4_test/compile/shared/tools/get_modules.pl --verbose --dst-dir=/media/jiny5707_60027/TY4_test --action=checkout --project_dir=src /media/jiny5707_60027/TY4_test/compile/shared/conf/svn_base.config /media/jiny5707_60027/TY4_test/compile/shared/conf/devices/svn_hi56xx_ty4.config
Can't locate Tie/IxHash.pm in @INC (you may need to install the Tie::IxHash module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.22.1 /usr/local/share/perl/5.22.1 /usr/lib/x86_64-linux-gnu/perl5/5.22 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl/5.22 /usr/share/perl/5.22 /usr/local/lib/site_perl /usr/lib/x86_64-linux-gnu/perl-base .) at /media/jiny5707_60027/TY4_test/compile/shared/tools/get_modules.pl line 47.
BEGIN failed--compilation aborted at /media/jiny5707_60027/TY4_test/compile/shared/tools/get_modules.pl line 47.

	apt-get install libtie-ixhash-perl



####2.编译报错：error while loading shared libraries: libmpc.so.3: cannot open shared object file: No such file or directory

find . -name "libmpc.so.3" | xargs ls -al		

发现该库存在编译工具链之中：/opt/trendchip/buildroot-gcc910_glibc229_arm64/lib/libmpc.so.3 
修改 LD_LIBRARY_PATH 变量：

	export LD_LIBRARY_PATH="/opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr/lib"

修改系统环境变量信息：在/etc/profile最后中新增此变量定义，重启生效；


####3.thd_open_src/libcap-ng 模块 configure 时，找不到 Python.h
解决方法：出现No such file or directory的错误，有两种情况，一种是没有Python.h这个文件，一种是Python的版本不对，可以进入/usr/include/文件夹下的Pythonx.x文件夹里查找是否有Python.h这个文件。
如果是第一种情况，那么需要安装Python-dev这个包，(sudo apt-get install python-dev)

	apt-get install python2.7
	apt-get install python-dev

另外，configure 提示 /usr/bin/python3-config 不存在，安装 python3-dev

	apt-get install python3-dev


####4.系统不支持 man 命令
解决方法：安装 man

	apt-get install man


####5.因 thd_open_src/libcap-ng 模块编译报错安装的软件：

	apt-get install glibc-doc
	apt-get install manpages-posix-dev

####6.方便从服务器传输文件，安装 lrzsz 工具

	apt-get install lrzsz

sz命令 发送文件到本地：	

	sz filename

rz命令 将本地上传文件到服务器	

	rz

执行该命令后，在弹出框中选择要上传的文件即可


####7.编译报错：make[2]: bison: Command not found
解决方法：
	sudo apt-get install bison
	sudo apt-get install libbison-dev


####8.thd_open_src 模块编译报错:configure: error *** You must have either have gettext support in your C library, or use the
*** GNU gettext library. (http://www.gnu.org/software/gettext/gettext.html)

解决方法：安装 gettext ： 

	apt-get install gettext


####9.dhcpv6 编译报错：make[2]: flex: Command not found

解决方法：安装 flex ：

	apt-get install flex


####10.编译报错：/bin/sh: ip6tables: command not found
解决方法：安装iptables：

	apt-get install iptables


####11.gdecms 编译报错：make[2]: gdbus-codegen: Command not found

解决方法：

	apt-get install libdbus-glib-1-dev




-----------------------------------------------------------

###总结

#####1.修改默认的sh

	sudo dpkg-reconfigure dash  

然后选择【No】


#####2.工具链

	svn://fhbbssvn2.fiberhome.com:3703/dep_driver/public/thd_sdk/sdk_mtk/EN7529/toolchain

从svn下载了工具链，解压到/opt/trendchip

	root@chgao-virtual-machine:/opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr# ls -l
	total 28
	drwxrwxrwx  6 10067037 10067037 4096 12月  3  2020 arm-buildroot-linux-gnueabi
	drwxrwxrwx  2 10067037 10067037 4096 12月  4  2020 bin
	drwxrwxrwx  3 10067037 10067037 4096 12月  3  2020 i686-pc-linux-gnu
	drwxrwxrwx  4 10067037 10067037 4096 12月  3  2020 include
	drwxrwxrwx  6 10067037 10067037 4096 12月  3  2020 lib
	drwxrwxrwx  4 10067037 10067037 4096 12月  3  2020 libexec
	drwxrwxrwx 13 10067037 10067037 4096 12月  3  2020 share

#####3.PATH环境变量变更

	export PATH=$PATH:/opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr/

	export LD_LIBRARY_PATH="/opt/trendchip/buildroot-gcc493_glibc222_arm32_32bServer/usr/lib"

	添加到/etc/profile最后面，重启

#####4.安装fakeroot

	apt-get purge fakeroot
	cd /home/intl_mtk/src/thd_code/thd_mtk_sdk_en752x/tools/fakeroot
	./configure --prefix=/usr/local/
	make
	make install

#####5.安装组件

	apt-get install make fakeroot gcc g++ zlib1g-dev lsb-core libstdc++6 lib32stdc++6 libssl-dev libc6-dev libc6-dev-i386 libtool automake libnfnetlink0 libnfnetlink-dev lib32z1 bc dos2unix libncurses5-dev mtd-utils bison libbison-dev libtie-ixhash-perl python2.7 python-dev python3-dev man glibc-doc manpages-posix-dev lrzsz gettext flex iptables libdbus-glib-1-dev
	
	
	
	
	
	
	
#####  编译报错

gcc编译时ld在链接时遇到了不合适的文件，因此需要安装对应的库文件。注意gcc-X-multilib中的X需要替换为你的gcc版本。

	sudo apt-get install gcc-X-multilib

