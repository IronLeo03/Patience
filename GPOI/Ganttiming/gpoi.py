maxtime = 0

#All the tasks
tasks = list()
class Task:
    def __init__(self, name, duration):
        global tasks
        self.name = name
        self.duration = duration
        self.depends_on = [list(), list()] #0 tasks needed to perform this task, 1 tasks that need this task to be performed
        self.time = [0, 0, 0, 0] #0 and 1 are soonest start and end, 2 and 3 are latest end and start
        self.done = False
        tasks.append(self)

    def link_after(self, task):
        task.depends_on[1].append(self)
        self.depends_on[0].append(task)
        return self


#Order 0: Calculate soonest, Order 1 Calculate latest
def calc(entry, order):
    global maxtime

    queue = list()    

    entry.time[0+order*2]=0
    entry.time[1+order*2]=entry.duration
    entry.done=not bool(order)

    queue.extend(entry.depends_on[1-order])

    while len(queue)>0:
        current = queue.pop()
        if all([bool(task.done^order) for task in current.depends_on[0+order]]):
            timemaxtime = 0
            
            if len(current.depends_on[0+order])!=0:
                timemaxtime = max([task.time[1+order*2] for task in current.depends_on[0+order]])
            
            current.time[0+order*2] = timemaxtime
            current.time[1+order*2] = timemaxtime+current.duration
            
            if order==0:
                maxtime = max(maxtime, current.time[1])
            
            current.done = not bool(order)
            queue.extend(task for task in current.depends_on[1-order] if task not in queue)
            
            pass
        else:
            queue.insert(0,current)
    

#Please be sure to include an "entry" task, otherwise first task will be ignored 
def run(tasks, time, addtoending = -1):
    calc(tasks[0], 0)
    calc(tasks[::-1][0], 1)
    
    for t in tasks:
        t.time[0] += time
        t.time[1] += time+addtoending
        t.time[2] = abs(t.time[2]-maxtime)-1
        t.time[3] = abs(t.time[3]-maxtime)
    
    with open("output.csv", "w+") as f:
        f.write("Name;Duration;Soonest start;Soonest end;Latest start;Latest end;\n")
        for t in tasks[1:]:
            f.write(f"{t.name};{t.duration};{t.time[0]};{t.time[1]};{t.time[3]};{t.time[2]}\n")

#Example task, from an homework solved using this code
#I translated the name of the tasks in english, but I haven't put much effort into it. Do not take names into consideration for the sake of this test
entry = Task("entry", 0)

first = Task("Selecting the staff", 18)
first.link_after(entry)

second = Task("Performing initial verifications", 22)
second.link_after(entry)

third = Task("Selecting equipment", 12)
third.link_after(first)

fourth = Task("Preparing layout", 34)
fourth.link_after(second)

fifth = Task("Linking site to services", 8)
fifth.link_after(second)

sixth = Task("Preparing working environment", 11)
sixth.link_after(first)

seventh = Task("Buy equipment", 20)
seventh.link_after(third)

eighth = Task("Build the hospital", 60)
eighth.link_after(fourth)

ninth = Task("Develop informative system", 7) 
ninth.link_after(first)

tenth = Task("Installing equipment", 7)
tenth.link_after(fifth).link_after(seventh).link_after(eighth)

eleventh = Task("Teaching how it works", 14)
eleventh.link_after(sixth).link_after(ninth).link_after(tenth)

run(tasks, 0)
