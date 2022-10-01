## 常量

### 指针和const

#### 指向常量的指针

指向常量的指针不能用于改变其所指对象的值，而且只有使用指向常量的指针才能存放常量对象的地址。

```c++
const double pi = 3.14;
double *ptr = &p1;			// 错误，ptr是一个普通指针
const double *cptr;			// 正确，cptr可以指向一个双精度常量
*cptr = 42;					// 错误，不能给指向常量的指针解引用复制
```

一般指针的类型必须与其所指对象的类型一致，但是有例外：

​		指向常量的指针可以指向普通的变量。即指向常量的指针没有规定只能指向常量，其限制只是不能通过这个指针修改指向对象的值，没有限制该对象通过其他途径改变。

```c++
double dval = 3.14;
cptr = &dval;			// 能够正确的取到地址，但是不用通过这个指针改变对象的值
```

#### 常指针

常指针只能指向一个固定的地址，常指针对象初始化之后就不能修改这一个指针对象的值。

```c++
int num = 0;
int *const numptr = &num;		// numptr 将一直且只能指向 num
const double pi = 3.14;
const double *const piptr = &pi;	// piptr 是一个指向常量对象的常指针
*numptr = 3;				// 正确，piptr 是一个常指针，指针的值不可变，但是通过它改变其指向的对象的值
```

### constexpr和常量表达式

#### 常量表达式

const expression：值不会改变且在编译过程中能得到计算结果的表达式。

```c++
const int max_files = 20;			// max_files是常量表达式
const int limit = max_files + 1;	// limit 是常量表达式
int staff_size = 27;				// staff_size 不是常量表达式。虽然右值是字面值常量，但是左值不是常量
const int sz = get_size();			//	运行的时候才能得到值，不是常量表达式
```

#### constexpr变量

C++11新标准规定，允许将变量声明为constexpr类型以便由编译器来验证变量的值是否是一个常量表达式。声明为constexpr的变量一定是一个常量，而且必须用常量表达式初始化

```c++
constexpr int mf = 20;			// 20 是常量表达式，mf 是常量
constexpr int limit = mf + 1;	// mf + 1 是常量表达式，limit是常量
constexpr int sz = size();		// 只有当size是一个constexpr函数时才是一条正确的声明语句
```

#### constexpr与指针

在constexpr声明中如果定义了一个指针，限定符constexpr仅对指针有效，与指针所指向的对象无关。

```c++
const int *p = nullptr;			// p 是一个指向整形常量的指针
constexpr int *q = nullptr;		// q 是一个指向整形的常指针
```

### nullptr与NULL

有些编译器会将 NULL 定义为 ((void*)0) ，有的直接定义为0。C++不允许直接吧void *隐式转换到其他类型。

nullptr 的类型为 nullptr_t ，能够隐式的转换为任何指针或成员指针的类型，也能和他们进行相等或者不等的比较。

```c++
int *p1 = nullptr;			// 正确，支持类型转换
double *p2 = NULL;			// 错误，编译器可能不支持这样的类型转换
```



## 类型处理

### 类型别名

#### typedef

```c++
typedef double wage;		// wage 是double的同义词
typedef wage base, *p;		// base、wage、double 是同义词，p是double*的同义词
```

#### 别名声明

```c++
using SI = Sales_item;
```

#### auto

自动类型

```c++
vector<string> v1;
auto l1 = v1.begin();		// l1 是一个迭代器
auto pi = 3.14;				// pi 是一个double类型变量
```

#### decltype

函数，函数、或表达式的返回值类型

```c++
decltype(func()) sum = x;		// sum 的类型就是函数f的返回值类型
const int c1 = 1, &c2 = c1;
decltype(c1) x = 2;				// x 的类型为 const int
decltype(c2) y = x;				// y 的类型为 const int&
decltype(c2) z;					// 错误，z的类型是const int&，必须初始化

int i = 42, *p = &i, &r = i;
decltype(r + 0) b;				// 加法运算的结果是int，因此b是一个（未初始化的）int
decltype(*p) c;					// 错误。指针解引用的结果是一个引用，所以c也是一个引用，必须初始化

decltype((i)) d;				// 错误。d是int&，必须初始化————decltype的表达式如果加上了括号结果将是引用
decltype(i) e;					// 正确，e是一个（未初始化的）int
```

### 显示强制类型转换

castName<targetType>(原始类型)，其中castName指定了执行的是哪种转换

#### static_cast

任何具有明确定义的类型转换,只要不包含底层const,都可以使用static_cast。例如，通过将一个运算对象强制转换成double类型就能使表达式执行浮点数除法

```c++
double d1 = static_cast<double>(j) / i;
```

当需要把一个**较大的算术类型赋值给较小的类型**时，static_cast非常有用。此时，强制类型转换告诉程序的读者和编译器:我们知道并且不在乎潜在的精度损失。一般来说，如果编译器发现一个较大的算术类型试图赋值给较小的类型，就会给出警告信息；但是当我们执行了显式的类型转换后，警告信息就会被关闭了。

static_cast对于**编译器无法自动执行的类型转换**也非常有用。例如，我们可以使用static cast找回存在于void*指针中的值:

