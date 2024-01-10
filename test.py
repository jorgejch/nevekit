import doctest
import pkgutil
import importlib

def load_modules(package):
    """
    Load all modules in the given package for testing.
    """
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        if not is_pkg:
            yield importlib.import_module(f"{package.__name__}.{name}")

def run_doctests(package):
    """
    Run doctests in all modules of the given package.
    """
    for module in load_modules(package):
        doctest.testmod(module)

if __name__ == "__main__":
    import nevekit  # Import the nevekit package
    run_doctests(nevekit)
