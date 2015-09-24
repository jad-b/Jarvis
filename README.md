jarvis
=======
Jarvis is a scripting framework for raising code.

Within, each code repo gets represented by a module. This module defines
implementations for a variety of interfaces, which themselves represent the
actions capable upon the code repo.

Here's an example. This interface allows for line substitution inside the code:
```python
class Substituter(metaclass=ABCMeta):
    """Substituter defines an interface for performing search|replace
    operations within a codebase.
    """

    def sub(self, target, repl, *args, dry_run=True, **kwargs):
        """Substitute pre-defined targets within the code for new ones.

        Note that 'dry_run' is an expected part of the interface.
        """
        pass

    def targets(self):
        """List all available substitution targets."""
        pass
```

This allows each repo to define what operations are allowed, and how they'll be
carried out.

Since it's Python, you can even package the modules with the code, and use
`entry_points` to install only the code bases you need.
