**项目结构**

![image-20240326161347136](./images/image-20240326161347136.png)

**bean.xml内容**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="user" class="com.mvstudy.spring6.User"></bean>
</beans>
```

# IoC容器

Inversion of Control，使用IoC容器来管理所有Java对象的实例化和初始化，控制对象与对象之间的依赖关系。这是一种设计思想并非技术。

实现方法：依赖注入

![image-20240325162001059](./images/image-20240325162001059.png)

## BeanFactory容器

功能：为依赖注入（DI）提供支持。在资源宝贵的移动设备或者基于 applet 的应用当中， BeanFactory 会被优先选择。否则，一般使用的是 ApplicationContext。

```java
package com.mvstudy.spring6;

public class User {
    public int add(int a, int b) {
        return a+b;
    }

    public static void main(String[] args) {
        User user = new User();
        System.out.println(user.add(4,7));
    }
}
```

```java
package com.mvstudy.spring6;

import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.xml.XmlBeanFactory;
import org.springframework.core.io.ClassPathResource;

public class TestUser {
    @Test
    public void testUserObject() {
        // 加载spring配置文件
        XmlBeanFactory factory = new XmlBeanFactory(new ClassPathResource("bean.xml"));
        // 获取实例
        User user = (User)factory.getBean("user");
    }
}
```

- `XmlBeanFactory factory = new XmlBeanFactory(new ClassPathResource("bean.xml"))`加载配置文件
- `User user = (User)factory.getBean("user");`获取实例

## ApplicationContext容器

容器中存放bean对象，使用map集合。加载配置文件中定义的bean，将所有bean集中在一起（以map的数据结构），当有请求的时候分配bean。

- **`FileStstemXmlApplicationContext`**：从 XML 文件中加载已被定义的 bean。需要提供给构造器 XML 文件的完整路径
- **`ClassPathXmlApplicationContext`**：从 XML 文件中加载已被定义的 bean。不需要提供 XML 文件的完整路径，只需正确配置 CLASSPATH 环境变量即可，因为容器会从 CLASSPATH 中搜索 bean 配置文件。
- **`WebXmlApplicationContext`**：在一个 web 应用程序的范围内加载在 XML 文件中已被定义的 bean。

```java
package com.mvstudy.spring6;

import org.junit.jupiter.api.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class TestUser {
    @Test
    public void testUserObject() {
        // 加载spring配置文件
        ApplicationContext context =
                new ClassPathXmlApplicationContext("bean.xml");
        User user = (User)context.getBean("user");
        System.out.println(user.toString());
        System.out.println("3 + 5 = " + user.add(3, 5));
    }
}
```

```java
package com.mvstudy.spring6;

public class User {
    public int add(int a, int b) {
        return a+b;
    }

    public static void main(String[] args) {
        User user = new User();
        System.out.println(user.add(4,7));
    }
}
```



# Bean

bean 是一个被实例化，组装，并通过 Spring IoC 容器所管理的对象。这些 bean 是由用容器提供的配置元数据创建的

- 如何创建一个bean
- bean 的生命周期的详细信息
- bean 的依赖关系

这些所有的配置元数据转换成一组构成每个bean。bean的属性：

| 属性                     | 描述                                                         |
| :----------------------- | :----------------------------------------------------------- |
| class                    | 这个属性是强制性的，并且指定用来创建 bean 的 bean 类。       |
| name                     | 这个属性指定唯一的 bean 标识符。在基于 XML 的配置元数据中，你可以使用 ID 和/或 name 属性来指定 bean 标识符。 |
| scope                    | 这个属性指定由特定的 bean 定义创建的对象的作用域，它将会在 bean 作用域的章节中进行讨论。 |
| constructor-arg          | 它是用来注入依赖关系的，并会在接下来的章节中进行讨论。       |
| properties               | 它是用来注入依赖关系的，并会在接下来的章节中进行讨论。       |
| autowiring mode          | 它是用来注入依赖关系的，并会在接下来的章节中进行讨论。       |
| lazy-initialization mode | 延迟初始化的 bean 告诉 IoC 容器在它第一次被请求时，而不是在启动时去创建一个 bean 实例。 |
| initialization 方法      | 在 bean 的所有必需的属性被容器设置之后，调用回调方法。它将会在 bean 的生命周期章节中进行讨论。 |
| destruction 方法         | 当包含该bean的容器被销毁时，使用回调方法。                   |

## Spring配置元数据

把配置元数据提供给Spring容器的方法：

- 基于XML的配置文件
- 基于注解的配置
- 基于Java的配置

基于 XML 配置文件的例子，这个配置文件中有不同的 bean 定义，包括延迟初始化，初始化方法和销毁方法：

```xml
<?xml version="1.0" encoding="UTF-8"?>
 
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

	<!-- A simple bean definition -->
   <bean id="..." class="...">
       <!-- collaborators and configuration for this bean go here -->
   </bean>
 
   <!-- A bean definition with 延迟初始化 set on -->
   <bean id="..." class="..." lazy-init="true">
       <!-- collaborators and configuration for this bean go here -->
   </bean>
 
   <!-- A bean definition with 舒适化方法 method -->
   <bean id="..." class="..." init-method="...">
       <!-- collaborators and configuration for this bean go here -->
   </bean>
 
   <!-- A bean definition with 销毁方法 method -->
   <bean id="..." class="..." destroy-method="...">
       <!-- collaborators and configuration for this bean go here -->
   </bean>
 
   <!-- more bean definitions go here -->
 
