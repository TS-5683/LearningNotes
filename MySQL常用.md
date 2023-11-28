[TOC]

# 1语句大致分类

## 1.1DDL

### 1.1.1数据库操作

#### 1.1.1.1查询所有数据库

```mysql
show databases;
```

#### 1.1.1.2创建新的数据库

```mysql
create [if not exists] database database_name [default charset 字符集] [collate 排序规则];  #[]表示其中的内容是可以省略的
#如：
create database ItHeima default charset utf8mb4;
#创建的数据库的字符集指定为utf-8
```

#### 1.1.1.3删除数据库

```mysql
drop database [if exists] database_name;
```

#### 1.1.1.4查看数据库定义信息

```mysql
show create database database_name;
```

#### 1.1.1.5切换到数据库

```mysql
use database database_name;
```

#### 1.1.1.6查询当前所处的数据库

```mysql
select database();  #()表示是一个函数
```

### 1.1.2表操作

#### 1.1.2.1查询当前数据库所有表

```mysql
show tables;
```

#### 1.1.2.2查询表结构。可以查看当前表中有哪些字段

```mysql
desc table_name;
```

#### 1.1.2.3查询指定表的定义信息

```mysql
show create table table_name;
```

#### 1.1.2.4创建表

```mysql
create table table_name(
	字段1 字段1类型 [comment 字段1注释],
	字段2 字段2类型 [comment 字段2注释],
	字段3 字段3类型 [comment 字段3注释]
)[comment 表注释];  #[]表示可选
```

#### 1.1.2.5删除表中字段

```mysql
alter table tablename drop [column] column_neme;  #[]表示内容可选
```

#### 1.1.2.6添加表中字段

```mysql
#单个添加
alter table tablename add column_name datatype;
#多个添加
alter table tablename add (
    column_name datatype [default...] [comment...],
    column_name datatype [default...] [comment...]
);
```

####   1.1.2.7修改字段名

```mysql
# 可以把字段名和字段属性一同修改
alter table tablename change oldcolumn newcolumn datatype;
#修改字段属性
alter table tablename modify column_name datatype;
#修改表名
alter table tablename rename to newtable_name;
```

### 1.1.3MySQL数据类型

#### 1.1.3.1数值类型

##### 1.1.3.1.1整数型

tinyint 1字节

smallint 2字节

mediumint 3字节

int 4字节

bigint 8字节

##### 1.1.3.1.2浮点型

float(m,d) 单精度

double(m,d) 双精度

m为总位数，d为小数点后位数

##### 1.1.3.1.4定点型

decimal(m,d)

m为总位数，d为小数点后位数

#### 1.1.3.2字符串类型

char(m)  长度为m的字符串，以空格填充

varchar(m)  长度可变，最大长度为m

tinytext[(m)]  段文本字符串0~255byte

text  长文本数据0~65535 byte

memiumtext[(m)] 中等长度文本 0~16777215 byte

longtext[(m)]   极大文本  0~429496725 byte

blob 二进制数据

tinyblob

mediumblob

lonblob

#### 1.1.3.3时间类型

date        yyyy-mm-dd

time        hh:mm:ss

year         yyyy

datetime        yyyy-mm-dd hh:mm:ss

timestamp        yyyy-mm-dd hh:mm:ss

## 1.2DML

### 1.2.1查询表中数据

```mysql
#查询表中所有数据
select * from tablename;
#查询制定字段数据
select column_name1,column_name2,... from tablename;
```

### 1.2.2添加数据（insert）

```mysql
#给指定字段添加数据
insert into tablename(column_name1,column_name2,...) values (value1,value2,...);
#给全部字段添加数据
insert into tablename values(value1,value2,...);  #值的顺序应和对应字段顺序相同
#批量添加数据
insert into tablename (column_name1,column_name2,...) values (value1_1,value1_2,...),(value2_1,value2_2,...),...;
insert into tablename values(value1_1,value1_2,...),(value2_1,value2_2,...),...;
```

### 1.2.3修改数据（update）

```mysql
UPDATE tablename SET column_name1 = value1, column_name2 = value2,... [WHERE condition_name];
UPDATE user SET name = '钱五' WHERE id = 1001;  #将id为1001的这一条数据的name字段值改为‘钱五’
#where 语句为可选，未写时更新整张表的数据
```

### 1.2.4删除数据（delete）

```mysql
delete from tablename where [condition_];
/*
无条件时删除表中所有数据
删除的是表中的数据，而不是表本身
不能单独删除某一个字段，如果有这个需要可以用update语句将其设为NULL
*/
```

## 1.3DQL——查询

```mysql
select 
	字段列表
from 
	表名列表
where 
	条件列表
group by 
	分组字段列表
having
	分组后条件列表
order 
	排序字段列表 
limit 
	分页参数;
```

\G 切换纵或横

### 1.3.1基本查询

#### 1.3.1.1查询多个字段

```mysql
select column_name1,column_name2,... from tablename;  #指定字段
select * from tablename;  #全部字段
```

#### 1.3.1.2设置别名

```mysql
select column_name1[as alias1],column_name2[as alias2],... from tablename;
```

#### 1.3.1.3去除重复记录

```mysql
select distinct column_name_list from tablename;
```



### 1.3.2条件查询

```mysql
select column_list from tablename where condition_list;
```

| 运算符                    | 描述                           |
| ------------------------- | ------------------------------ |
| >                         | 大于                           |
| =                         | 等于                           |
| <                         | 小于                           |
| >=                        | 大于等于                       |
| <=                        | 小于等于                       |
| <> or !=                  | 不等于                         |
| between value1 and value2 | 介于，闭区间                   |
| in(...)                   | 在in之后的列表中的额值，多选一 |
| like 占位符               | 模糊匹配                       |
| is null                   | 空                             |
|                           |                                |
| and 或 &&                 | 逻辑与                         |
| or 或 \|\|                | 逻辑或                         |
| not 或 !                  | 逻辑非                         |

### 1.3.3聚合函数

将一列数据作为一个整体进行纵向计算。

常用函数：

| 函数名 | 描述     |
| ------ | -------- |
| count  | 统计数量 |
| max    | 最大值   |
| min    | 最小值   |
| avg    | 平均值   |
| sum    | 求和     |

```mysql
select function_name(column_list) from tablename [where condition];

#查询表中数据总数
select count(*) from tablename;
select count(*) from users where age > 30;  #查询用户表中年龄大于30的用户数量
```

### 1.3.4分组查询

```mysql
select 字段列表 from 表名 [where 过滤条件] group by 分组字段名 [having 分组后过滤条件];
/*
where 条件在分组前过滤
having 条件在分组后过滤
*/
select gender, count(*) from user group by gender;
```

### 1.3.5排序查询

```mysql
select 字段列表 from 表名 [where 过滤条件] order by 排序字段1 排序方式1,排序字段2 排序方式2,...;
/*
当排序字段1的值相同时按照排序字段2排序
*/
```

asc 升序

desc 降序

### 1.3.6分页查询

```mysql
select 字段列表 from 表名 limit 起始位置,数据条数;
/*
第一条数据的索引为0
*/
```

## 1.4DCL——管理数据库的用户，管理数据库的访问权限

### 1.4.1查询用户

```mysql
use mysql;
select * from user;
```

### 1.4.2创建用户

```mysql
create user '用户名'@'主机名' identified by '密码';
#主机名为localhost表示只可在本机登录
#主机名为%表示可在任何主机登录
```

### 1.4.3修改用户密码

```mysql
alter user '用户名'@'主机名' identified with mysql_native_password by '新密码';
```

### 1.4.4删除用户

```mysql
drop user '用户名'@'主机名';
```

### 1.4.5权限控制

| 常用权限           | 说明               |
| ------------------ | ------------------ |
| all,all privileges | 所有权限           |
| select             | 查询数据           |
| insert             | 插入数据           |
| update             | 修改数据           |
| delete             | 删除数据           |
| alter              | 修改表             |
| drop               | 删除数据库/表/视图 |
| create             | 创建数据库/表      |

#### 1.4.5.1查询权限

```mysql
show grants for '用户名'@'主机名';
```

#### 1.4.5.2授予权限

```mysql
grant 权限列表 on 数据库名.表名 to '用户名'@'主机名';  #授予操作指定数据库、指定表的权限
grant 权限列表 on *.* to '用户名'@'主机名';  #所有数据库所有表
grant 权限列表 on 数据库名.* to '用户名'@'主机名';  #指定数据库的所有表
```

#### 1.4.5.3插销权限

```mysql
revoke 权限列表 on 数据库名.表名 from '用户名'@'主机名';
revoke 权限列表 on *.* from '用户名'@'主机名';
revoke 权限列表 on 数据库名.* from '用户名'@'主机名';
```



# 2函数

## 2.1字符串函数

