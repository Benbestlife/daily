多线程编程
------------------------------------------------
1 简介

1.1 多线程出现的缘由

    多线程(multithreaded,MT)编程出现之前,计算机程序的执行是由单个步骤序列组成的,
    该序列在主机的 CPU 中按照同步顺序执行.
    无论是任务本身,还是整个程序(包含多个子任务),都需要按照步骤顺序的方式执行.
    这些子任务相互独立,没有因果关系,要是让这些独立的任务同时运行,会怎么样?
    很明显,这种并行处理方式可以显著地提高整个任务的性能.
    这就是多线程编程.

1.2 多线程适合的任务

    多线程编程对于具有如下特点的编程任务而言是非常理想的:
        1.本质上是异步的;
        2.需要多个并发活动;
        3.每个活动的处理顺序可能是不确定的,或者说是随机的、不可预测的。
    这种编程任务可以被组织或划分成多个执行流,其中每个执行流都有一个指定要完成的任务。
    根据应用的不同,这些子任务可能需要计算出中间结果,然后合并为最终的输出结果。

1.3 单线程处理任务的解决方案

    计算密集型的任务可以比较容易地划分成多个子任务,然后按顺序执行或按照多线程方式执行。
    而使用单线程处理多个外部输入源的任务,
    就需要为串行程序使用一个或多个计时器,并实现一个多路复用方案。
    一个串行程序需要从每个 I/O 终端通道来检查用户的输入;
    然而,程序在读取 I/O 终端通道时不能阻塞,
    因为用户输入的到达时间是不确定的,并且阻塞会妨碍其他 I/O 通道的处理。
    串行程序必须使用非阻塞 I/O 或拥有计时器的阻塞 I/O(以保证阻塞只是暂时的).
    由于串行程序只有唯一的执行线程,因此它必须兼顾需要执行的多个任务,
    确保其中的某个任务不会占用过多时间,并对用户的响应时间进行合理的分配。
    这种任务类型的串行程序的使用,往往造成非常复杂的控制流,难以理解和维护。

1.4 多线程编程的结构

    使用多线程编程,以及类似 Queue 的共享数据结构,可以规划成几个执行特定函数的线程。
    1.UserRequestThread:
        负责读取客户端输入,该输入可能来自 I/O 通道。
        程序将创建多个线程,每个客户端一个,客户端的请求将会被放入队列中。
    2.RequestProcessor:
        该线程负责从队列中获取请求并进行处理,为第 3 个线程提供输出。
    3.ReplyThread:
        负责向用户输出,将结果传回给用户,或者把数据写到本地文件系统或数据库中。
    使用多线程来规划编程任务可以降低程序的复杂性,使其实现更加清晰、高效、简洁。
    每个线程中的逻辑都不复杂,因为它只有一个要完成的特定作业。

-----------------------------------------------------------
2 线程和进程

2.1 进程

程序:
    程序只是存储在磁盘上的可执行二进制(或其他类型)文件。
    只有把它们加载到内存中并被操作系统调用,才拥有其生命期。

进程:
    进程(或称重量级进程)则是一个执行中的程序。
    每个进程都拥有自己的地址空间、内存、数据栈以及其他用于跟踪执行的辅助数据。
    操作系统管理其上所有进程的执行,并为这些进程合理地分配时间。
    进程也可以通过派生(fork 或 spawn)新的进程来执行其他任务,
    不过因为每个新进程也都拥有自己的内存和数据栈等,所以只能采用进程间通信(IPC)的方式共享信息。

2.2 线程

线程与进程的区别:
    线程(或轻量级进程)与进程类似,不过它们是在同一个进程下执行的,并共享相同的上下文。
    可以将它们认为是在一个主进程或“主线程”中并行运行的一些“迷你进程”。

线程的组成:
    线程包括开始、执行顺序和结束三部分。
    它有一个指令指针,用于记录当前运行的上下文。
    当其他线程运行时,它可以被抢占(中断)和临时挂起(也称为睡眠)——这种做法叫做让步(yielding)。

线程的特点:可并发执行,共享进程资源
    一个进程中的各个线程与主线程共享同一片数据空间,
    因此相比于独立的进程而言,线程间的信息共享和通信更加容易。
    线程一般是以并发方式执行的,正是由于这种并发和数据共享机制,使得多任务间的协作成为可能。

