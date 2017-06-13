"""
 * Copyright (C) Caleb Marshall and others... - All Rights Reserved
 * Written by Caleb Marshall <anythingtechpro@gmail.com>, May 27th, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
"""

from curionet import task

task_manager = task.TaskManager()

@task_manager.add_deferred
def task_func_0(task):

    print ("Ran task_func_0 task.")
    print ("Duration: %d" % task.duration)

    return task.cont

def task_func_1(task):

    print ("Ran task_func_1 task.")
    print ("Duration: %d" % task.duration)

    return task.cont

@task_manager.add_deferred
def task_func_2(task):

    print ("Ran task_func_2 task.")
    print ("Duration: %d" % task.duration)

    return task.cont

def task_func_3(task):

    print ("Ran task_func_3 task.")
    print ("Duration: %d" % task.duration)

    return task.cont

t0 = task_func_0()
t1 = task_manager.add(task_func_1)

t2 = task_func_2()
t3 = task_manager.add(task_func_3)

def task_func_4_delayed(task):
    print ("Ran task_func_4_delayed with delayed")
    print ("Duration since last execution: %d" % task.duration)

    return task.again

task_manager.do_method_later(5.0, task_func_4_delayed)

@task_manager.add_deferred
def r(task):

    task_manager.remove(t0)
    task_manager.remove(t1)

    task_manager.remove(t2)
    task_manager.remove(t3)

    print ("Removed all active tasks from the task manager.")

    return task.done

# removes all tasks from the task manager,
# then returns done state
#t4 = r()

# runs the task manager's main loop on the main thread,
# can also be ran on a seperate thread; and is by default.
task_manager.run(False)
