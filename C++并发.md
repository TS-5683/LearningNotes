C++编辑注意事项：

- 成员函数首字母大写，
- 成员变量首字母小写，
- 私有成员变量结尾加_
- 私有成员通过函数成外开放时函数名小写开头不加_

# C++并发编程

## 1 并发简介

### 1.1  定义

以前单核计算机同时执行多个任务的方式：高频切换任务造成同时执行的“假象”

问题：

- 每一次切换中间有一定时间上的分隔
- 每一次上下文切换都有一定的时间开销
- 上下文切换时系统必须为当前运行的任务保存CPU的状态和指令指针并计算出要切换到哪一个任务，并为即将切换到的任务重新加载处理器状态
- CPU可能要将新任务的指令和数据的内存载入到缓存中，会阻止CPU执行任何指令，从而造成的更多的延迟。

#### 1.1.1 并发的途径

- 多进程并发：相当于两个程序员分别在两·个办公室办公![image-20220715174947286](C:\Users\ewigk\AppData\Roaming\Typora\typora-user-images\image-20220715174947286.png)

  优点：

  ​	1独立的进程可以通过进程间常规的通信渠道传递讯息(信号、套接字、文件、管道等等)；

  ​	2操作系统在进程间提供的附加保护操作和更高级别的通信机制 → 可以更容易编写安全(safe)的并发代码；

  ​	3可以使用远程连接的方式，在不同的机器上运行独立的进程

  缺点：

  ​	1通信通常设置复杂或者速度慢，这是因为操作系统会在进程间提供了一定的保护措施，以避免一个进程去修改另一个进程的数据；

  ​	2运行多个进程所需的固定开销：需要时间启动进程，操作系统需要内部资源来管理进程；

  ​	3C++标准中并没有提供对进程间通信的原生支持，需要平台的相关API，降低可移植性。

- 多线程并发：相当于两个程序员在同一个办公室的两台电脑上办公![image-20220715175005245](C:\Users\ewigk\AppData\Roaming\Typora\typora-user-images\image-20220715175005245.png)

  每个线程相互独立运行，且线程可以在不同的指令序列中运行。进程中的所有线程都共享地址空间，并且所有线程访问到大部分数据———全局变量仍然是全局的，指针、对象的引用或数据可以在线程之间传递。

  优点：

  ​	地址空间共享，以及缺少线程间数据的保护，使得操作系统的记录工作量减小，所以使用多线程相关的开销远远小于使用多个进程。

  缺点：

  ​	这种共享通常难以建立且难以管理，因为同一数据的内存地址在不同的进程中不相同。

  ​	如果数据要被多个线程访问，那么程序员必须确保每个线程所访问到的数据是一致的（锁）。

### 1.2 为何使用并发

关注点分离（SOC）和性能

#### 1.2.1 分离关注点

通过将相关的代码与无关的代码分离，可以使程序更容易理解和测试，从而减少出错的可能性。即使一些功能区域中的操作需要在同一时刻发生的情况下，依旧可以使用并发分离不同的功能区域；若不显式地使用并发，就得编写一个任务切换框架，或者在操作中主动地调用一段不相关的代码。

如在一个单线程的音乐播放器应用中，播放音频的同时需要定期检查用户的输入来判断是否需要播放下一曲或暂停；而多线程的应用中音频播放和用户界面事件就不需要放在一起。

#### 1.2.2 性能

计算能力的提高不是源自使单一任务运行的更快，而是并行运行多个任务。如果想要利用日益增长的计算能力，那就必须设计多任务并发式软件。

利用并发提升性能的方式：

- 将一个单个任务分成几部分，且各自并行运行，从而降低总运行时间 —— 任务并行（task parallelism）；
- 每个线程在不同的数据部分上执行相同的操作 —— 数据并行(data parallelism)

#### 1.2.3 不适宜使用并发的场景

收益小于成本时不适用并发

- 使用并发的代码在很多情况下难以理解，因此编写和维护的多线程代码就会产生直接的脑力成本，同时额外的复杂性也可能引起更多的错误。除非潜在的性能增益足够大或关注点分离地足够清晰，能抵消所需的额外的开发时间以及与维护多线程代码相关的额外成本
- 性能增益可能会小于预期。因为系统需要从内核分配资源，所以启动线程时存在固有的开销才能把新线程加入调度器中，需要时间
- 线程是有限的资源。如果让太多的线程同时运行，则会消耗很多操作系统资源，从而使得操作系统整体上运行得更加缓慢；运行太多的线程也会耗尽进程的可用内存或地址空间。服务器端为每一个链接启动一个独立的线程，对于少量的链接是可以正常工作的，但当同样的技术用于需要处理大量链接的高需求服务器时，也会因为线程太多而耗尽系统资源。这个就需要使用线程池来做一定的优化。
- 最后，运行越多的线程，操作系统就需要做越多的上下文切换，每个上下文切换都需要耗费本可以花在有价值工作上的时间。所以在某些时候，增加一个额外的线程实际上会降低，而非提高应用程序的整体性能。

### 1.3 C++中使用并发和多线程

C++11之后标准下才能编写不依赖平台扩展的多线程代码



## 2 创建线程方法

### 2.1thread

```c++
#include <iostream>
#include <thread>
using namespace std;

void func() {
    cout << "Son thread begin.\n";
    for (int i = 0; i < 10; i++) {
        cout << "task running " << i << endl;
        this_thread::sleep_for(500ms);
    }
    cout << "Son thread end.\n";
}

int main() {
    cout << "Ded thread begin.\n";
    thread myth(func);  // 创建即开始执行子线程
    myth.detach();  // 分离
    cout << "Ded thread end.\n";
    return 0;
}
```

1. 线程创建时即开始执行子线程

2. 主线程结束or等待：thread::join() -> 在此处等待；thread::detach() -> 主线程直接继续执行不等待，自己执行完之后直接结束任务，在主线程结束之后子线程可能还在运行。两者不能都出现否则出错。

   joinable：子线程是否可以成功使用join()或detach()

3. 当前线程编号：std::this_thread::get_id()，主线程的 id 为 1；线程对象编号：std::thread::id

   ```C++
   #include <iostream>
   #include <thread>
   using namespace std;
   
   void func(int x, int y) {
       printf("%d+%d=%d",x,y,x+y);
       cout << "This thread's ID is " << this_thread::git_id() << endl;
   }
   
   int main() {
       thread myth(func, 3, 10);
       myth.join();
       cout << "main thread's ID is " << this_thread::git_id() << endl;
       return 0;
   }
   ```

4. sleep： this_thread::sleep_for()

   ```C++
   #include <iostream>
   #include <thread>
   using namespace std;
   
   void func() {
       cout << "Son thread begin.\n";
       for (int i = 0; i < 10; i++) {
           cout << "task running " << i << endl;
           this_thread::sleep_for(500ms);
       }
       cout << "Son thread end.\n";
   }
   
   int main() {
       cout << "Ded thread begin.\n";
       thread myth(func);  // 创建即开始执行子线程
       myth.detach();  // 分离
       cout << "Ded thread end.\n";
       return 0;
   }
   ```

5. 硬件支持的最大线程数量

   ```c++
   std::thread::hardware_concurrency();
   ```



#### 2.1.1 通过函数指针

**thread(函数名)**

```C++
#include <iostream>
#include <thread>
using namespace std;

void func() {
    cout << "This is a son thread" << endl;
}

int main() {
    thread myth1(func);
    cout << "This is the ded thread\n";
    myth1.join();
    
    return 0;
}
```



#### 2.1.2 通过函数对象

`thread(func_obj_name)`

```C++
#include <iostream>
#include <thread>
using namespace std;

class Func {
public:
    void operator() () {
        cout << "This is a son thread\n";
        
        while(m < 100) {
            cout << "n = " << n << endl;
        }
    }
    
private:
    int &m;
};

int main() {
    int n = 0;
    cin >> n;
    Func f1;
    thread myth(f1);
    cout << "This is the ded tread\n";
    myth.detach();
    
    return 0;
}
```



#### 2.1.3 通过lambda表达式

```C++
#include <iostream>
#include <thread>
using namespace std;

int main() {
    auto mylamth = [] {
        cout << "This is a son thread\n";
        cout << "Son thread over\n";
    }
    
    thread mylamth1(mylamth);
    
    cout << "This is the ded thread\n";
    
    mylamth1.detach;
    return 0;
}
```



#### 2.1.4 通过对象成员函数

```c++
#include <iostream>
#include <thread>
using namespace std;

class MyThread {
public:
    string name = "Hello";

    void Main(int a) {
        printf("Son thread begin.\n");
        cout << "p.name = " << name << " " << a << endl;
        printf("Son thread end.\n");
    }
};

int main() {
    cout << "main thread begin.\n";
    MyThread MT1;
    thread myth(&MyThread::Main, &MT1, 5);
    // thread(函数地址, 类对象地址, 函数参数)   函数地址：&类名::函数名
    myth.join();
    cout << "main thread end.\n";
    return 0;
}
```