线程的执行规划:
    在单核 CPU 系统中,真正的并发是不可能的,所以线程的执行是这样规划的:
    每个线程运行一小会儿,然后让步给其他线程(再次排队等待更多的 CPU 时间)。
    在整个进程的执行过程中,每个线程执行它自己特定的任务,在必要时和其他线程进行结果通信。

线程共享的风险:竞态条件-->同步原语,线程无法分配合理的执行时间
    如果两个或多个线程访问同一片数据,由于数据访问顺序不同,可能导致结果不一致。
    这种情况通常称为竞态条件(race condition)。
    幸运的是,大多数线程库都有一些同步原语,以允许线程管理器控制执行和访问。

    线程无法给予公平的执行时间。
    因为一些函数会在完成前保持阻塞状态,
    如果没有专门为多线程的这种情况进行修改,会导致 CPU 的分配时间向这些贪婪的函数倾斜。

-------------------------------------------------------------
3 线程和Python

3.1 全局解释器锁 GIL

    Python代码的执行是由Python虚拟机(又名解释器主循环)进行控制的。
    Python在设计时是这样考虑的,在主循环中同时只能有一个控制线程在执行.
    就像单核CPU系统中的多进程一样,内存中可以有许多程序,但是在任意给定时刻只能有一个程序在运行。
    同理,尽管Python解释器中可以运行多个线程,但是在任意给定时刻只有一个线程会被解释器执行。

    对Python虚拟机的访问是由全局解释器锁(GIL)控制的。
    这个锁用来保证同时只能有一个线程运行的。
    在多线程环境中,Python虚拟机将按照下述方式执行。
        1.设置 GIL。
        2.切换进一个线程去运行。
        3.执行下面操作之一。
            a.指定数量的字节码指令。
            b.线程主动让出控制权(可以调用 time.sleep(0)来完成)。
        4.把线程设置回睡眠状态(切换出线程)。
        5.解锁 GIL。
        6.重复上述步骤。

    当调用外部代码(即,任意C/C++扩展的内置函数)时,
    GIL会保持锁定,直至函数执行结束(因为在这期间没有Python字节码计数)。
    编写扩展函数的程序员有能力解锁 GIL,
    然而,作为Python开发者,并不需要担心Python代码会在这些情况下被锁住。

    例如,对于任意面向I/O的Python例程(调用了内置的操作系统 C 代码的那种),
    GIL会在I/O调用前被释放,以允许其他线程在 I/O 执行的时候运行。
    而对于那些没有太多 I/O 操作的代码而言,更倾向于在该线程整个时间片内始终占有处理器(和GIL)。
    换句话说就是,I/O 密集型的 Python 程序要比计算密集型的代码能够更好地利用多线程环境。
    (如果对源代码、解释器主循环和 GIL 感兴趣,可以看看 Python/ceval.c 文件)

3.2 退出线程

    当一个线程完成函数的执行时,它就会退出。
    另外,还可以通过调用诸如 thread.exit()之类的退出函数,
    或者 sys.exit()之类的退出 Python 进程的标准方法,
    亦或者抛出 SystemExit异常,来使线程退出。
    不过,你不能直接“终止”一个线程。

    thread 和 threading 两个模块中,不建议使用thread.
    有很多原因,其中一个最明显的原因是在主线程退出之后,所有其他线程都会在没有清理的情况下直接退出。
    而 threading 会确保在所有“重要的”子线程退出前,保持整个进程的存活。

    主线程应该做一个好的管理者,负责了解每个单独的线程需要执行什么,
    每个派生的线程需要哪些数据或参数,这些线程执行完成后会提供什么结果。
    这样,主线程就可以收集每个线程的结果,然后汇总成一个有意义的最终结果。

3.3 在Python中使用线程

    Python支持多线程编程,但取决于它所运行的操作系统。
    支持多线程的操作系统:绝大多数类UNIX平台(如Linux、Solaris、Mac OS X、*BSD等),以及Windows平台。
    Python使用兼容 POSIX 的线程,也就是众所周知的 pthread。

3.4 不使用线程的情况
    参见 onethread.py

