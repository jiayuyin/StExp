## 建立本地PC与gitbub关联  

1. 创建ssh key  
    ```
    ssh-keygen -t rsa -C "yin.jiayu@qq.com"
    ```

    然后在用户目录下会有一个.ssh文件夹  

    复制id_rsa.pub的内容，复制里面的内容绑定在github上

    绑定之后验证一下:  
    ```
    ssh -T git@github.com
    ```

    出现successful就成功了


2. 绑定用户，邮箱
    ```
    git config --global user.name "jiayuyin"
    git config --global user.email "yin.jiayu@qq.com"
    ```

上面的做了之后就不用再在本地电脑设置了

---
## 创建项目

1. github创建仓库

    创建之后它会教你怎么使用，如下：
    ```
    …or create a new repository on the command line

    echo "# StExp" >> README.md
    git init  //把这个目录变成Git可以管理的仓库
    git add README.md  //文件添加到仓库
    git commit -m "first commit"  //把文件提交到仓库并附加log
    git branch -M main  //选择分支
    git remote add origin git@github.com:jiayuyin/StExp.git  //关联远程仓库
    git push -u origin main  //把本地库的所有内容推送到远程库上

    …or push an existing repository from the command line

    git remote add origin git@github.com:jiayuyin/StExp.git
    git branch -M main
    git push -u origin main
    ```

上面的做了之后本地仓库就可以跟github上的关联起来了，后续可以提交代码

---
## 基本操作

1. 下载，提交，更新
    ```
    提交代码三步：
    git add .
    git commit -m "first commit"
    git push -u origin main

    下载
    git clone 地址  //下载到本地
    git clone -b 分支名 地址    //下载分支的代码到本地

    更新
    git pull
    ```

2. git add回退
    ```
    git status 先看一下add中的文件，确定已经添加的文件。  
    git reset HEAD 如果后面什么都不跟的话，就是add已添加的全部撤销。  
    git reset HEAD xxx.c 只撤销所列出的文件。  
    ```

3. git commit回退
    ```
    git reset --soft HEAD^  
    ```
    这样就成功的撤销了你的commit。注意，仅仅是撤回commit操作，您写的代码仍然保留。

    HEAD^的意思是上一个版本，也可以写成HEAD~1，如果你进行了2次commit，想都撤回，可以使用HEAD~2  

    --mixed 不删除工作空间改动代码，撤销commit，并且撤销git add . 操作，这个为默认参数, git reset --mixed HEAD^ 和 git reset HEAD^ 效果是一样的。

    --soft  不删除工作空间改动代码，撤销commit，不撤销git add .
    
    --hard 删除工作空间改动代码，撤销commit，撤销git add .

    如果commit注释写错了，只是想改一下注释，只需要：
    ```
    git commit --amend
    ```

4. 分支
    ```
    git checkout . ////回退所有的修改
    git checkout -- filename //回退filename的修改

    git checkout -b 分支名    //新建分支并切换至新分支
    git branch -d XX    //普通删除分支
    git branch -D XX    //强制删除分支
    ```

5. 其他
    ```
    git config --list  //查看已有配置
    git remote -v //查看远程路径
    ```

## 遇到的问题

---
如果你clone下来一个别人的仓库，在此基础上完成你的代码，推送到自己的仓库可能遇到如下问题：  
`error: remote origin already exists.`  
表示远程仓库已存在。因此你要进行以下操作：  
1、先输入git remote rm origin 删除关联的origin的远程库  
2、关联自己的仓库 git remote add origin https://github.com/xxxxxx.git  
3、最后git push origin master，这样就推送到自己的仓库了。  

---

git status不显示中文：  
`git config --global core.quotepath false`  
然后设置Options->test  
Locale：zh_CN  
Character：UTF-8  

