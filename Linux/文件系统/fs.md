### dd命令：

用指定大小的块拷贝一个文件，并在拷贝的同时进行指定的转换。

常用参数：

if:输入文件名，缺省为标准输入。即指定源文件  
of:输出文件名，缺省为标准输出。即指定目的文件  
bs:同时设置读入/输出的块大小为bytes个字节  
count:仅拷贝blocks个块，块大小等于ibs指定的字节数  

eg:

`dd if=/dev/zero of=test.bin bs=1M count=1`

做一个1M的全是0的文件出来，dd命令还可以测试磁盘读写速度

### mount命令：

-t vfstype 指定文件系统的类型，通常不必指定，mount 会自动选择正确的类型。


-o options 主要用来描述设备或档案的挂接方式。

    loop：用来把一个文件当成硬盘分区挂接上系统  
    ro：采用只读方式挂接设备  
    rw：采用读写方式挂接设备  
    iocharset：指定访问文件系统所用字符集  

---

## ubifs制作

1. mkfs.ubifs

    制作UBIFS image  

    ```
    mkfs.ubifs -r system -m 2048 -e 126976 -c 1057 -x zlib -o system.ubifs
    mkfs.ubifs -r rootfs -o rootfs.img -F -m 2048 -e 124KiB -c 40
    ```

    -r：待制作的文件系统目录

    -o：输出的image名字。

    -F：使能“white-space-fixup”，如果是通过u-boot烧写需要使能此功能

    -m：Nand Flash的最小读写单元，一般为page size。

    -e：LEB size，说的是逻辑擦除块大小，大家知道nand flash页读页写块擦，一个设备多个块，一个块多个页，一般也都是一个块是64个页，这样算一下无论擦除块大小就是2048\*64=131072，-e的算法是物理擦除块大小-2\*页大小，这里就是131072-2*2048=126976

    -c：说的是最大逻辑块数量，这个很重要，不能大也不能小，太小也要大于image大小，太大mount有问题。计算起点是分区的物理块数量，比如128MiB的mtd分区，物理块数量是128MiB/2048/64 = 1024个，需要减去2个坏块保留块，减去1个wear-leveling块，还要减去1个eba的块，等等，比如最终的值是1022，注意，如果物理上这个分区有坏块的话，kernel会扫描到的，这时候，我们计算的这个值就要减去坏块数了，否则会有逻辑块大于物理块数的内核问题mount失败，确切知道坏块数是比较困难的，一般做法是做一个坏块容忍数，比如20个，这样我们再减去20个坏块，不要担心这个会浪费空间，ubinize的autoresize选项就是解决这个问题的。具体的这个值需要计算。

    -x：说的是压缩方法，默认是lzo，还支持zlib，zlib压缩率高些，但是lzo压缩解压速度快 。

2. ubinize

    根据UBIFS image制作ubi.img，这个ubi.img是通过u-boot直接烧写到nand flash分区上的。

    `ubinize -o system.ubi -m 2048 -p 131072 ubinize.cfg`

    -o说的是输出image  
    -m还是页大小  
    -p是物理擦除块大小 131072 = 128 * 1024

    ubinize.cfg是volume配置文件，例子如下：  
    ```
    [ubifs]
    mode=ubi
    image=system.ubifs #说的是mkfs.ubifs的结果
    vol_id=0
    vol_size=100MiB #说的是volume大小，用-e和-c的值做乘法计算，一般不用写，autoresize会自动根据mtd分区大小适应，默认值是image大小，写了这个作用是帮助检查image是否超过了分区限制，制作时候就提示，否则mount会出错。-c的值是经过计算的最大值了，不过autoresize参数会自适应大小，不会浪费空间的。
    vol_type=dynamic
    vol_alignment=1
    vol_name=system #说的是分区名字
    vol_flags=autoresize
    ```

## ubifs mount

假设我们想在mtdblock1上加载ubifs文件系统，步骤如下：
1. `/ubiformat /dev/mtd1`  

    格式化mtdblock1

2. `/ubiattach /dev/ubi_ctrl -m 1`  

    将mtdblock1与ubi建立连接，系统自动将mtd1关连到ubi2上，假设系统中已经存在ubi0, ubi1了。  

    -m x  mtd号  
    -d x  ubi device  

3. `ls /sys/class/ubi/`  

    可以看到该目录下增加了一个ubi2的子目录

4. `cat /sys/class/ubi/ubi2/dev`

    可以得到该ubi2设备的主次设备号，如249：0

5. `cat /sys/class/ubi/ubi2/volumes_count`

    结果为0，表示该ubi上没有任何volume

6. `ls /dev/ubi*`

    如果/dev中没有ubi2, 则手工创建“mknod /dev/ubi2 c 249 0”

(删卷操作：`./ubirmvol /dev/ubi2 -N my_ubi_vol`)

7. `./ubimkvol /dev/ubi2 -s 100MiB -N my_ubi_vol`

    在ubi2上创建一个volume  

    -s x 指定volume大小 单位KiB, MiB  
    -S x 指定volume大小 指定x个LEB  
    -N x 指定卷名

8. `ls /sys/class/ubi/`

    可以看到该目录下增加一个ubi2_0的目录，代表ubi2上的第一个volume，如果“cat /sys/class/ubi/ubi2_0/name”， 你可以得到“my_ubi_vol”，这就是（7）中的名字。

9. `cat /sys/class/ubi/ubi2_0/dev `

    得到该volume的主次设备号，如249：1

10. `mknod /dev/ubi2_0 c 249 1 `

    如果/dev中没有ubi2_0, 则需要手工创建

11. ` mount -t ubifs ubi2_0 /mnt 或者 mount -t ubifs ubi2:my_ubi_vol /mnt`

    将ubi2_0挂载到本地目录 /mnt上，

12. `mount`

    可以看到ubi2_0成功挂载在/mnt上。

参考：

http://t.zoukankan.com/embedded-linux-p-5674218.html

---

## Squashfs制作

mksquashfs4命令


## jffs2

`mount -o rw,sync -t jffs2 /dev/mtdblock5 /fhbak`