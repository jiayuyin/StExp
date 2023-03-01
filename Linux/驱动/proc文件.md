## 创建proc文件

基本上就是固定套路

/proc 文件系统是一种内核和内核模块用来向进程 (process) 发送信息的机制 (所以叫做 /proc)。  
这个伪文件系统让你可以和内核内部数据结构进行交互，获取有关进程的有用信息，在运行中 (on the fly) 改变设置 (通过改变内核参数)。  
 与其他文件系统不同，/proc 存在于内存之中而不是硬盘上。

文件权限定义

S_IRUSR：用户读权限

S_IWUSR：用户写权限

S_IRGRP：用户组读权限

S_IWGRP：用户组写权限

S_IROTH：其他组都权限

S_IWOTH：其他组写权限

```
// 声明在文件linux/uaccess.h中，记得在驱动代码中包含进去
static __always_inline unsigned long __must_check copy_to_user(void __user *to, const void *from, unsigned long n)    //第一个参数是目的地址，第二个参数是源地址，第三个参数是数据的size
static __always_inline unsigned long __must_check copy_from_user(void *to, const void __user *from, unsigned long n)    //第一个参数是目的地址，第二个参数是源地址，第三个参数是数据的size
```