```c++
double d = 3.14;
void *p = &d;		// 任何非常两对象的地址都能存入void *
double *dp = static_cast<double*>(p);
```

当我们把指针存放在void*中，并且使用static_cast将其强制转换回原来的类型时，应该确保**指针的值保持不变**。也就是说，强制转换的结果将与原始的地址值相等，因此我们必须确保**转换后所得的类型就是指针所指的类型**。类型一旦不符，将产生未定义的后果。

#### const_cast

const_cast 只能改变运算对象的底层const

```c++
const char *pc;
char *p = const_cast<char *>(pc);		// 正确，但是通过p写值是未定义的行为
```

常量对象转换成非常两对象->“去掉const性质”，编译器不再组织对该对象进行写操作。吐过对象本身不是一个常量，使用强制类型转换获得写权限时合法的，但是如果对象本身是一个行亮，再使用const_cast执行写操作就会产生未定义的行为。

#### reinterpret_cast

为运算对象的位模式提供较低层次上的重新解释



## 函数相关

### 内联函数

执行内联函数时相当于是把内联函数的代码块复制到调用的地方，可以避免函数调用的开销。

在类型内声明时直接定义的成员函数默认是内联函数。非成员内联函数或成员函数类外实现在声明和定义时都要在前面加关键字inline

### constexpr函数

能用于常量表达式的函数。定义的方法与其他函数类似，但是：

- 函数的返回值类型及所有形参的类型都需要是字面值类型
- 函数体中必须有且只有一个return语句

```c++
constexpr int new_sz() {return 42;}
constexpr int foo = new_sz();		// 正确，foo是一个常量表达式
```

constexpr函数的返回值也可以不是一个常量，但是要是常量

```c++
constexpr size_t scale(size_t cnt) { return new_sz * cnt;}
int arr[scale(2)];		// 正确，scale(2) 是常量表达式
```

当scale的实参是常量表达式时其返回值也是常量表达式，否则不是。



## 智能指针

头文件memory

### shared_ptr类

多个shared_ptr可以指向同一个对象，每拷贝一次或者作为返回值shared_ptr的引用计数器值递增；销毁掉一个shared_ptr，或者被赋予新的值，指向原对象的shared_ptr的计数器值递减，减为0时销毁所指向的对象

#### shared_ptr和unique_ptr都有的操作

```c++
shared_ptr<T> sp;		// 空智能指针，可以指向类型为T的对象
unique_ptr<T> up;
p;						// 若智能指针p指向一个对象则返回true，否则false
*p;						// 解引用p
p->mem;					// 等价于(*p).mem
p.get();				// 返回p中保存的指针
swap(p, q);				// 交换p、q中的指针
p.swap(q);
```

#### shared_ptr独有的操作

```c++
make_shared<T>(args);		// 返回一个shared_ptr，指向一个动态分配的、用args初始化的类型为T的对象
shared_ptr<T>p(q);			// p是shared_ptr q的拷贝；此操作会递增q中的计数器。q中的指针必须能转换为T*
p = q;						// p 和 q 都是shared_ptr，所保存的指针必须能互相转换。此操作会递减 p 的引用计数；若 p 的引用计数变为 0，将释放其管理的内存
p.unique();					// 若p.use_count() 为1，返回true，否则false
p.use_count();				// 返回与p共享对象的智能指针的数量
```

#### make_shared函数：

```c++
shared_ptr<int>p3 = make_shared<int>(42);
shared_ptr<string> p4 = make_shared<string>("Hello");
```

#### 拷贝与赋值

当进行拷贝或赋值操作时，每个shared_ptr都会记录有多少个其他shared_ptr指向相同的对象。

```c++
auto p = make_shared<int>(42);		// p指向的对象只有一个引用者
auto q(p);						// 拷贝，p、q指向相同的对象，此对象有两个引用者
```

#### 与new结合

```c++
shared_ptr<double> p1(new double(3.1415));		// 正确
shared_ptr<double> p2 = new double(3.14);		// 错误，必须使用直接初始化形式

shared_ptr<int> clone(int p) {
    //return new int(p);		// 错误，必须直接初始化或者显式类型转换
    return shared_ptr<int>(new int(p));
}
```

#### 定义和改变shared_ptr的其他方法

```c++
shared_ptr<T> p(q);			// q必须是new分配的内存或者或者shared_ptr，且能够转换为T*类型
shared_ptr<T> p(u);			// p 从unique_ptr u处接管了对象的所有权，并将u置空
shared_ptr<T> p(q, d);		// p接管了普通指针q所指向的对象的所有权。q必须能转换为T*类型。p将使用可调用对象d来替代delete
shared_ptr<T> p(p2, d);		// p是shared_ptr p2的拷贝，但是用可调用对象d来代替delete
p.reset();
p.reset(q);
p.reset(q, d);
/*若q是唯一指向其对象的shared_ptr，reset会释放此对象。若传递了可选的参数普通指针q，会令p指向q,否则会将p置空。若还传递了参数d，将会调用d而不是delete来释放q*/
```

### unique_ptr类

一个unique_ptr“拥有”它所指向的对象。与shared ptr不同，某个时刻只能有一个unique_ptr指向一个给定对象。当unique _ptr被销毁时，它所指向的对象也被销毁。