| 函数                     | 功能                                        |
| ------------------------ | ------------------------------------------- |
| concat(s1,s2,…,sn)       | 字符串拼接                                  |
| lower(str)               | 全部转为小写                                |
| upper(str)               | 全部转为大写                                |
| lpad(str,n,pad)          | 左填充，用字符串pad对str左边填充，长度达到n |
| rpad(str,n,pad)          | 右填充，用字符串pad对str左边填充，长度达到n |
| trim(str)                | 去掉字符串头尾的空格                        |
| substring(str,start,len) |                                             |

## 2.2数值函数

| 函数       | 功能                |
| ---------- | ------------------- |
| ceil(x)    | 向上取整            |
| floor(x)   | 向下取整            |
| mod(x)     | 整除取余            |
| rand()     | 0~1的随机数         |
| round(x,y) | 四舍五入保留y位小数 |

## 2.3日期函数

| 函数                              | 功能                                        |
| --------------------------------- | ------------------------------------------- |
| curdate()                         | 返回当前日期                                |
| curtime()                         | 返回当前时间                                |
| now()                             | 返回当前日期和时间                          |
| year(date)                        | 获取指定日期的年份                          |
| month(date)                       | 获取指定日期的月份                          |
| day(date)                         | 获取指定日期的日期                          |
| date_add(date,interval expr type) | 返回一个日期/时间加上一个时间间隔后的时间值 |
| datediff(date1,date2)             | 返回date1和date2的天数差                    |

## 2.4流程控制函数

| 函数                                                        | 功能                                                  |
| ----------------------------------------------------------- | ----------------------------------------------------- |
| if(value,t,f)                                               | value为true返回t，否则返回f                           |
| ifnull(valur1,value2)                                       | value1不为空返回value1，否则返回value2                |
| case when [val1] then [res1] … else  [default] end          | val1为true返回res1，……否则返回default默认值           |
| case [expr] whien [cal1] then [res1] ..  Else [default] end | 如果expr值等于val1，返回res1，……否则返回default默认值 |

# 3约束

| 约束     | 描述                                                     | 关键字         |
| -------- | -------------------------------------------------------- | -------------- |
| 非空约束 | 限制该字段值不可为null                                   | not null       |
| 唯一约束 | 保证字段的所有数据都是唯一的，不重复的                   | unique         |
| 主键约束 | 主键是一行数据的唯一标识，非空且唯一                     | primary key    |
| 默认约束 | 保存数据时如果未指定值则采用默认值                       | default        |
| 检查约束 | 保证字段值满足某一要求                                   | check          |
| 外检约束 | 原来让两张表的数据之间建立连接，保证数据的一致性和完整性 | forign key     |
| 自增约束 | 当添加数据时该条数据的改字段值自动设置为上一条的值+1     | auto_increment |

```mysql
#创建表时设置约束
create table 表名(
    字段名 数据类型 约束关键字,
    ...
);

#修改字段属性添加约束
alter table 表名 modify 字段名 数据类型 约束关键字;
```

## 3.1外键约束

```mysql
#在创建表时设置外键
create table 表名(
    字段名 数据类型,
    ...
    [constraint] [外键名] foreign key(外键字段名) references 主表(主表列名);
);

#创建之后设置外键
alter table 表名 add constraint 外键名 foreign key(外键字段名) references 主表(主表列表);
```

### 3.1.1删除更新行为

| 行为        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| no action   | 当在父表中删除/更新对应记录时，首先检查记录是否有对应外键，如果有则不允许删除/更新 |
| restrict    | 当在父表中删除/更新对应记录时，首先检查记录是否有对应外键，如果有则不允许删除/更新 |
| casade      | 当在父表中删除/更新对应记录时，首先检查记录是否有对应外键，如果有则也删除/更新外键在子表中的记录 |
| set null    | 当在父表中删除对应记录时，首先检查记录是否有对应外键，如果有则设置子表中该外键值为null |
| set default | 父表有变更时，子表将外键列设置为一个默认值                   |

```mysql
alter table 表名 add constraint 外键名称 foreign key(外键字段) references 主表名(主表字段名) on update cascade on delete cascade;
```



# 4多表查询

## 4.1表间关系：

### 4.1.1一对多

如多名员工属于同一部门，但一个员工不能属于不同部门。

在“多”的一方的建立外键指向“一”的一方的主键

```mysql
select 字段名列表 from 子表,父表 where 子表外键字段名 = 子表外键所连接的字段名;
#子表、父表：用外键关联的两个表，外键所在表为子表，另一为父表
```

### 4.1.2多对多

如一名学生可以选多门课程，一门课程有多名学生选修。

创建一“中间表”，添加两个外键分别关联学生表和课程表的主键

### 4.1.3一对一

在任意一方加入外键关联另一方主键并设置约束unique

## 4.2多表查询分类

### 4.2.1连接查询

内连接：查询A、B交集部分数据

#### 4.2.1.1隐式内连接

```mysql
select 字段列表 from 表1,表2 where 过滤条件;

select staffs.id, staffs.name, divisions.name from staffs,divisions where staff.division_id = division.id;
select s.id,s.name,d.name from staff s,diviosion d where s.division_id = d.id;
```

#### 4.2.1.2显示内连接

```mysql
select 字段列表 from 表1 [inner] join 表2 on 连接条件;

select s.id,s.name,d.name from staffs s inner join divisions d on s.division_id = d.id;
```

外连接：

内连接示例中，staff.division_id可以为空，此值为空则查询不到该条数据，所以需要外连接

#### 4.2.1.3左外连接

查询左表所有数据以及两表交集部分数据

```mysql
select 字段列表 from 表1 left outer join 表2 on 过滤条件;

select s.*,d.name from staffs s left outer join divisions d on s.division_id = d.id;
```

#### 4.2.1.4右外连查

询右表所有数据以及两表交集部分数据

```mysql
select 字段列表 from 表1 right outer join 表2 on 过滤条件;
```

#### 4.2.1.5自连接

案例：

​		现有一个包含字段：员工id、员工姓名、领导id的表，要求查询出每一个员工的id、姓名、领导姓名。当然，领导的信息同样在此表中。虽然需要 查询的信息都在这一张表中，但是单表查询并不能满足要求，所以需要两次连接到同一张表→自连接查询。

当前表与自身的连接查询，自连接必须使用表别名。

```mysql
select 字段列表 from 表1 别名1 [left/right] join 表1 别名2 on 过滤条件 ...;
```

### 4.2.2联合查询

union all、union

把多次查询结果合并起来形成一心的查询结果集

```mysql
select 字段列表 from 表1...
union[all]
select 字段列表 from 表2...;

# union all 是单纯的把两次查询结果合并
# union 在 union all 基础上取出重复
```

### 4.2.3子查询

在SQL语句中嵌套 select 语句 → 嵌套查询、子查询

```mysql
select 字段列表 from 表1 where 字段1 = (select 字段1 from t2);
# 外部的语句可以使 insert/update/delete/select 中的任何一个
```

#### 4.2.3.1标量子查询

子查询结果为单个值

子查询位置：where之后、from之后、select之后

```mysql
# 查询“研发部”员工信息
select * from staffs where division_id = (select id from divisions where name = '研发部');、
# 查询“卫庄”之后入职的员工信息
select * from staffs where date_in > (select date_in from staff where name = '卫庄');
```

#### 4.2.3.2列子查询

子查询结果为一列

| 操作符 | 描述                             |
| ------ | -------------------------------- |
| in     | 属于                             |
| not in | 不属于                           |
| any    | 子查询返回列中有任意一个满足即可 |
| some   | 与any等同                        |
| all    | 咋查询返回列中所有制都必须瞒住   |

```mysql
# 查询“市场部”、“研发部”的员工信息
select * from staffs where division_id in (select id from divisions where name in ('市场部', '研发部'));

# 查询比“财务部”所有人工资都要高的员工信息
select * from staffs where salaey > all (select salary from staffs where division_id = (select id from divisions where name = '财务部'));

# 查询比“研发部”任意一人工资高的员工信息
select * from staffs where salaey > any (select salary from staffs where division_id = (select id from divisions where name = '研发部'));
```

#### 4.2.3.3行子查询

子查询结果为一行。常用操作符：in、not in、=、<>

```mysql
# 查询与“张无忌”工资和直属领导相同的员工信息
select * from staffs where (salary, manager_id) = (select salary, manager_id from staffs where name = '张无忌');
```

#### 4.2.3.4表子查询

子查询结果为多行多列

```mysql
# 查询职位、薪资和鹿杖客或宋远桥相同的员工信息
select * from staffs where (job, salary) in (select job,salary from staffs where name in ('鹿杖客','宋远桥'));

# 查询职位、薪资和鹿杖客或宋远桥相同的员工信息及其部门信息
select s.*,d.* from (select * from staffs where (job,salary) in (select job,salary from staffs where name in ('鹿杖客','宋远桥'))) s left join divisions d on s.division_id = d.id;
```



