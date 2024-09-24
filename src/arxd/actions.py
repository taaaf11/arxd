from argparse import Action
from collections import namedtuple

from .constants import PROG_VER_INFO

HelpComponents = namedtuple("HelpComponents", "desc usage options_help epilog".split())


class CustomHelpAction(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nargs = 0
        self.help = "Show this help message and exit."

    def split_help(self, parser):
        description = parser.description or ""
        epilog = parser.epilog or ""
        usage = parser.format_usage()

        help_ = parser.format_help()

        # removing substrings until options' help is left
        help_ = help_.replace(description, "")
        help_ = help_.replace(epilog, "")
        help_ = help_.replace(usage, "")
        help_ = help_.strip()
        split = help_.split("\n")

        # split[0] is "options:"
        opt_help = "\n".join(split[1:])

        usage = usage[0].upper() + "".join(list(usage[1:]))

        return HelpComponents(description, usage, opt_help, epilog)

    def __call__(self, parser, namespace, values, option_string):
        h_cmpnts = self.split_help(parser)

        print(h_cmpnts.desc, end="\n" * 2)

        print(h_cmpnts.usage, end="\n" * 2)

        print("Options:")
        print(h_cmpnts.options_help, end="\n")

        if h_cmpnts.epilog:
            print()
            print(h_cmpnts.epilog)

        parser.exit()


class VerInfoAction(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nargs = 0
        self.help = "Print version info."

    def __call__(self, parser, namespace, values, option_string):
        print(PROG_VER_INFO)