与shared_ptr 不同，没有类似make_shared 的标准库函数返回一个unique_ptr。当我们定义一个unique_ptr时，需要将其绑定到一个new返回的指针上。类似shared_ptr，初始化unique _ptr必须采用直接初始化形式

```c++
unique_ptr<double> p1;
unique_ptr<int> p2(new int(21));
```

#### 不支持普通的拷贝和赋值

```c++
unique_ptr<string> p1(new string("Hello")); // 正确
unique_ptr<string> p2(p1); // 错误，不支持同类型（同为unique_ptr<T>）的拷贝
unique_ptr<string> p3;
p3 = p2; // 错误，不支持赋值
```

#### 操作

```c++
unique_ptr<T> u1; // 空unique_ptr，u1会使用delete释放，u2会使用一个类型为D的可调用对象释放
unique_ptr<T, D> u2;

unique_ptr<T, D> u(d); // 空unique_ptr，指向类型为T的对象，用类型为D的对象d来代替delete
u = nullptr; // 释放u指向的对象，将u置空
u.release(); // 放弃对指针的控制权，返回指针，并将u置空
u.reset(); // 释放u指向的对象
u.reset(q); // 如果提供了普通指针q，令u指向这个对象，否则将u置空
u.reset(nullptr);
```

虽然我们不能拷贝或赋值unique ptr，但可以通过调用release或reset将指针的所有权从一个（非const) unique _ptr转移给另一个unique:

```c++
unique_ptr<string> p2(p1.release()); // release将p1置空，同时转移给p2
unique_ptr<string> p3(new string("Hello"));
p2.reset(p3.release()); // reset释放了p2原来指向的内存，并指向了p3原本指向的空间，再将p3置空
```

#### 传参和返回

不能拷贝unique _ptr的规则有一个例外:我们可以拷贝或赋值一个将要被销毁的unique ptr。最常见的例子是从函数返回一个unique_ptr:

```c++
unique_ptr<int> clone(int p) {
    return unique_ptr<int>(new int(p));
}

unique_ptr<int> clone1(int p) {
    unique_ptr<int> ret(new int(p));
    return ret;
}
```

### weak_ptr类

weak_ptr是一种不控制所指向对象生存期的智能指针，它指向由一个shared_ptr管理的对象。将一个weak_ptr绑定到一个shared_ptr不会改变shared_ptr的引用计数。一旦最后一个指向对象的shared_ptr被销毁，对象就会被释放。即使有 weak_ptr指向对象，对象也还是会被释放，因此，weak_ptr的名字抓住了这种智能指针“弱”共享对象的特点。

```c++
weak_pre<T> w; // 空weak_ptr
weak_pre<T> w(sp); // 与shared ptr sp指向相同对象的weak ptr。T必须能转换为sp指向的类型
w = p; // p可以是一个shared_ptr或一个weak_ptr。赋值后w与p共享对象
w.reset(); // 将w置空
w.use_count(); // 与w共享对象的shared ptr的数量
w.expired(); // 若w.use_count()为0则返回true，否则false
w.lock(); // 如果expired为true，返回一个空shared ptr;否则返回一个指向w的对象的shared ptr
```

#### 创建并使用shared_ptr初始化

```c++
auto p = make_shared<int>(42);
weak_ptr<int> wp(p); // wp弱共享p，p的引用计数不增；
```



## allocator

有点类似C语言中的malloc，只分配内存，不构造对象。new在分配的同时构造对象，但是有时我们需要在一个较大的空间中根据需要进行构造对象，这时就需要内存的分配和对象的构造分离，即我们可以分配大块内存，但是真正需要时才真正执行对象构造操作（同时有一定开销）

标准库allocator类定义在头文件 memory中，它帮助我们将内存分配和对象构造分离开来。它提供一种类型感知的内存分配方法，它分配的内存是原始的、未构造的。表12.7概述了allocator支持的操作。

```c++
#include <iostrea>
#include <memory>

int n = 10;
std::allocator<string> alloc;		// 可以分配string的allocator对象
auto const p = alloc.allocate(n);	// 分配n个为初始化的string
```

```c++
allocator<T> a;		// 定义了一个名为a的allocator对象，可以为类型为T的对象分配内存
a.allocate(n);		// 分配一段原始的、未构造的内存，保存n个类型为T的对象
a.deallocate(p, n);	// 释放从T*指针p中地址开始的内存，这块内存保存了n个类型为T的对象；
					// p必须是一个先前由allocate返回的指针，且n必须是p创建时所要求的大小。在调用deallocate之前，
					// 必须对每个在这块内存中创建的对象调用destroy
a.construct(p, args);	// p必须是一个类型为T*的指针，指向一块原始内存;arg被传递给类型为T的构造函数，
						// 用来在p指向的内存中构造一个对象。一个哟。负责对象构造，在已经开辟好的内存上构造一个对象
a.destroy(p);		// p是T*类型的指针，对p指向的对象执行析构函数
```

### 内存空间未构造

使用时用a.consttruct函数构造，用a.deallocate析构



## tuple

