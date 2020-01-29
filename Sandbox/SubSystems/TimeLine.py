#class CallBack():
   
import time
class Timer():
    def __init__(self):
        self.started = False
        
    def start(self):
        self.start_time = time.time()
        self.passed = 0
        self.prev_time = self.start_time
        self.started = True
        
    def update(self):
        if not self.started:
            self.start()
        self.current_time = time.time()
        self.passed = self.current_time - self.prev_time
        self.prev_time = self.current_time
        
        self.relative_time = self.current_time - self.start_time
        return self.passed
    
    def time_now(self):
        return self.relative_time

class Function():
    def __init__(self, callback, *params):
        self.callback = callback
        self.params = params
    
    def call(self):
        self.callback(*self.params)
    
class TimeStamp():
    def __init__(self, time):
        self.time = time
        self.executed = False
        self.funcion_list = []
        
        
    def addCallBack(self, callback, *params):
        self.callback = callback
        self.params = params
    
    def add_function(self, callback, *params):
        self.funcion_list.append(Function(callback, *params))
        
    def done(self):
        return self.executed
    
    def reset(self):
        self.executed = False
    
    def execute(self):
        self.executed = True
        for fun in self.funcion_list:
            fun.call()
    
class TineLine():
    def __init__(self):
        self.speed_multiplier = 1
        
        self.timer_obj = Timer()
        
        self.time_stamp_dict = {}
        self._closed = False
        
        self.time_instances = []
        
    def __del__(self):
        pass
    
    def add(self, stamp):
        self.li_.append(stamp)
    
    def create_time_stamp(self, time, callback, *params):
        if time in self.time_instances:
            self.time_stamp_dict[time].add_function(callback, *params)
            return
        time_stamp = TimeStamp(time)
        time_stamp.add_function(callback, *params)
        self.time_stamp_dict[time] = time_stamp
        self.time_instances = sorted (self.time_stamp_dict.keys())
        
    def start(self):
        self.timer_obj.start()
    
    def close(self):
        self._closed = True
        
    def closed(self):
        return self._closed
        
    def update(self):
        
        t = self.timer_obj.update()
        # update all other objects
        progress_time = t * self.speed_multiplier
        for time_i in self.time_instances:
            if time_i < self.timer_obj.time_now():
                stamp = self.time_stamp_dict[time_i]
                if not stamp.done():
                    stamp.execute()
    def jump_to(self):
        pass
        
    def pause(self):
        pass
    
def spr(name):
    print ("spr created named", name)
    
timeline = TineLine()
timeline.create_time_stamp(5, timeline.close)
timeline.create_time_stamp(5, spr, "params")
timeline.create_time_stamp(5, timeline.close)

while(not timeline.closed()):
    timeline.update()