</beans>
```

## Bean的作用域

| 作用域           | 描述                                                         |
| :--------------- | :----------------------------------------------------------- |
| `singleton`      | 该作用域将 bean 的定义的限制在每一个 Spring IoC 容器中的一个单一实例(默认)。 |
| `prototype`      | 该作用域将单一 bean 的定义限制在任意数量的对象实例。         |
| `request`        | 该作用域将 bean 的定义限制为 HTTP 请求。只在 web-aware Spring ApplicationContext 的上下文中有效。 |
| `session`        | 该作用域将 bean 的定义限制为 HTTP 会话。 只在web-aware Spring ApplicationContext的上下文中有效。 |
| `global-session` | 该作用域将 bean 的定义限制为全局 HTTP 会话。只在 web-aware Spring ApplicationContext 的上下文中有效。 |

### singleton 作用域

刚好创建一个由该 bean 定义的对象的实例。该单一实例将存储在这种单例 bean 的高速缓存中，以及针对该 bean 的**所有后续的请求和引用都返回缓存对象**。相当于是个**单例**

<small>Beans.xml</small>
![image-20240326191845179](./images/image-20240326191845179.png)

<small>MainApp.java</small>
![image-20240326192133574](./images/image-20240326192133574.png)

<small>HelloWorld.java</small>
![image-20240326192226601](./images/image-20240326192226601.png)

<small>输出结果：</small>
![image-20240326192259617](./images/image-20240326192259617.png)

在main中请求了两次该类的bean，且只有第一次设置了其中的属性，但是返回的是属性相同的对象。

### prototype 作用域

如果作用域设置为 prototype，那么每次特定的 bean 发出请求时 Spring IoC 容器就创建对象的新的 Bean 实例。一般，满状态的 bean 使用 prototype 作用域和没有状态的 bean 使用 singleton 作用域。

```xml
<bean id="..." class="..." scope="prototype">
   <!-- collaborators and configuration for this bean go here -->
