'''
This module of cul is developed to parse semantic versioning strings and determine their lower and upper bounds.
Parsing semver is necessary as it helps in understanding the version constraints of modules, ensuring compatibility and proper dependency management which is a critical feature for any package management system.

This module is still in development.

Right now the code written supports very basic semver parsing and does not cover all the edge cases.
But it will be improved in future updates.
'''

def get_major_minor_patch(version: str) -> tuple[int, int, int]:
    try:
        major, minor, patch = map(int, version.split("."))
        return major, minor, patch
    except ValueError:
        raise ValueError(f"Invalid version format: {version}. Expected format: x.y.z")

def parse_semver(version: str):
    
    if version.startswith("^"):
        lower = version[1:]
        major, minor, patch = get_major_minor_patch(lower)
        upper = f"{major + 1}.0.0"

    elif version.startswith("~"):
        lower = version[1:]
        major, minor, patch = get_major_minor_patch(lower)
        upper = f"{major}.{minor + 1}.0"

    elif version.startswith(">="):
        lower = version[2:]
        major, minor, patch = get_major_minor_patch(lower)
        upper = None

    elif version.startswith("<="):
        upper = version[2:]
        major, minor, patch = get_major_minor_patch(upper)
        lower = None

    elif version.startswith(">"):
        lower = version[1:]
        major, minor, patch = get_major_minor_patch(lower)
        lower = f"{major}.{minor}.{patch + 1}"
        upper = None

    elif version.startswith("<"):
        upper = version[1:]
        major, minor, patch = get_major_minor_patch(upper)

        upper = f"{major}.{minor}.{patch - 1}"
        lower = None

    else:
        lower = upper = version

    print("------- For version " + version + " -------")
    print("Lower bound: ", lower)
    print("Upper bound: ", upper)
    print()

if __name__ == "__main__":
    parse_semver(">=1.2.3")
    parse_semver("<=1.2.3")
    parse_semver(">1.2.3")
    parse_semver("<1.2.3")
    parse_semver("^1.2.3")
    parse_semver("~1.2.3")
    parse_semver("1.2.3")