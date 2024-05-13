import importlib
import os
from time import time
from typing import Generator, Tuple


def log(message: str, verbose: bool):
    if verbose:
        print(message)  # Simple print can be replaced with any logging mechanism


def square_to_curly_brackets(path: str) -> str:
    """Convert square brackets in a path to curly brackets for route parameters."""
    return path.replace("[", "{").replace("]", "}")


def walk(directory: str) -> Generator[Tuple[str, list[str], list[str]], None, None]:
    """Walk through the directory yielding each folder's path and filenames."""
    yield from os.walk(directory)


def load_routes(app, directory: str, auto_tags: bool = True, verbose: bool = False):
    """
    Dynamically load FastAPI routes from a specified directory.

    Args:
        app: The FastAPI app instance to include routers into.
        directory: The directory path where route files are located.
            It should follow
            a structure where each file represents a route module, and nested
            directories are translated into URL path segments. Files named 'route.py'
            are treated as index routes for their directory. Filenames other than
            'route.py' are appended to the path as additional segments. Square brackets
            in directory names are converted to curly brackets in route paths to denote
            path parameters.
        auto_tags: Automatically set tags for routes based on file paths.
        verbose: Enable detailed logging.

    Example:
        Given a directory structure:
            /api
                /users
                    route.py       # Translates to /users
                    [user_id].py   # Translates to /users/{user_id}
                /documents
                    /[document_id]
                        route.py   # Translates to /documents/{document_id}

        The 'route.py' file should define an 'APIRouter' instance named 'router'.
        This function will load each router and configure it within the FastAPI application.
    """
    start = time()
    log(f"Loading routes from {directory}", verbose)

    routers = []

    for root, _, files in walk(directory):
        if root.endswith("__"):
            continue
        for filename in files:
            if filename.startswith("__") or not filename.endswith(".py"):
                continue

            module_path = os.path.join(root, filename).replace("/", ".")[:-3]
            route_module = importlib.import_module(module_path)
            router = getattr(route_module, "router", None)
            if router is None:
                log(f"Router {module_path} does not contain a router", verbose)
                continue

            route_path = square_to_curly_brackets(
                root.replace(directory, "").replace(os.sep, "/")
            )
            if filename != "route.py":
                route_path += f"/{filename[:-3]}"

            if auto_tags:
                router.tags.append(route_path.strip("/"))

            routers.append((route_path, router))

    for route_path, router in sorted(routers, key=lambda x: x[0]):
        log(f"Loaded router with path /{route_path}", verbose)
        app.include_router(router, prefix=f"/{route_path}", tags=router.tags)

    log(f"Routes loaded in {time() - start:.2f}s", verbose)
    return app


# Example usage: load_routes(app, 'path/to/routes', verbose=True)