对象成员函数是这个类的所有对象公用这一个函数指针，所以传参传入函数指针时不使用`对象.成员函数`的方式，而使用`类名::成员函数, 对象指针`

thread构造传参时，第一个参数为对象的成员函数，第二个参数需要是对象的指针，因为在成员函数的运行中需要用到this指针



#### 2.1.5 把thread封装进类

```c++
// 把thread封装进类

#include <iostream>
#include <thread>

class MyThread {
public:
    void start()
    {
        th = std::thread(&MyThread::Main, this);
    }

    virtual void Main() = 0;

private:
    std::thread th;
};

class ThreadTest : public MyThread {
public:
    std::string name;

    ThreadTest(std::string str = "Hello")
        : name(str)
    {
    }

    void Main()
    {
        std::cout << "Son thread begin.\n";
        std::cout << "My name is " << name << std::endl;
        std::cout << "Son thread end.\n";
    }
};

int main()
{
    ThreadTest test1("test thread 1");
    test1.start();
    system("pause");
    return 0;
}
/*
output；
	Son thread begin.
	My name is test thread 1
	Son thread end.
	Press any key to continue . . . 
*/
```

这里按键之后输出 `terminate called without an active exception` ，大概是因为没有选择join or detach导致的，可以在基类中再写一个wait函数实现 join

```C++
// 把thread封装进类

#include <iostream>
#include <thread>

class MyThread {
public:
    virtual void start();
    virtual void wait();
    virtual void noWait();
    virtual void Main() = 0;

private:
    std::thread th;
};
void MyThread::start(){
    th = std::thread(&MyThread::Main, this);
}
void MyThread::wait(){
    if (th.joinable())
        th.join();
}
void MyThread::noWait(){
    if (th.joinable())
        th.detach();
}

class ThreadTest : public MyThread {
public:
    std::string name;

    ThreadTest(std::string str = "Hello")
        : name(str)    {
    }

    void Main();
};
void ThreadTest::Main(){
    std::cout << "Son thread begin.\n";
    std::cout << "My name is " << name << std::endl;
    std::cout << "Son thread end.\n";
}

int main(){
    ThreadTest test1("test thread 1");
    test1.start();
    test1.noWait();
    system("pause");
    return 0;
}
```

这次的执行就没有再抛出错误

```c++
// 把thread封装进类

#include <iostream>
#include <thread>
using namespace std;

class MyThread {
public:
    virtual void start();
    virtual void wait();
    virtual void noWait();
    virtual void stop();
    virtual void Main() = 0;

protected:
    bool exit = false;
    std::thread th;
};
void MyThread::start(){
    th = std::thread(&MyThread::Main, this);
}
void MyThread::wait(){
    if (th.joinable())
        th.join();
}
void MyThread::noWait(){
    if (th.joinable())
        th.detach();
}
void MyThread::stop(){
    if (!exit)
        exit = !exit;
    cout << "Son thread exit.\n";
}

class ThreadTest : public MyThread {
public:
    std::string name;

    ThreadTest(std::string str = "Hello")
        : name(str)    {
    }
    void Main();
};
void ThreadTest::Main(){
    std::cout << "Son thread begin.\n";
    std::cout << "My name is " << name << std::endl;
    while (!exit) {
        std::this_thread::sleep_for(200ms);
        std::cout << "."
                  << " " << std::flush;
    }
    std::cout << "Son thread end.\n";
}

int main(){
    ThreadTest test1("test thread 1");
    test1.start();
    test1.noWait();
    this_thread::sleep_for(3s);
    test1.stop();
    return 0;
}
```



#### 2.1.6 std::call_once

只使用thread的情况下可以出现同一函数多次创建同一函数的线程，利用`call_once()`（在文件mutex中）可以实现函数只执行一次

```c++
#include <iostream>
#include <mutex>
#include <thread>

void SystemInit(){
    std::cout << "Call SystemInit\n";
}

void SystemInitOnce(){
    static std::once_flag flag; // 需要一个标志来标志是否已经执行过
    std::call_once(flag, SystemInit);
}

int main(){
    for (int i = 0; i < 3; i++) {
        SystemInitOnce();
    }

    return 0;
}
/*
output:
	Call SystemInit
*/ // 从输出上来看只执行了一次，创建线程也是一样的效果
```



#### 2.1.7 向线程函数传参

在thread构造函数中，第一个参数是可执行对象或函数的指针，第二个对象开始是线程函数的参数列表。在构造thread时，会把线程函数的参数列表拷贝一份到子线程。

##### 2.1.7.1 值传递

##### 2.1.7.2 引用传递

上面提到，thread构造时会把提供的参数列表拷贝一份到子线程。当提供的实参是一个变量时，即使形参是引用，但是拷贝到子线程中的仍是一个变量而非引用，在线程函数执行过程中改变的是拷贝到子线程中的那一份变量，主线程中的变量的值并没有改变。所以需要在传入实参时传入一个引用或`ref()`

```c++
void func03(std::string& s){
    std::cout << "From son thread: &s = " << &s << std::endl;
}

void test03(){
    std::string str = "Hello";
    std::cout << "From main: &s = " << &str << std::endl;
    std::thread myth(func03, ref(str));
    myth.join();
}

int main(){
    test03();
    return 0;
}
/*
output:
	From main: &s = 0x64fea0
	From son thread: &s = 0x64fea0
*/
```

##### 2.1.7.3 指针传递

指针传参即复制了一个地址相同的指针，即指针的值是一样的。

```c++
#include <iostream>
#include <thread>
using namespace std;

void func1(int x, int y) {
    printf("%d+%d=%d",x,y,x+y);
}

void func2(int &l, string *m) {  // 线程函数的引用类型参数只能是常引用
    printf("This is thread_%d, thread_name is %s", l, *m);
}

class func3 {
public:
    void operator() (int n) {
        cout << "This is thread_%d.\n";
    }
};

int main() {
    thread myth1(func1, 3, 10);  // 即thread构造函数的第一个参数为函数指针时，之后的参数即第一个参数指向的函数的参数列表
    int n = 2;
    thread myth2(func2, ref(n), string("myth2"));  // 但线程函数的参数是引用时需要告诉thread对象传入的是引用，使用ref来标记
    thread myth3(func, 3);  // 仿函数也一样的传参
    myth1.join();
    myth2.join();
    myth3.join();
    return 0;
}
```

##### 2.1.7.4 类对象参数

类对象作为参数也可以传到子进程

**注意**：类型转换

例如线程函数的形参是`string`，但是在thread构造时传入的实参是`char *`，这时拷贝到子线程中的是`char *`，然后再类型转换成`string`；但是，thread构造即开始执行，可能线程函数已经开始执行了类型转换还没有完成，从而出现一些不可意料的结果。

避免的方法：在传参时使用`string(s)`，用`char *s`构造出一个临时对象传入子线程

```c++
#include <iostream>
#include <thread>
using namespace std;

class Person {
public:
    Person() {
        cout << "Person::creat\n";
    }
    
    Person(const Person &p) {
        cout << "Person::copy\n";
    }
    
    ~Person() {
        cout << "Person::drop\n";
    }
};

void func(Person p) {
    printf("Son thread: thread_%d\n", this_thread::get_id());
}

int main() {
    Person p1;
    thread myth(func, p1);
    myth.join();
}

/*
output:
	Person::creat  ->  主线程中的对象的创建
	Person::copy  ->  创建子线程时的拷贝
	Person::drop  ->  子线程执行结束前的销毁
	Person::copy  ->  子线程执行结束后的回调的拷贝
	Person::drop  ->  子线程回调结束
	Person::drop  ->  主线程结束时的销毁
*/
```

##### 2.1.7.5 传参存在类型转换

当传参过程中存在类型转换 -> 传参的时机

```c++
void func04(const std::string& s){
    std::cout << "From func04: s = " << s << std::endl;
}

void test04(){
    char str[] = "Hello, World!";
    std::cout << "From main: s = " << str << std::endl;
    std::thread myth(func04, str);  // 1需要 char* 向 std::string 的类型转换
    myth.detach();
}

int main(){
    test04();
    return 0;
}
```

1处可能出现main线程已经结束了类型转换还没有完成的情况 -> 类型转换实际上是在子线程中完成的；怎样在主线程中完成类型转换？：在主线程传入时使用`std::string(str)。`

#### 2.1.8 所有权转移

##### 2.1.8.1变量所有权转移

提供的参数可以"移动"(move)，但不能"拷贝"(copy)。原始对象中的数据转移给另一对象，而转移的这些数据就不再在原始对象中保存。这一点可以通过`std::unique_ptr`来实现，但当原对象是一个命名对象，则转移需要使用`std::move`显示移动，将一个对台对象移动到一个线程中：

```c++
void process_big_object(std::unique_ptr<big_object>);
std::unique_ptr<big_object> p(new big_object);
p->prepare_data(42);
std::thread t(process_big_object,std::move(p));
```