</bean>
```

## Bean 的生命周期

当一个 bean 被实例化时，它可能需要执行一些初始化使它转换成可用状态。同样，当 bean 不再需要，并且从容器中移除时，可能需要做一些清除工作。

- **`init-method`**：指定一个方法，实例化 bean 时，立即调用该方法
- **`destroy_method`**：指定一个方法，只有在从容器中一处bean时才能调用该方法

### 初始化回调

在基于 XML 的配置元数据的情况下，可以使用 **init-method** 属性来指定带有 void 无参数方法的名称。

<small>User.java</small>

```java
public class User {
    public int add(int a, int b) {
        return a+b;
    }
    public void init() {
        System.out.println("哎嗨嗨，鸡汤来罗");
    }
}
```

<small>TestUser.java</small>

```java
public class TestUser {
    @Test
    public void testUserObject() {
        // 加载spring配置文件
        ApplicationContext context =
                new ClassPathXmlApplicationContext("bean.xml");
        User user = (User)context.getBean("user");
        System.out.println(user.toString());
        System.out.println("3 + 5 = " + user.add(3, 5));
        User user1 = (User)context.getBean("user");
        System.out.println(user1.toString());
    }
}
```

<small>bean.xml</small>
`<bean id="user" class="com.mvstudy.spring6.User" init-method="init" scope="prototype"></bean>`

prototype作用域下每次请求User对象时都会调用其初始化回调，并且返回新的对象；
singleton作用域下只有第一次请求User对象时会创建对象并调用其初始化回调，返回的还是第一次请求时创建的对象。

### 销毁回调

在基于 XML 的配置元数据的情况下，你可以使用 **destroy-method** 属性来指定带有 void 无参数方法的名称。

在非 web 应用程序环境中使用 Spring 的 IoC 容器，如在丰富的客户端桌面环境中，那么在 JVM 中你要注册关闭 hook。这样做可以确保正常关闭，为了让所有的资源都被释放，可以在单个 beans 上调用 destroy 方法。

`AbstractApplicationContext`类的索引指向容器，调用`.registerShutdownHook()`即释放容器，此时即会调用销毁回调。

<u>释放容器之后创建出来的对象没有被释放，仍可继续使用</u>

### 默认的初始化和销毁方法

如果有太多具有相同名称的初始化或者销毁方法的 Bean，那么不需要在每一个 bean 上声明**初始化方法** 和**销毁方法** 。框架使用元素中的 **default-init-method** 和 **default-destroy-method** 属性提供了灵活地配置这种情况

![image-20240326215108705](./images/image-20240326215108705.png)

## Bean 后置处理器

Bean后置处理器（Bean Post-Processor）是Spring框架中的一个扩展点，它允许开发者在Bean初始化前后进行自定义的处理。具体来说，Bean后置处理器的作用主要体现在以下几个方面：

1. **初始化前后的自定义处理**：Bean后置处理器可以在Spring容器初始化Bean的前后进行拦截，从而执行一些自定义的逻辑。例如，可以在Bean初始化之前进行一些安全检查，或者在初始化之后进行一些额外的配置。
2. **属性的动态修改**：通过Bean后置处理器，可以在运行时动态地修改Bean的属性。这在某些情况下非常有用，比如当需要根据环境变化调整Bean的配置时。
3. **依赖关系的检查**：Bean后置处理器可以用来检查Bean之间的依赖关系是否正确，确保所有的依赖都已经满足。
4. **性能监控**：可以在Bean后置处理器中添加代码来监控Bean的初始化时间，从而对Spring容器的性能进行分析。
5. **自定义初始化方法**：虽然Spring提供了`@PostConstruct`注解来指定Bean的初始化方法，但是Bean后置处理器提供了一种更为灵活的方式来自定义初始化逻辑。
6. **Bean的替换**：在某些特殊情况下，可能需要用一个自定义的Bean来替换掉容器中的某个Bean，Bean后置处理器可以在Bean初始化后进行这种替换。

BeanPostProcessor 可以对 bean（或对象）实例进行操作，这意味着 Spring IoC 容器实例化一个 bean 实例，然后 BeanPostProcessor 接口进行它们的工作。

要实现一个Bean后置处理器，需要实现`org.springframework.beans.factory.config.BeanPostProcessor`接口，并重写其中的`postProcessBeforeInitialization`和`postProcessAfterInitialization`方法。然后，通过将实现类注册为Spring容器中的Bean，Spring容器在启动时会自动检测并应用这些后置处理器。

- `postProcessBeforeInitialization`：在初始化之前执行
- `postProcessAfterInitialization`：在初始化之后执行

**ApplicationContext** 会自动检测由 **BeanPostProcessor** 接口的实现定义的 bean，注册这些 bean 为后置处理器，然后通过在容器中创建 bean，在适当的时候调用它。

User.java

```java
package com.mvstudy.spring6;

public class User {
    private String massage;

    public void setMassage(String massage) {
        this.massage = massage;
    }

    public String getMassage() {
        return massage;
    }

    public void init() {
        System.out.println("诶嘿嘿，鸡汤来咯");
    }

    public void destroy() {
        System.out.println("都得死");
    }
}
```

InitUser.java

```java
package com.mvstudy.spring6;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;

public class InitUser implements BeanPostProcessor {
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        System.out.println("BeforeInitialization: " + beanName);
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException{
        System.out.println("AfterInitialization: " + beanName);
        return bean;
    }
}
```

TestUser.java

```java
package com.mvstudy.spring6;

import org.junit.jupiter.api.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class TestUser {
    @Test
    public void testUserObject() {
        AbstractApplicationContext context =
                new ClassPathXmlApplicationContext("bean.xml");
        User user = (User)context.getBean("user");
        System.out.println(user.getMassage());
        context.registerShutdownHook();
    }
}
```

运行结果：
![image-20240326221602042](./images/image-20240326221602042.png)

## Bean 定义继承

bean 定义可以包含很多的配置信息，包括构造函数的参数，属性值，容器的具体信息例如初始化方法，静态工厂方法名，等等。

子 bean 的定义继承父定义的配置数据。子定义可以根据需要重写一些值，或者添加其他值。

Spring Bean 定义的继承与 Java 类的继承**无关**，但是继承的概念是一样的。可以定义一个父 bean 的定义作为模板，其他子 bean 就可以从父 bean 中继承所需的配置。

当使用基于 XML 的配置元数据时，通过使用父属性，指定父 bean 作为该属性的值来表明子 bean 的定义。
