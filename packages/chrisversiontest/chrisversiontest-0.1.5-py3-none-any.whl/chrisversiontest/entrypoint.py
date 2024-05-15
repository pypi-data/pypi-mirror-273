from semver import Version
try:
    from .__version__ import version as VERSION
    print("Used __version__ to determine version")
except ImportError:
    from setuptools_scm import get_version
    VERSION = get_version(version_scheme="only-version", local_scheme="no-local-version")
    print("Used setuptools_scm to determine version")

SEMANTIC_VERSION = Version.parse(VERSION)


def main() -> int:
    print(VERSION)
    print(SEMANTIC_VERSION)
    return 0

if __name__ == "__main__":
    exit(main())
