from argparse import Action
from typing import NamedTuple, override


class HelpComponents(NamedTuple):
    desc: str
    usage: str
    options_help: str
    epilog: str


class CustomHelpAction(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nargs = 0
        self.help = "Show this help message and exit."

    @staticmethod
    def split_help(parser):
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

        usage = f"U{usage[1:].strip()}"  # Usage: ...

        return HelpComponents(description, usage, opt_help, epilog)

    @override
    def __call__(self, parser, namespace, values, option_string=None):
        h_cmpnts = CustomHelpAction.split_help(parser)

        print(h_cmpnts.desc, end="\n" * 2)

        print(h_cmpnts.usage, end="\n" * 2)

        print("Options:")
        print(h_cmpnts.options_help, end="\n")

        if h_cmpnts.epilog:
            print()
            print(h_cmpnts.epilog)

        parser.exit()