# 5事务

| id   | name | money |
| ---- | ---- | ----- |
| 1    | 张三 | 2000  |
| 2    | 李四 | 2000  |

张三给李四转账1000元时，先将张三的余额减1000，再将李四的余额加1000；但两条语句中间抛出异常时，张三的余额减少了1000但是并没有到账。

```mysql
update account set money = money - 1000 where name = '张三';
wrong # 这一句并不是sql语句，所以会报错
update account set money = money + 1000 where name = '李四';

# 执行之后张三的余额为1000，李四的余额为2000
```

## 5.1事务操作

### 5.1.1方式1：设置@@autocommit

```mysql
# 事务提交之后才会改变数据库中的数据

# 查看当前事务提交方式
select @@autocommit;
# 设置事务提交方式
set @@autocommit = 1/0  # 1 表示为自动提交，0 表示为手动提交

# 提交事务
commit;
# 回滚事务
rollback;
```

```mysql
set @@autocommit = 0  #设置提交方式为手动

update account set money = money - 1000 where name = '张三';
wrong # 这一句并不是sql语句，所以会报错
update account set money = money + 1000 where name = '李四';

rollback; # 回滚

commit; # 提交

/*
将事务提交方式设置为手动提交之后，执行：
	update account set money = money - 1000 where name = '张三';
	wrong # 这一句并不是sql语句，所以会报错
	update account set money = money + 1000 where name = '李四';
会报错，但并未像之前一样改变数据（以为没有提交）。
	此时提交之后，张三的1000就转出去了，但是并没有到账；
	此时回滚，数据变为初始数据。
*/
```

### 5.1.2方式2：transaction

```mysql
start transaction;

update account set money = money - 1000 where name = '张三';
wrong # 这一句并不是sql语句，所以会报错
update account set money = money + 1000 where name = '李四';

rollback;

commit;
```

## 5.2事务特性

1. 原子性（Atomicity):事务是不可分割的最小操作单元，要么全部成功，要么全部失败。
2. 一致性（Consistency):事务完成时，必须使所有的数据都保持一致状态。
3. 隔离性（lsolation)∶数据库系统提供的隔离机制，保证事务在不受外部并发操作影响的独立环境下运行。
4. 持久性（Durability):事务一旦提交或回滚，它对数据库中的数据的改变就是永久的。

## 5.3并发事务问题

| 问题       | 描述                                                         |
| ---------- | ------------------------------------------------------------ |
| 脏读       | 一个事务读到另外一个事务还没有提交的数据。                   |
| 不可重复读 | 一个事务先后读取同一条记录，但两次读取的数据不同，称之为不可重复读。 |
| 幻读       | 一个事务按照条件查询数据时，没有对应的数据行，但是在插入数据时，又发现这行数据已经存在，好像出现了“幻影” |

## 5.4事务隔离级别

| 隔离级别         | 脏读 | 不可重复读 | 幻读 |
| ---------------- | ---- | ---------- | ---- |
| read uncommitted | √    | √          | √    |
| read committed   | ×    | √          | √    |
| repeatable read  | ×    | ×          | √    |
| serializable     | ×    | ×          | ×    |

| 错误类型   | 描述                                                         |
| ---------- | ------------------------------------------------------------ |
| 脏读       | 一个事务中读取到另一个事务未提交的结果                       |
| 不可重复读 | 一个事务中两次执行相同查询语句结果不一样（被另一个事务修改） |
| 幻读       | 事务A、B开启后，事务B向数据库插入数据并提交，事务A查询不到插入的数据，在相同位置插入数据时报错 |

```mysql
# 查看事务隔离级别
select @@transaction_isolation;

# 设置事务隔离级别
set[session/global] transaction isolation level {readuncommited / readcommitted / repeatableread / seralzable};
# session 会话，仅对当前客户端回话窗口有效
# global 对所有客户端的会话窗口有效
```

# 6存储引擎

```mysql
# 创建表时指定存储引擎
create table tablename(
	column_list;
)engine = engine_name;

# 查看当前数据库支持的存储引擎
show engines;
```

## 6.1存储引擎选择

逻辑结构：表空间、段、区、页

| 存储引擎 | 适用场景                                                     |
| -------- | ------------------------------------------------------------ |
| InnoDB   | MySQL默认，支持事务、外键、行级锁；对事务的完整性有比较高的要求，在并发条件下要求诗句的一致性；数据操作除了插入和查询外，还包含很多更新、删除操作 |
| MyISAM   | 不支持事务、外键，仅表锁；应用以读操作和插入操作为主，只有很少的更新和删除操作，并且对事务的完整性、并发性要求不是很高 |
| MENORY   | 将所有数据保存在内存中，访问速度快，通常用于临时表及缓存。缺陷是对表的大小有限制，太大的表无法缓存在内存中，而且无法保障数据的安全性 |

## 6.2索引

| 分类     | 含义                                                 | 特点                    | 关键字   |
| -------- | ---------------------------------------------------- | ----------------------- | -------- |
| 主键索引 | 针对于表中主键创建的索引                             | 默认自动创建,只能有一个 | primary  |
| 唯一索引 | 避免同一个表中某数据列中的值重复                     | 可以有多个              | unique   |
| 常规索引 | 快速定位特定数据                                     | 可以有多个              |          |
| 全文索引 | 全文索引查找的是文本中的关键词，而不是比较索引中的值 | 可以有多个              | fulltext |

### 6.2.1InnoDB 索引

| 分类     | 含义                                                       | 特点                |
| -------- | ---------------------------------------------------------- | ------------------- |
| 聚集索引 | 将数据存储与索引放到了一块,索引结构的叶子节点保存了行数据  | 必须有,而且只有一个 |
| 二级索引 | 将数据与索引分开存储，索引结构的叶子节点关联的是对应的主键 | 可以存在多个        |

一级索引叶节点指向该行数据，二级索引叶节点指向该行数据的“主键”值

聚集索引选取规则:

- 如果存在主键，主键索引就是聚集索引
- 不存在主键，第一个唯一索引为聚集索引
- 如果表没有主键和唯一索引，则会自动生成一个rowid作为隐藏的聚集索引

#### 6.2.1.1 回表查询

当查询并不以主键字段来查询时，会按照对应的二级索引找到该数据的主键值，在按照聚集索引查询到该数据的所有内容。

### 6.2.2 索引语法

#### 6.2.2.1 创建索引

```mysql
create [unique / fulltext] index index_name on table_name_ (index_column_name,...);
# 关联多个字段→单列索引
# 关联多个字段→联合索引
# 中括号中不添加关键字则为常规索引。没有创建索引则查询时使用全表扫描，效率低下
```

#### 6.2.2.2 查看索引

```mysql
show index from table_name_;
```

#### 6.2.2.3 删除索引

```mysql
drop index index_name on table_name_;
```

## 6.3 SQL 性能分析

### 6.3.1 SQL执行频数

```mysql
# 查看当前数据库的各类操作的次数
show global/session status like 'Com_______';  # 七个‘_’表示7个字符，即_select、_delete、_update等
```

### 6.3.2 慢查询日志

记录所有执行时间超过指定参数（默认为10秒）的所有SQL语句的日志。默认没有开启，需要在MySQL配置文件（linux系统中为：/etc/my.cnf）中配置

```mysql
# 查看当前慢查询日志开关的状态
show variables like 'show_query_log';

#以下需要在MySQL配置文件（\etc/my.cnf）中配置
# 开启MySQL慢查询日志开关
show_query_log = 1
# 设置慢查询的时间定义（以秒为单位）
long_query_time = t
```

在Linux系统中，mysql的慢查询日志存放在/var/lib/mysql

### 6.3.3 profile详情

记录SQL命令及其耗时。

```mysql
# 查看是否支持profile
select @@have_profiling;
# 查看开关状态
select @@profiling;
# 开/关profile
set profiling = 1/0;

# 可以添加关键字session、global

# 查看每一条SQL语句及其耗时
show frofiles;
# 查看指定query_id的SQL语句各个阶段的耗时情况
show profile for query query_id;
# 查看指定query_id的SQL语句CPU使用情况
show profile cpu for query quety_id;
```

### 6.3.4 explain 执行计划

展示SQL语句执行的细节及其顺序。

```mysql
explain select * from table_name_;
```

执行计划各字段名称及其含义

