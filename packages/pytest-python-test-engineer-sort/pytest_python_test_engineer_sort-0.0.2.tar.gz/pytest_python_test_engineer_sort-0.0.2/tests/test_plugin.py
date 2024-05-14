import pytest


@pytest.fixture()
def examples(pytester):
    pytester.copy_example("src/test_sort.py")


def test_sort(pytester, examples):
    result = pytester.runpytest("-v")

    result.stdout.fnmatch_lines(
        [
            "*test_sort.py::test_a PASSED*",
            "*test_sort.py::test_r PASSED*",
            "*test_sort.py::test_s PASSED*",
            "*test_sort.py::test_x PASSED*",
            "*test_sort.py::test_y PASSED*",
            "*test_sort.py::test_z PASSED*",
        ]
    )

    # etc for all tests
    result.stdout.fnmatch_lines(
        [
            "*==== 6 passed in*",
        ]
    )

    result.assert_outcomes(passed=6)


def test_sort_desc(pytester, examples):
    result = pytester.runpytest("-v", "--desc")
    result.stdout.fnmatch_lines(
        [
            "*===> DESC:*",
        ]
    )
    result.stdout.fnmatch_lines(
        [
            "*test_sort.py::test_z PASSED*",
            "*test_sort.py::test_y PASSED*",
            "*test_sort.py::test_x PASSED*",
            "*test_sort.py::test_s PASSED*",
            "*test_sort.py::test_r PASSED*",
            "*test_sort.py::test_a PASSED*",
        ]
    )
    result.assert_outcomes(passed=6)


# fails if order reversed so this shows they are in desc
