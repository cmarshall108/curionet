"""
 * Copyright (C) Caleb Marshall and others... - All Rights Reserved
 * Written by Caleb Marshall <anythingtechpro@gmail.com>, May 27th, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
"""

import time
import threading

class TaskResult(object):
    """
    A enum for (returnable) task outputs
    """

    DONE = 0
    CONT = 1
    WAIT = 2

class TaskError(RuntimeError):
    """
    A task specific runtime error
    """

class Task(object):
    """
    An asynchronous task instance
    """

    def __init__(self, id):
        self.id = id
        self.name = '%s-%d' % (self.__class__.__name__, id)
        self.function = None
        self.timestamp = time.time()
        self.args = []
        self.kwargs = {}
        self.active = False

    @property
    def done(self):
        return TaskResult.DONE

    @property
    def cont(self):
        return TaskResult.CONT

    @property
    def wait(self):
        return TaskResult.WAIT

    @property
    def duration(self):
        return time.time() - self.timestamp

    def execute(self):
        if not callable(self.function):
            raise TaskError('Failed to execute task %s, function not callable!' % self.name)

        return self.function(self, *self.args, **self.kwargs)

    def run(self):
        if not self.active:
            raise TaskError('Failed to run task %s, never activated!' % self.name)

        return self.execute()

    def destroy(self):
        self.id = self.name = self.function = self.timestamp = self.args = self.kwargs = None

class TaskManagerError(RuntimeError):
    """
    A task manager specific runtime error
    """

class TaskManager(object):
    """
    An asynchronous threaded task managment system to distribute the work load away
    from the built in curio task manager; for background tasks only.
    """

    TIMEOUT = 0.01

    def __init__(self):
        self.running = {}
        self.waiting = {}
        self.id = 0

    @property
    def next_id(self):
        self.id += 1; return self.id

    def has(self, name):
        return name in self.running or name in self.waiting

    def delete(self, task, destroy):
        try:
            del self.waiting[task.name]
        except KeyError:
            del self.running[task.name]

        if destroy:
            task.destroy()

    def activate(self, task):
        if self.has(task.name):
            raise TaskManagerError('Failed to activate task %s, already activated!' % task.name)

        # set the task as activated
        task.active = True

        # place the task in the waiting queue
        self.waiting[task.name] = task

        return task

    def deactivate(self, task, destroy=False):
        if not self.has(task.name):
            raise TaskManagerError('Failed to deactivate task %s, never activated!' % task.name)

        # set the task as inactive
        task.active = False

        # remove the task from the task manager
        self.delete(task, destroy)

    def add(self, function, *args, **kwargs):
        task = Task(self.next_id)
        task.function = function
        task.args = args
        task.kwargs = kwargs

        return self.activate(task)

    def add_deferred(self, function):

        def decorate(*args, **kwargs):
            return self.add(function, *args, **kwargs)

        return decorate

    def remove(self, task):
        self.deactivate(task, destroy=True)

    def cycle(self, task):
        # deactivate the task from the queue
        self.deactivate(task)

        # reactivate the task in the queue
        self.activate(task)

    def execute(self):
        while True:
            for name in list(self.waiting):
                self.running[name] = self.waiting.pop(name)

            for task in list(self.running.values()):
                result = task.run()

                if result == TaskResult.DONE:
                    self.remove(task)
                elif result == TaskResult.CONT:
                    self.cycle(task)
                elif result == TaskResult.WAIT:
                    raise NotImplemented
                else:
                    self.remove(task)

            # pause the process for a specified amount of time
            # to help reduce the overall cpu load.
            time.sleep(self.TIMEOUT)

    def run(self, threaded=True, daemon=True):
        try:
            if threaded:
                thread = threading.Thread(target=self.execute)
                thread.daemon = daemon
                thread.start()
            else:
                self.execute()
        except (KeyboardInterrupt, SystemExit):
            self.destroy()

    def destroy(self):
        for name in list(self.waiting):
            self.waiting.pop(name).destroy()

        for name in list(self.running):
            self.running.pop(name).destroy()

        self.id = 0