在 `std::thread` 的构造函数中指定 `std::move(p)` ,big_object对象的所有权就被首先转移到新创建线程的的内部存储中，之后传递给`process_big_object`函数。

##### 2.1.8.2 线程所有权转移

`std::thread` 所有权可以在多个实例中互相转移，因为这些实例是可移动(movable)且不可复制(aren't copyable)。在同一时间点，就能保证只关联一个执行线程；同时，也允许程序员能在不同的对象之间转移所有权。

假设要写一个在后台启动线程的函数，想通过新线程返回的所有权去调用这个函数，而不是等待线程结束再去调用；或完全与之相反的想法：创建一个线程，并在函数中转移所有权，都必须要等待线程结束。总之，新线程的所有权都需要转移。

```c++
void some_function();
void some_other_function();
std::thread t1(some_function); // 1
std::thread t2=std::move(t1); // 2 将t1关联的线程的所有权转移给t2
t1=std::thread(some_other_function); // 3
std::thread t3; // 4
t3=std::move(t2); // 5 将t2关联的额线程的所有权转移给t3
t1=std::move(t3); // 6 试图将t3管理的线程转移给t1，但是t1已心有所属，赋值操作将使程序崩溃
```

`std::thread` 支持移动，线程的所有权可以在函数外进行转移

```c++
std::thread f(){
void some_function();
return std::thread(some_function);
}
std::thread g(){
void some_other_function(int);
std::thread t(some_other_function,42);
return t;
}
```

当所有权可以在函数内部传递，就允许 `std::thread` 实例可作为参数进行传递

```c++
void f(std::thread t);
void g(){
void some_function();
f(std::thread(some_function));
std::thread t(some_function);
f(std::move(t));
}
```

支持移动，所以可以把一个线程转移给一个类管理，在这个类的析构函数中`join()`，这样可以确保线程程序退出前完成

```c++
class scoped_thread{
	std::thread t;
public:
	explicit scoped_thread(std::thread t_): // 1
		t(std::move(t_)){
		if(!t.joinable()) // 2
		throw std::logic_error(“No thread”);
	}
	~scoped_thread(){
		t.join(); // 3
	}
	scoped_thread(scoped_thread const&)=delete;
	scoped_thread& operator=(scoped_thread const&)=delete;
};
struct func; // 定义在清单2.1中
void f() {
int some_local_state;
scoped_thread t(std::thread(func(some_local_state))); // 4
do_something_in_current_thread();
} 
```



#### 2.1.9 问题避免

##### 2.1.9.1线程函数传参中的问题

thread创建的构造函数中会对所有的参数进行复制，线程函数中操作的对象都是复制后的变量。

```C++
#include <iostream>
#include <thread>
using namespace std;

void func(const int &x) {  // 引用传参时只形参只能是常引用，否则报错
    cout << "&x = " << &x << endl;
    // &x = 0xf31a7c
}

int main() {
    int n = 3;
    cout << "&n = " << &n << endl;
    // &n = 0x62feb8
    thread myth(func, 3);
    myth.detach();
    
    return 0;
}
```

以上用例中，通过引用传参的方式把n穿到子线程，但是在子线程中取地址发现两个变量的地址并不相同 —— 实际上是一个**值传递**，即便主线程先结束了子线程中在用到x也还是安全的

```C++
#include <iostream>
#include <thread>
using namespace std;

void func(int* x)
{
    cout << "x = " << x << endl;
    // x = 0x62feb8，指针在detach子线程中不安全
}

int main()
{
    int n = 3;
    cout << "&n = " << &n << endl;
    // &n = 0x62feb8
    thread myth(func, &n);
    myth.join();

    return 0;
}
```

这个用例中，以指针方式传参后发现x就是n的地址，即子线程中复制的这一个指针和传入的指针指向同一个地址，所以如果是detach而且指针指向的变量是局部变量，这将可能不安全。

```C++
#include <iostream>
#include <thread>
using namespace std;

class P {
public:
    string name;
};

void func(P *ptr) {
    this_thread::sleep(100ms);
    cout << "ptr->name = " << ptr->name << endl;
}

int main() {
    {
        P ptr;
        ptr.name = "class P::obj";
        thread myth(func, &ptr);
        myth.detach();
	}
    return 0;
}
/*
output:
	ptr->name =  // 这之后的ptr->name并没有成功执行，因为这个时候子线程中指针ptr指向的对象已经被销毁了
*/
```

尽量使用值传递，少使用地址传递



##### 2.1.9.2 空间提前释放问题

传入的**指针**变量指向的主线程局部变量被释放但子线程仍在运行且用到该指针，此时会出错

```c++
#include <iostream>
#include <thread>
using namespace std;

void func(int n) {
    cout << "Son_thread n begin.\n";
    for (int i = 0; i < 10; i++) {
        this_thread::sleep_for(500ms);
    }
    cout << "Son_thread end.\n";
}

int main() {
    cout << "Ded_thread begin.\n";
    {
        thread myth(func, 1);
    }
    // 栈区中的变量会在遇到大括号时释放，但是子线程需要五秒时间才能结束，即线程对象被销毁了但是子线程任然在运行——>出错
    {
        thread myth(func, 2);
        myth.detach();
    }
    // 此时，这个并不会报错，因为子线程和主线程分离了，相当于创建了后台守护线程，与子线程无关
    // 但是还有问题：主线程退出后子线程不一定退出
    cout << "Ded_thread end.\n";
    return 0;
}
```

解决方法：避免空间提前释放（锁、全局变量、堆区变量等）

普通类型变量引用传参：实际上是复制了变量

```C++
#include <iostream>
#include <thread>
using namespace std;
using namespace this_thread;

class Person {
public:
    Person() {
        cout << "Person::creat\n";
    }
    
    Person(const Person &p) {
        cout << "Person::copy\n";
    }
    
    ~Person() {
        cout << "Person::drop\n";
    }
};


void func(int& x)
{
    while (x++ < 5) {
        cout << "x = " << x << endl;
        sleep_for(500ms);
    }
}

int main()
{
    {
        int n = 0;
        thread myth(func, ref(n));
        myth.detach();
    }

    return 0;
}
// 输出正常
```

对象变量引用传参：复制了变量

```C++
#include <iostream>
#include <thread>
using namespace std;
using namespace this_thread;

class Person {
public:
    string name;

    Person()
    {
        cout << "Person::creat\n";
    }

    Person(const Person& p)
    {
        cout << "Person::copy\n";
    }

    ~Person()
    {
        cout << "Person::drop\n";
    }
};

void func(Person& p)
{
    sleep_for(200ms);
    cout << "p.name = " << p.name << endl;
}

int main()
{
    {
        Person p1;
        p1.name = "Hello";
        thread myth(func, ref(p1));
        myth.detach();
    }

    getchar();
    return 0;
}

// output:   // 正常输出
//	Person::creat
//	Person::drop
//	p.name = Hello
```

### 2.2 创建 n 个线程

可以实现批量的管理。

```c++
vector<thread> v;
for (int i = 1; i < n; i++) {
    v.push_back(thread(func, args));
}
for (auto &i : v) {
    i.join();
}
```

运行发现，线程的执行顺序并不一定和push_back()的顺序相同

### 2.3 线程数量

**`std::thread::hardware_concurrency()`**		返回能同时并发在一个程序中的线程数量。核系统中，返回值可以是CPU核芯的数量。返回0：系统信息可能无法获取。

将整体工作拆分成小任务交给每个线程去做，其中设置最小任务数，可以避免产生太多的线程。

```c++
template<typename Iterator,typename T>
struct accumulate_block{
	void operator()(Iterator first,Iterator last,T& result){
		result=std::accumulate(first,last,result);
	}
};

template<typename Iterator,typename T>
T parallel_accumulate(Iterator first,Iterator last,T init){
	unsigned long const length=std::distance(first,last);
	if(!length) // 1
		return init;
	unsigned long const min_per_thread=25;
	unsigned long const max_threads = (length+min_per_thread-1)/min_per_thread; // 2
	unsigned long const hardware_threads=std::thread::hardware_concurrency();
	unsigned long const num_threads= std::min(hardware_threads != 0 ? hardware_threads : 2, max_threads); // 3
	unsigned long const block_size=length/num_threads; // 4
	std::vector<T> results(num_threads);
	std::vector<std::thread> threads(num_threads-1); // 5
	Iterator block_start=first;
	for(unsigned long i=0; i < (num_threads-1); ++i) {
		Iterator block_end=block_start;
		std::advance(block_end,block_size); // 6
		threads[i]=std::thread( // 7
		accumulate_block<Iterator,T>(),
		block_start,block_end,std::ref(results[i]));
		block_start=block_end; // 8
	}
	accumulate_block<Iterator,T>()(
	block_start,last,results[num_threads-1]); // 9
	std::for_each(threads.begin(),threads.end(),
	std::mem_fn(&std::thread::join)); // 10
	return std::accumulate(results.begin(),results.end(),init); // 11
}
```

如果范围内多于一个元素时，都需要用范围内元素的总数量除以线程(块)中最小任务数，从而确定启动线程的最大数量，这样能避免无谓的计算资源的浪费。计算量的最大值和硬件支持线程数中，较小的值为启动线程的数量，因为上下文频繁的切换会降低线程的性能。

## 3 多线程通信和同步

### 3.1 多线程状态

#### 3.1.1 线程状态说明

- 初始化 (Init) :该线程正在被创建。

- 就绪(Ready)︰该线程在就绪列表中，等待CPU调度。

- 运行(Running) :该线程正在运行。

- 阻塞（Blocked)∶该线程被阻塞挂起。Blocked状态包括: pend(锁、事件、信号量等阻塞)、suspend (主动pend) . delay(延时阻塞)、pendtime(因为锁、事件、信号量时间等超时等待)。

