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
    AGAIN = 2

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
        self.delay = 0.0
        self.can_delay = True
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
    def again(self):
        return TaskResult.AGAIN

    @property
    def duration(self):
        """
        Returns the amount of time in ms, in which the task has been running for
        """

        return time.time() - self.timestamp

    def execute(self):
        """
        Executes the tasks target function, and if a delay is specified it will proceed appropiately
        """

        if not callable(self.function):
            raise TaskError('Failed to execute task %s, function not callable!' % self.name)

        if self.can_delay:
            if self.duration < self.delay:
                return self.again
            else:
                self.timestamp = time.time()

        return self.function(self, *self.args, **self.kwargs)

    def run(self):
        """
        Checks for activation, then calls execute function above
        """

        if not self.active:
            raise TaskError('Failed to run task %s, never activated!' % self.name)

        return self.execute()

    def destroy(self):
        """
        Destroys the current task instance
        """

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
        """
        Allocates next task identification number
        """

        self.id += 1; return self.id

    def has(self, name):
        """
        Returns true if the task exists in the queue else false
        """

        return name in self.running or name in self.waiting

    def delete(self, task, destroy):
        """
        Removes a specific task from which ever queue its currently in
        """

        try:
            del self.waiting[task.name]
        except KeyError:
            del self.running[task.name]

        if destroy:
            task.destroy()

    def activate(self, task):
        """
        Activates the task and places it in the waiting queue to be executed by the main loop
        """

        if self.has(task.name):
            raise TaskManagerError('Failed to activate task %s, already activated!' % task.name)

        # set the task as activated
        task.active = True

        # place the task in the waiting queue
        self.waiting[task.name] = task

        return task

    def deactivate(self, task, destroy=False):
        """
        Deactivates a task from whichever queue its currently running in
        """

        if not self.has(task.name):
            raise TaskManagerError('Failed to deactivate task %s, never activated!' % task.name)

        # set the task as inactive
        task.active = False

        # remove the task from the task manager
        self.delete(task, destroy)

    def prepend(self, function, delay, *args, **kwargs):
        """
        Creates and appends the task to the queue to be executed
        """

        task = Task(self.next_id)
        task.function = function
        task.delay = delay
        task.args = args
        task.kwargs = kwargs

        return self.activate(task)

    def add(self, function, *args, **kwargs):
        """
        Adds a new task to the task manager without a delay
        """

        return self.prepend(function, 0, *args, **kwargs)

    def do_method_later(self, delay, function, *args, **kwargs):
        """
        Adds a new task to the task manager with a delay
        """

        return self.prepend(function, delay, *args, **kwargs)

    def add_deferred(self, function):
        """
        A decorator method for setting up a task managed function
        """

        def decorate(*args, **kwargs):
            return self.add(function, *args, **kwargs)

        return decorate

    def remove(self, task):
        """
        Removes and destroys the task fron the queue
        """

        self.deactivate(task, destroy=True)

    def cycle(self, task):
        """
        Recycles the task through the queue
        """

        # deactivate the task from the queue
        self.deactivate(task)

        # reactivate the task in the queue
        self.activate(task)

    def execute(self):
        """
        Main task manager loop, executes tasks one by one
        """

        while True:
            for name in list(self.waiting):
                self.running[name] = self.waiting.pop(name)

            for task in list(self.running.values()):
                result = task.run()

                # only the task can say it should be delayed again...
                if task.can_delay:
                    task.can_delay = False

                if result == TaskResult.DONE:
                    self.remove(task)
                elif result == TaskResult.CONT:
                    self.cycle(task)
                elif result == TaskResult.AGAIN:
                    task.can_delay = True
                else:
                    self.remove(task)

            # pause the process for a specified amount of time
            # to help reduce the overall cpu load.
            time.sleep(self.TIMEOUT)

    def run(self, threaded=True, daemon=True):
        """
        Runs the task manager main loop method, by default on a seperate thread
        """

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
        """
        Destroys the task manager instance
        """

        for name in list(self.waiting):
            self.waiting.pop(name).destroy()

        for name in list(self.running):
            self.running.pop(name).destroy()

        self.id = 0