当我们希望将一些数据组合成单一对象，但又不想麻烦地定义一个新数据结构来表示这些数据时，tuple是非常有用的。

```c++
tuple<T1, T2, ..., Tn> t;		// t是一个tuple，成员数为n，第i个成员的类型为Ti。所有成员都进行值初始化
tuple<T1, T2, ..., Tn> t(v1, v2, ..., nv);		// t是一个tuple，每个成员用对应的初始值vi进行初始化
make_tuple(v1, v2, ..., nv);	// 返回一个用给定初始值初始化的 tuple。tuple 的类型从初始值的类型推断
t1 == t2;		// 当两个tuple具有相同数量的成员且成员对应相等时，两个tuple相等。
t1 != t2;		// 这两个操作使用成员的==运算符来完成。一旦发现某对成员不等，接下来的成员就不用比较了
t1 relop t2		// tuple的关系运算使用字典序。两个tuple必须具有相同数量的成员。
    			// 使用<运算符比较t1的成员和t2中的对应成员
git<i> (t)		// 返回t的第i个数据成员的引用;如果t是一个左值,结果是一个左值引用;
    			// 否则，结果是一个右值引用。tuple的所有成员都是public的
tuple_size<tupleType>::value	// 一个类模板，可以通过一个tuple类型来初始化。
    						// 它有一个名为value的public constexpr static数据成员，类型为size t，
    						// 表示给定tuple类型中成员的数量
tuple_element<i, tupleType>::type		// 一个类模板，可以通过一个整型常量和一个tuple类型来初始化。
    								// 它有一个名为type的 public成员，表示给定tuple类型中指定成员的类型
```

### 定义和初始化

```c++
tuple<T1, T2, ..., Tn> t;
tuple<T1, T2, ..., Tn> t(v1, v2, ..., nv);
tuple<size_t, size_t, size_t> threeD{1, 2, 3};		// 正确
tuple<size_t, size_t, size_t> threeD1 = {1, 2, 3};	// 错误
```

### 访问成员

```c++
auto book =get<0>(item);			// 返回item第一个成员
auto cnt = get<1>(item);			// 返回item第二个成员
auto price = get<2> (item)/cnt;		// 返回item的第三个成员
get<2>(item) *= 0.8;				// 第三个成员打了个八折

size_t sz = tuple_size<decltype(item)>::value;		// 返回item类型对象的成员数量
tuple_element<1, decltype(item)>::type cnt;			// cnt的类型与item中第二个成员相同
```

```c++
double gpa;
char grade;
std::string name;

// 元 组 进 行 拆 包
std::tie(gpa, grade , name) = get_student(1);
std::cout << "ID: 1, "
<< "GPA: " << gpa << ", "
<< "成 绩: " << grade << ", "
<< "姓 名: " << name << ’\n’;
```

### 运行期索引

std::git<> 依赖一个编译期的常量

```c++
int index = 1;
std::get<index>(t);  // 报错

tuple<string, int, string> t1("田松", 21, "复旦大学");
constexpr int ind = 2;
auto s_ind = get<ind>(t1);	// 正确
cout << s_ind << endl;		// 输出 复旦大学
```

另外，在C++17中引入了variant<>的类型模板参数可以让一个variant<>容纳提供的几种类型的变量

### 合并

```c++
auto new_tuple = std::tuple_cat(get_student(1), std::move(t));
```



## 面向对象

### 委托构造

C++11 引入了委托构造的概念，这使得构造函数可以在同一个类中一个构造函数调用另一个构造函数，从而达到简化代码的目的

```c++
class Base {
public:
    int value1 = 0, value2 = 0;
    Base() {
        value1 = 1;
    }
    Base(int num): Base() {  // 委托 Base() 构造函数
        value2 = num;
    }
};

void test02() {
    Base b(2);
    std::cout << b.value1 << " " << b.value2 << std::endl;
    // 1 2
}
```

### 继承构造

在传统 C++ 中，构造函数如果需要继承是需要将参数一一传递的，这将导致效率低下。C++11 利用关键字 using 引入了继承构造函数的概念：

```c++
class Base {
public:
    int value1 = 0, value2 = 0;
    Base() {
        value1 = 1;
    }
    Base(int num): Base() {
        value2 = num;
    }
};

class Base2: public Base {
public:
    using Base::Base;  // 继承构造
};

void test03() {
    Base2 b(3);
    std::cout << b.value1 << " " << b.value2 << std::endl;
}
```

### 显示虚函数继承

在传统 C++ 中，经常容易发生意外重载虚函数的事情。例如：

```c++
struct Base {
    virtual void foo();
};

struct subClass: Base {
    void foo();
};
```

SubClass::foo 可能并不是程序员尝试重载虚函数，只是恰好加入了一个具有相同名字的函数。另一
个可能的情形是，当基类的虚函数被删除后，子类拥有旧的函数就不再重载该虚拟函数并摇身一变成为
了一个普通的类方法，这将造成灾难性的后果。

C++11 引入了 override 和 final 这两个关键字来防止上述情形的发生。

#### override

重载虚函数时，引入override关键字显式告知编译器进行重载，编译器将检查基函数是否存在这样的虚继承，否则无法通过编译

