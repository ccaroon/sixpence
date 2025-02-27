from invoke import task

import util

TEST_ROOT = "src/tests/*"

@task(
    help={
        "module": "Specific Test Module to execute. Ex: tests.module.test_note"
    }
)
def unit_tests(ctx, module=None):
    """ Run Unit Tests """

    cmd = "nose2 -v "
    if module:
        cmd += f"{module}"
    else:
        cmd += f"-s {util.ROOT_DIR}/src/tests"

    ctx.run(cmd)


@task(
    help={
        "module": "Specific Test Module to execute. Ex: tests.module.test_note"
    }
)
def coverage(ctx, module=None):
    """ Run Code Coverage """
    cmd = f"coverage run -m nose2 -v "
    if module:
        cmd += f"{module}"
    else:
        cmd += f"-s {util.ROOT_DIR}/src/tests"

    ctx.run(cmd)
    ctx.run(f"coverage report --omit={TEST_ROOT}")
    ctx.run(f"coverage html --omit={TEST_ROOT}")


@task
def clean(ctx):
    """ Delete Testing Detritus """
    ctx.run(f"rm -rf {util.ROOT_DIR}/htmlcov {util.ROOT_DIR}/.coverage")
