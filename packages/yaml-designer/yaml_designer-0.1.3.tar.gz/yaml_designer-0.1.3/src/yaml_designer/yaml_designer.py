import yaml

def iterable(cls):
    def iterfn(self):
        iters = dict((x,y) for x,y in cls.__dict__.items() if x[:2] != '__')
        iters.update(self.__dict__)

        for x,y in iters.items():
            yield x,y

    cls.__iter__ = iterfn
    return cls

@iterable
class yamlclass_node():
    def __init__(self):
        pass

class yamlclass():
    def __init__(self):
        self.node = yamlclass_node()
    def add(self, name, value):
        setattr(self.node, name, value)
    def get(self, name):
        return getattr(self.node, name)
    def build(self, filename):
        names_yaml = str(dict(self.node))
        names = yaml.safe_load(names_yaml)
        with open(filename, 'w') as file:
            yaml.dump(names, file)
    def yaml(self):
        return dict(self.node)

