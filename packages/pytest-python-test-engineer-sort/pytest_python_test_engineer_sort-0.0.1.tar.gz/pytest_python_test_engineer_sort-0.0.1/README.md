# pytest-sort

As there are many moving parts to this project, we will do the following:

1. Have an overview demo of the whole process so that we have a general idea.
2. Break the project into smaller chunks and work through them.
3. Have a final summary overview of the process.
4. Change the plugin name and code so that you can see how to make changes for your own plugin.

  *Most of this is boiler plate code that we don't have to understand - we just need to know what is expected of us for plugin distribution to take place.*

What do we need to do to create and maintain a distributable plugin project/repo?

1. We need to convert the conftest.py into a distributable version rather than asking users to put this file in their code.
2. We also need to manage our distributable plugin project.
3. We need to test that the plugin does what we want it to do, (sort by test name).
4. We also need to test that the plugin once installed by user sorts by test name and the --desc flag works.

So we now have a plugin project to maintain.

There is a pytest-plugin cookie cutter to scaffold out the project but I found I had to make changes to it.

As it is mostly boiler plate code, we will use the given template but we will also carry out an exercise where we change it to your specifications. We will look at what you need to change to do this.

## Building a .whl file.

To make some code distributable, we need to build a .whl file.

When we do `pip install pytest` for example, what this command is foing is downloading a .whl file and then doing `pip install the_dot_wheel.whl` file.

We will use a whl builder like flit to create this wheel file but whatever tool works best for you is fine.

Copy conftest.py local to pytest_sort.py as this is the plugin with rest of template. 

For Flit we need to add a version number in this file.

Remember, a plugin is just the hook code. `conftest.py` is a plugin but a local one. 

Our plugin will be called pytest-sort, with a file called plugin_sort.py.

PyPi can accept plugin names with a '_' but prefers a '-' so that is why we have both pytest-sort and pytest_sort.

1. Copy conftest.py inot pytest_sort.py and add `__version__ = "0.0.1"`

To test src code before and after installation of our plugin:

`python -m pytest -vs .\src\test_sort.py`.

This is just regular testing and is part of the plugin project. *It is not needed for the distributable.* All we need is the plugin code in plugin_sort.py.

We get no sorting:
```
src/test_sort.py::test_s PASSED
src/test_sort.py::test_z PASSED
src/test_sort.py::test_a PASSED
src/test_sort.py::test_y PASSED
src/test_sort.py::test_x PASSED
src/test_sort.py::test_r PASSED
```
2. We need to build a `.whl` file as this is distributable and is what is on PyPi when we use `pip install <plugin>`.

We use `flit build --format=wheel` to build a whl file which we then need to install so that our plugin is active:

`pip install .\dist\pytest_sort-0.0.1-py3-none-any.whl` 

Once we install our plugin, we get test sorted alphabetically

```
src/test_sort.py::test_a PASSED
src/test_sort.py::test_r PASSED
src/test_sort.py::test_s PASSED
src/test_sort.py::test_x PASSED
src/test_sort.py::test_y PASSED
src/test_sort.py::test_zPASSED
```
and with the --desc flag get the reverse:

```
src/test_sort.py::test_z PASSED
src/test_sort.py::test_y PASSED
src/test_sort.py::test_x PASSED
src/test_sort.py::test_s PASSED
src/test_sort.py::test_r PASSED
src/test_sort.py::test_a PASSED
```
as well as 
```
===> DESC: True
```

We can confirm our plugin works in terms of sorting with and without the --desc flag.

Our end user will install our plugin and then run their tests, getting tests sorted alphabetically in either asc or desc order depending on whether the --desc flag is supplied.

We need to test this funcionality and we do this with Pytester which is built to test plugins. It comes with PyTest.

Thus we have a tests folder to test the plugin operation.

1. Create a conftest.py file in tests and add
```
pytest_plugins = ["pytester"]
```
so that we can use Pytester.

We now can run tests to very plugin useage by our user.

We need to test what happens if once installed we run our tests with no flag and with the flag.

`test_plugin.py` has two tests:

One to run tests and we add the `-v` flag so we can see test ouput_.

Another to test with the flag `-v --desc `. We pass them in as separate arguments - see file.

We then run two individual tests from test_plugin.py to test the plugin itself not the src code. The end user will just run their test files with --desc or not. The plugin will then sort one way or the other.

It is the same as we saw in the project.

We do this:
```
result = pytester.runpytest("-v")
```
and we test that the output is ascending

We get:

```
src/test_sort.py::test_a PASSED
src/test_sort.py::test_r PASSED
src/test_sort.py::test_s PASSED
src/test_sort.py::test_x PASSED
src/test_sort.py::test_y PASSED
src/test_sort.py::test_zPASSED
```
and with the --desc flag get the reverse:

```
src/test_sort.py::test_z PASSED
src/test_sort.py::test_y PASSED
src/test_sort.py::test_x PASSED
src/test_sort.py::test_s PASSED
src/test_sort.py::test_r PASSED
src/test_sort.py::test_a PASSED
```

as well as 
```
===> DESC: True
```
and we see the reverse order and the presence of `===> DESC: `. We don't need to check for True as the presence of this indicates the flag was set.

We also get 6 tests passed.

These are then the tests:

Do we get 6 lines of tests and is the total of passed test == 6.

```    result.stdout.fnmatch_lines(
        [
            "*test_sort.py::test_a PASSED*",
            "*test_sort.py::test_r PASSED*",
            "*test_sort.py::test_s PASSED*",
            "*test_sort.py::test_x PASSED*",
            "*test_sort.py::test_y PASSED*",
            "*test_sort.py::test_z PASSED*",
        ]
    )
```
fnmatch_lines is a way of seeing if the test ouput contains a line with certain text. We use * wild cards to focus on a what we need to see.

```
result.assert_outcomes(passed=6)
```
tests if we do in fact have 6 passed tests.

If these tests pass then we can feel assured that our plugin works satisfactorily as a plugin and we have also tested the functionality of the plugin code to sort test names alphabetically.

If you change the plugin_sort.py or any other plugin file, uninstall the plugin, delete the dist folder and then rebuild and install.

To uninstall the plugin:

`pip uninstall .\dist\pytest_sort-0.0.1-py3-none-any.whl` (change .whl name as per your project).