- 退出(Exit) ︰该线程运行结束，等待父线程回收其控制块资源（不包含堆区资源）。

  ![image-20220717212857603](C:\Users\ewigk\AppData\Roaming\Typora\typora-user-images\image-20220717212857603.png)



## 4 数据共享

### 4.1 只读数据

```c++
vector<int> v { 1, 2, 3, 5 };

void v_print() {	// 函数中并没有对全局变量v进行改变
    for (const int &i : v) {
        cout << i << " ";
    }
    cout << endl;
}

int main() {
    cout << "Hello, World!\n";
    vector<thread> v1;
    for (int i = 0; i < 10; i++) {
        v1.push_back(thread(v_print));
    }
    for (auto &i : v1) {
        i.join();
    }
    return 0;
}
// 这段代码是没有问题的，因为线程函数中并没有对全局变量进行任何写操作
```

### 4.2 读写

- 只读的数据是安全的稳定的，不需要特别的处理手段，直接读就可以
- 但是有读有写的情况也是很常见的：2个线程写，8个线程读，如果没有特别的处理，那么程序肯定是会崩溃的。（我还没有写完你给删了，你删了我还得继续写但是往哪写？）
- 写的步骤比较多时，由于任务的切换，导致各种诡异的事情发生
- 最简单的处理：读的时候不能写，写的时候不能读。两个线程不能同时写 -> 保护共享数据：操作数据时把共享数据锁住，其他需要操作共享数据的线程需要等待解锁

### 4.3 互斥量

#### 4.3.1 std::mutex

- 一个类对象，可理解为锁
- 多个线程尝试用lock()成员函数加锁，只有一个线程能锁定成功（锁成功的标志：lock()函数返回），没有成功的线程就卡在lock()不断尝试加锁
- 保护数据，操作时用代码把共享数据锁住，其他想操作共享数据的线程必须排队
- 排队就增加了运行的时间，但是确保了数据的安全性

互斥量成员函数

- `lock()`、`unlock()`、`try_lock()`
- 先lock操作共享数据之后`unlock()`
- `lock()`、`unlock()`一定要成对使用
- `try_lock()`：尝试锁定互斥锁。立即返回。成功获取锁后，返回 `true` ，否则返回 `false` 。使用前提：此前没有`lock()`

```c++
#include <iostream>
#include <thread>
#include <list>
#include <mutex>

// Solution类功能：实现接收和读取命令队列
class Solution {
public:
    void inMsgQueue();
    void outMsgRecvQueue();
    bool outMsgQueue(int &cmd) {  // 代码比较简单所以使用内联函数
        if (!msgQueue.empty()) {
            cmd = msgQueue.front();
            msgQueue.pop_front();
            return 1;
        }
        return 0;
    }

private:
    std::list<int> msgQueue;
    std::mutex my_mut;
};
void Solution::inMsgQueue() {	// 有循环所以使用非内联
    for (int i = 1; i < 100000; i++) {
        my_mut.lock();
        msgQueue.push_back(i);
        std::cout << "inMsgQueue(): " << i << std::endl;
        my_mut.unlock();
    }
}
void Solution::outMsgRecvQueue() {
    int cmd = 0;

    for (int i = 0; i < 100000; i++) {
        my_mut.lock();
        bool result = outMsgQueue(cmd);
        my_mut.unlock();

        if (result) {
            std::cout << "outMsgQueue(): " << cmd << std::endl;
            // do something here
        }
        else {
            std::cout << "命令队列为空\n";
        }
    }

    std::cout << "end.\n-------------------------\n";
}

int main(int argc, char **argv) {
    Solution S1;
    std::thread myth1(Solution::inMsgQueue, &S1);
    std::thread myth2(Solution::outMsgRecvQueue, &S1);
    myth1.join();
    myth2.join();
    return 0;
}
```

```c++
void attempt_10k_increases()
{ 
	for (int i = 0; i<10000; ++i) 
	{
		if (mtx.try_lock())		// 加锁失败立即返回false，并不会阻塞
		{
			++counter;
			mtx.unlock(); 
		} 
        //mtx.lock();
        //++counter;
		//mtx.unlock(); 
	}
}
```

 但是对于开发者，保证lock和unlock的成对是有一定难度的——>于是引入了std::lock_guard：会自己unlock

#### 4.3.2 std::lock_guard

- 自动`lock()`、`unlock()`
- 直接取代`lock()`、`unlock()`，即使用`lock_guard`后不能再使用`lock()`、`unlock()`

使用方法：在需要lock的地方用`std::lock_guard<std::mutex> guar1(mutex_name)`

```c++
#include <iostream>
#include <thread>
#include <list>
#include <mutex>

// Solution类功能：实现接收和读取命令队列
class Solution {
public:
    void inMsgQueue();
    void outMsgRecvQueue();
    bool outMsgQueue(int &cmd) {  // 代码比较简单所以使用内联函数
        if (!msgQueue.empty()) {
            cmd = msgQueue.front();
            msgQueue.pop_front();
            return 1;
        }
        return 0;
    }

private:
    std::list<int> msgQueue;
    std::mutex my_mut;
};
void Solution::inMsgQueue() {	// 有循环所以使用非内联
    for (int i = 1; i < 100000; i++) {
        std::lock_guard<std::mutex> guard1(my_mut);  // 在需要lock的地方用std::lock_guard<std::mutex> guar1(mutex_name)
        //my_mut.lock();
        msgQueue.push_back(i);
        std::cout << "inMsgQueue(): " << i << std::endl;
        //my_mut.unlock();
    }
}
void Solution::outMsgRecvQueue() {
    int cmd = 0;

    for (int i = 0; i < 100000; i++) {
        my_mut.lock();
        bool result = outMsgQueue(cmd);
        my_mut.unlock();

        if (result) {
            std::cout << "outMsgQueue(): " << cmd << std::endl;
            // do something here
        }
        else {
            std::cout << "命令队列为空\n";
        }
    }

    std::cout << "end.\n-------------------------\n";
}

int main(int argc, char **argv) {
    Solution S1;
    std::thread myth1(Solution::inMsgQueue, &S1);
    std::thread myth2(Solution::outMsgRecvQueue, &S1);
    myth1.join();
    myth2.join();
    return 0;
}
```

原理：

`lock_guard`对锁的管理还是基于mutex的。在`std::lock_guard guard1`的构造函数中，传入了参数mutex my_mut，即在`lock_guar`d构造函数中执行了`my_mut.lock()`，guard1是一个栈区局部变量，函数返回后会自动析构，在析构函数中调用了`my_mut.unlock()。`

但是，使用`lock_guard`其实并不是很灵活，并不能随时解锁，而且这样锁住的时间可能会比较长而影响到整体执行的效率。解决方法：

- 把lock_guard放在作用域 {} 里面，当运行到 } 时即执行析构函数解锁。

  ```c++
  class func {
  public:
      std::mutex my_mut;
      void operator() (std::vactor<int> &v) {
          // do_something_here
          {
              std::lock_guard<std::mutex> my_guard(my_mut);
              // do_something
          }
          // do_some_thing
      }
  }
  ```



#### 4.3.3 死锁

- 假设两个线程A、B；两个互斥量金锁、银锁，
- 线程A执行时锁住了金锁，接下来要去锁银锁，但是
- 此时因为线程数量多于系统硬件支持的线程数量，出现了上下文切换，B线程执行
- B线程先锁了银锁，然后要去锁金锁
- 上文提到一个锁不能重复lock或者重复unlock
- 所以A线程等待B线程解银锁，B线程等待A线程解金锁
- ——死锁

死锁解决方法：

- 保证两个互斥量的加锁顺序相同即不会出现死锁的情况

避免死锁：

- 避免嵌套锁：

  一个线程已获得一个锁时，再别去获取第二个，因为每个线程只持有一个锁，锁上就不会产生死锁；当需要获取多个锁，使用一个 std::lock 来做

- 避免在持有锁时调用用户提供的代码

- 使用固定顺序获取锁