```c++
struct Base{
    virtual void foo();
};

struct SubClass: Base {
	virtual void foo(int) override;  // OK
    virtual void foo(float) override;	// Worn! 父类没有这个虚函数
};
```

#### final

final 则是为了防止类被继续继承以及终止虚函数继续重载引入的。

```c++
struct Base {
	virtual void foo()final ;
} ;

struct subClass1 f inal : Base {}; 	//合法

struct subClass2 : subClass1 {}; //非法，Sub Class1 已 f in a l

struct subClass3 : Base i
	void foo() ; //非法, f oo 已f i n a l
};
```

### 显式禁用默认构造函数

在传统 C++ 中，如果程序员没有提供，编译器会默认为对象生成默认构造函数、复制构造、赋值算符以及析构函数。另外，C++ 也为所有类定义了诸如 new delete 这样的运算符。当程序员有需要时，可以重载这部分函数。

这就引发了一些需求：无法精确控制默认函数的生成行为。例如禁止类的拷贝时，必须将复制构造函数与赋值算符声明为 private 。尝试使用这些未定义的函数将导致编译或链接错误。

并且，编译器产生的默认构造函数与用户定义的构造函数无法同时存在。若用户定义了任何构造函
数，编译器将不再生成默认构造函数，但有时候我们却希望同时拥有这两种构造函数，这就造成了尴尬。

C++11 提供了上述需求的解决方案，允许显式的声明采用或拒绝编译器自带的函数。

```c++
class Magic {
public:
    Magic() = default;  // 显式声明使用编译器生成的构造
    Magic& operator=(const Magic&) = delete;  // 显式声明拒绝编译器生成赋值构造
    Magic(int magic_num);
};
```

### mutable变量

- const修饰的函数不修改对象内部状态。
- 声明时mutable修饰的变量，告诉编译器这个变量不算对象内部状态。
- 于是const修饰的函数就能修改这个变量啦



### 强类型枚举

传统 C++ 中，枚举类型并非类型安全，枚举类型会被视作整数，则会让两种完全不同的枚举类型可以进行直接的比较（虽然编译器给出了检查，但并非所有），甚至同一个命名空间中的不同枚举类型的枚举值名字不能相同。

```c++
int main() {
    enum class Status {
        ok,
        error
    };
    enum struct Status2 {
        ok,
        error
    };
    
    Status flag1 = 1;	// 将会报错，无法隐式类型转换
    Status flag2 = ok;	// 将会报错，必须使用强制类型名称
    
    Status flag3 = Status::ok;	// ok
    
    // 指定枚举类型的底层数据类型为char
    enum class C: char {
        C1 = 1,
        C2 = 2
    };
    
    // 指定枚举的底层数据类型为unsigned int
    enum class D: unsigned int {
        D1 = 1,
        D2 = 2,
        Dbig = 0xFFFFFFF0U
    };
    
    std::cout << sizeof(C::C1) << std::endl;	// 1
    std::cout << (unsigned int)D::Dbig << endl;		// 4294967280
    cout << (unsigned int)D::D2 << endl;   // 2
    cout << sizeof(D::D1) << endl;         // 4
    cout << sizeof(D::Dbig) << endl;       // 4
    
    return 0;
}
```

实现了类型安全，首先他不能够被隐式的转换为整数，同时也不能够将其与整数数字进行比较，更不可能对不同的枚举类型的枚举值进行比较。但相同枚举值之间如果指定的值类型相同，那么可以进行比较

```c++
if (new_enum::value3 == new_enum::value4) {
	// 会 输 出
	std::cout << "new_enum::value3 == new_enum::value4" << std::endl;
}
```

枚举类型后面使用了冒号及类型关键字来**指定枚举中枚举值的类型**，这使得我们能够为枚举赋值（未指定时将默认使用 **int**）。

而希望获得枚举值的值时，将必须显式的进行类型转换，不过可以通过重载 << 这个算符来进行输出

```c++
#include <iostream >
template <typename T>
std::ostream& operator <<(typename std::enable_if <std::is_enum <T>::value , std::ostream >::type& stream , const T& e) {
	return stream << static_cast <typename std::underlying_type <T>::type >(e);
}
```



## lambda表达式

```c++
[捕获列表](参数列表) mutable(可 选) 异常属性 -> 返回类型（可以自动推导） {
    // 函 数 体
}
```

### 捕获

捕获列表，其实可以理解为参数的一种类型，lambda 表达式内部函数体在默认情况下是不能够使用函数体外部的变量的，这时候捕获列表可以起到传递外部数据的作用。根据传递的行为，捕获列表也分为以下几种：

#### 值捕获

与函数参数传值类似，值捕获的前提是变量可以拷贝，不同之处则在于，被捕获的变量在 lambda表达式被**创建时拷贝**，而非调用时才拷贝

```c++
void lambda_value_capture() {
	int value = 1;
	auto copy_value = [value] {
		return value;
	};
	value = 100;
	auto stored_value = copy_value();
	std::cout << "stored_value = " << stored_value << std::endl;
	// 这 时 , stored_value == 1, 而 value == 100.
	// 因 为 copy_value 在 创 建 时 就 保 存 了 一 份 value 的 拷 贝
}
```