3.5 threading模块

    Python 提供了多个模块来支持多线程编程,包括 thread、threading 和 Queue 模块等。
    程序是可以使用 thread 和 threading 模块来创建与管理线程。
    thread 模块提供了基本的线程和锁定支持;
    threading 模块提供了更高级别、功能更全面的线程管理。
    Queue 模块,用户可以创建一个队列数据结构,用于在多线程之间进行共享。

避免使用 thread 模块

    1.threading模块更加先进,有更好的线程支持,并且thread中的一些属性会和threading有冲突。
    2.低级别的 thread 模块拥有的同步原语很少(只有一个),而 threading模块则有很多。
    3.thread 对于进程何时退出没有控制。
        当主线程结束时,所有其他线程也都强制结束,不会发出警告或者进行适当的清理。
        threading 模块能确保重要的子线程在进程退出前结束。

---------------------------------------------------------------
4 thread 模块

4.1 thread 模块提供:

    派生线程;
    锁对象(lock object,也叫原语锁、简单锁、互斥锁、互斥和二进制信号量),基本的同步数据结构.

4.2 thread 模块和锁对象

thread 模块的函数
    start_new_thread (function, args, kwargs=None)
        核心函数,派生一个新的线程,使用给定的 args 和可选的 kwargs 来执行 function
    allocate_lock()
        分配 LockType 锁对象
    exit()
        给线程退出指令

LockType 锁对象的方法
    acquire (wait=None)
        尝试获取锁对象
    locked ()
        如果获取了锁对象则返回 True,否则,返回 False
    release ()
        释放锁

4.3 守护线程

    避免使用 thread 模块的另一个原因是该模块不支持守护线程这个概念。
    当主线程退出时,所有子线程都将终止,不管它们是否仍在工作。
    如果不希望发生这种行为,就要引入守护线程的概念。

    threading 模块支持守护线程,
    其工作方式是:守护线程一般是一个等待客户端请求服务的服务器。
    如果没有客户端请求,守护线程就是空闲的。
    如果把一个线程设置为守护线程,就表示这个线程是不重要的,进程退出时不需要等待这个线程执行完成。

    如果主线程准备退出时,不需要等待某些子线程完成,就可以为这些子线程设置守护线程标记。
    该标记值为真时,表示该线程是不重要的,或者说该线程只是用来等待客户端请求而不做任何其他事情。

    要将一个线程设置为守护线程,需要在启动线程之前执行如下赋值语句:
    thread.daemon = True(调用 thread.setDaemon(True)的旧方法已经弃用)。
    同样,要检查线程的守护状态,也只需要检查这个值即可(对比过去调用 thread.isDaemon()的方法)。
    一个新的子线程会继承父线程的守护标记。
    整个 Python 程序(可以解读为:主线程)将在所有非守护线程退出之后才退出(没有剩下存活的非守护线程时)。

---------------------------------------------------
5 threading 模块

    参见 mtsleepA.py 和 mtsleepB.py

threading 模块的对象
    Thread
        表示一个执行线程的对象
    Lock
        锁原语对象(和 thread 模块中的锁一样)
    RLock
        可重入锁对象,使单一线程可以(再次)获得已持有的锁(递归锁)
    Condition
        条件变量对象,使得一个线程等待另一个线程满足特定的“条件”,比如改变状态或某个数据值
    Event
        条件变量的通用版本,任意数量的线程等待某个事件的发生,在该事件发生后所有线程将被激活
    Semaphore
        为线程间共享的有限资源提供了一个“计数器”,如果没有可用资源时会被阻塞
    BoundedSemaphore
        与 Semaphore 相似,不过它不允许超过初始值
    Timer
        与 Thread 相似,不过它要在运行前等待一段时间
    Barrier
        创建一个“障碍”,必须达到指定数量的线程后才可以继续

5.1 Thread 类

    Thread 类是 threading 模块主要的执行对象。

Thread 对象数据属性
    name
        线程名
    ident
        线程的标识符
    daemon
        布尔标志,表示这个线程是否是守护线程

