import threading
import logging

class Progress:

    def __init__(self):
        self.cur = 0
        self.max = 1
        self._lock = threading.Lock()

    def increment_cur(self, increment):
        """
        Increment cur. Only positive increment values will be applied to guarantee cur is always smaller than max.

        :param increment:
        :return:
        """
        if increment > 0:
            with self._lock:
                new_cur = self.cur + int(increment)
                if new_cur < self.max:
                    self.cur = new_cur
                    logging.info(f"Current progress: {self.cur}/{self.max} ({int(self.cur/self.max * 100)}%)")


    def increment_max(self, increment):
        """
        Increment max value. Only positive value can be set to make sure max is always greater than cur so
        progress can never be set to 100% other than calling set_finished() method. Negative values are ignored.

        :param increment: positive integer
        :type increment: int
        """
        if increment > 0:
            with self._lock:
                self.max += int(increment)


    def increment_progress(self, cur_increment, max_increment):
        """
        Increment progress by setting cur and max.
        Function makes sure cur is always smaller than max. If you want to set finished use set_finished().

        :param cur_increment: positive integer
        :type cur_increment: int
        :param max_increment: positive integer
        :type max_increment: int
        :return:
        """
        if cur_increment > 0 and max_increment >= 0:
            with self._lock:
                new_cur = self.cur + int(cur_increment)
                new_max = self.max + int(max_increment)
                if new_cur < new_max:
                    self.cur = new_cur
                    self.max = new_max
                    logging.info(f"Current progress: {self.cur}/{self.max} ({int(self.cur/self.max * 100)}%)")

    def set_progress(self, cur, max):
        """
        Set progress (cur and max) to specific value.
        Cur must be smaller than

        :param cur: current progress (number of steps done)
        :param max: max progress (number of steps todo)
        :return:
        """
        if cur < max:
            with self._lock:
                self.cur = int(cur)
                self.max = int(max)
                logging.info(f"Set progress to: {self.cur}/{self.max} ({int(self.cur / self.max * 100)}%)")


    def reset(self):
        """
        Reset progress back to zero and max back to 1.

        :return:
        """
        with self._lock:
            self.cur = 0
            self.max = 1
            logging.info(f"Reset progress to: {self.cur}/{self.max} ({int(self.cur / self.max * 100)}%)")


    def get_progress(self):
        """
        Return progress in percent as integer.

        Progress is computed by (cur/ max) * 100

        :return: progress in percent
        """
        progress = int(self.cur / self.max * 100)
        return progress

    def set_finished(self):
        """
        Set progress to finished.
        This is the only way to set the progress to finished.
        All other methods are implemented so that it is guaranteed that max will always be at least one greater
        than cur. So you can be sure that get_progress() on return true after set_finished() was called.
        :return:
        """
        with self._lock:
            self.cur = self.max
            logging.info(f"Set progress to finished. {self.cur}/{self.max} ({int(self.cur / self.max * 100)}%)")