| 字段         | 含义                                                         |
| ------------ | ------------------------------------------------------------ |
| id           | select查询的序列号，表示查询中执行select子句或者是操作表的顺序(id相同，执行顺序从上到下;id不同，值越大，越先执行)。 |
| select_type  | 表示SELECT的类型，常见的取值有SIMIPLE(简单表，即不使用表连接或者子查询)、PRIMARY(主查询，即外层的查询)、UNION  （UNION中的第二个或者后面的查询语句)、SUBQUERY (SELECT/WHERE之后包含了子查询）等 |
| **type**     | 表示连接类型，性能由好到差的连接类型为NULL、system、const、 eq_ref、ref、range、index、all 。 |
| posiible_key | 显示可能应用在这张表上的索引，一个或多个。                   |
| **key**      | 实际使用的索引，NULL表示没有使用索引                         |
| **key_len**  | 表示索引中使用的字节数，该值为索引字段最大可能长度，并非实际使用长度，在不损失精确性的前提下，长度越短越好 |
| rows         | MySQL认为必须要执行查询的行数，在innodb引擎的表中，是一个估计值，可能并不总是准确的。 |
| filtered     | 表示返回结果的行数占需读取行数的百分比， filtered 的值越大越好。 |
| **extra**    | 额外信息。                                                   |

## 6.4 索引使用

### 6.4.1 最左前缀法则

如果使用了多列（联合索引），查询总索引的最左列开始，并且不跳过中间的列。如果跳过了中间的某一列索引将部分失效（后面的索引失效）。

对于联合索引，如果查询中出现了范围查询，则范围查询右侧的列索引将失效。

### 6.4.2 索引失效

在索引列上进行运算之后索引将失效。

```mysql
explain select * from table1 where substring(phone_num,10,2) = '00';
# type字段显示为all，效率很低
```

字符串不加单引号存在隐式转换，字符串列上的索引失效。

模糊匹配中，如果模糊的部分不包括字符串的开头，那就能够使用索引，否则索引失效。因为字符串的大于小于比较只看第一个字符的（当然了，第一个相同再看第二个……）

联合索引的列不包括条件的列时不用到索引。

or条件时，or连接的两个列都有各自的索引时用到索引，只有一个列有索引是不会用到索引。

索引自适应：大多数行满足条件，则不走查询。换句话说，mysql评估使用和不适用索引时的效率来从优选择。

### 6.4.3 or连接的条件

若or前的条件中的列有索引，而后面的没有，那么涉及到的索引不会被用到。

### 6.4.4 SQL提示

```mysql
# 指定查询语句使用的索引
select column_list from table_name_ use index(index_name) where ...;
# 指定不用
select column_list from table_name_ ignore index(index_name) where ...;
# 强制使用
select column_list from table_name_ force index(index_name) where ...;
```

### 6.4.5覆盖索引

尽量使得需要返回的列在该索引（联合索引）中已经能全部找到。

查询计划中显示：

- using index condition: 查找使用了索引但是需要回表查询
- using where; using index: 查找使用了索引，但是需要的数据都在索引列中能找到→不需要回表查询→效率更高

### 6.4.6前缀索引

当字段类型为字符串(varchar,text等）时，有时候需要索引很长的字符串，这会让索引变得很大，查询时，浪费大量的磁盘O，影响查询效率。此时可以只将字符串的一部分前缀，建立索引，这样可以大大节约索引空间，从而提高索引效率。

```mysql
create index index_name on table_name(column_name(n));
# 对前n个字符建立索引
```

长度可以根据索引的选择性来决定，而选择性是指不重复的索引值（基数）和数据表的记录总数的比值，索引选择性越高则查询效率越高，唯一索引的选择性是1，这是最好的索引选择性，性能也是最好的。

选择性：不重复记占所有记录占比。

```sql
select count(distinct email)/count(*) from users_table;
# 结果即为所有记录中不重复记录占比
```

换句话说，大多数行的该字段前三位是相同的，那n<=3就很不合适。

### 6.4.7建议使用联合索引

当一次查询中有多个查询条件时（condition1 <u>and</u> condition2……），如果这些字段各自有索引，也只会用到一个索引；当这几个字段在一个联合索引中，则会使用该联合索引，效率更高。

### 6.4.8索引设计原则

1. 针对数据量较大、查询较为频繁的表建立索引
2. 针对常作为查询条件、排序、分组操作的字段建立索引
3. 尽量选择区分度高的字段作为索引，如身份证号码、电话号码等
4. 对于字符串字段，如果字符串长度较长，可以考虑使用使用前缀索引
5. 尽量使用联合查询，联合索引很多时候可以覆盖索引，提高效率、避免回表查询
6. 控制索引的数量，避免在不必要的字段上建立索引

## 6.5其他SQL语句优化

### 6.5.1插入优化

插入多条数据时，建议：

- 批量插入
- 手动事务提交
- 主键顺序插入
- 一次需要插入大批量数据→insert性能较差→可使用load进行文件的加载

```mysql
# 客户端连接服务器时加上参数  --local-indile
mysql --local-infile -u root -p

# 开启local_infile开关才能从本地加载文件导入数据
set global local_infile = 1;

# 执行load将准备好的文本文件中的数据加载到表中
load data local infile '...'(文件绝对地址) into table '表名' fields terminated by ','(字段间分隔符) lines terminated by '\n'(行间分隔符);
```

### 6.5.2 主键优化

主键索引的叶子节点指向这一条数据，而且叶子节点是有序的，主键顺序插入的时候就一直是在后面插入，主键乱序插入的话就会出现页分裂的情况；同样，删除数据的时候可能会发生页合并。

- 满足业务需求的情况下，尽量降低主键的长度。
- 插入数据时，尽量选择顺序插入，选择使用AUTO_INCREMENT自增主键。
- 尽量不要使用UUID做主键或者是其他自然主键，如身份证号。
- 业务操作时，避免对主键的修改。

### 6.5.3 order by优化

- Using filesort：通过表的索引或全表扫描，读取满足条件的数据行，然后在排序缓冲区sort buffer中完成排序操作，所有不是通过索引直接返回排序结果的排序都叫FileSort排序。
- Using index:通过有序索引顺序扫描直接返回有序数据，这种情况即为using index，不需要额外排序，操作效率高

```mysql
create index idx_user_age_pho_ad on tb_user (age asc, phone desc);
# 创建两个字段不同顺序的联合索引
```

- 根据排序字段建立合适的索引，多字段排序时，也遵循最左前缀法则。
- 尽量使用覆盖索引。
- 多字段排序,一个升序一个降序，此时需要注意联合索引在创建时的规则(ASC/DESC)。
- 如果不可避免的出现filesort，大数据量排序时，可以适当增大排序缓冲区大小 sort_buffer_size(默认256k)。

### 6.5.4 group by优化

在分组操作时，可以通过索引来提高效率。
分组操作时,索引的使用也是满足最左前缀法则的。

### 6.5.5 limit优化 

优化方法：覆盖索引+子查询

```mysql
select t.* from tb_sku t ,(select id from tb_sku order by id limit 200000, 10) a where t.id = a.id;
```

### 6.5.6  count 优化

返回字段值不为NULL的行数

总的来说效率都不高，都会遍历整张表。

count(*)≈count(1)>count(主键)>count(一般字段)

### 6.5.7 update 语句优化

innoDB有行级锁，where 条件在索引字段上时不影响其他事务执行其他行；但是where 条件不在索引字段上时或索引失效，就会升级为表锁，其他进程的事务就不能对表中数据进行更新。

所以在进行更行数据时，以有索引的字段来作为条件。

# 7 视图

视图是一张虚拟的表

## 7.1 基本操作

### 7.1.1创建视图

```mysql
create [or replace] view 视图名称[字段名列表] as select语句 [with [cascaded / local] check option];
```

### 7.1.2查询视图

```mysql
show create view view_name;
select 字段列表 from view_name;
```

### 7.1.3修改视图

```mysql
# 方式1
create [or replace] view 视图名称[字段列表] as select语句 [with [cascaded / local] check option];

# 方式2
alter view 视图名称[字段列表] as as select语句 [with [cascaded / local] check option];
```

### 7.1.4删除视图

```mysql
drop view [if exists] view_name[column_list];
```

## 7.2 视图与数据

### 7.2.1向视图插入数据

视图是一张虚拟的表，并不存储数据，数据实际上插入到了基表中。另外，当插入的数据某字段值违反创建视图时的条件时，数据插入成功，但是再次查询视图时并不能找到该条数据。

在创建视图时加上 with cascaded/local check option 后插入不符合视图创建时的条件时会报错

### 7.2.2 视图的检查选项

当使用WITH CHECK OPTION子句创建视图时，MySQL会通过视图检查正在更改的每个行，例如插入，更新，删除，以使其符合视图的定义。MySQL允许基于另一个视图创建视图，它还会检查依赖视图中的规则以保持一致性。为了确定检查的范围，mysql提供了两个选项;CASCADED 和LOCAL，默认值为CASCADED（级联）。

- cascaded（级联）→ 不仅会检查当前，还会检查所基于的视图。
- loacal → 不仅会检查当前和所基于的视图，还会检查所基于的视图基于的视图...

### 7.2.3视图的更新

要使视图可更新，视图中的行与基础表中的行之间必须存在一对一的关系。如果视图包含以下任何一项，则该视图不可更新:

- 聚合函数或窗口函数(SUM()、MIN()、MAX()、COUNT()等)
- DISTINCT
- GROUP BY4.HAVING
- having
- UNION 或者UNION ALL

## 7.3 视图的作用

简单：视图不仅可以简化用户对数据的理解，也可以简化他们的操作。那些被经常使用的查询可以被定义为视图，从而使得用户不必为以后的操作每次指定全部的条件。

安全：数据库可以授权，但不能授权到数据库特定行和特定列上。通过视图用户只能查询和修改他们能看到的数据。

数据独立：可以帮助用户屏蔽真实表结构变化带来的影响。

# 8 存储过程

- 封装，复用
- 可以接受参数，也可以返回数据
- 减少网络交互，提升效率

### 8.0.1 创建

```mysql
create procedure 存储过程名称(参数列表)
begin
	SQL语句
end
# 在命令行中执行创建存储过程的SQL时，需要通过关键字delimiter指定SQL语句结束符。如：
delimiter $$

create procedure p1()
begin
	select count(*) from table1;
end$$

delimiter ;
```

### 8.0.2 存储

```mysql
call 名称(实参);
```

### 8.0.3 查看

```mysql
select * from information_schema.routines where routine_schema = 'database_name';  # 查询指定存储过程及其状态

show create procedure procedure_name;  # 查询某个存储过程的定义
```

### 8.0.4 删除

```mysql
drop procedure [if exists] procedure_name;
```

## 8.1 变量

### 8.1.1系统变量

MySQL服务器提供，不是用户定义的，属于服务器层面。分为全局变量(GLOBAL)、会话变量(SESSION)。

```mysql
# 查看系统变量
show [session/global] variables;  # 查看所有系统变量
show [session/global] variables like '...';  # 可以通过模糊匹配方式查找系统变量
select @@[session/global] 系统变量名;  # 查看指定变量的值

# 设置系统变量
set [session/global] 系统变量名 = val;
set @@[session/global].系统变量名 = val;

show variables like 'auto%';
set @@global.autocommit = 0;
```

### 8.1.2 用户自定义变量

用户定义变量是用户根据需要自己定义的变量，用户变量不用提前声明，在用的时候直接用“@变量名”使用就可以。其作用域为当前连接。

```mysql
#赋值
set @变量名1 = val1,...;
set @变量名1 := val1,...;
select @变量名1 := val1,...;
select 字段名 from 表名 into @变量名 from 表名；

# 使用
select @变量名;
```

### 8.1.3 局部变量

局部变量是根据需要定义的在局部生效的变量，访问之前，需要DECLARE声明。可用作存储过程内的局部变量和输入参数，局部变量的范围是在其内声明的BEGIN ... END块。

```mysql
# 声明变量
declare 变量名 变量类型 [default 初始值];

# 赋值
set 变量名 = val;
set 变量名 := val;
select 字段名 into 变量名 from 表名...;

create procedure pro1()
begin
	declare stu_count int default 0;
	select count(*) into stu_count from S;
	select stu_count;
end;
```

### 8.1.4 if

```mysql
if condition1 then
	...
elseif condition2 then
	...
...
else
	...
end if;
```

### 8.1.5 参数

| 类型  | 含义                                        | 备注 |
| ----- | ------------------------------------------- | ---- |
| IN    | 该类参数作为输入,也就是需要调用时传入值     | 默认 |
| oUT   | 该类参数作为输出,也就是该参数可以作为返回值 |      |
| INOUT | 既可以作为输入参数，也可以作为输出参数      |      |

```mysql
create procedure 过程名([in/out/inout 参数名 参数类型])
begin
	...
end;
```

### 8.1.6 case

```mysql
case 表达式
	when val1 then
		...
	when val2 then
		...
	else
		...
end case;
```

```mysql
case 
	when 表达式1 then
		...
	when 表达式2 then
		...
	else
		...
end case;
```

### 8.1.7 while

```mysql
while condition1 do
	...
end while;
```

### 8.1.8 repeat

满足条件时退出循环，相当于until。无论是否满足条件都会执行一次。

```mysql
repeat
	...
	until condition
end repeat;
```

### 8.1.9 loop

LOOP实现简单的循环，如果不在sQL逻辑中增加退出循环的条件，可以用其来实现简单的死循环。LOoP可以配合一下两个语句使用：

- LEAVE:配合循环使用,退出循环。（break）
- ITERATE:必须用在循环中，作用是跳过当前循环剩下的语句，直接进入下一次循环。（continue）

```mysql
[循环名称:] loop
	...
end loop [循环结束标识];


# 计算1累加到n的值
create procedure pro1(in n int)
begin
	declare total int default 0;
	
	sum1: loop
		if n<=0 then
			leave sum1;
		end if;
		set total := total + n;
		set n := n - 1;
	end loop sum1;
	
	select total;
end;

# 计算1到n之间的偶数的和
create procedure pro2(in n int)
begin
	declare total int default 0;
	
	sum2: loop
		if n <= 0 then
			leave sum2;
		end if;
	
		if n % 2 = 1 then
			set n := n - 1;
			iterate sum2;
		end if;
		
		set total := total + n;
		set n := n - 1;
	end loop sum2;
	
	select total;
end;
```

### 8.1.10 游标

游标、(CURSOR）是用来存储查询结果集的数据类型,在存储过程和函数中可以使用游标对结果集进行循环的处理。

游标的使用包括游标的声明、OPEN、FETCH和CLOSE。

```mysql
# 声明游标
declare 游标名称 cursor for 查询语句;

# 打开游标
open 游标名;

# 获取游标中的一条记录
fetch 游标名 into 标量列表;

# 关闭游标
close 游标名;
```

### 8.1.11 条件处理程序

条件处理程序（(Handler）可以用来定义在流程控制结构执行过程中遇到问题时相应的处理步骤，常用语类似于 while true 的死循环中。具体语法为:

```mysql
#条件处理程序声明
DECLARE handler_action HANDLER FOR condition_value [, condition_value] ... statement ;
declare exit handler for sqlstate '02000' close u_cursor;
```

handler_action：
	CONTINUE:继续执行当前程序
	EXIT:终止热行当前程序
condition_value：
	SQLSTATE sqlstate_value:状态码，如02000
	SQLWARNING:所有以01开头的 SQLSTATE 代码的简写
	NOT FOUND:所有以02开头的 SQLSTATE 代码的简写
	SQLEXCEPTION:所有没有被SQLWARNING或 NOT FOUND 捕获的 SQLSTATE 代码的简写

案例：

```mysql
create procedure pro1(in uage int)
begin
	declare uname varchar(10);
	declare upro varchar(20);
	declare u_cursor for select name, profession from tb_user where age <= uage;
	declare exit handler for sqlstate '02000' close u_cursor;
	
	drop table if exists tb_user_pro;
	create table tb_user_pro(
    	id int primary key auto_increment,
        name varchar(10);
        profession varchar(20)
    );
    
    open u_cursor;
    while true do
    	fetch u_cursor into uname, upro;
    	insert into tb_user_pro(name, profession) values (uname, upro);
    end while;
    close u_cursor;
end;
```

# 9存储函数

存储函数是有返回值的存储过程，参数只能是in类型。

```mysql
create function 函数名(参数列表)
returns 类型 [特性]  # 指定函数的返回值类型
begin
	...
	return ...;
end;

/*
“特性”：
	deterministic: 相同的输入参数产生相同的结果
	no sql: 不包含SQL语句
	reads sql data: 包含读取数据的语句但是不包含写入数据的语句
*/

create function func1(n int)
returns int deterministic
begin
	declare total int default 0;
	
	while n>0 do
		set total := total + n;
		set n := n - 1;
	end while;
	
	return total;
end;
```

# 10 触发器

触发器是与表有关的数据库对象，指在insert/update/delete 之前或之后，触发并执行触发器中定义的SQL语句集合。触发器的这种特性可以协助应用在数据库端确保数据的完整性，日志记录，数据校验等操作。

使用别名 OLD 和 NEW 来引用触发器中发生变化的记录内容，这与其他的数据库是相似的。现在触发器还只支持行级触发，不支持语句级触发。

| 触发器类型      | new&old                                              |
| --------------- | ---------------------------------------------------- |
| insert 型触发器 | new 表示将要或者已经新增的数据                       |
| update 型触发器 | old 表示修改之前的数据，new 表示将要或修改之后的数据 |
| delete 型触发器 | old 表示将要或者已经删除的数据                       |

```mysql
# 创建
create trigger 触发器名
before/after insert/update/delete
on 表名 for each row  # 行级触发器
begin
	...
end;

# 查看
show triggers;

# 删除
drop trigger [数据库名.]触发器名;  # 默认删除当前数据库下的触发器



#案例：要求通过触发器记录user表的数据变更日志（user_logs），包含修改增加删除

create table user_log(
	id int(11) not primary key auto_increment,
    operation varchar(20) not null comment '造作类型',
    ope_time datetime not null comment '操作时间',
    ope_id int(11) not null comment '操作的数据的id',
    ope_params varchar(500) comment '操作参数'
)

create trigger tb_user_insert_trigger
	after insert on tb_user for each row
begin
	insert into user_log values
		(null,'insert',now(),new.id,concat('插入的数据内容为：id = ',new.id,'name=',new.name,'phone=',new.phone,'email=',new.email,'profession = ',new.profession));
end;
```

# 11 锁

锁是计算机协调多个进程或线程并发访问某一资源的机制。在数据库中，除传统的计算资源（CPU、RAM、I/O)的争用以外，数据也是一种供许多用户共享的资源。如何保证数据并发访问的一致性、有效性是所有数据库必须解决的一个问题，锁冲突也是影响数据库并发访问性能的一个重要因素。从这个角度来说，锁对数据库而言显得尤其重要，也更加复杂。

### 11.0.1分类

| 类别   | 描述                       |
| ------ | -------------------------- |
| 全局锁 | 锁定数据库中的所有表。     |
| 表级锁 | 每次操作锁住整张表。       |
| 行级锁 | 每次操作锁住对应的行数据。 |

## 11.1 全局锁

全局锁就是对整个数据库实例加锁，加锁后整个实例就处于**只读**状态，后续的DML的写语句，DDL语句，已经更新操作的事务提交语句都将被阻塞。

其典型的使用场景是做**全库的逻辑备份**，对所有的表进行锁定，从而获取一致性视图，保证数据的完整性。

```mysql
use database_name;
flush tables with read lock;  # 加全局锁，加锁之后所有用户只读
exit;  # 退出数据库。数据库备份语句不是sql语句，在Windows终端中执行即可
mysqldump -h 192.168.200.202 -u root -p 1234 db01 > D:/db01.sql
	#  备份命令。由于要远程操作所以-h 参数不能省略；“db01”为要备份的数据库，db01.sql 为生成的文件
mysql -u root -p 1234
use db01
unlock tables;  # 解锁
```

## 11.2表级锁

表级锁，每次操作锁住整张表。锁定粒度大，发生锁冲突的概率最高，并发度最低。应用在MyISAM、InnoDB、BDB等存储引擎中。

对于表级锁，主要分为以下三类:

- 表锁
- 元数据锁( meta data lock,MDL)
- 意向锁

### 11.2.1表锁 

- 表共享读锁（read lock）：加锁之后其他客户端只能读
- 表独占写锁（write lock）：加锁之后其他客户端不可读不可写

```mysql
# 加锁
lock tables 表名列表 read/write
# 解锁
unlock tables; / 客户端断开连接自动解锁
```

### 11.2.2 元数据锁

MDL加锁过程是系统自动控制，无需显式使用，在访问一张表的时候会自动加上。MDL锁主要作用是维护表元数据的数据一致性，在表上有活动事务的时候，不可以对元数据进行写入操作。

在MySQL5.5中引入了MDL，当对一张表进行增删改查的时候，加MDL读锁(共享);当对表结构进行变更操作的时候，加MDL写锁(排他)。

| 对应SQL                                          | 锁类型                                   | 说明                                             |
| ------------------------------------------------ | ---------------------------------------- | ------------------------------------------------ |
| lock tables xxx read / write                     | SHARED_READ_ONLY /  SHARED_NO_READ_WRITE |                                                  |
| select . select ... lock in share mode           | SHARED_READ                              | 与SHARED_READ、SHARED_WRITE兼容，与EXCLUSIVE互斥 |
| insert . update、 delete、select ... for  update | SHARED_WRITE                             | 与SHARED_READ、SHARED_WRITE兼容,与EXCLUSIVE互斥  |
| alter table ...                                  | EXCLUSIVE                                | 与其他的MDL都互斥                                |

### 11.2.3 意向锁

为了避免DML在执行时，加的行锁与表锁的冲突，在InnoDB中引入了意向锁，使得表锁不用检查每行数据是否加锁，使用意向锁来减少表锁的检查。

- 意向共享锁（IS）：由语句select...lock in share mode添加。与表锁共享锁( read)兼容，与表锁排它锁( write）互斥。
- 意向排他锁（IX）：由insert、update、delete、select...for update添加。与表锁共享锁( read）及排它锁(write）都互斥。意向锁之间不会互斥。

```mysql
# 查看当前数据库意向锁、行所的加锁情况
select object_schema, object_name, index_name, lock_type, lock_mode, lock_data from performance_schema.data_locks;

```

## 11.3行级锁

行级锁，每次操作锁住对应的行数据。锁定粒度最小，发生锁冲突的概率最低，并发度最高。应用在InnoDB存储引擎中。

InnoDB的数据是基于索引组织的，行锁是通过对索引上的索引项加锁来实现的，而不是对记录加的锁。对于行级锁，主要分为以下三类：

- 行锁〈Record Lock)∶锁定单个行记录的锁，防止其他事务对此行进行update和delete。在RC、RR隔离级别下都支持。
- 间腺锁（GapLock):锁定索引记录间隙（不含该记录)，确保索引记录间隙不变，防止其他事务在这个间隐进行insert，产生幻读。在RR隔离级别下都支持。
- 临键锁（Next-Key Lock)︰行锁和间隙锁组合，同时锁住数据，并锁住数据前面的间隙Gap。在RR隔离级别下支持。

### 11.3.1行锁

lnnoDB实现了以下两种类型的行锁:
1.共享锁(S)︰允许一个事务去读一行，阻止其他事务获得相同数据集的排它锁。即和共享锁兼容。
2．排他锁(X)∶允许获取排他锁的事务更新数据，阻止其他事务获得相同数据集的共享锁和排他锁。

| SQL                           | 行锁类型   | 说明                                     |
| ----------------------------- | ---------- | ---------------------------------------- |
| INSERT....                    | 排他锁     | 自动加锁                                 |
| UPDATE ...                    | 排他锁     | 自动加锁                                 |
| DELETE ..                     | 排他锁     | 自动加锁                                 |
| SELECT（正常)                 | 不加任何锁 |                                          |
| SELECT  ...LOCK IN SHARE MODE | 共享锁     | 需要手动在SELECT之后加LOCK IN SHARE MODE |
| SELECT ...  FOR UPDATE        | 排他锁     | 需要手动在SELECT之后加FOR UPDATE         |

默认情况下，InnoDB在REPEATABLE READ事务隔离级别运行，InnoDB使用next-key锁进行搜索和索引扫描，以防止幻读。

- 针对唯一索引进行检索时，对已存在的记录进行等值匹配时，将会自动优化为行锁。
- InnoDB的行锁是针对于索引加的锁，不通过索引条件检索数据，那么InnoDB将对表中的所有记录加锁，此时就会升级为表锁。

### 11.3.2 间隙锁、临键锁

默认情况下，InnoDB在REPEATABLE READ事务隔离级别运行，InnoDB使用next-key锁进行搜索和索引扫描，以防止幻读。

- 索引上的等值查询(唯一索引)，给不存在的记录加锁时,优化为间隙锁。
- 索引上的等值查询(普通索引)，向右遍历时最后一个值不满足查询需求时，next-key lock退化为间隙锁。
- 索引上的范围查询(唯一索引)--会访问到不满足条件的第一个值为止。

临键锁：锁住两条数据之间的间隙，此时在这个间隙里插入数据会被阻塞。

间隙锁唯一目的是防止其他事务插入间隙。间隙锁可以共存，一个事务采用的间隙锁不会阻止另一个事务在同一间隙上采用间隙锁。

# 12 InnoDB 存储引擎

## 12.1 逻辑存储结构

![image-20220426193634302](.\images\image-20220426193634302.png)

- 表空间（ ibd文件)，一个mysql实例可以对应多个表空间，用于存储记录、索引等数据。
- 段，分为数据段(Leaf node segment)、索引段(Non-leaf node segment)、回滚段(Rollback segment)，InnoDB是索引组织表，数据段就是B+树的叶子节点，索引段即为B+树的非叶子节点。段用来管理多个Extent(区)
- 区，表空间的单元结构，每个区的大小为1M。默认情况下， InnoDB存储引擎页大小为16K，即一个区中一共有64个连续的页。
- 页，是InnoDB存储引擎磁盘管理的最小单元，每个页的大小默认为16KB。为了保证页的连续性，InnoDB存储引擎每次从磁盘申请4-5个区。
- 行，lnnoDB存储引擎数据是按行进行存放的。



