from abc import ABC, abstractmethod

class ContactStorage(ABC):
    
    @classmethod
    @abstractmethod
    def get_contacts(cls, start_key, amount=50, **filters):
        pass

    @classmethod
    @abstractmethod
    def get_contact(cls, key):
        pass

    @classmethod
    @abstractmethod
    def save_contact(cls, contact):
        pass

    @classmethod
    @abstractmethod
    def delete_contact(cls, key):
        pass