- 使用锁的层次结构

##### 4.3.3.1 std::lock() 函数模板

- 可以一次锁住两个或者两个以上的互斥量
- 不存在因为锁的顺序引起的死锁的问题
- 只要有一个互斥量没有锁住，`std::lock()` 就会等待全部解锁
- 即所有互斥量互斥量不会出现有的锁了有的没锁的情况
- 要么两个互斥里都锁住，要么两个互斥量都没锁住。如果只锁了一个，另外一个没锁成功，则它立即把已经锁住的解锁。

```c++
std::lock(my_mut1, my_mut2);  // 两个都锁住

my_mut1.unlock();
my_mut2.unlock();	// 需要分别unlock()
```

可以使用`lock_guard`来自动解锁。但是与之前不一样的是，这里lock_guard管理的是已经被加锁的互斥量，需要用**`std::adopt_lock`**来表示“领养”了一个已经加锁的互斥量。

```c++
std::lock(my_mut1, my_mut2);
std::lock_guard<std::mutex> guard1(my_mut1, std::adopt_lock), guard2(my_mut2, std::adopt_lock);
// Do-Something

// 相当于lock_guard对象领养（adopt）了lock，自己不再需要lock
```

##### 4.3.3.2 std::mutex::try_lock()

尝试锁定互斥锁。立即返回。成功获取锁后，返回 `true` ，否则返回 `false` 。

- 使用前提：此mutex没有拥有线程调用，即此前不能已经加锁，否则行为未定义
- 使用场景：避免死锁和类似死锁的情况

#### 4.3.4 unique_lock

灵活的锁

- `std::unqiue_lock` 使用更为自由的不变量，这样 `std::unique_lock` 实例不会总与互斥量的数据类型相关，使用起来要比 `std:lock_guard` 更加灵活，但是相应需要消耗更多内存且执行的速度稍慢。

```c++
std::lock_guard<std::mutex> my_guard(my_mut1);
std::unique_lock<std::mutex> my_guard1(my_mut2);	// 这种使用方法几乎和lock_guard相同
```

`std::unique_lock`构造的其他参数：和std::lock_guard支持标记一样，`std::unique_lock`也支持一些标记

##### 4.3.4.1 标记参数

- `std::adopt_lock`：**“领养”一个已经加锁的互斥量**

  前提：使用之前已经lock

- 其他类似死锁的情况：

  A线程上锁了但是没有执行而是执行了`sleep_for()`，在线程A sleep的这段时间里，B线程不能上锁就“堵住”了。

- `std::defer_lock`：表明互斥量应保持解锁状态，即不获得互斥的所有权，**构造时没有上锁**。这样，就可以被 `std::unique_lock` 对象(不是互斥量)的`lock()`函数的所获取，或传递 `std::unique_lock` 对象到 `std::lock()` 中。

  ```c++
  void swap(X& lhs, X& rhs) {
  	if(&lhs==&rhs)
  		return;
  	std::unique_lock<std::mutex> lock_a(lhs.m,std::defer_lock); // 1
  	std::unique_lock<std::mutex> lock_b(rhs.m,std::defer_lock); // 1 std::def_lock 留下未上锁的互斥量
  	std::lock(lock_a,lock_b); // 2 互斥量在这里上锁；但是上锁之后不需要手动解锁，因为unique_lock自己会管理
  	swap(lhs.some_detail,rhs.some_detail);
  }
  ```

- `std::try_to_lock`：尝试使用mutex的`lock()`去锁定mutex，但如果没有锁成功也会立即返回`false`，并不会阻塞。

  前提：线程不能自己先去lock。功能类似于`std::try_lock(std::mutex &)`

  **`std::unique_lock::owns_lock()`**：是否拥有特定的互斥量，即是否已经加锁；如果实例拥有互斥量，那么析构函数必须调用`unlock()`；但当实例中没有互斥量时，析构函数就不能去调用`unlock()`

  ```c++
  std::unique_lock<std::mutex> guard1(my_mut1, std::try_to_lock);
  if (guar1.owns_lock()) {
      msgQueue.push_back(i);
      // ..
  }
  else {
      cout << "inMsgQueue(): 没拿到锁，只能干点别的啥了" << i << std::endl;
  }
  // std::unique_lock<mutex>::owns_lock() // 返回unique_lock是否持有锁的所有权，即是否上锁
  ```

  

  ##### 4.3.4.2 成员函数

  - `lock()`：一般是构造函数中使用标记`defer_lock`的`unique_lock`对象才会用到
  
  - `unlock()`：用的时候比较少，因为unique析构时会自动解锁。一般是有一些非共享代码需要处理时才用；或者是函数中代码量比较多但是操作共享数据的部分只占一小部分时，提前解锁。是`unique_lock`的灵活性的体现之一。
  
    ```c++
    std::unique_lock<mutex> my_guard(my_mut1, std::defer_lock);
    my_guard1.lock();
    /*
    操作一些共享代码
    */
    my_guard.unlock();
    /*
    处理一些非共享
    */
    my_guard.lock();
    // 继续处理共享代码
    ```
  
    
  
  - `try_lock`：尝试加锁，失败则返回`false`，不阻塞
  
  - `release()`：返回所管理的`mutex`对象的指针，并释放所有权。注意和`unlock`的区别：一个是解锁，一个是抛弃。

##### 4.3.4.3 不同域中互斥量所有权的传递

`std::unique_lock` 实例没有与自身相关的互斥量，一个互斥量的所有权可以通过移动操作，在不同的实例中进行传递。

- 某些情况下，这种转移是自动发生的，例如:当函数返回一个实例；
- 另些情况下，需要显式的调用 std::move() 来执行移动操作。

注意：`std::unique_lock` 是可移动，但不可赋值的类型（有点像`std::unique_ptr`）

```c++
std::unique_lock<std::mutex> get_lock(){	// 函数get_lock()锁住了互斥量，然后准备数据，返回锁
	extern std::mutex some_mutex;
    std::unique_lock<std::mutex> lk(some_mutex);
	prepare_data();
	return lk; // 1	lk在函数中被声明为自动变量，它不需要调用 std::move() ，可以直接返回
}
void process_data() {
	std::unique_lock<std::mutex> lk(get_lock()); // 2
	do_something();
}
```

- std::unique_lock 的灵活性同样也允许实例在销毁之前放弃其拥有的锁。可以使用unlock()来做这件事，如同一个互斥std::unique_lock 的成员函数提供类似于锁定和解锁互斥量的功能。 

#### 4.3.5 锁的粒度

- 加锁粒度就是你要锁住的范围是多大。

- 比如你在家上卫生间，你只要锁住卫生间就可以了吧，不需要将整个家都锁起来不让家人进门吧，卫生间就是你的加锁粒度。

- 设计合理的锁粒度：

  其实卫生间并不只是用来上厕所的，还可以洗澡，洗手。这里就涉及到优化加锁粒度的问题。
  你在卫生间里洗澡，其实别人也可以同时去里面洗手，只要做到隔离起来就可以，如果马桶，浴缸，洗漱台都是隔开相对独立的，实际上卫生间可以同时给三个人使用；当然三个人做的事儿不能一样。这样就细化了加锁粒度，你在洗澡的时候只要关上浴室的门，别人还是可以进去洗手的。如果当初设计卫生间的时候没有将不同的功能区域划分隔离开，就不能实现卫生间资源的最大化使用。这就是设计架构的重要性。



## 5 单例设计模式

- 这是一种**保护共享数据的初始化过程**的方法

- 设计模式中使用较多的设计模式

- 单例：整个项目中，有某个或者某些特殊的类，这种类只能创建一个示例

  ```c++
  #include <iostream>
  
  class MyCs {
  private:
      MyCs() {};		// 禁用了外部直接构造的方式
      static MyCs *m_instance;    // 静态成员变量
  
  public:
      static MyCs *GetIstance() {		// 内部的函数调用构造函数返回对象指针
          if (m_instance == nullptr) {
              m_instance = new MyCs;
          }
          return m_instance;
      }
  
      ~MyCs() {
          if (MyCs::m_instance) {
              delete m_instance;
              m_instance = nullptr;
          }
      }
  
      void test01() {
          std::cout << "test01()\n";
      }
  };
  
  MyCs *MyCs::m_instance = nullptr;
  
  void func() {
      
  }
  
  int main() {
      MyCs *ptr_a = MyCs::GetIstance();   // 返回了一个MyCs类的指针
      MyCs *ptr_b = MyCs::GetIstance();   // 实际上在这一次执行时没有运行到这个函数的if块中，返回的指针的值和ptr_a是相同的
  
      std::cout << "ptr_a = " << ptr_a << std::endl;
      std::cout << "ptr_b = " << ptr_b << std::endl;  // 结果显示两个指针的值的相同的
  
      ptr_a->test01();
  
      return 0;
  }
  ```