## 12.2 架构

### 12.2.1 缓冲池

缓冲池：数据的增删改查发生在挨内存中的缓冲区，之后再以一定频率刷到磁盘

缓冲池以Page页为单位，底层采用链表数据结构管理Page。根据状态，将Page分为三种类型:

​	free page:空闲page，未被使用。
​	clean page:被使用page，数据没有被修改过。
​	dirty page:脏页，被使用page，数据被修改过，也中数据与磁盘的数据产生了不一致。



### 12.2.2 更改缓冲区

Change Buffer:更改缓冲区（针对于非唯一二级索引页)，在执行DML语句时，如果这些数据Page没有在Buffer Pool中，不会直接操作磁盘，而会将数据变更存在更改缓冲区Change Buffer中，在未来数据被读取时，再将数据合并恢复到Buffer Pool中，再将合并后的数据刷新到磁盘中。



### 12.2.3 自适应哈希索引

Adaptive Hash Index:自适应hash索引，用于优化对Buffer Pool数据的查询。InnoDB存储引擎会监控对表上各索引页的查询，如果观察到hash索引可以提升速度，则建立hash索引，称之为自适应hash索引。

```mysql
# 参数：adaptive_hash_index
```



### 12.2.4 日志缓冲区

Log Buffer:日志缓冲区，用来保存要写入到磁盘中的log日志数据（redg log . undo log)，默认大小为16MB，日志缓冲区的日志会定期刷新到磁盘中。如果需要更新、插入或删除许多行的事务，增加日志缓冲区的大小可以节省磁盘I/O。
参数:

