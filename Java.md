# Java内存分配

- 方法区
  **所有线程共享**，存储已被虚拟机加载的**类信息**、**常量**、**静态变量**和**即时编译器编译后的代码**等数据。
- 堆
  被**所有线程共享**，虚拟机启动时创建，**存放对象实例**，
- 栈
  java虚拟机栈是**线程私有**的，它的生命周期与线程相同。描述的是Java方法执行的内存模型：每个方法在执行的时候都会同时创建一个栈帧用于存储**局部变量表**、**操作栈**、**动态链接**、**方法返回地址**等信息。每一个方法从被调用直至执行完成的过程，就对应着一个栈帧在虚拟机栈中从入栈到出栈的过程。
- 本地方法栈
  虚拟机栈为虚拟机执行Java方法（也就是字节码）服务，而本地方法栈则**为虚拟机使用到的Native方法服务**。
- 程序计数器
  可以看作是当前线程所执行的字节码的**行号指示器**。字节码解释器工作时就是通过改变这个计数器的值来选取下一条需要执行的字节码指令，分支、循环、跳转、异常处理和线程恢复等基础功能都需要依赖这个计数器来完成。

![img](./images/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9qaW1teXN1bi5ibG9nLmNzZG4ubmV0,size_16,color_FFFFFF,t_70.png)

# Java变量

## 变量的有效范围

**成员变量**：在类体中定义的变量，分为静态变量和实例变量

- 静态变量：
  java的静态变量与C++中类中定义的静态变量定义和功能相似（java是纯面向对象语言，所以不存在C++中所说的全局变量），静态变量只属于类不属于类的实例。会在程序运行期间一直有效
- 实例变量
  属于对象的变量，这个变量在类中、方法外定义。每个对象都有自己的实例变量（这个该类中有定义的话），在对象存在期间有效

**局部变量**：在类的方法体中定义的变量，只在这个方法内部大括号之间的代码块中有效。

## Final关键字

可以修饰类、方法、变量

- final类：最终类，不能被**继承**
- final方法：不能被**重写**
- final变量：只能在定义时**赋值**
  final基本类型变量：存储的**数据**不能被改变
  final引用类型变量：存储的**地址**不能被改变，但是地址所指向的对象的内容是可以被改变的

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

| 修饰符    | 本类中 | 同包其他类 | 任意包子类 | 任意包任意类 |
| --------- | ------ | ---------- | ---------- | ------------ |
| private   | √      |            |            |              |
| 缺失      | √      | √          |            |              |
| protected | √      | √          | √          |              |
| public    | √      | √          | √          | √            |

**this**引用对象本身

##  类的五大成分

成员变量、方法、构造器、代码块（初始化块）、内部类

**权限修饰**

| 修饰符    | 本类中 | 同包其他类 | 任意包子类 | 任意包任意类 |
| --------- | ------ | ---------- | ---------- | ------------ |
| private   | √      |            |            |              |
| 缺失      | √      | √          |            |              |
| protected | √      | √          | √          |              |
| public    | √      | √          | √          | √            |

**是否静态**

静态方法只能引用静态变量和静态方法。非静态方法能够引用静态变量和静态方法。
静态的方法和变量属于类，非静态的变量和方法属于类的实例——对象

### 成员变量

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

### 方法

- **静态方法**：属于类，不需要实例即可调用，只能调用静态方法，引用静态变量
  **工具类**不需要实例对象，只需要通过类名的引用即可调用类中的方法、变量来实现相应的功能，这样的类中的变量、方法都用static修饰（属于类并不是属于对象）

- **非静态方法**：属于对象，需要实例才能调用

- **不定长参数方法**：可以接受任意数量的参数，语法：在参数类型后面加上省略号（`...`）

  ```java
  public class VarargsExample {
      // 定义一个接受不定长参数的方法
      public static void printNumbers(int... numbers) {
          for (int number : numbers) {
              System.out.println(number);
          }
      }
  
      public static void main(String[] args) {
          // 调用方法，传递不定数量的参数
          printNumbers(1, 2, 3, 4, 5);
          printNumbers(10, 20, 30);
          printNumbers(); // 传递零个参数
      }
  }
  ```

- **局部变量**：定义在方法内、代码块内的变量

### 代码块

**静态初始化块**

- 静态初始化块在类加载时执行，且只执行一次。
- 它通常用于初始化静态成员变量或执行只需进行一次的静态代码。
- 静态初始化块在类的所有实例创建之前执行。

```java
public class ClassA {
	static {
		// 这里的代码在类加载时执行一次
	}
}
```

**实例初始化块**

- 实例初始化块在每次创建类的实例时执行。
- 它用于初始化实例成员变量或执行其他实例级别的初始化操作。
- 实例初始化块在构造函数执行之前执行。

```java
public class ClassA {
	{
		// 这里的代码在每次创建实例时执行
	}
}
```

### 构造器

C++中的构造函数，最好写上一个无参的构造器（因为不会像C++那样自动生成）

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

关键字为**extends**，子类可以继承父类的非私有成员

| 修饰符    | 本类中 | 同包其他类 | 任意包子类 | 任意包任意类 |
| --------- | ------ | ---------- | ---------- | ------------ |
| private   | √      |            |            |              |
| 缺失      | √      | √          |            |              |
| protected | √      | √          | √          |              |
| public    | √      | √          | √          | √            |

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

