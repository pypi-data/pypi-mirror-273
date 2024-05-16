from jinja2 import Environment, BaseLoader, TemplateNotFound
import os
from markdown import markdown


class GasperLoader(BaseLoader):
    def __init__(self, searchpath, parent):
        self.searchpath = searchpath
        self.config = parent.config
        self.parent = parent

    def get_source(self, environment, template):
        path = os.path.join(self.searchpath, template)
        if not os.path.isfile(path):
            raise TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
            
        matter = self.parent.global_matter
        source = self.parent.env.from_string(source).render(page=matter, content=None, site=self.config)
        if path.endswith(".md") or path.endswith(".markdown"):
            source = markdown(source, extensions=['fenced_code'])
        return source, path, lambda: mtime == os.path.getmtime(path)
