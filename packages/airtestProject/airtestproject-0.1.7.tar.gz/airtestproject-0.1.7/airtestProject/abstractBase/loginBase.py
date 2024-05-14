from abc import ABC, abstractmethod


class LoginBase(ABC):

    @abstractmethod
    def input_account(self):
        pass

    @abstractmethod
    def click_login(self):
        pass
