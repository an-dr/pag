import threading
import time


class TimerMulTh(threading.Thread):
    def __init__(self, period_sec, timeout, out_list: list, print_val=False):
        threading.Thread.__init__(self)  # init from Thread
        self.value = out_list  # list for outer access
        self.print_val = print_val
        # timer params
        self.period = period_sec
        self.timeout = timeout
        # self.value = 0

    def run(self):
        """
        :return:
        """
        # self.value = [self.timeout]
        # === setting up a list
        if len(self.value) == 0:
            self.value.append(0)
        self.value[0] = self.timeout
        # === timer while
        while self.value[0] > self.period/2:
            # while > half-period. At the last iteration it will cause:
            #   - full period waiting, if remains more then half
            #   - 0 if remains the less
            time.sleep(self.period)
            self.value[0] -= self.period
            if self.print_val:
                print(self.value)
        self.value[0] = 0


if __name__ == '__main__':
    # Create new thread and value
    def example():
        val = []
        timer = TimerMulTh(0.1, 10, val)
        timer.start()
        while 1:
            time.sleep(.2)
            print('Value: ' + str(val))

    example()
