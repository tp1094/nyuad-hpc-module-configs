class Parent(object):
    def __init__(self, name=None):
        self.name = name
    def hello(self):
        print("hello,{}".format(self.name))

class Child(Parent):
    def __init__(self, name=None, **kwargs):
        self.name = name
        self.extra_args = kwargs
    def print_kwargs(self):
        for key, value in self.extra_args:
           print("Name: {} \t Value: {}".format(key, value))
