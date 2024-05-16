#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2024 suyambu developers (http://suyambu.net/gasper)
See the file 'LICENSE' for copying permission
"""

import sys, os
from jinja2 import Environment, BaseLoader
from markdown import markdown
import pathlib
import re
import yaml
from slugify import slugify
import json
from watchdog.events import FileSystemEventHandler
import requests
import base64
import time
import copy
from bs4 import BeautifulSoup

from .libs.argparse import ArgParse
from .util import ext, colorify
from .generator.mysql import generate as mysql_generate
from .generator.posts import generate as posts_generate
from .generator.json_parser import generate as json_generate
from .core.loader import GasperLoader
from .core import io
from .core.copytree import copytree


sys.path.insert(0, "site/_plugins")


class Gasper(FileSystemEventHandler):
    def __init__(self):
        yaml.SafeLoader.add_constructor("tag:yaml.org,2002:python/unicode", self.yaml_constructor)
        self.global_matter = {}
        self.path = None
        self.args = self.parse_arguments()
        # self.env = Environment(loader=FileSystemLoader(self.path), autoescape = True)
        self.config = self.load_config()
        self.env = Environment(loader=GasperLoader(io.path_join(self.path, "_include"), self))
        self.apply_filters()
        self.allowed_extension = [
            "html",
            "txt",
            "xml",
            "json",
            "exe",
            "bin"
        ]
        self.sitemap = []
        self.load_sitemap()
    
    def load_sitemap(self):
        sitemap_path = io.path_join("dist", "sitemap.xml")
        if os.path.exists(sitemap_path):
            with open(sitemap_path, "r") as f:
                soup = BeautifulSoup(f.read(), features="xml")
            locs = set(soup.select("url loc"))
            
            for loc in locs:
                self.sitemap.append(loc.text)            

    def yaml_constructor(self, loader, node):
        return node.value
        
    def task_print(self, s):
        print(f"{colorify.gray("[  TASK  ]")} {s}")
    
    def error_print(self, s):
        print(f"{colorify.red("[ EXCEPT ]")} {s}")
        
    def success_print(self, s):
        print(f"{colorify.green("[   OK   ]")} {s}")
        
    def load_config(self):
        config_path = io.path_join(self.path, "_config.yaml")
        config = {}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f.read())
        return config
    
    def apply_filters(self):
        self.env.filters["slugify"] = slugify
        self.env.globals["json"] = json
        self.env.filters["b64encode"] = self.b64encode
        self.env.filters["b64decode"] = base64.b64decode

    def b64encode(self, s):
        return base64.b64encode(s.encode()).decode()
        
    def get_file_path_from_src_path(self, src_path):
        file_path = src_path.replace(self.path, "")
        if file_path.startswith("\\") or file_path.startswith("/"):
            file_path = file_path[1:]
        file_path = file_path.replace("\\", "/")
        return file_path
    
    def generate_content(self, src_path, prev_content=None, prev_matter={}):
        file_path = self.get_file_path_from_src_path(src_path)
        
        # dummy, _ = self.extract_frontmatter(file_path, prev_matter)
        # dummy.update(prev_matter)
        matter, output = self.extract_frontmatter(file_path, prev_matter)
        
        if matter is None:
            matter = {}

        matter.update(prev_matter)
        try:
            self.global_matter = matter
            if "parser" in matter and matter.get("parser") == "text":
                content = self.env.from_string(output).render(page=matter, content=prev_content, site=self.config)
            else:
                content = markdown(self.env.from_string(output).render(page=matter, content=prev_content, site=self.config), extensions=['fenced_code'])
        except json.decoder.JSONDecodeError:
            print(f"Error: {matter["title"]}")
            return output
        
        if matter.get("trimContent"):
            content = content.strip()
        
        if "layout" in matter:
            if os.path.exists(io.path_join(self.path, "_layout", matter["layout"] + ".md")):
                matter["layout"] = io.path_join(self.path, "_layout", matter["layout"] + ".md")
            elif os.path.exists(io.path_join(self.path, "_layout", matter["layout"] + ".markdown")):
                matter["layout"] = io.path_join(self.path, "_layout", matter["layout"] + ".markdown")
            elif os.path.exists(io.path_join(self.path, "_layout", matter["layout"] + ".html")):
                matter["layout"] = io.path_join(self.path, "_layout", matter["layout"] + ".html")
            layout = matter.pop("layout")
            return self.generate_content(layout, content, matter)
        
        return content
    
    def handle_generator_related(self, generator, rows, row, index):
        related = {}
        if generator["from"] == "mysql":
            if generator.get("related"):
                s = yaml.dump(generator.get("related")).replace("\\u2192\\u2192", "{{").replace("\\u2190\\u2190", "}}")
                s = self.env.from_string(s).render(page={ 
                    "generator": {
                        "row": row,
                        "index": index,
                        "count": len(rows),
                        "related": {},
                        "rows": rows
                    } 
                }, content=None, site=self.config)
                tmp_related = yaml.safe_load(s)
                for r in tmp_related:
                    related_rows = mysql_generate(self, generator["db"], r["table"], generator["host"], generator["port"], generator["username"], generator["password"], r.get("where"), r.get("limit"), r.get("order"), r.get("only"), r.get("unique", False), plugin=r.get("plugin"))
                    related[r["table"]] = related_rows
        return related

    def dumpTo(self, generator, rows, related):
        if generator.get("dumpTo"):
            self.task_print(f"Dumping to {generator.get("dumpTo")}")
            dump_path = io.path_join("dist", generator["dumpTo"])
            if not os.path.exists(os.path.dirname(dump_path)):
                os.makedirs(os.path.dirname(dump_path))
            
            with open(dump_path, "wb+") as f:
                f.write(json.dumps({ "rows": rows, "related": related }).encode("utf-8"))
    
    def handle_generator(self, generator):
        if generator["from"] == "mysql":
            rows = mysql_generate(self, generator["db"], generator["table"], generator["host"], generator["port"], generator["username"], generator["password"], generator.get("where"), generator.get("limit"), generator.get("order"), generator.get("only"), generator.get("unique", False), plugin=generator.get("plugin"))

            return rows
        elif generator["from"] == "posts":
            path = generator.get("path")
            if path is None:
                path = "_posts"
            path = io.path_join(self.path, path)
            posts = posts_generate(self, path, plugin=generator.get("plugin"))
            return posts
        elif generator["from"] == "json":
            path = generator.get("path")
            path = io.path_join(self.path, "_data", path)
            return json_generate(self, path, exclude=generator.get("exclude"), limit=generator.get("limit"), plugin=generator.get("plugin"), reverse=generator.get("reverse"))
        
    def generate(self, src_path, dist_path, permalink=None, init_matter={}):
        html = self.generate_content(src_path, prev_content=None, prev_matter=init_matter)
        
        output_path = io.path_join(dist_path, "index.html")
        if permalink is not None:
            if permalink.startswith("/"):
                permalink = permalink[1:]
            if permalink.split(".")[-1] in self.allowed_extension:
                output_path = f"dist/{permalink}"
            else:
                output_path = f"dist/{permalink}/index.html"

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        with open(output_path, "wb") as f:
            f.write(html.encode("utf-8"))
            
        if "sitemap" in self.config and init_matter.get("sitemap") != "ignore":
            nodes = list(pathlib.Path(output_path).parts)
            nodes.pop(0)
            if nodes[-1] == "index.html":
                nodes.pop()
            final_url = self.config.get("url") + "/" + "/".join(nodes)
            if len(nodes) > 0 and "." not in nodes[-1]:
                final_url += "/"
            if final_url not in self.sitemap:
                self.sitemap.append(final_url)

            s = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
            """
            for m in self.sitemap:
                level = "1.0"
                parts = m.split(self.config.get("url"))
                parts = parts[-1][1:].split("/")
                if len(parts) <= 1:
                    level = "1.0"
                elif len(parts) <= 2:
                    level = "0.8"
                else:
                    level = "0.7"
                s += f"""<url>
  <loc>{m}</loc>
  <priority>{level}</priority>
</url>
"""
            s += "</urlset>"
            with open(io.path_join("dist", self.config.get("sitemap")), "wb+") as f:
                f.write(s.encode("utf-8"))
            
        self.task_print(f"{src_path} → {output_path}")

    def build(self):
        if not os.path.exists("dist"):
            os.mkdir("dist")
        
        only = None
        if self.args.only:
            only = io.path_join(self.path, self.args.only)
        else:
            io.clean_directory("dist", ["static", ".git", "CNAME"])
        
        self.task_print("moving static files...")
        if os.path.exists(io.path_join(self.path, "_static")):
            copytree(io.path_join(self.path, "_static"), io.path_join("dist", "static"))
        
        if not os.path.exists("dist"):
            os.mkdir("dist")
        for subdir, dirs, files in os.walk(self.path):
            for file in files:
                if file.startswith("_"):
                    continue
                src_path = io.path_join(subdir, file)

                if only is not None and os.path.isdir(only) and not io.is_file_under_folder(only, src_path):
                    continue
                elif only is not None and os.path.isfile(only) and src_path != only:
                    continue
                if ext.any_startswith("_", pathlib.Path(src_path).parts):
                    continue
                
                dist_path = io.path_join(subdir, file).replace(self.path, "dist")
                if dist_path.endswith("index.md") or dist_path.endswith("index.markdown") or dist_path.endswith("index.html"):
                    dist_path = os.path.dirname(dist_path)
                elif dist_path.endswith(".md") or dist_path.endswith(".html"):
                    file_name = pathlib.Path(dist_path).name
                    dist_path = io.path_join(os.path.dirname(dist_path), file_name.split(".md")[0].split(".html")[0].split(".markdown")[0])
                                
                file_path = self.get_file_path_from_src_path(src_path)
                dummy, _ = self.extract_frontmatter(file_path, is_raw=True)
                generator_copy = copy.deepcopy(dummy)
                rows = None
                related = {}
                if "generator" in dummy:
                    rows = self.handle_generator(dummy["generator"])

                if dummy.get("generator", None) is not None and dummy["generator"].get("skip") == True:
                    related = self.handle_generator_related(generator_copy["generator"], rows, None, -1)
                    self.dumpTo(generator_copy["generator"], rows, related)
                    dummy["generator"] = {
                        "row": None,
                        "index": -1,
                        "count": len(rows),
                        "related": related,
                        "rows": rows
                    }
                    init_matter, _ = self.extract_frontmatter(file_path, dummy)
                    init_matter["generator"] = dummy["generator"]
                    self.generate(src_path, dist_path, init_matter.get("permalink", None), init_matter=init_matter)
                elif rows is not None:
                    total_rows = len(rows)
                    for index, row in enumerate(rows):
                        # print(index, "\n\n")
                        # input()
                        related = self.handle_generator_related(generator_copy["generator"], rows, row, index)
                        dummy["generator"] = {
                            "row": row,
                            "index": index,
                            "count": total_rows,
                            "related": related,
                            "rows": rows
                        }
                        init_matter, _ = self.extract_frontmatter(file_path, dummy)
                        init_matter["generator"] = dummy["generator"]
                        self.generate(src_path, dist_path, init_matter.get("permalink", None), init_matter=init_matter)
                else:
                    init_matter, _ = self.extract_frontmatter(file_path, dummy)
                    self.generate(src_path, dist_path, init_matter.get("permalink", None), init_matter=init_matter)    

    def extract_frontmatter(self, path, prev_matter={}, is_raw=False, debug=False):
        if os.path.exists(path):
            abspath = path
        else:
            abspath = io.path_join(self.path, path)

        with open(abspath, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = re.compile(r'---\n(.*?)\n---', re.DOTALL)
        m = re.search(pattern, content)
        matter = {}
        output = content
        if m:
            if is_raw:
                s = m.group(1).replace("{{", "→→").replace("}}", "←←")
            else:
                s = self.env.from_string(m.group(1)).render(page=prev_matter, content=None, site=self.config)
            matter = yaml.safe_load(s)
            output = re.sub(pattern, "", output)
        return (matter, output)
    
    def parse_arguments(self):
        parser = ArgParse(argument_space_count=20, usage="gasper [path] [options]")
        parser.add_argument(["--help", "-h"], description="show help", is_flag=True)
        parser.add_argument(["--watch", "-w"], description="build and watch for changes", is_flag=True)
        parser.add_argument(["--build", "-b"], description="build the site", is_flag=True)
        parser.add_argument(["--only"], description="only build under this directory")
        args = parser.parse()
        if len(sys.argv) < 1 or not os.path.exists(sys.argv[1]) or os.path.isfile(sys.argv[1]):
            parser.print_help()
            sys.exit(1)
        
        if args.help:
            parser.print_help()
            sys.exit(0)

        self.path = sys.argv[1]
        if self.path.endswith("\\") or self.path.endswith("/"):
            self.path = self.path[:-1]
        
        if not args.watch and not args.build:
            parser.print_help()
            sys.exit(1) 
        
        self.path = self.path.replace("\\", "/")
        if args.only:
            args.only = args.only.replace("\\", "/")
        return args
    
    def handle(self):
        # try:
        self.build()
        # except Exception as e:
        #     self.error_print(e)
            
    def exit(self):
        print(self.is_terminated)
        while not self.is_terminated:
            time.sleep(1)
            r = requests.get("http://localhost:8080")
            print(r.status_code)

    def run(self):
        if self.args.watch:
            self.handle()
            
            # http_server = io.MyHTTPServer("dist", 8080)
            # http_server.start()
            io.watch_directory(self.path, self)

            # try:
            #     inp = input("Do you really want quit? (Y/n) ").strip().lower()
            #     if inp == "" or inp == "y" or inp == "yes":
            #         raise Exception() 
            # except:
            #     print(f"\n{colorify.gray("[ SERVER ]")} Exiting...")
            #     http_server.server.shutdown()
            #     http_server.join()
            #     sys.exit(0)
            
        elif self.args.build:
            self.handle()
            
    def on_modified(self, event):
        self.handle()



def main():
    gasper = Gasper()
    gasper.run()


if __name__ == "__main__":
    main()