- 以上代码的多线程中，我们可能会面临`GetInstance()`这种成员函数要互斥

  ```c++
  #include <iostream>
  #include <thread>
  #include <mutex>
  
  std::mutex res_mutex;
  
  class MyCs {
  private:
      MyCs() {};
      static MyCs *m_instance;    // 静态成员变量
  
  public:
      static MyCs *GetIstance() {
          std::unique_lock<std::mutex> my_mutex(res_mutex);
          if (m_instance == nullptr) {
              m_instance = new MyCs;
          }
          return m_instance;
      }
  
      ~MyCs() {
          if (MyCs::m_instance) {
              delete m_instance;
              m_instance = nullptr;
          }
      }
  
      void test01() {
          std::cout << "test01()\n";
      }
  };
  
  MyCs *MyCs::m_instance = nullptr;
  
  void func() {
      printf("thread_%d begin.\n", std::this_thread::get_id());
      MyCs *ptr = MyCs::GetIstance();
      ptr->test01();
      printf("thread_%d end.\n", std::this_thread::get_id());
  }
  
  int main() {
      std::thread myth1(func);
      std::thread myth2(func);
      myth1.join();
      myth2.join();
  
      return 0;
  }
  ```

- 但是这样做还是有问题

  为初始化的时候加锁，实际上在很大很多用户的项目中（实际线程数量明显多于系统支持的最大线程数量，会发生线程之间的切换即上下文切换），效率是比较低的。

  ```c++
  static MyCs *GetIstance() {
      // 双重检查
      if (m_instance != nullptr) {
          std::unique_lock<std::mutex> my_mutex(res_mutex);
          if (m_instance == nullptr) {
              m_instance = new MyCs;
          }
          return m_instance;
      }
  }
  ```
  
  将”构造“函数改成这样之后能够提高效率：
  
  ​		使用双重检查之前，是先给上锁了之后再判断是否返回`new MyCs`，使用双重检查之后，在第一次检查通过时才上锁，第一次检查没有通过则不加锁，则只有单例类第一次构造时会上锁，其他不上锁 -> 从而提高效率。
  
- **`std::call_once`**见**2.1.6**

  保证函数只被调用一次

  具备互斥量的能力，而且效率高，消耗资源少

  使用时，需要和结构`std::once_flag`配合使用，`call_once`能记录函数是否执行

  ```c++
  #include <iostream>
  #include <mutex>
  #include <thread>
  
  void SystemInit(){
      std::cout << "Call SystemInit\n";
  }
  
  void SystemInitOnce(){
      static std::once_flag flag; // 需要一个标志来标志是否已经执行过
      std::call_once(flag, SystemInit);
  }
  
  int main(){
      for (int i = 0; i < 3; i++) {
          SystemInitOnce();
      }
  
      return 0;
  }
  /*
  output:
  	Call SystemInit
  */ // 从输出上来看只执行了一次，创建线程也是一样的效果
  ```



## 6 条件变量

### 6.1 `std::condition_variable` 

头文件：condition_variable

- 功能（概）：

  线程A：等待一个条件满足

  线程B：专门往消息队列汇中扔消息（数据）

  线程A获得一个B中的消息后不再等待，继续执行

- `std::ondition_variable`

  是一个类，与条件相关，即等待一个条件达成。

  需要和互斥量配合使用，用时需要生成此类的实例

- 成员函数

  `std::wait`

  `std::notify_one`：“唤醒”一个线程

- 功能（详）
  
  `wait()`：`.wait(锁对象, 可调用对象)`

  如果第二个参数的可调用对象的返回值是`false`，`.wait()`将解锁互斥量（这样其他线程就可以操作共享代码），并堵塞到本行；直到某个线程调用同一条件变量对象的`.notify_one()`成员函数为止，然后又上锁，再检查第二个参数的返回值，为`false`则重复以上操作，为`true`则继续操作。
  
  第二个参数返回`true`时立即返回。
  
  如果没有第二个参数，即`.wait(互斥量对象)`，则和第二个参数返回`false`的情况相同，不同点只在于唤醒之后不需要再检查。
  
  ```c++
  #include <iostream>
  #include <thread>
  #include <list>
  #include <mutex>
  #include <condition_variable>
  
  // Solution类功能：实现接收和读取命令队列
  class Solution {
  public:
      void inMsgQueue();
      void outMsgRecvQueue();
      bool outMsgQueue(int &cmd) {  // 代码比较简单所以使用内联函数
          if (!msgQueue.empty()) {
              cmd = msgQueue.front();
              msgQueue.pop_front();
              return 1;
          }
          return 0;
      }
  
  private:
      std::list<int> msgQueue;
      std::mutex my_mut;
      std::condition_variable my_cond;
  };
  void Solution::inMsgQueue() {	// 有循环所以使用非内联
      for (int i = 1; i < 100000; i++) {
          std::unique_lock<std::mutex> guard1(my_mut);  // 在需要lock的地方用std::unique_lock<std::mutex> guar1(mutex_name)
          //my_mut.lock();
          msgQueue.push_back(i);
          my_cond.notify_one();   // 将condition_variable唤醒
          guard1.unlock();
          // 当outRecvMsgQueue正在处理其他事务而不是卡在my_cond.wait()，这一次唤醒或许没有啥效果
          std::cout << "inMsgQueue(): " << i << std::endl;
          //my_mut.unlock();
      }
  }
  void Solution::outMsgRecvQueue() {
      int cmd = 0;
  
      for (int i = 0; i < 100000; i++) {
          std::unique_lock<std::mutex> guard2(my_mut);
  
          my_cond.wait(guard2, [this] {
              if (msgQueue.empty()) {
                  return false;
              }
              return true;
              });
  
          bool result = outMsgQueue(cmd);
          guard2.unlock();
          std::cout << "outMsgQueue(): " << cmd << std::endl;
      }
  
      std::cout << "end.\n-------------------------\n";
  }
  
  int main(int argc, char **argv) {
      Solution S1;
      std::thread myth1(Solution::inMsgQueue, &S1);
      std::thread myth2(Solution::outMsgRecvQueue, &S1);
      myth1.join();
      myth2.join();
      return 0;
  }
  ```

### 6.4 `std::notify_all`

唤醒其他的所有线程，但是只有一个能拿到互斥量的调度，即只有一个线程能运行下去。



## 7 异步

### 7.1 `std::async`、`std::futrue`

头文件：`<future>`

功能：获得线程返回的结果

- `std::async()`：一个函数模板，用来启动一个异步任务，返回一个`std::future`对象
- 启动一个异步任务：自动创建一个线程并开始执行对应的入口函数，返回一个`std::future`对象
- `std::future`：一个类模板，其实例中含有线程入口函数所返回的结果，`.get()`可获取其中含有的结果

获取结果的方式不止有这种方式，还可以在传参到线程入口时传入一个用来接收结果的引用或指针

`std::future`：有人认为`std::future`提供了一种访问异步操作结果的机制。

使用方法：

- `future`

  声明与定义：`std::future<int（线程函数返回值类型）> result = std::async(myThread, args);`创建线程并绑定关系

- 获取其中包含的值：

  `resualt.get()`，返回的其中包含的值。

```c++
#include <iostream>
#include <thread>
#include <future>

int myThread() {
    printf("thread_%d begin.\n", std::this_thread::get_id());
    std::this_thread::sleep_for(std::chrono::milliseconds(3000));
    printf("thread_%d end.\n", std::this_thread::get_id());
    return 3;
}

int main(int argc, char **argv) {
    printf("main_thread begin.\n");
    std::future<int> result = std::async(myThread);
    printf("continue...\n");
    printf("result = %d\n", resualt.get());
    printf("main_thread end.\n");

    return 0;
}
/*
    main_thread begin.
    continue...
    thread_2 begin.
    thread_2 end.
    resualt = 3
    main_thread end.
*/
```

note：

​		Future——将来，这个值在定义时并没有获得线程的返回值，等待到线程函数执行结束之后才能得到结果，即将来的某个时刻。当main运行到`result.get()`时会卡在这一行等待线程执行结束之后才继续执行（当然了，如果已经结束了的话就不用等啦）。另外，`.get()`只能调用一次，不然会报错。

虽然这里实现了`join()`的功能但是最好还是显式地使用join()或者detach()，不然可能会报错：“在没有活动异常的情况下终止调用”（terminate without an active exception）(没有活动异常，看起来好像问题不大)

`std::future::wait()`：等待，但是不拿到值。

#### 7.1.1 `std::async()`的额外参数

可以通过额外向`async()`传递`std::launch`类型（枚举类型），来达到特殊的效果

