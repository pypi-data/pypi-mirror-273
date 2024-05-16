from jinja2 import BaseLoader, TemplateNotFound
from os.path import exists, getmtime

class BlupLoader(BaseLoader):
    def __init__(self):
        self.path = None

    def get_source(self, _, template):
        path = template
        if not exists(template):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, template, lambda: mtime == getmtime(path)

