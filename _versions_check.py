import sys

try:
    from importlib.metadata import version, PackageNotFoundError  # py>=3.8
except Exception:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


def get_version(dist_names, module_paths=None):
    # Try distribution names first
    for dn in dist_names:
        try:
            return version(dn)
        except Exception:
            pass
    # Then try importing module and reading __version__
    module_paths = module_paths or []
    for mp in module_paths:
        try:
            mod = __import__(mp, fromlist=['__version__'])
            v = getattr(mod, '__version__', None)
            if v:
                return str(v)
        except Exception:
            pass
    return None

print("Python:", sys.version.replace('\n', ' '))
print("Executable:", sys.executable)

checks = [
    ("google-adk", ["google-adk", "adk", "google.adk", "google_adk"], ["google.adk"]),
    ("mcp", ["mcp"], ["mcp"]),
    ("openai", ["openai"], ["openai"]),
    ("httpx", ["httpx"], ["httpx"]),
    ("pydantic", ["pydantic"], ["pydantic"]),
]

for label, dists, mods in checks:
    v = get_version(dists, mods)
    print(f"{label}:", v or "not installed")