```mysql
innodb_log_buffer_size  #缓冲区大小
innodb_flush_log_at_trx_commit  #日志刷新到磁盘时机
	1:日志在每次事务提交时写入并刷新到磁盘0:每秒将日志写入并刷新到磁盘一次。
	2:日志在每次事务提交后写入，并每秒刷新到磁盘一次。
```



## 12.3 事务原理

![image-20220426210127175](.\images\image-20220426210127175.png)



### 12.3.1 redolog 与事务的持久性

重做日志，记录的是事务提交时数据页的物理修改，是用来实现事务的持久性。
该日志文件由两部分组成﹔重做日志缓冲(redo log buffer)以及重做日志文件(redo log file) ,前者是在内存中，后者在磁盘中。当事务提交之后会把所有修改信息都存到该日志文件中,用于在刷新脏页到磁盘,发生错误时,进行数据恢复使用。



### 12.3.2 undo log 与事务的原子性

回滚日志，用于记录数据被修改前的信息，作用包含两个:提供回滚和MVCC(多版本并发控制)。
undo log和redo log记录物理日志不一样，它是逻辑日志。可以认为当delete一条记录时，undo log中会记录一条对应的insert记录，反之亦然，当update一条记录时，它记录一条对应相反的update记录。当执行rollback时，就可以从undo log中的逻辑记录读取到相应的内容并进行回滚。
Undo log销毁: undo log在事务执行时产生，事务提交时，并不会立即删除undo log，因为这些日志可能还用于MVC
Undo log存储: undo log采用段的方式进行管理和记录，存放在前面介绍的 rollback segment 回滚段中，内部包含1024个undo logsegment。



