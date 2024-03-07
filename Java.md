# Java内存分配

- 方法区
- 堆
- 栈
- 本地方法栈
- 程序计数器

![image-20240307170755750](./images/image-20240307170755750.png)

![image-20240307170936152](./images/image-20240307170936152.png)

# Java变量

## 变量的有效范围

**成员变量**：在类体中定义的变量，分为静态变量和实例变量

- 静态变量：
  java的静态变量与C++中类中定义的静态变量定义和功能相似（java是纯面向对象语言，所以不存在C++中所说的全局变量），静态变量只属于类不属于类的实例。会在程序运行期间一直有效
- 实例变量
  属于对象的变量，这个变量在类中、方法外定义。每个对象都有自己的实例变量（这个该类中有定义的话），在对象存在期间有效

**局部变量**：在类的方法体中定义的变量，只在这个方法内部大括号之间的代码块中有效。

# Java字符串

String(char a[])  ->  用一个字符数组a创建String对象

String(char a[], int offset, int length)  ->  对字符数组a从第offset个字符开始截取length个字符

String(char[] value)  ->  分配一个新的String对象，表示字符数组中所有元素连接的结果

## 字符串连接

运算符'+'

连接其他数据类型时会将这些数据直接转换为字符串。

## 字符串信息

### 字符串长度

String str = "hello"

str.length()

# Java面向对象

其实这么说不太准确，因为Java本身就是纯面向对象的

## 成员变量

定义在类中、方法外

```java
public class Book {
    private String name;
    
    public String getName() {
        int id = 0;
        setNmae("Java");
        return id + this.name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public Book getBook() {
        return this;  // 返回Book对象的引用
    }
}
```

## 成员方法

```
权限修饰符 返回值类型 方法名(参数类型 参数名) {
	// 方法体
	return 返回值;  // 返回类型为void的不需要return
}
```

|                  | private | protected | public |
| ---------------- | ------- | --------- | ------ |
| 本类             | 可见    | 可见      | 可见   |
| 同包其他类或子类 | 不可见  | 可见      | 可见   |
| 其他包的类或子类 | 不可见  | 不可见    | 可见   |

### this

this引用对象本身