Thread 对象方法
    _init_(
        group=None,
        tatget=None,
        name=None,
        args=(),
        kwargs ={},
        verbose=None,
        daemon=None
        )
        实例化一个线程对象,需要有一个可调用的 target,以及其参数 args或 kwargs。
        还可以传递 name 或 group 参数,不过后者还未实现。
        此外, verbose 标志也是可接受的。
        而 daemon 的值将会设定thread.daemon 属性/标志
    start()
        开始执行该线程
    run()
        定义线程功能的方法(通常在子类中被应用开发者重写)
    join (timeout=None)
        直至启动的线程终止之前一直挂起;除非给出了 timeout(秒),否则会一直阻塞
    is_alive ()
        布尔标志,表示这个线程是否还存活


使用 Thread 类,可以有很多方法来创建线程。
    下面介绍其中比较相似的三种方法。
        1.创建 Thread 的实例,传给它一个函数。
        2.创建 Thread 的实例,传给它一个可调用的类实例。
        3.派生 Thread 的子类,并创建子类的实例。
    当你需要一个更加符合面向对象的接口时,会选择第三个;否则会选择第一个。
    第二种方案显得有些尴尬并且稍微难以阅读。

    1.创建 Thread 的实例,传给它一个函数
        把 Thread 类实例化,然后将函数(及其参数)传递进去,和之前例子中采用的方式一样。
        当线程开始执行时,这个函数也会开始执行。
        参见 mtsleepC.py

    2.创建 Thread 的实例,传给它一个可调用的类实例
        与传入函数相似的一个方法是传入一个可调用的类的实例,用于线程执行——
        这种方法更加接近面向对象的多线程编程。
        这种可调用的类包含一个执行环境,比起一个函数或者从一组函数中选择而言,有更好的灵活性。
        现在你有了一个类对象,而不仅仅是单个函数或者一个函数列表/元组。
        参见 mtsleepD.py

    3.派生 Thread 的子类,并创建子类的实例
        这个例子要调用 Thread()的子类,和mesleepD.py可调用类的例子有些相似。
        当创建线程时使用子类要相对更容易阅读。
        参见 mtsleepE.py 和 myThread.py


5.2 threading 模块的其他函数
    除各种同步和线程对象外,threading 模块还提供了一些函数
    active_count()
        当前活动的 Thread 对象个数
    current_thread
        返回当前的 Thread 对象
    enumerate()
        返回当前活动的 Thread 对象列表
    settrace (func)
        为所有线程设置一个 trace 函数
    setprofile (func)
        为所有线程设置一个 profile 函数
    stack_size (size=0)
        返回新创建线程的栈大小;或为后续创建的线程设定栈的大小为 size

----------------------------------------------------
6 单线程和多线程执行对比
    参见　mtfacfib.py

-----------------------------------------------------
7 多线程实践

    由于 Python 虚拟机是单线程(GIL)的原因,
    只有线程在执行 I/O 密集型的应用时才能更好地发挥 Python 的并发性(对比计算密集型应用,它只需要做轮询),
    因此让我们看一个 I/O 密集型的例子,然后作为进一步的练习,尝试将其移植到 Python 3 中,

7.1 豆瓣爬虫示例
    参考　bookrank.py

7.2 同步原语

    一般在多线程代码中,总会有一些特定的函数或代码块不希望(或不应该)被多个线程同时执行,
    通常包括修改数据库、更新文件或其他会产生竞态条件的类似情况。
    竞态条件: 如果两个线程运行的顺序发生变化,就有可能造成代码的执行轨迹或行为不相同,或者产生不一致的数据.
    这就需要使用同步。

    当任意数量的线程可以访问临界区的代码,但在给定的时刻只有一个线程可以通过时,就是使用同步的时候。
    程序员选择适合的同步原语,或者线程控制机制来执行同步。
    进程同步有不同的类型,Python 支持多种同步类型.

    这里使用其中两种类型的同步原语演示程序:
    锁/互斥,以及信号量。
        锁是所有机制中最简单、最低级的机制,
        而信号量用于多线程竞争有限资源的情况。

