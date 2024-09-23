from argparse import Action, RawDescriptionHelpFormatter, SUPPRESS
from collections import namedtuple


HelpComponents = namedtuple("HelpComponents", "desc usage options_help epilog".split())


class CustomHelpAction(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nargs = 0
        self.help = "Show this help message and exit."

    def split_help(self, parser):
        description = parser.description or ""
        epilog = parser.epilog or ""
        usage = parser.format_usage().strip().capitalize()

        help_ = parser.format_help()
        help_ = help_.replace(description, "")
        help_ = help_.replace(epilog, "")
        split = [i for i in help_.split("\n") if i]

        # usage is always there
        opt_help_idx = 1
        opt_help_idx += 1 if description else 0
        opt_help = "\n".join(split[opt_help_idx:])

        return HelpComponents(description, usage, opt_help, epilog)

    def __call__(self, parser, namespace, values, option_string):
        h_cmpnts = self.split_help(parser)

        print(h_cmpnts.desc, end="\n" * 2)

        print(h_cmpnts.usage, end="\n" * 2)

        print("Options:")
        print(h_cmpnts.options_help, end="\n" * 2)

        print(h_cmpnts.epilog)

        parser.exit()


def remove_empty_strings(l: list[str]) -> list:
    return [_ for _ in l if _]