## 12.4 MVCC→多版本并发控制

### 12.3.0 基本概念

当前读：读取的是记录的最新版本，读取时还要保证其他并发事务不能修改当前记录，会对读取的记录进行加锁。对于我们日常的操作，如：select ... lock in share mode(共享锁)，select ... for update、update、insert、delete(排他锁)都是一种当前读.



快照读：简单的select (不加锁）就是快照读，快照读，读取的是记录数据的可见版本，有可能是历史数据，不加锁，是非阻塞读。

- Read Committed:每次select，都生成一个快照读。
- Repeatable Read:开启事务后第一个select语句才是快照读的地方。
- Serializable:快照读会退化为当前读。



MVCC：全称Multi-Version Concurrency Control，多版本并发控制。指维护一个数据的多个版本，使得读写操作没有冲突，快照读为MySQL实现MVCC提供了一个非阻塞读功能。MCC的具体实现，还需要依赖于数据库记录中的三个隐式字段、undo log日志、readView。



### 12.3.1 实现原理

1. 记录中的隐藏字段

   ![image-20220427092825704](.\images\image-20220427092825704.png)

| 隐藏字段    | 含义                                                         |
| ----------- | ------------------------------------------------------------ |
| DB_TRX_ID   | 最近修改事务ID，记录插入这条记录或最后一次修改该记录的事务ID。 |
| DB_ROLL_PTR | 回滚指针，指向这条记录的上一个版本，用于配合undo log，指向上一个版本。 |
| DB_ROW_ID   | 隐藏主键，如果表结构没有指定主键,将会生成该隐藏字段。        |

2. undo log

   回滚日志，在insert、update、delete的时候产生的便于数据回滚的日志。
   当insert的时候，产生的undo log日志只在回滚时需要，在事务提交后，可被立即删除。
   而update、delete的时候，产生的undo log日志不仅在回滚时需要，在快照读时也需要，不会立即被删除。 

   undo log 版本链：不同事务或相同事务对同一条记录进行修改，会导致该记录的undolog生成一条记录版本链表，链表的头部是最新的旧记录，链表尾部是最早的旧记录。

3. readview

   ReadView(读视图）是快照读SQL执行时MVCC提取数据的依据，记录并维护系统当前活跃的事务（未提交的) id。ReadView中包含了四个核心字段：

   | 字段           | 含义                                                 |
   | -------------- | ---------------------------------------------------- |
   | m_ids          | 当前活跃的事务ID集合                                 |
   | min_trx_id     | 最小活跃事务ID                                       |
   | max_trx_id     | 预分配事务ID，当前最大事务ID+1（因为事务ID是自增的） |
   | creator_trx_id | ReadView创建者的事务ID                               |

   ![image-20220427181811105](.\images\image-20220427181811105.png)

   不同隔离级别，生成readview的时机不同：

   READ COMMITTED:在事务中每一次执行快照读时生成ReadView.
   REPEATABLE READ:仅在事务中第一次执行快照读时生成ReadView，后续复用该ReadView.

# 13 MySQL 管理

## 13.1 系统数据库

| 数据库             | 含义                                                         |
| ------------------ | ------------------------------------------------------------ |
| mysql              | 存储MySQL服务器正常运行所需要的各种信息（时区、主从、用户、权限等) |
| information_schema | 提供了访问数据库元数据的各种表和视图，包含数据库、表、字段类型及访问权限等 |
| performance_schema | 为MySQL服务器运行时状态提供了一个底层监控功能，主要用于收集数据库服务器性能参数 |
| sys                | 包含了一系列方便 DBA和开发人员利用performance_schema性能数据库进行性能调优和诊断的视图 |



## 13.2 常用工具

## 13.2.1 mysql

该mysql不是指mysql服务，而是指mysql的客户端工具。

```mysql
# 语法
mysql [options] [database]

# 选项
	-u, --user=name         # 指定用户名
	-p, --password          # 指定密码
	-h, --hose=name         # 指定服务器IP或域名
	-P， --port=port        # 指定连接端口
	-e, --execute=name      # 执行SQL语句并退出
	
mysql -h 192.168.200.202 -u root -p 1234 itcast -e "select * from stu"
```



### 13.2.2 mysqladmin

mysqladmin是一个执行管理操作的客户端程序。可以用它来检查服务器的配置和当前状态、创建并删除数据库等。

```mysql
# 语法例如：
mysqladmin -uroot -p123456 drop 'test01 ';
mysqladmin-uroot -p123456 version;
```



### 13.2.3 mysqlbinlg

由于服务器生成的二进制日志文件以二进制格式保存，所以如果想要检查这些文本的文本格式，就会使用到mysqlbinlog日志管理工具。

![image-20220427185929965](.\images\image-20220427185929965.png)



### 13.2.4 mysqlshow

mysqlshow客户端对象查找工具，用来很快地查找存在哪些数据库、数据库中的表、表中的列或者索引。

![image-20220427194908019](.\images\image-20220427194908019.png)



### 13.2.5 mysqldump

mysqldump客户端工具用来备份数据厍或在不同数据厍之间进行数据过移。备份内容包含创建表，及插入表的SQL语句。

![image-20220427200510299](.\images\image-20220427200510299.png)



### 13.2.6 mysqlimport/soyrce

mysqlimport是客户端数据导入工具，用来导入mysqldump加-T参数后导出的文本文件。

![image-20220428083134829](.\images\image-20220428083134829.png)

# 14 日志

## 14.1 错误日志

记录了当mysqld启动和停止时，以及服务器在运行过程中发生任何严重错误时的相关信息。当数据库出现任何故障导致无法正常使用时，建议首先查看此日志。

