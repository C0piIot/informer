from abc import ABC, abstractmethod

class ContactStorage(ABC):
    
    @classmethod
    @abstractmethod
    def get_contacts(cls, environment, start_key=None, amount=50, **filters):
        pass

    @classmethod
    @abstractmethod
    def get_contact(cls, environment, key):
        pass

    @classmethod
    @abstractmethod
    def save_contact(cls, environment, contact):
        pass

    @classmethod
    @abstractmethod
    def delete_contact(cls, environment, key):
        pass