public class B extends A {
    public void print1() {
        System.out.println("B::" + i);
    }
}
```

带有继承关系的类对象的创建方式：**extends**

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

    @Override
    public void f() {
        System.out.println("ClassB.f(): GO");
    }

    public void myF() {
        System.out.println("ClassB.myF(): GO");
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
	创建子类对象时会先调用父类的构造器，再调用自己的构造器（或者说子类的构造器中最上方调用了父类的构造器）。如果重写了方法即使是使用父类的变量引用子类的对象来调用在子类中重写过的方法，调用的也是子类的方法。如果使用ClassA类型的变量引用ClassB类型的实例并调用只在ClassB有定义的方法那么就会报错。
	实例化子类对象时会自动调用父类的无参构造器，若需要调用有参的构造器需要使用**super**关键字。

**单继承**：不支持多继承，支持多层继承

**Object类**：java所有类的“祖宗类”

- getClass().getName() 获取类的名称
- toString() 将一个对象返回为字符串形式
- equals() 比较两个对象的实际内容是否相等。“==”比较的时两个变量引用的是不是同一个对象

### 方法重写

继承之后子类可以重写方法

子类的方法、构造器中可以使用**supre**引用父类的变量、调用父类的方法

**注意事项**：

- 重写父类方法是，修改方法的修饰权限只能从小的范围到大的范围。换句话说重写方法的权限范围需要大于等于父类的方法。
- 使用**@Override**注解，可以制定java编译器，检查方法重写的格式是否正确，提高代码可读性。
- 重写的方法返回值类型必须与被重写方法的返回值类型一样或者范围更小。
- 私有方法、静态方法不能被重写。

### 对象类型的转换

**向上转换**（子类向父类）

```java
public class A {……}

public class B extends A {……}

public void func(A a) {……}
```

上面声明的func方法的形参为A类型的对象，当传入其子类B类型的对象时会自动将对象转换为A类型

**向下转换**（父类向子类）

这种转换一般需要显示类型转换除

当在程序中执行向下转型操作时，如果父类对象不是子类对象的实例时会发生异常，所以在执行向下转型之前需要判断父类变量引用的是否为子类的实例。**instanceof**

```java
myobject instanceof MyClass
// myobject: 某个对象引用（变量）  MyClass: 某个类
// 判断变量引用的对象是否为某类的实例
```

## 多态

目标：一个方法可以供很多其他的类使用。继承就是一种方式。

**对象多态**：一个类可以有多个子类，如学生老师都是人

**行为多态**：多个类有同一种方法，但是不同类有不同的实现方式，如人两条腿走，狗四条腿走

### 抽象类与接口

#### 抽象类

解决实际问题时，一般将父类定义为抽象类，需要使用这个父类进行继承与多态处理。回想继承和多态原理，继承树中越是在上方的类越抽象，如鸽子类继承鸟类、鸟类继承动物类等。在多态机制中，并不需要将父类初始化对象，我们需要的只是子类对象，所以在Java语言中设置抽象类不可以实例化对象，因为图形类不能抽象出任何一种具体图形，但它的子类却可以。

抽象类：不可以实例化对象，但其子类可以。关键字：**abstract**

```java
public abstract class Test {
	abstract void testAbstract();
}
```

使用abstract关键字定义的类称为抽象类，而使用这个关键字定义的方法称为**抽象方法**。抽象方法**没有方法体**，这个方法本身没有任何意义，**除非它被重写**，而承载这个抽象方法的抽象类必须被继承，实际上抽象类除了被继承之外没有任何意义。
只要类中有一个抽象方法，此类就被标记为抽象类。

- 抽象类中可以不写抽象方法，但是有抽象方法的类一定是抽象类
- 类有的成员抽象类都具备
- 抽象类不能实例对象，仅作为一种特殊的父类让自来继承并实现
- 一个类继承抽象类必须重写抽象类的所有抽象方法

被继承后需要**实现其中所有的抽象方法**。但是可能有的子类不需要父类中的某些方法，于是出现了接口。

**模板方法设计模式**：吧子类中只需要部分个性化的方法设计为非抽象方法（模板方法），这个方法中需要个性化的部分封装在另外一个抽象方法中让模板方法来调用，以后子类继承时只需要重写父类中的抽象方法。为防止子类重写模板方法可在模板方法声明前缀**final**

### 接口

抽象类的延伸，纯粹的抽象类，所有方法都没有方法体。需要接口内方法的子类实现这个接口。
关键字：**interface**

```java
public interface drawTest {
	void draw();
}
```

一个类可使用**implements**关键字实现一个接口。实现了接口的类即该接口的实现类

在接口中，方法必须被定义为public或abstract形式，其他修饰权限不被Java编译器认可。或者说，即使不将该方法声明为public形式，它也是public。

- 接口的成员只能有成员变量和方法（构造器都不能有）
- 接口中的成员变量默认为常量
- 不能定义方法体

```java
public interface A {
	String SCHOOL_NAME = "University";
	void test();  // 默认public、abstract
}
```

```java
public class ClassA implements 接口1, 接口2…… {
	// ……
}
```

**接口的好处**：

- 弥补了类单继承的不足
- 面向接口编程，可以灵活方便的切换业务实现
  一个接口可以被多个类实现

```java
// 班级操作接口
public interface Operator {
	void printInfo();
    void printScore();
}

// 班级管理员1类
public class Maniger1 implements Operator{
    @Override
    void printInfo(){
        // 输出信息方案1
    }
    
    @Override
    void printScore(){
        // 输出成绩方案1
    }
}

// 班级管理员2类
public class Maniger2 implements Operator{
    @Override
    void printInfo(){
        // 输出信息方案2
    }
    
    @Override
    void printScore(){
        // 输出成绩方案2
    }
}


// 班级类
public class Class {
    private ArrayList<Student> students = new ArrayList({
        // ……
    });
    private operator = new Maniger1();  // 后续如果需要更换解决方案是只需要更改这里
    
    public void printInfo() {
        operater.printInfo();
    }
    
    public void printScore() {
        operator.printScore();
    }
}
```

