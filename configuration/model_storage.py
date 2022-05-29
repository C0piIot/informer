from abc import ABC, abstractmethod

class ModelStorage:
    
    @classmethod
    @abstractmethod
    def get_models(cls, environment, start_key=None, amount=50, **filters):
        pass

    @classmethod
    @abstractmethod
    def get_model(cls, environment, key):
        pass

    @classmethod
    @abstractmethod
    def save_model(cls, environment, contact):
        pass

    @classmethod
    @abstractmethod
    def delete_model(cls, environment, key):
        pass