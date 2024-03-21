## 连接

**查看源**：`git remote -v`

**源端起别名**：`git remote add [源别名] [origin_shhaddress]`

## 配置

**配置用户名**：`git config -global user.name "userName"`

**配置用户邮箱**：`git cinfig --global user,email "mail@163.com`

## 基础操作

初始化Git库：`git init`：在当前工作目录下创建

查当前修改状态：`git status`

把修改提交到暂存区：`git add [file name]`

指定文件：`git add .`:所有文件

提交修改：`git commit -m [注释内容]`

查看、回滚之前的提交：
	`git log`：查看本次操作的提交记录
	`git reset --hard [commit_id]`：回滚到之前的某个commit

上传、拉取：
	`git push [origin_sshaddress] [brand_name]`：将修改同步到云端
	`git pull`：从云端拉取内容
	`git fetch upstream`：从上游更新本地代码

## 忽略清单

- 将不需要管理的文件名添加到子文件中后执行git时git会忽略此文件
- 忽略清单文件名：`.gitignore`

## 分支

- `git branch`：查看所有分支
- `git branch [newBranchName]`：新建分支
- `git checkout [branchName]`：切换到已存在的分支
- `git checkout -b [branchName]`：新建并切换

合并分支：

- 要求：要出于main分支
- `git branch merge [branchName]`
- `git merge upstream/main`：把源中的主分支代码同步到当前分支
- `git branch -D [branchName]`：产出分支