- `std::launch::deferred`：表示线程入口函数被延迟到使用`std::future::wait()`或者`std::future::get()`时才执行

  如果没有用`std::future::wait()`或者`std::future::get()`，则直接都没有新线程创建出来。

  使用方法：`std::future<线程函数返回值类型> result = std::async(std::launch::defderred, 线程函数指针, args)`

  ```c++
  #include <iostream>
  #include <thread>
  #include <future>
  
  int myThread(int n) {
      printf("son thread_%d begin.\n", std::this_thread::get_id());
  
      int len = 0;
      while (n) {
          n /= 10;
          len++;
      }
  
      printf("son thread_%d end.\n", std::this_thread::get_id());
      return len;
  }
  
  int main() {
      printf("main thread_%d begin.\n", std::this_thread::get_id());
  
      std::future<int> result = std::async(std::launch::deferred, myThread, 2000);
      printf("continue……\n");
      printf("intLen(2000) = %d\n", result.get());
  
      printf("main thread_%d end.\n", std::this_thread::get_id());
      return 0;
  }
  /*
  main thread_1 begin.
  continue……
  son thread_1 begin.
  son thread_1 end.
  intLen(2000) = 4
  main thread_1 end.
  */
  ```

  在以上代码的执行结果中我们可以看到：主线程和“子线程”的ID相同 → 实际上并没有创建线程，还是在主线程中执行的代码

- `std::launch::async`：和`deferred`正好相反，调用`async`即创建线程开始执行。（用和不用的效果是一样的，相当于是一个默认值）

#### 7.1.2 `std::packaged_task`

打包任务

一个类模板，模板参数是各种可调用对象；通过`std::packaged_task`可以把各种可调用对象包装起来，方便将来调用

```c++
#include <iostream>
#include <thread>
#include <future>

int myThread(int n) {
    printf("son thread_%d begin.\n", std::this_thread::get_id());

    int len = 0;
    while (n) {
        n /= 10;
        len++;
    }

    printf("son thread_%d end.\n", std::this_thread::get_id());
    return len;
}

int main() {
    printf("main thread_%d begin.\n", std::this_thread::get_id());

    std::packaged_task<int(int)> myPack(myThread);	// 包装起来
    std::thread t1(std::ref(myPack), 100);	// 这里的“1”是作为包装起来的线程函数的参数
    std::future<int> result = myPack.get_future();	// result 保存线程函数的返回结果
	printf("result = %d\n", result.get());
    printf("main thread_%d end.\n", std::this_thread::get_id());
    return 0;
}
```

- 当然也能包装lambda表达式（只要是可调用对象就OK，其他的就不再展示了）

  ```c++
  #include <iostream>
  #include <future>
  
  int main() {
      printf("main thread_%d begin.\n", std::this_thread::get_id());
  
      std::packaged_task<int(int)> myPack([](int num) -> int {
          printf("son thread_%d begin.\n", std::this_thread::get_id());
          int len = 0;
          while (num) {
              num /= 10;
              len++;
          }
          printf("son thread_%d end.\n", std::this_thread::get_id());
          return len;
          });	// 包装起来
      std::thread t1(std::ref(myPack), 100);	// 这里的“1”是作为包装起来的线程函数的参数
      std::future<int> result = myPack.get_future();	// result 保存线程函数的返回结果
      printf("result = %d\n", result.get());
      printf("main thread_%d end.\n", std::this_thread::get_id());
      return 0;
  }
  /*
  main thread_1 begin.
  son thread_2 begin.
  son thread_2 end.
  result = 3
  main thread_1 end.
  */
  ```

- 另外，`std::packaged_task`还能直接调用，仍然需要用一个期望来获得其结果

  ```c++
  #include <iostream>
  #include <future>
  
  int main() {
      printf("main thread_%d begin.\n", std::this_thread::get_id());
  
      std::packaged_task<int(int)> myPack([](int num) -> int {
          printf("son thread_%d begin.\n", std::this_thread::get_id());
          int len = 0;
          while (num) {
              num /= 10;
              len++;
          }
          printf("son thread_%d end.\n", std::this_thread::get_id());
          return len;
          });	// 包装起来
      // std::thread t1(std::ref(myPack), 100);	// 这里的“1”是作为包装起来的线程函数的参数
      myPack(1000);
      std::future<int> result = myPack.get_future();	// result 保存线程函数的返回结果
      printf("result = %d\n", result.get());
      printf("main thread_%d end.\n", std::this_thread::get_id());
      return 0;
  }
  /*
  main thread_1 begin.
  son thread_1 begin.
  son thread_1 end.
  result = 4
  main thread_1 end.
  */
  ```

  但是输出的结果就不太一样了。输出显示是在同一个线程中运行的，没有创建新的线程，在`result.get()`这一行当然就不会堵住了

#### 7.1.3 `std::promise`

类模板。功能：能够在某个线程中给它赋值，然后可以在其他线程中读取这个值。

常用成员函数

- 构造：`std::promise<T> pro_name`
- `.set_value(date)`：对其中保存的值赋值
- `.get_future()`：返回一个`std::future<T>`对象（绑定而非赋值？），可以通过这个期望对象获取承诺对象中存储的值

```c++
#include <iostream>
#include <thread>
#include <future>

bool isPrime(int n) {
    for (int i = 2; i < n / 2; i++) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

// 返回小于等于给定非负整数的所有质数的和
void myThread(std::promise<unsigned int> &my_pro, unsigned int num) {
    printf("thread_%d begin.\n", std::this_thread::get_id());
    unsigned int result = 0;

    // 一系列复杂的操作
    for (int i = 2; i <= num; i++) {
        std::cout << "running.....\n";
        if (isPrime(i))
            result += i;
    }

    // 保存结果到promise对象中
    my_pro.set_value(result);
    printf("thread_%d end.\n", std::this_thread::get_id());
}

int main() {
    printf("main_thread_%d begin.\n", std::this_thread::get_id());
    std::promise<unsigned int> my_pro;
    std::thread t1(myThread, std::ref(my_pro), 10000);

    // 获取结果值，future对象绑定promise来获取值
    std::future<unsigned int> my_result = my_pro.get_future();
    t1.join();
    unsigned int result = my_result.get();
    std::cout << "result = " << result << std::endl;

    printf("main_thread_%d end.\n", std::this_thread::get_id());
    return 0;
}
```

通过promise对象保存一个值，在将来用future对象绑定这个promise对象，从而获取其中保存的值

#### 7.1.4 `std::future`成员函数

- `.wait()`：等待执行完毕

  `.wait_for()`：等待参数给定的时间段

  `.wait_until()`：等待直到给定的时间点

  如果在指定的超时时间内不可用,则返回。接收一个`std::chrono::duration`（时间）类型的参数，返回一个`std::future_status`（枚举类型）的值。

  ```c++
  enum class future_status {
      ready,	// 共享状态（wait_for()返回此值即执行完成，已就绪）
      timeout,	// 在指定的超时时间过去之前,共享状态没有准备好。(wait_for()规定时间内没有执行完成)
      deferred	// 共享状态包含一个递延函数,因此只有在明确请求时才会计算结果。延迟了，请求了才开始执行
  };
  ```

  ```c++
  // 判断是否是质数
  bool isPrime(int n) {
      for (int i = 2; i < n / 2; i++) {
          if (n % i == 0) {
              return false;
          }
      }
      return true;
  }
  
  // 返回小于等于给定非负整数的所有质数的和
  void myThread(std::promise<unsigned int> &my_pro, unsigned int num) {
      printf("thread_%d begin.\n", std::this_thread::get_id());
      unsigned int result = 0;
  
      // 一系列复杂的操作
      for (int i = 2; i <= num; i++) {
          std::cout << "running.....\n";
          if (isPrime(i))
              result += i;
      }
      std::this_thread::sleep_for(std::chrono::seconds(5));
      // 再来五秒
  
      // 保存结果到promise对象中
      my_pro.set_value(result);
      printf("thread_%d end.\n", std::this_thread::get_id());
  }
  
  int main() {
      printf("main_thread_%d begin.\n", std::this_thread::get_id());
  
      // 获取结果值，future对象绑定promise来获取值
      std::future<unsigned int> my_result = std::async(myThread, 10000);
      std::cout << "continue...\n";
      
      std::future_status stat(my_result.wait_for(std::chrono::seconds::(1));	// wait for 1 second	
  	if (stat == std::future::timeout) {	// 超时，线程还没有执行完成
          printf("超时，线程还没有执行完\n");
      }
  	else if (stat == std::future::ready) {	// 期望就绪，线程返回
          printf("线程执行完毕，返回\n");
      }
  	else {
          // deferred，仍处于延迟执行的状态，还没有开始执行
          // get()或wait()行延迟执行，不用get()或者wait()则不执行。
          // future对象构造使使用std::launch::deferred则会返回deferred
      }
      printf("main_thread_%d end.\n", std::this_thread::get_id());
      return 0;
  }
  ```

- `.valid()`：是否可用，检查期望是否有共享状态。

  仅对于不是默认构造或未从其转移（即由 `std::promise::get_future()` ， `std::packaged_task::get_future()` 或 `std::async()` ）的期货才是这种情况时间 `get()` 或 `share()` 被调用。

  如果在未引用共享状态的 `future `调用除析构函数，移动分配运算符或 `valid` 成员以外的任何成员函数，则行为未定义（尽管在这种情况下，鼓励实现抛出 `std::future_error` 指示 `no_state` ） 。从 `valid()` 为 `false` 的将来对象移出是有效的。



