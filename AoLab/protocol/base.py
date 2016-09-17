# In The Name Of God
# ========================================
# [] File Name : base.py
#
# [] Creation Date : 18-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import abc


class AoLabSerialProtocol:

    @abc.abstractmethod
    def handle(self, message: str):
        pass

    @abc.abstractmethod
    def process(self):
        pass
