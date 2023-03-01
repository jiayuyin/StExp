```c
#include<sys/syscall.h>

//放在线程函数里
int my_tid = syscall(SYS_gettid);
printf("my tid is %d\n", my_tid);
```