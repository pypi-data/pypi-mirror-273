"""
Plugin code for pytest-sort package
"""

import pytest

print("\n\n")


def pytest_addoption(parser):
    parser.addoption("--desc", action="store_true", default=False)


@pytest.fixture(scope="session")
def desc(request):
    if request.config.option.desc:
        return True
    else:
        return False


# A pytest hook to for modifying collected items
def pytest_collection_modifyitems(items, config):
    # we can sort order of items (tests) as needed
    # can ber used to sort by fixtures used if one is say expensive in time
    # items.sort(key=lambda item: "expensive" in item.fixturenames)

    if config.option.desc:
        items.sort(key=lambda item: item.nodeid.split("::")[-1], reverse=True)
        print(f"\n\n===> DESC: {config.option.desc}\n")
    else:
        items.sort(key=lambda item: item.nodeid.split("::")[-1])
