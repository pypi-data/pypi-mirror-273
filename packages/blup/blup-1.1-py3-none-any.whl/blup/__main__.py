from json import load, JSONDecodeError
from blup.blup_loader import BlupLoader
from jinja2 import Environment, select_autoescape, TemplateError, TemplateNotFound
from argparse import ArgumentParser
from collections.abc import Iterable
from blup.exceptions import BlupIterableJson
from os.path import exists, getmtime
from time import sleep

class Blup:
    def __init__(self, args):
        self.source = args.source
        self.template = args.template
        self.output = args.output

        self.env = Environment(
            loader=BlupLoader(),
            autoescape=select_autoescape()
        )

    def build(self):
        template = self.env.get_template(self.template)
        with open(self.source) as file:
            json = load(file)
            if isinstance(json, list):
                raise BlupIterableJson()
            if not self.output:
                print(template.render(**json))
            else:
                with open(self.output, "w") as output_file:
                    output_file.write(template.render(**json))


def execute(args, blup):
    try:
        blup.build()
    except FileNotFoundError as e:
        print(f'{e.strerror} : {e.filename}')
    except JSONDecodeError:
        print("Problem with your JSON file !")
    except BlupIterableJson as e:
        print(e)
    except TemplateNotFound as e:
        print(f'No such file or directory : {args.template}')
    except TemplateError:
        print("Error with your template file.")

def serve(args, blup):
    if not exists(args.source):
        print(f'No such file or directory : {args.source}')
        return
    if not args.output:
        print(f'Can\'t run Blup in background without a output file')
        return

    print("Running Blup in real time !")
    last = 0.0
    try:
        while True:
            now = getmtime(args.source)
            if last != now:
                print("Regenerating the template :)")
                execute(args, blup)
                last = now
            sleep(1)
    except KeyboardInterrupt:
        return

def main():
    parser = ArgumentParser(
        prog="Blup",
        description="Turn JSON file to HTML using Jinja."
    )
    parser.add_argument('template', help='Template file in Jinja format')
    parser.add_argument('source', help='Source of the data to use')
    parser.add_argument('-o', '--output', required=False, help='Output file to be created')
    parser.add_argument('-s', '--serve', action='store_true')

    args = parser.parse_args()
    blup = Blup(args)

    if not args.serve:
        execute(args, blup)
    else:
        serve(args, blup)

