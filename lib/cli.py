#!/usr/bin/python3
"""
cli
===
Helpful functions for dealing with the command line.
"""
import string

# Either this will create a new 'jarvis' logger, or it will inherit the
# pre-existing one from the importing script.
_logger = logging.getLogger('jarvis')


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


class JarvisShell(cmd.Cmd):
    """Interactive shell into Jarvis."""
    intro = 'Welcome, {user}'.format(user=os.getenv('USER'))
    prompt = '[jarvis]$ '

    def do_about(self, arg):
        """Print the 'about' statement."""
        _logger.info(__doc__)