#### 引用捕获

与引用传参类似，引用捕获保存的是引用，值会发生变化。

```c++
void lambda_refrence_capture() {
    int value = 1;
    auto copy_value = [&value] {
        return value;
    };
    value = 100;
    auto stored_value = copy_value();
    std::cout << "stored_value = " << stored_value << std::endl;
    // stored_value = 100, value = 100，因为copy_value保存的是引用
}
```

#### 隐式捕获

手动书写捕获列表有时候是非常复杂的，这种机械性的工作可以交给编译器来处理(自动推导)，这时候可以在捕获列表中写一个 & 或 = 向编译器声明采用引用捕获或者值捕获

- []		空捕获列表
- [name1, name2,...]	  值捕获一系列变量
- [&]      引用捕获，编译器自动推导补货列表
- [=]      值捕获，自动推导

#### 表达式捕获

值捕获、引用捕获都是已经在外层作用域声明的变量，因此这些捕获方式捕获的均为左值，而不能捕获右值。

C++14允许捕获的成员用任意的表达式进行初始化 --> 允许了右值的捕获，被声明的捕获变量类型会根据表达式进行判断，判断方式与使用 auto 本质上相同

```c++
#include <iostream>
#include <utility>

int main() {
	auto important = std::make_unique <int >(1);
	auto add = [v1 = 1, v2 = std::move(important)](int x, int y) -> int {
		return x+y+v1+(*v2);
	};
	std::cout << add(3,4) << std::endl;
}  // important 是一个独占指针，是不能够被捕获到的，这时候我们需要将其转移为右值，在表达式中初始化。
```

### 泛型lambda

 auto 关键字不能够用在参数表里，这是因为这样的写法会与模板的功能产生冲突。但是 Lambda 表达式并不是普通函数，所以 Lambda 表达式并不能够模板化。这就为我们造成了一定程度上的麻烦：参数表不能够泛化，必须明确参数表类型。

 C++14 开始，Lambda 函数的形式参数可以使用 auto 关键字来产生意义上的泛型

```c++
auto add = [] (auto x, auto y) {
    return x + y;
};

add(1,2);
add(1.1,2.2);
```



## 函数对象包装

### std::function

Lambda 表达式的本质是一个和函数对象类型相似的类类型（称为闭包类型）的对象（称为闭包对象），当 Lambda 表达式的捕获列表为空时，闭包对象还能够转换为函数指针值进行传递

```c++
#include <iostream >

using foo = void(int); // 定 义 函 数 类 型 , using 的 使 用 见 上 一 节 中 的 别 名 语 法
void functional(foo f) { // 定义在参数列表中的函数类型foo 被 视 为 退 化后的函数指针类型foo*
	f(1); // 通过函数指针调用函数
}

int main() {
	auto f = [](int value) {
		std::cout << value << std::endl;
	};
	functional(f); // 传递闭包对象，隐式转换为foo*类型的函数指针值，再调用
	f(1); // lambda 表 达 式 调 用
	return 0;
}
```

C++11 std::function 是一种通用、多态的函数封装，它的实例可以对任何可以调用的目标实体进行存储、复制和调用操作，它也是对 C++ 中现有的可调用实体的一种类型安全的包裹（相对来说，函数指针的调用不是类型安全的），换句话说，就是函数的容器。当我们有了函数的容器之后便能够更加方便的将函数、函数指针作为对象进行处理。

```c++
#include <functional >
#include <iostream >

int foo ( int para ) {
	return para ;
}

int main () {
	// std::function 包装了一个返回值为int，参数为int的函数
	std::function<int(int)>func = foo;
	int important =10 ;
    
    // 包装了一个返回值类型为int，参数为int，引用捕获的lambda表达式
	std::function<int(int)> func2 = [&](int value) -> int {
		return 1+value+important ;
	};
	std::cout << func(10) << std::endl;
    std::cout << func2 (10) << std::endl;
}
```

### std::bind、std::placeholder

std::bind 则是用来绑定函数调用的参数的，它解决的需求是我们有时候可能并不一定能够一次性获得调用某个函数的全部参数，通过这个函数，我们可以将部分调用参数提前绑定到函数身上成为一个新的对象，然后在参数齐全后，完成调用。

```c++
int foo(int a, int b, int c) {
	;
}

int main() {
	// 将参数1,2绑定到函数foo 上，但是使用std::placeholders::_1来对第一个参数进行占位
	auto bindFoo = std::bind(foo, std::placeholders::_1, 1,2);
	// 这 时 调 用 bindFoo 时， 只 需 要 提 供 第 一 个 参 数 即 可
	bindFoo(1);
}
```

## 

## 右值引用*

 C++11 引入的与 Lambda 表达式齐名的重要特性之一。它的引入解决了 C++ 中大量的历史遗留问题，消除了诸如 std::vector 、 std::string 之类的额外开销，也才使得函数对象容器 std::function 成为了可能。

### 左值、右值的纯右值、将亡值、右值

- **左值** (lvalue, left value)：赋值符号左边的值。准确来说，左值是表达式（不一定是赋值表达式）后依然存在的持久对象。

