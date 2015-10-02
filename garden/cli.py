#!/usr/bin/python3
"""
cli
===
Helpful functions for dealing with the command line.
"""
import string

# Either this will create a new 'garden' logger, or it will inherit the
# pre-existing one from the importing script.
_logger = logging.getLogger('garden')


def read_until_valid(prompt, valid_inputs=None, lmbda=None):
    """Loop until a valid input has been received.

    The lambda will be applied before the input is validated, so be aware of
    any type transformation you incur.

    It is up to the caller to handle exceptions that occur outside the realm of
    calling their lambda, such as KeyboardInterrupts (^c, a.k.a C-c).

    :arg str prompt: Prompt to display.
    :kwarg ``Iterable`` valid_inputs: Acceptable inputs. If none are provided,
        then the first non-exceptional value entered will be returned.
    :arg ``func`` lmbda: Function to call on received inputs. Any errors will
        result in a re-prompting.
    """
    while True:
        user_input = input(prompt).strip(string.whitespace)
        # Apply a given function
        if lmbda is not None:
            try:
                user_input = lmbda(user_input)
            except Exception as e: # Any errors are assumed to be bad input
                _logger.warning(e)
                continue           # So keep trying
        if valid_inputs is not None:
            if user_input in valid_inputs:
                return user_input
        else:
            return user_input


def assemble_subparsers(groups, module_registry):
    """Aggregates entrypoints under a single ArgumentParser.

    Example CLI call:

        garden <action> <module> [args...]

    The alternative would be to expect each entrypoint module to provide an
    ArgumentParser, and to handle sub-commands ourselves.
    """
    parser = argparse.ArgumentParser(prog='garden')

    for group in groups: # For each sub-command, like 'bump'
        # Create subparser for registration: <action>
        subparsers = parser.add_subparsers(title=subgroup)
        # For each implementing module
        for k, v in module_registry.get(group, []):
            # Which module will we be deferring to: <module>
            module_parser = subparsers.add_parser(k)
            # Consume all arguments remaining for passthrough: [args...]
            module_parser.add_argument('args', nargs=argparse.REMAINDER)
            # Set default to registered module's entrypoint function
            module_parser.set_defaults(func=v.load())

    return parser



class GardenShell(cmd.Cmd):
    """Interactive shell into Garden."""
    intro = 'Welcome, {user}'.format(user=os.getenv('USER'))
    prompt = '[garden]$ '

    def do_about(self, arg):
        """Print the 'about' statement."""
        _logger.info(__doc__)
