"""
Vendored replacement for the unmaintained ``pytest-circleci-parallelized``
plugin. It provides the ``--circleci-parallelize`` option used in CI to split
tests across CircleCI containers by class name via ``circleci tests split``.

Vendored because the upstream package (last released 0.1.0 in 2019) declares a
``startdir`` argument in its ``pytest_report_collectionfinish`` hook, which was
removed from the pytest 9 hookspec and breaks plugin registration.
"""

import collections
import subprocess

import pytest


def pytest_addoption(parser):
    """Register the ``--circleci-parallelize`` command line option."""
    group = parser.getgroup("circleci-parallelized")
    group.addoption(
        "--circleci-parallelize",
        dest="circleci_parallelize",
        action="store_true",
        default=False,
        help="Enable parallelization across CircleCI containers.",
    )


def circleci_parallelized_enabled(config):
    """Return whether CircleCI parallelization was requested."""
    return config.getoption("circleci_parallelize")


def get_class_name(item):
    """Return the ``module.Class`` (or module) identifier for a test item."""
    class_name, module_name = None, None
    for parent in reversed(item.listchain()):
        if isinstance(parent, pytest.Class):
            class_name = parent.name
        elif isinstance(parent, pytest.Module):
            module_name = parent.module.__name__
            break

    if class_name:
        return f"{module_name}.{class_name}"
    return module_name


def pytest_report_collectionfinish(config, items):
    """Report the number of items retained after CircleCI splitting."""
    if not circleci_parallelized_enabled(config):
        return ""
    if config.option.verbose == 0:
        return f"running {len(items)} items due to CircleCI parallelism"
    class_names = ", ".join(map(get_class_name, items))
    return f"running {len(items)} items due to CircleCI parallelism: {class_names}"


def filter_tests_with_circleci(test_list):
    """Split the given class names across CircleCI containers by timings."""
    circleci_input = "\n".join(test_list).encode("utf-8")
    with subprocess.Popen(
        [
            "circleci",
            "tests",
            "split",
            "--split-by=timings",
            "--timings-type=classname",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ) as process:
        circleci_output, _ = process.communicate(circleci_input)
    return [
        line.strip() for line in circleci_output.decode("utf-8").strip().split("\n")
    ]


@pytest.hookimpl(hookwrapper=True)
def pytest_cmdline_main(config):
    """Treat an empty-collection exit code as success when parallelizing."""
    outcome = yield config
    exit_code = outcome.get_result()

    # Exit code 5 indicates no tests were collected. With more workers than
    # tests this is expected, so cast it to a successful exit code.
    if circleci_parallelized_enabled(config) and exit_code == 5:
        outcome.force_result(0)


def pytest_collection_modifyitems(config, items):
    """Retain only the test items assigned to this CircleCI container."""
    if not circleci_parallelized_enabled(config):
        return

    class_mapping = collections.defaultdict(list)
    for item in items:
        class_mapping[get_class_name(item)].append(item)

    filtered_tests = filter_tests_with_circleci(class_mapping.keys())

    new_items = []
    for name in filtered_tests:
        new_items.extend(class_mapping[name])

    items[:] = new_items