- **右值**（rvalue， right value）：表达式结束后就不再存在的临时对象。

  而 C++11 中为了引入强大的右值引用，将右值的概念进行了进一步的划分，分为：纯右值、将亡值。

- **纯右值** (prvalue, pure rvalue)：要么是纯粹的字面量，例如 10 , true ；要么是求值结果相当于字面量或匿名临时对象，例如 1+2 。非引用返回的临时变量、运算表达式产生的临时变量、原始字面量、Lambda 表达式都属于纯右值。

- **将亡值** (xvalue, expiring value)，是 C++11 为了引入右值引用而提出的概念（因此在传统 C++
  中，纯右值和右值是同一个概念），也就是即将被销毁、却能够被移动的值。

```c++
std::vector <int> foo() {
    std::vector<int> temp = { 1,2，3,4 };
    return temp;
}
std::vector<int> v = foo();
```

函数 foo 的返回值 temp 在内部创建然后被赋值给 v ，然而 v获得这个对象时，会将整个 temp 拷贝一份，然后把 temp 销毁，如果这个 temp 非常大，这将造成大量额外的开销（这也就是传统 C++ 一直被诟病的问题）。

在最后一行中， v 是左值、 foo() 返回的值就是右值（也是纯右值）。但是， v 可以被别的变量捕获到，而 foo() 产生的那个返回值作为一个临时值，一旦被 v 复制后，将立即被销毁，无法获取、也不能修改。而将亡值就定义了这样一种行为：临时的值能够被识别、同时又能够被移动。

 C++11 之后，编译器为我们做了一些工作，此处的左值 temp 会被进行此隐式右值转换，等价于static_cast<std::vector<int> &&>(temp) ，进而此处的 v 会将 foo 局部返回的值进行移动。 ——> 移动语义

### 左值引用和右值引用

要拿到一个将亡值，就需要用到右值引用的申明： T && ，其中 T 是类型。右值引用的声明让这个临时值的生命周期得以延长、只要变量还活着，那么将亡值将继续存活。

C++11 提供了 std::move 这个方法将左值参数无条件的转换为右值，有了它我们就能够方便的获得一个右值临时对象。

```c++
#include<iostream >
#include <string >

void reference(std::string &str) {
    std::cout << "左值" << std::endl;
}
void reference(std::string &&str) {
    std::cout << "右值" << std::endl;
}
int main() {
    std::string lv1 = "string , "; // lu1 是一个左值
    // std::string &&r1 = lv1; //非法，右值引用不能引用左值
    std::string &&rv1 = std::move(lv1); //合法, std : : move可以将左值转移为右值
    std::cout << rv1 << std::endl; // string,
    const std::string &lv2 = lv1 + lv1;//l合法，常量左值引用能够延长临时变量的生命周期
    // lv2 += " Test "; 1 / 非法﹐常量引用无法被修改
    std::cout << lv2 << std::endl; // string, string
    std::string &&rv2 = lv1 + lv2;//合法，右值引用延长临时对象生命周期, 左值
    rv2 += " Test " ; //合法﹐非常量引用能够修改临时变量
    std::cout << rv2 << std::endl; // string, string, string, Test
    reference(rv2); // 输出左值
    return 0;
}
```

但是：

```c++
#include <iostream >

int main() {
	// int &a = std::move(1); // 不 合 法， 非 常 量 左 引 用 无 法 引 用 右 值
	const int &b = std::move(1); // 合 法 , 常 量 左 引 用 允 许 引 用 右 值

	std::cout << a << b << std::endl;
}
```

不允许非常量引用绑定非左值的原因：

```c++
void increase(int & v) {
	v++;
}

void foo() {
	double s = 1;
	increase(s);
}
```

因为int&不能引用double参数，所以必须产生一个淋湿值来保存s的值，从而当increase()修改这个淋湿值时，调用完成后s本身并没有被修改

常量引用允许绑定到非左值？因为该引用不修改值。

### 移动语义

传统 C++ 通过拷贝构造函数和赋值操作符为类对象设计了拷贝/复制的概念，但为了实现对资源的移动操作，调用者必须使用先复制、再析构的方式，否则就需要自己实现移动对象的接口。这就像是把所有东西新买了一份到新家再把原来的东西全扔掉，很反人类。

传统的 C++ 没有区分『移动』和『拷贝』的概念，造成了大量的数据拷贝，浪费时间和空间。右值引用的出现恰好就解决了这两个概念的混淆问题

```c++
#include <iostream >
class A {
public:
    int *pointer;
    A():pointer(new int(1)) {
        std::cout << "构 造" << pointer << std::endl;
    }
    A(A &a):pointer(new int(*a.pointer)) {
        std::cout << "拷 贝" << pointer << std::endl;
    } // 无 意 义 的 对 象 拷 贝
    A(A &&a):pointer(a.pointer) {
        a.pointer = nullptr;
        std::cout << "移 动" << pointer << std::endl;
    }
    ~A() {
        std::cout << "析 构" << pointer << std::endl;
        delete pointer;
    }
};
// 防 止 编 译 器 优 化
A return_rvalue(bool test) {
    A a, b;
    if (test) return a; // 等 价 于 static_cast <A&&>(a);
    else return b; // 等 价 于 static_cast <A&&>(b);
}
int main() {
    A obj = return_rvalue(false);
    std::cout << "obj:" << std::endl;
    std::cout << obj.pointer << std::endl;
    std::cout << *obj.pointer << std::endl;
    return 0;
}
```



