# -*- coding: utf-8 -*-
import collections
import queue

Event = collections.namedtuple('Event', 'time proc action')


def taxi_process(ident, trips, start_time=0):
    """每次改变状态时创建事件，把控制权交给控制器"""
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')

    yield Event(time, ident, 'going home')

def compute_duration(previous_action):
    pass



class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue() # 按时间顺序排列
        self.procs = dict(procs_map)

    def run(self, end_time):
        """排定并先是事件，直到事件结束"""
        # 排定各辆出租车的第一个事件
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)

        # 仿真系统的主循环
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print("*** end of events ***")
                break

            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print('taxi: ', proc_id, proc_id * "  ", current_event)
            active_proc = self.procs[proc_id]
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))