7.3 锁示例

    锁有两种状态:锁定和未锁定。
    它也只支持两个函数:获得锁和释放锁。

    1.当多线程争夺锁时,允许第一个获得锁的线程进入临界区,并执行代码。
    2.所有之后到达的线程将被阻塞,直到第一个线程执行结束,退出临界区,并释放锁。
    3.此时,其他等待的线程可以获得锁并进入临界区。
    不过,那些被阻塞的线程是没有顺序的,胜出线程的选择是不确定的,
    而且还会根据 Python 实现的不同而有所区别。

    参考　mtsleepF.py

    I/O 和访问相同的数据结构都属于临界区,因此需要用锁来防止多个线程同时进入临界区。
    为了加锁,需要添加一行代码来引入 Lock(或 RLock),然后创建一个锁对象,
    因此需要添加/修改代码以便在合适的位置上包含这些行。

    threading.enumerate()
    作为一种替代方案,可以考虑使用threading.enumerate(),
    该方法会返回仍在运行的线程列表(包括守护线程,但不包括没有启动的线程)。
    在本例中并没有使用这个方案,因为它会显示两个额外的线程,所以我们需要删除这两个线程以保持输出的简洁。
    这两个线程是当前线程(因为它还没结束),以及主线程(没有必要去显示)。

    threading.active_count()
    如果只需要对当前运行的线程进行计数,那么可以使用 threading.active_count()来代替


使用上下文管理

    with 语句
    有一种方案可以不再调用锁的 acquire()和 release()方法,从而更进一步简化代码。
    这就是使用 with 语句,此时每个对象的上下文管理器负责在进入该套件之前调用 acquire(),
    并在完成执行之后调用 release()。
    with lock:
        remaining.add(myname)
        print('xxx')
    sleep(nsec)

    threading 模块的对象 Lock、RLock、Condition、Semaphore 和 BoundedSemaphore
    都包含上下文管理器,也就是说,它们都可以使用 with 语句。


7.4 信号量示例

    锁非常易于理解和实现,也很容易决定何时需要它们。
    然而,如果情况更加复杂,你可能需要一个更强大的同步原语来代替锁。
    对于拥有有限资源的应用来说,使用信号量可能是个不错的决定。

    信号量是最古老的同步原语之一。
    它是一个计数器,当资源消耗时递减,当资源释放时递增。可以认为信号量代表它们的资源可用或不可用。
    1.消耗资源使计数器递减的操作习惯上称为 P()(来源于荷兰单词 probeer/proberen),
        也称为 wait、 try、 acquire、 pend 或 procure。
    2.相对地,当一个线程对一个资源完成操作时,该资源需要返回资源池中。
        这个操作一般称为 V() (来源于荷兰单词 verhogen/verhoog),
        也称为 signal、 increment、 release、 post、 vacate。

    Python 简化了所有的命名,使用和锁的函数/方法一样的名字:acquire 和 release。
    信号量比锁更加灵活,因为可以有多个线程,每个线程拥有有限资源的一个实例。

    threading 模块包括两种信号量类:Semaphore 和 BoundedSemaphore。
    信号量实际上就是计数器,它们从固定数量的有限资源起始。

    当分配一个单位的资源时,计数器值减 1,而当一个单位的资源返回资源池时,计数器值加 1。
    BoundedSemaphore 的一个额外功能是这个计数器的值永远不会超过它的初始值,
    换句话说,它可以防范其中信号量释放次数多于获得次数的异常用例。

    参考　candy.py

进行调试

    在某种情况下需要调试一个使用了信号量的脚本,
    此时需要知道在任意给定时刻信号量计数器的精确值。

    如，需要为 candy.py 实现一个显示计数器值的解决方案,或许可以将其称为 candydebug.py。
    为了做到这一点,需要查阅threading.py 的源码。
    你会发现 threading 模块的同步原语并不是类名,即便它们使用了驼峰式拼写方法,看起来像是类名。
    实际上,它们是仅有一行的函数,用来实例化你认为的那个类的对象。

    这里有两个问题需要考虑:
    其一,你不能对它们子类化(因为它们是函数);
    其二,变量名在 2.x 和 3.x 版本间发生了改变。
    如果这个对象可以给你整洁/简单地访问计数器的方法,整个问题就可以避免了,
    但实际上并没有。
    计数器的值只是类的一个属性,所以可以直接访问它,

    这个变量名从 Python2 版本的 self.__value,即 self._Semaphore__value,
    变成了 Python 3 版本的 self._value。
    对于开发者而言,最简洁的 API　是继承 threading._BoundedSemaphore类,
    并实现一个__len__()方法,不过要注意,
    如果你计划对 2.x 和 3.x 版本都支持,还是需要使用刚才讨论过的那个正确的计数器值。