## 容器

### std::array

vector缺点：

- 自动扩容，开销

- 清空时删除其中元素但不会归还空间，需要使用std::vector::shrink_to_fit()

  ```c++
  std::vector <int> v;
  std::cout << "size:" << v.size() << std::endl; // 输 出 0
  std::cout << "capacity:" << v.capacity() << std::endl; // 输 出 0
  // 如 下 可 看 出 std::vector 的 存 储 是 自 动 管 理 的， 按 需 自 动 扩 张
  // 但 是 如 果 空 间 不 足， 需 要 重 新 分 配 更 多 内 存， 而 重 分 配 内 存 通 常 是 性 能 上 有 开 销 的 操 作
  v.push_back(1);
  v.push_back(2);
  v.push_back(3);
  std::cout << "size:" << v.size() << std::endl; // 输 出 3
  std::cout << "capacity:" << v.capacity() << std::endl; // 输 出 4
  
  // 这 里 的 自 动 扩 张 逻 辑 与 Golang 的 slice 很 像
  v.push_back(4);
  v.push_back(5);
  std::cout << "size:" << v.size() << std::endl; // 输 出 5
  std::cout << "capacity:" << v.capacity() << std::endl; // 输 出 8
  
  // 如 下 可 看 出 容 器 虽 然 清 空 了 元 素， 但 是 被 清 空 元 素 的 内 存 并 没 有 归 还
  v.clear();
  std::cout << "size:" << v.size() << std::endl; // 输 出 0
  std::cout << "capacity:" << v.capacity() << std::endl; // 输 出 8
  
  // 额 外 内 存 可 通 过 shrink_to_fit() 调 用 返 回 给 系 统
  
  v.shrink_to_fit();
  std::cout << "size:" << v.size() << std::endl; // 输 出 0
  std::cout << "capacity:" << v.capacity() << std::endl; // 输 出 0
  ```

std::array结构上类似于数组，其大小固定；但是封装了一些操作函数，如获取数组大小及检查是否为空，还能使用标准库中的容器算法

```c++
std::array <int, 4> arr = {1, 2, 3, 4};  // 声明与定义

arr.empty(); // 检 查 容 器 是 否 为 空
arr.size(); // 返 回 容 纳 的 元 素 数

// 迭 代 器 支 持
for (auto &i : arr)
{
// ...
}

// 用 lambda 表 达 式 排 序
std::sort(arr.begin(), arr.end(), [](int a, int b) {
return b < a;
});

// 数 组 大 小 参 数 必 须 是 常 量 表 达 式
constexpr int len = 4;
std::array <int, len> arr = {1, 2, 3, 4};
// atd::array<int, 4> arr2;    报错

// 非 法 ,不 同 于 C 风 格 数 组， std::array 不 会 自 动 退 化 成 T*
// int *arr_p = arr;
```

而且不同于C数组，array不能自动退化成T*，但是其结构任然是顺序存储的，所以还是有办法能够兼容C风格接口

```c++
void foo(int *p, ine len) {
    return ;
}

std::array<int, 4> arr{1,2,3,4};

// foo(arr, arr.size());     // 错误，无法隐式转换
foo(&arr[0], arr.size());
foo(arr.data(), arr.size());
```

### std::forward_list

std::forward_list 是一个列表容器，使用方法和 std::list 基本类似,使用单向链表进行实现，当不需要双向迭代时，具有比 std::list 更高的空间利用率。

### std::priority_queue

头文件：queue

C++中优先队列是用数据结构中的堆来实现的，与普通队列先入先出的性质不同，优先队列中是每进入一个新元素，队列内部会按照规则重新排序，最终使得优先级最高的元素总是在队首。在C++中默认为大顶堆，即数值越大优先级越高，当然也可以通过重载运算符和重写仿函数来修改优先级比较规则。

```c++
//和队列基本操作相同:
top() 访问队头元素
empty() 队列是否为空
size() 返回队列内元素个数
push() 插入元素到队尾 (并排序)
emplace() 原地构造一个元素并插入队列
pop() 弹出队头元素
swap() 交换内容
    
//定义：
priority_queue<Type, Container, Functional>;
	// Type: 数据类型
	// Container：容器类型（Container必须是用数组实现的容器，比如vector,deque
	// Functional 比较的方式
	//方式一
		priority_queue<int> pq;
	//方式二
		priority_queue<int,vector<int>,greater<int>> pq;//升序排列
		priority_queue<int,vector<int>,less<int>> pq;//降序排列

//使用基本数据类型时，只需要传入数据类型，默认是大顶堆。
priority_queue<int> a; 
```

以自定义类型作为元素时需要对该类型重载<运算符或重载greater或less函数

```C++
struct node {
    int x;
    int y;
    friend bool operator < (node n1,node n2) {//重载运算符
        return n1.x > n2.x; //x越小优先级越高，如果是<,则相反
    }
};
priority_queue<node> pq;
```

