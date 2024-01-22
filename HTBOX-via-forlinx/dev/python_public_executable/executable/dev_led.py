#!/usr/bin/env python
# cython: language_level=3
# -*- coding: utf-8 -*-
import argparse
import os
import time
from threading import Thread


class DevLed(Thread):

    def __init__(self, state: str):
        self.leds = ["led_stat", "led_sign", "led_rc"]
        self.states = ["update", "test"]

        super().__init__()
        self.state = state

    def led_on(self, led_name: str):
        value = open(f"/sys/class/leds/{led_name}/brightness", "w")
        value.write(str(1))
        value.close()

    def led_off(self, led_name: str):
        value = open(f"/sys/class/leds/{led_name}/brightness", "w")
        value.write(str(0))
        value.close()

    def led_twinkle(self, led_name: str, delay: float, times: int, interval: float, reverse: bool):
        if reverse:
            self.led_on(led_name)
        else:
            self.led_off(led_name)

        for i in range(times):
            if reverse:
                self.led_off(led_name)
                time.sleep(delay)
                self.led_on(led_name)
            else:
                self.led_on(led_name)
                time.sleep(delay)
                self.led_off(led_name)

            if i < times - 1:
                time.sleep(interval)

    def run(self):
        if self.state in self.states:
            while True:
                if self.state == "update":
                    # 全灭-1s
                    self.led_off(self.leds[0])
                    self.led_off(self.leds[1])
                    self.led_off(self.leds[2])
                    time.sleep(1)

                    # 0闪2次
                    self.led_twinkle(self.leds[0], delay=0.3, times=2, interval=0.5, reverse=False)
                    time.sleep(0.5)

                    # 跑流水
                    for i in range(3):
                        self.led_twinkle(self.leds[i], delay=0.1, times=1, interval=0, reverse=False)
                        time.sleep(0.05)
                elif self.state == "test":
                    # 全灭-1s
                    self.led_off(self.leds[0])
                    self.led_off(self.leds[1])
                    self.led_off(self.leds[2])
                    time.sleep(1)

                    # 全亮-1s
                    self.led_on(self.leds[0])
                    self.led_on(self.leds[1])
                    self.led_on(self.leds[2])
                    time.sleep(1)

        else:
            print("WRONG STATE!")


class JobShell:

    @staticmethod
    def get_pids(text):
        pids = []
        shell_lines = os.popen("ps -ef | grep \"" + text + "\" | grep -v grep").readlines()
        if len(shell_lines) > 0:
            shell_lines = os.popen("ps -ef | grep \"" + text + "\" | grep -v grep | awk '{print $1}'").readlines()
        for pid in shell_lines:
            pids.append(int(pid.replace("\n", "")))
        return pids

    @staticmethod
    def killjob(pid):
        os.system('kill -9 ' + str(pid))
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LED control script')
    parser.add_argument("--state", type=str, default="update")
    args = parser.parse_args()

    mypid = os.getpid()
    print("This pid is " + str(mypid))
    pids = JobShell.get_pids("dev_led")

    if len(pids) > 0:
        for pid in pids:
            if pid != mypid:
                print("Kill " + str(pid))
                JobShell.killjob(pid)

    thr = DevLed(args.state)
    thr.setDaemon(False)
    thr.start()