日志文件默认存放目录：/var/log/mysqld.log

```mysql
# 查询错误日志存放目录
show variables like '%log_error%';
```



## 14.3 二进制日志

二进制日志（BINLOG）记录了所有的DDL(数据定义语言）语句和DML(数据操纵语言）语句，但不包括数据查询(SELECT、SHOW)语句。

作用:①.灾难时的数据恢复;②.MySQL的主从复制。在MySQL8版本中，默认二进制日志是开启着的。

```mysql
# 查看二进制日志参数
show variables like '%log_bin%';
```

日志格式(默认为row)：

| 日志格式  | 含义                                                         |
| --------- | ------------------------------------------------------------ |
| STATEMENT | 基于sQL语句的日志记录，记录的是sQL语句，对数据进行修改的sQL都会记录在日志文件中。 |
| ROW       | 基于行的日志记录,记录的是每一行的数据变更。（默认)           |
| MIXED     | 混合了STATEMENT和ROW两种格式，默认采用STATEMENT，在某些特殊情况下会自动切换为ROW进行记录。 |

```mysql
# 查看当前采用的日志格式
show variables like '%binlog_format%';
```



由于日志是以二进制方式存储的，不能直接读取，需要通过二进制日志查询工具mysqlbinlog来查看

![image-20220428085850234](.\images\image-20220428085850234.png)



日志删除

| 指令                                              | 含义                                                         |
| ------------------------------------------------- | ------------------------------------------------------------ |
| reset master                                      | 删除全部binlog日志，删除之后，日志编号，将从 binlog.000001重新开始 |
| purge master logs to 'binlon ***实**\|            | 删除******编号之前的所有日志                                 |
| purge master logs before 'yyyy-mm-dd  hh24:mi:ss' | 删除日志为"yyyy-mm-dd hh24:mi:ss"之前产生的所有日志          |

也可以在mysql的配置文件中配置二进制日志的过期时间，设置了之后，二进制日志过期会自动删除。

```mysql
show variables like '%binlog_expire_logs_seconds%';
```



## 14.2 查询日志

查询日志中记录了客户端的所有操作语句，而二进制日志不包含查询数据的SQL语句。默认情况下
查询日志是未开启的。

相关系统变量：general_log(默认为off)、general_log_file(文件目录)

![image-20220428092742335](.\images\image-20220428092742335.png)



## 14.3 慢查询日志

慢查询日志记录了所有执行时间超过参数long_query_time设置值并且扫描记录数不小于min_examined_row_limit的所有的SQL语句的日志，默认未开启。long_query_time默认为10秒，最小为0，精度可以到微秒。

```mysql
# 开启慢查询日志开关
show_query_log = 1
# 执行时间参数
long_query_time = 2
```

# 15 主从复制

主从复制是指将主数据库的DDL和DML操作通过二进制日志传到从库服务器中，然后在从库上对这些日志重新执行（也叫重做)，从而使得从库和主库的数据保持同步。

MySQL支持一台主库同时向多台从库进行复制，从库同时也可以作为其他从服务器的主库，实现链状复制。



MySQL复制的有点主要包含以下三个方面:

- 主库出现问题，可以快速切换到从库提供服务。
- 实现读写分离，降低主库的访问压力。
- 可以在从库中执行备份,以避免备份期间影响主库服务。34 



## 15.1 复制的原理：

复制分成三步:

1. Master主库在事务提交时，会把数据变更记录在二进制日志文件Binlog中。
1. 从库读取主库的二进制日志文件 Binlog，写入到从库的中继日志Relay Log 。
1. slave重做中继日志中的事件，将改变反映它自己的数据。



## 15.2 主从复制的搭建

### 15.2.1 服务器准备

至少两台服务器→开放端口号或关闭防火墙

![image-20220428215106044](.\images\image-20220428215106044.png)



### 15.2.2 主库配置

修改配置文件  /etc/my.cnf

```mysql
#mysql服务ID，保证整个集群环境中唯一，取值范围:1~2^32-1，默认为1
server-id=1

#是否只读,1代表只读,0代表读写
read-only=O

#忽略的数据,指不需要同步的数据库
#binlog-ignore-db=mysql

#指定同步的数据库
#binlog-do-db=db01
```

重启MySQL服务器

```mysql
systemctl restart mysql
```

登录mysql，创建远程连接的账户，并授予主从复制权限

```mysql
#创建itcast用户,并设置密码,该用户可在任意主机连接该MySQL服务
CREATE USER 'itcast'@'%'IDENTIFIED WITH mysql_native_password BY 'Root@123456';
#为'itcast'@ %'用户分配主从复制权限
GRANT REPLICATION SLAVE ON*.* TO 'itcast'@'%";
```

通过指令，查看二进制日志坐标

```mysql
show master status;
```

字段含义说明:

file：从哪个日志文件开始推送日志文件

position：从哪个位置开始推送日志

hinlog ignore_dh：指定不需要同步的数据库



### 15.2.3 从库配置

修改配置文件 /etc/my.cnf

```mysql
#mysql服务ID，保证整个集群环境中唯一，取值范围:1-232-1，和主库不一样即可
server-id=2
#是否只读,1代表只读,0代表读写
read-only = 1
```

super-read-only  可以设置超级管理员的读写权限



重启mysql服务

```mysql
systemctl restart mysqld
```



登录mysql，设置主库配置

```mysql
CHANGE REPLICATION SOURCE TO SOURCE HOST=-xc.o', SDURCE_USER-o', SOURCE PASSWORD=.xo,SDURCE LOG FLE=-os , SOURCE LOG POS=xxx;

# 如果是8.0.23之前的版本中需要执行：
CGHNGE MASTER TO MASTER HOST-kx.osc..x , NASTER USER=.xo , NASTER PASSWORD=.o'，MASTER_LOG FLE=xo', MASTER_LOG_POS=xxx;
```

| 参数名          | 含义               | 8.0.23之前      |
| --------------- | ------------------ | --------------- |
| SOURCE_HOST     | 主库IP地址         | MASTER_HOST     |
| SOURCE_USER     | 连接主库的用户名   | MASTER_USER     |
| SOURCE_PASSWORD | 连接主库的密码     | MASTER_PASSWORD |
| SOURCE_LOG_FILE | binlog日志文件名   | MASTER_LOG_FILE |
| SOURCE_LOG_POS  | binlog日志文件位置 | MASTER_LOG_POS  |



开启同步操作

```mysql
start replica ; #8.0.22之后
start slave ;  #8.0.22之前
```



查看主从同步状态

```mysql
show replica status;   # 8.0.22 之后
show slave status;     # 8.0.22 之前
```



# 16 分库分表

### 16.0.1 问题

单数据库进行数据存储，存在以下性能瓶颈：

​		IO瓶颈:热点数据太多，数据库缓存不足，产生大量磁盘IO，效率较低。请求数据太多，带宽不够，网络IO瓶颈。

​		CPU瓶颈:排序、分组、连接查询、聚合统计等SQL会耗费大量的CPU资源，请求数太多，CPU出现瓶颈.



### 16.0.2 拆分策略

![image-20220429105551407](.\images\image-20220429105551407.png)

#### 16.0.2.1 垂直拆分

垂直分库：以表为依据，根据业务将不同表拆分到不同库中。特点：

- 每个库的表结构都不一样
- 每个库的数据也不一样
- 所有库的并集是全量数据

![image-20220429105822341](.\images\image-20220429105822341.png)

垂直分表：以字段为依据，根据字段属性将不同字段拆分到不同表。特点：

- 每个表的结构都不一样
- 每个表的数据也不一样一般通过一列（主键/外键）关联
- 所有表的并集是全量数据

#### 16.0.2.2水平拆分

![image-20220429110200959](.\images\image-20220429110200959.png)

水平分库：以字段为依据，按照一定策略，将一个库的数据拆分到多个库中。特点：

- 每个库的表结构都一样
- 每个库的数据都不一样
- 所有库的并集是全量数据

![image-20220429110358061](.\images\image-20220429110358061.png)

水平分表：按照一定策略，将一个表中的数据拆分到多个表中。特点：

- 每个表的结构一样
- 每个表的数据不一样
- 所有表的并集是全量数据



### 16.0.3 实现技术

- shardingJDBC:基于AOP原理，在应用程序中对本地执行的SQL进行拦截，解析、改写、路由处理。需要自行编码配置实现，只支持java语言，性能较高。
- MyCat:数据库分库分表中间件，不用调整代码即可实现分库分表，支持多种语言，性能不及前者。

![image-20220429110757257](.\images\image-20220429110757257.png)



## 16.1 Mycat

Mycat是开源的、活跃的、基于Java语言编写的MySQL数据库中间件。可以像使用mysql一样来使用mycat，对于开发人员来说根本感觉不到mycat的存在。