#### 7.1.5 `std::shared_future`

功能：实现多个线程的等待

- `std::future`只支持移动而不支持拷贝，`std::future` 模型独享同步结果的所有权，并且在第一次调用get()后，就没有值可以再获取了。所以当多线程在没有额外同步的情况下，访问一个独立的 std::future 对象时，就会有数据竞争和未定义的行为。
- `std::shared_future` 实例是可拷贝的，所以多个对象可以引用同一关联“期望”的结果。
- 但光是这样在每一个 `std::shared_future` 的独立对象上成员函数调用返回的结果还是不同步的，所以为了在多个线程访问一个独立对象时，避免数据竞争，必须使用锁来对访问进行保护。
- 优先使用的办法：为了替代只有一个拷贝对象的情况，可以让每个线程都拥有自己对应的拷贝对象。

![image-20220729024746467](C:\Users\ewigk\AppData\Roaming\Typora\typora-user-images\image-20220729024746467.png)

`std::shared_future` 的实例同步 `std::future` 实例的状态。当 `std::future` 对象没有与其他对象共享同步状态所有权，那么所有权必须使用 `std::move` 将所有权**传递**到 `std::shared_future` ：

```c++
std::promise<int> p;
std::future<int> f(p.get_future());
assert(f.valid()); // 1 "期望" f 是合法的
std::shared_future<int> sf(std::move(f));
assert(!f.valid()); // 2 "期望" f 现在是无效的
assert(sf.valid()); // 3 sf 现在是有效的
```

转移所有权也可以直接从`std::promise::git_future()`（隐式移动语义）：

```c++
std::promise<std::string> p;
std::shared_future<std::string> sf(p.get_future()); // 1 隐式转移所有权
```

`std::futrue::share()`：返回一个`std::share_future`对象，并且可以直接转移“期望”的所有权

```c++
std::promise< std::map< SomeIndexType, SomeDataType, SomeComparator, SomeAllocator>::iterator> p;
auto sf=p.get_future().share();
```

### 7.2 std::async 再探

虽然说async能够创建一个线程，但是我们叫他异步任务，因为它有时并没有创建线程，比如使用`std::launch::deferred`时，执行时还是在主线程中执行的。

- `std::launch::async`：和`deferred`正好相反，调用`async`即创建线程开始执行。（用和不用的效果是一样的，相当于是一个默认值）

- `std::launch::async`、`std::launch::deferred`一起使用

  `std::launch::async | std::launch::deferred` ：两者选其一，系统决定选择哪一个

- 不带额外参数

  默认使用了`std::launch::async | std::launch::deferred`，系统自行决定使用异步（新线程）还是同步（不创建新线程）方式运行。

- `std::thread` 和 `std::async`区别：

  `std::thread`创建线程，如果系统资源进场，创建线程失败，则整个程序就会报错崩溃。而且得到返回值的方式也不是很方便。

  `std::async`创建异步任务，取线程返回值的方式也比较方便。如果系统资源紧张导致无法创建新线程时，`std::async` 不加额外参数的方式就不会创建新的线程，而在调用 `.get()` 的线程中执行，所以不会报错

- 一般情况：线程数量不宜超过200

## 8 原子操作

原子操作应用范围：

- 互斥量：多线程编程中保护共享数据，锁 → 操作共享数据 → 开锁

- 两个线程对一个变量进行操作，比如一个只是读取值，另一个只是写值

  ```c++
  // main() 中定义共享变量
  datatype data = value;
  // 读取线程
  datatype val = data;`
  // 写线程
  data = new_velue;
  ```

- C++中的一条语句可能对应多条汇编语句，在读取线程执行时，读取到一半，上下文切换到写线程了，写线程执行完之后右返回到读取线程，这时读取线程读取熬的值可能与预期中的结果有一定的差距。可能读取旧值读取到一半，切换到了写值线程，写值完成之后又回到读取线程，读取线程又继续从被打断的地方读取，则最终读取到的结果是旧值一半和新值一半的组合。当然了，两个线程都是又读又写的情况也会遇到这样的情况。

  ```c++
  #include <iostream>
  #include <thread>
  #include <ctime>
  
  int my_count = 0;
  
  void myThread() {
      for (int i = 0; i < 10000000; i++) {
          my_count++;
      }
  }
  
  int main() {
      time_t start_time = clock();
      
      std::thread t1(myThread);
      std::thread t2(myThread);
      t1.join();
      t2.join();
      std::cout << my_count << std::endl;
      
      time_t end_time = clock();
      printf("消耗时间：%fs\n", static_cast<float>(end_time - start_time) / CLOCKS_PER_SEC);
      return 0;
  }
  /*
  开始运行...
  10533005
  消耗时间：0.072076s
  */	// lightly 在线IDE
  ```
  
  这里大概是因为出现了上述的错误，导致输出结果与预期有较大的出入
  
  ```c++
  #include <iostream>
  #include <ctime>
  #include <mutex>
  #include <thread>
  #include <atomic>
  
  int my_count(0);
  std::mutex my_mutex;
  
  void myThread() {
      for (int i = 0; i < 10000000; i++) {
          my_mutex.lock();
          my_count++;
          my_mutex.unlock();
      }
      return;
  }
  
  int main() {
      time_t start_time(clock());
      std::thread my_th1(myThread);
      std::thread my_th2(myThread);
      my_th1.join();
      my_th2.join();
      std::cout << my_count << std::endl;
      time_t end_time(clock());
      std::cout << "消耗时间：" << static_cast<double>(end_time - start_time) / CLOCKS_PER_SEC << "s\n";
      return 0;
  }
  /*
  开始运行...
  20000000
  消耗时间：2.44594s
  */	// lightly 在线IDE
  ```
  
- 原子操作：可以理解为一种不适用互斥量加锁技术的多线程并发编程方式

  在线程中不会打断的程序执行判断，执行的效率比互斥量技术更高。

- 互斥量与原子操作的比较

  互斥量的加锁解锁操作一般是对于一段代码的，而原子操作主要是对于一个变量，而非一段代码

- 原子操作：

  不可分割的操作，其状态只有**没有操作**或者**已经完成**，没有中间的状态

### 8.1 使用方法

- `std::stomic<T>`：类模板，封装一个 T 类型的变量，之后可以向操作 T 类型的变量一样操作构造出来的 atomic<T> 对象

- 构造函数：`std::stomic<T>obj(T date)`。可能也能够使用`std::stomic<T>obj = data`，之所以说“可能”是因为这应该是与编译器有关

  ```c++
  #include <iostream>
  #include <ctime>
  #include <thread>
  #include <mutex>
  
  std::atomic<unsigned int> my_count = 0;		// 封装一个unsigned int类型的变量为atomic
  
  void myThread() {
      for (int i = 0; i < 10000000; i++) {
          my_count++;		// 就把 my_count 当做 unsigned int 来使用就可。因为是一个原子对象，所以不会被打断
      }
      return ;
  }
  
  int main() {
      time_t start_time(clock());
      std::thread my_th1(myThread);
      std::thread my_th2(myThread);
      my_th1.join();
      my_th2.join();
      std::cout << my_count << std::endl;
      time_t end_time(clock());
      std::cout << "消耗时间：" << static_cast<double>(end_time - start_time) / CLOCKS_PER_SEC << "s\n";
      return 0;
  }
  /*
  开始运行...
  20000000
  消耗时间：0.489298s
  */	// lightly 在线IDE
  // 消耗时间远小于互斥锁的方法
  ```

- `std::atomic` 既不可复制也不可移动。

- `std::stomic`只支持在原子类型地址上的操作，设计其他地址的操作并不支持。比如++、--、+=、-=是支持的。当atomic_obj++改写为atomic_obj = atomic_obj + 1这些操作可能并不支持。所以原子类型一般用作计数

  ```c++
  #include <iostream>
  #include <ctime>
  #include <thread>
  #include <atomic>
  
  std::atomic<int> my_count(0);   // 封装一个unsigned int类型的变量为atomic
  
  void myThread() {
      for (int i = 0; i < 10000000; i++) {
          // my_count++;		// 就把 my_count 当做 unsigned int 来使用就可。因为是一个原子对象，所以不会被打断
          my_count = my_count + 1;
      }
      return;
  }
  
  int main() {
      time_t start_time(clock());
      std::thread my_th1(myThread);
      std::thread my_th2(myThread);
      my_th1.join();
      my_th2.join();
      std::cout << my_count << std::endl;
      time_t end_time(clock());
      std::cout << "消耗时间：" << static_cast<double>(end_time - start_time) / CLOCKS_PER_SEC << "s\n";
      return 0;
  }
  /*
  14527106
  消耗时间：0.739s
  */
  // 这个结果就和预期有比较大的出入
  ```
