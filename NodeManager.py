import subprocess
import os
import sys
import time
import psutil
import readline
import json

class NodeManager():
    def __init__(self, config_file):
        self.config_file = config_file
        with open(self.config_file) as json_file:
            self.mgr_config = json.load(json_file)
        self.pwd = self.mgr_config["pwd"]
        # index: decoding: 0, computing: 1, encoding: 2
        self._cmds = [
                self.mgr_config["decoding_command"],
                self.mgr_config["computing_command"],
                self.mgr_config["encoding_command"]
                ]
        self._callable_fn = [
                "help",
                "change_pwd",
                "reboot",
                "start_0",
                "kill_0",
                "restart_0",
                "start_1",
                "kill_1",
                "restart_1",
                "start_2",
                "kill_2",
                "restart_2",
                "start_all",
                "restart_all",
                "kill_all",
                "list_proc"
                ]
        self.procs = [
                subprocess.Popen(['echo', 'Warm up decoding']),
                subprocess.Popen(['echo', 'Warm up computing']),
                subprocess.Popen(['echo', 'Warm up encoding'])
                ]

    def indirect(self, operation):
        operation = str(operation)
        if operation in self._callable_fn:
            method=getattr(self, str(operation))
            return method()
        else:
            print("Invalid operation.")

    def _proc_is_running(self, ind):
        if self.procs[ind].poll() == None:
            print("[INFO] Node %d is BUSY with PID %d" % (ind, self.procs[ind].pid))
            return True
        else:
            print("[INFO] Node %d is AVAILABLE" % ind)
            return False

    def _start_proc(self, ind, cmd):
        if not self._proc_is_running(ind):
            self.procs[ind] = subprocess.Popen(cmd)

    def _kill_proc(self, ind):
        self.procs[ind].kill()

    def _restart_proc(self, ind, cmd):
        self._kill_proc(ind)
        self._start_proc(ind, cmd)

    def help(self):
        print("Operation Available:")
        for operation in self._callable_fn:
            print(str(operation))

    def reload_config(self):
        with open(self.config_file) as json_file:
            self.mgr_config = json.load(json_file)

    def reboot(self):
        self.kill_all()
        cmd = "echo " + str(self.pwd) + " | sudo -S reboot"
        print(cmd)
        # Be careful to uncomment the actual function!
        #os.system(cmd)

    def kill_0(self):
        self._kill_proc(0)

    def start_0(self):
        self._start_proc(0, self._cmds[0])

    def restart_0(self):
        self._restart_proc(0, self._cmds[0])

    def kill_1(self):
        self._kill_proc(1)

    def start_1(self):
        self._start_proc(1, self._cmds[1])

    def restart_1(self):
        self._restart_proc(1, self._cmds[1])

    def kill_2(self):
        self._kill_proc(2)

    def start_2(self):
        self._start_proc(2, self._cmds[2])

    def restart_2(self):
        self._restart_proc(2, self._cmds[2])

    def start_all(self):
        self._start_proc(0, self._cmds[0])
        self._start_proc(1, self._cmds[1])
        self._start_proc(2, self._cmds[2])

    def restart_all(self):
        self._restart_proc(0, self._cmds[0])
        self._restart_proc(1, self._cmds[1])
        self._restart_proc(2, self._cmds[2])

    def kill_all(self):
        self._kill_proc(0)
        self._kill_proc(1)
        self._kill_proc(2)

    def list_proc(self):
        print(self.procs[0].pid)
        print(self.procs[1].pid)
        print(self.procs[2].pid)


