gdb编译

首先，需要调试的程序必须保留调试信息，在编译时带上`-g`选项，否则无法调试

如果不确定是否带调试符号，可以通过如下命令验证：

`gdb main`

如果出现`no debugging symbols found`字段，则表示不带调试符号

还有使用`readelf`查看

`readelf -S main | grep debug`

如果有`debug`字段，则说明可以调试

gdb 

1.直接启动进程来调试

`gdb test`

2.进程运行后实时调试

`gdb attach pid` 或 `gdb -p pid`

基本操作

1. 运行  
`r` (run)

2. 查看调用栈  
`bt` (backtrace)

3. 断点  
`b 行号` (break)  
`b 文件名:行号`  
`b 函数名`
`b 文件名:行号 if xxx` 条件断点  
`i b` (info breakpoints)  
`d x` (delete breakpoints) x为num  