----------------------------------------------------------------
8 生产者-消费者问题和 Queue/queue 模块

    queue 模块提供线程间通信的机制,从而让线程之间可以互相分享数据.

Queue/queue 模块的类
    Queue(maxsize=0)
        创建一个先入先出队列。
        如果给定最大值,则在队列没有空间时阻塞;否则(没有指定最大值),为无限队列
    LifoQueue(maxsize=0)
        创建一个后入先出队列。
        如果给定最大值,则在队列没有空间时阻塞;否则(没有指定最大值),为无限队列
    PriorityQueue(maxsize=0)
        创建一个优先级队列。
        如果给定最大值,则在队列没有空间时阻塞,否则(没有指定最大值),为无限队列

Queue/queue 异常
    Empty
        当对空队列调用 get*()方法时抛出异常
    Full
        当对已满的队列调用 put*()方法时抛出异常

Queue/queue 对象方法
    qsize()
        返回队列大小(由于返回时队列大小可能被其他线程修改,所以该值为近似值)
    empty()
        如果队列为空,则返回 True;
        否则,返回 False
    full()
        如果队列已满,则返回 True;
        否则,返回 False
    put(item, block=Ture, timeout=None)
        将 item 放入队列。
        如果 block 为 True(默认)且 timeout 为 None,则在有可用空间之前阻塞;
        如果 timeout 为正值,则最多阻塞 timeout 秒;
        如果 block 为 False,则抛出 Empty 异常
    put_nowait(item)
        和 put(item, False)相同
    get(block=True, timeout=None)
        从队列中取得元素。
        如果给定了 block(非 0),则一直阻塞到有可用的元素为止
    get_nowait()
        和 get(False)相同
    task_done()
        用于表示队列中的某个元素已执行完成,该方法会被下面的 join()使用
    join()
        在队列中所有元素执行完毕并调用上面的 task_done()信号之前,保持阻塞

    生产者-消费者问题案例参考　prodcons.py

---------------------------------------------------------------
9 线程的替代方案

    通常来说,多线程是一个好东西.不过，由于 Python 的 GIL 的限制,
    多线程更适合于 I/O 密集型应用(I/O 释放了 GIL,可以允许更多的并发),
    而不是计算密集型应用。
    对于后一种情况而言,为了实现更好的并行性,你需要使用多进程,以便让 CPU 的其他内核来执行。
    (这个主题内已经在 Core Python Programming 或
    Core PythonLanguage Fundamentals 的“执行环境”章节中有所涵盖)

    对于多线程或多进程而言, threading模块的主要替代品包括以下几个:

    1.subprocess 模块
        这是派生进程的主要替代方案,可以单纯地执行任务,
        或者通过标准文件(stdin、stdout、stderr)进行进程间通信。

    2.multiprocessing 模块
        该模块允许为多核或多 CPU 派生进程,其接口与 threading模块非常相似。
        该模块同样也包括在共享任务的进程间传输数据的多种方式。

    3.concurrent.futures 模块
        这是一个新的高级库,它只在“任务”级别进行操作,
        也就是说,你不再需要过分关注同步和线程/进程的管理了。
        你只需要指定一个给定了“worker”数量的线程/进程池,提交任务,然后整理结果。

        对于 I/O 密集型应用,多线程更有用,可以使用concurrent.futures.ThreadPoolExecutor。
        而对于计算密集型应用而言,可以使用 concurrent.futures.ProcessPoolExecutor 来代替。


-----------------------------------------------------------
10 相关模块

    多线程应用编程中可能会使用到的一些模块

    _thread
        基本的、低级别的线程模块

    threading
        高级别的线程和同步对象

    multiprocessing
        使用“threading”接口派生/使用子进程

    subprocess
        完全跳过线程,使用进程来执行

    Queue
        供多线程使用的同步先入先出队列

    concurrent.futures
        异步执行的高级别库

    SocketServer
        创建/管理线程控制的 TCP/UDP 服务器