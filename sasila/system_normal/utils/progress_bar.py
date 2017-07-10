#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width

    def move(self, log_str=None):
        self.count += 1
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        if log_str:
            print log_str
        progress = self.width * self.count / self.total
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


# if __name__ == '__main__':
#     import time
#     bar = ProgressBar(total=10)
#     for i in range(10):
#         # bar.move('We have arrived at: ' + str(i + 1))
#         bar.move()
#         time.sleep(0.2)
