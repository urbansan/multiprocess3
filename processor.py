from collections import deque
import threading
import subprocess
from datetime import datetime as dt


class Processor:
    def __init__(self, commands, max_processes):
        self.cmds = deque(commands)
        self.max_procs = max_processes
        self.running_threads = set()
        self.status = dict()
        self.task_finished_event = threading.Event()

    def start_available_tasks(self):
        while len(self.running_threads) < self.max_procs:
            cmd = self.pop_next_cmd()
            self.run_cmd_in_new_thread(cmd)

    def start(self):
        while self.cmds:
            self.start_available_tasks()
            self.task_finished_event.wait(timeout=1)
            self.join_finished_threads()
            self.task_finished_event.clear()
        self.join_threads(self.running_threads)

    def join_finished_threads(self):
        finished_threads = self.running_threads - set(threading.enumerate())
        self.join_threads(finished_threads)

    def join_threads(self, threads):
        for th in set(threads):
            th.join()
            self.status[th.name]['finished'] = dt.now()
            self.running_threads.remove(th)


    def pop_next_cmd(self):
        try:
            return self.cmds.popleft()
        except IndexError:
            return None

    def run_cmd_in_new_thread(self, cmd):
        th = threading.Thread(target=self.run_cmd_in_subprocess, args=[cmd])
        th.start()
        self.status[th.name] = {'started': dt.now(), 'cmd': cmd}
        self.running_threads.add(th)


    def report_progress(self):
        for th_name, status in self.status.items():
            elapsed = status['finished'] - status['started']
            print(f'{th_name}: {elapsed}, {status["cmd"]}, joined: {status["finished"]}')

    def run_cmd_in_subprocess(self, cmd):
        th = threading.current_thread()
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE,
                             encoding='utf-8')
        started = dt.now()
        print(f'starting {th.name}, cmd: "{cmd:>8}", timestamp: "{started.time()}"')
        output, status = p.communicate()
        finished = dt.now()
        print(f'finished {th.name}, cmd: "{cmd:>8}", timestamp: "{finished.time()}"')
        self.task_finished_event.set()




if __name__ == '__main__':
    cmds = [
        'sleep 1',
        'sleep 5',
        'sleep 10',
    ] * 100
    import time
    # time.sleep(5)
    import os
    print(os.getpid())
    start = dt.now()
    p = Processor(cmds, 10)
    p.start()
    p.report_progress()
    elapsed = dt.now() - start
    print(f'Executed in {elapsed}...')