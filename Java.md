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

## Final变量

类、方法中有final修饰的变量即一个常量，不能被修改。



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

| 修饰符    | 本类中 | 同包其他类 | 任意包子类 | 任意包任意类 |
| --------- | ------ | ---------- | ---------- | ------------ |
| private   | √      |            |            |              |
| 缺失      | √      | √          |            |              |
| protected | √      | √          | √          |              |
| public    | √      | √          | √          | √            |

### this

this引用对象本身

### 类静态方法

#### 工具类

工具类不需要实例对象，只需要通过类名的引用即可调用类中的方法、变量来实现相应的功能，这样的类中的变量、提供给外界的方法都用static修饰（属于类并不是属于对象）

这样的工具类的构造器可以设置为private，这样外部就不能实例化除这个类的对象。

#### “静态”注意事项

静态方法只能引用静态变量和静态方法。非静态方法能够引用静态变量和静态方法。
静态的方法和变量属于类，非静态的变量和方法属于类的实例——对象

##  类的五大成分

成员变量、方法、构造器、代码块（初始化块）、内部类

### 构造器

构造类、对象的方法

### 内部类

**成员内部类**

- 成员内部类是外部类的一个成员，它可以声明为public、protected、private或默认访问级别。
- 它不能包含静态成员，因为静态成员属于类级别，而内部类实例化时需要外部类的实例。

```java
public class OuterClass {
    private int outerField = 10;

    public class MemberInnerClass {
        public void display() {
            System.out.println("Outer field: " + outerField);
        }
    }
}
```

**静态内部类**

- 静态内部类是外部类的静态成员，它可以声明为public或private。
- 它可以包含静态和非静态成员，并且不需要外部类的实例就可以创建。
- 静态内部类不能直接访问外部类的非静态成员。

```java
public class OuterClass {
    public static class StaticInnerClass {
        public void display() {
            System.out.println("Outer class is accessed using OuterClass.class");
        }
    }
}
```

**局部内部类**

- 局部内部类是定义在方法或作用域内的类。
- 它只能在定义它的区域内被访问和使用。
- 可以访问其外部方法中声明为final或effectively final的局部变量。

```java
public class OuterClass {
    public void outerMethod() {
        final int localVariable = 5;
        class LocalInnerClass {
            public void display() {
                System.out.println("Local variable: " + localVariable);
            }
        }
        LocalInnerClass lic = new LocalInnerClass();
        lic.display();
    }
}
```

**匿名内部类**

- 匿名内部类是没有名称的局部内部类。
- 它通常用于创建一个继承自类或实现接口的对象，并同时声明和实例化该对象。
- 它可以访问其外部方法中声明为final或effectively final的局部变量。

```java
public class OuterClass {
    public void outerMethod() {
        Runnable r = new Runnable() {
            @Override
            public void run() {
                System.out.println("Anonymous Inner Class");
            }
        };
        new Thread(r).start();
    }
}
```

## 单例设计模式

确保类只有一个对象

- 把类的静态构造器写好
- 定义一个静态类变量用来引用类的一个对象
- 定义一个静态类方法返回这个对象的引用

```java
public class Temp {
    private static Temp a = new Temp();  // 这里已经实例化了

    private Temp() {}

    public static Temp getTemp() {
        return a;
    }
}
```

类的构造器私有之后就只能生成一个对象。

**饿汉式单例**：取对象时对象早已经创建好了（代码示例如上）

**懒汉式单例**：取对象时对象才开始创建

```java
public class Temp {
    private static Temp a;
    private Temp () {}
    private static getTemp() {
        if (Temp == null) {
            a = new Temp();
        }
        return a;
    }
}
```

## 继承

关键字为extends，子类可以继承父类的非私有成员

```java
public class A {
	public int i;
	public A() {
		this.i = 10;
	}
	public void print1() {
		System.out.println(this.i);
	}
}

public class B extend A {
    public void print1() {
        System.out.println("B::" + i);
    }
}
```

带有继承关系的类对象的创建方式：

```java
public class ClassA {
    public ClassA() {
        System.out.println("ClassA(): GO");
    }

    public void f() {
        System.out.println("ClassA.f(): GO");
    }
}

public class ClassB extends ClassA {
    public ClassB() {
        System.out.println("ClassB(): GO");
    }

    public void f() {
        System.out.println("ClassB.f(): GO");
    }
}

public class RunCode {
    public static void main(String[] args) {
        System.out.println("hello");
        ClassA b = new ClassB();
        b.f();
    }
}
```

输出结果为：
hello
ClassA(): GO
ClassB(): GO
ClassB.f(): GO

也就是说：
	创建子类对象时会先调用父类的构造器，再调用自己的构造器。即使是使用父类的变量来引用子类的对象调用方法，调用的也是子类的方法。

**单继承**：不支持多继承，支持多层继承

**Object类**：java所有类的“祖宗类”

### 方法重写

