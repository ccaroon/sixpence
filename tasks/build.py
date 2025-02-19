import platform

from invoke import task

os_to_platform = {
    "Darwin": "macos",
    "Linux": "linux"
}

run_commands = {
    "Darwin": "open build/macos/Sixpence.app",
    "Linux": "build/linux/sixpence"
}

@task
def app(ctx, target=None):
    """ Build The Application for `target` Platform """
    if not target:
        os_name = platform.system()
        target = os_to_platform.get(os_name)
    ctx.run(f"flet build {target}", echo=True)
    print("=> Build Complete")

@task
def run(ctx):
    """ Run the built Application """
    os_name = platform.system()
    cmd = run_commands.get(os_name)
    if cmd:
        ctx.run(cmd)
    else:
        print(f"=> Error: Don't know to run on {os_name}.")


@task
def clean(ctx):
    """ Clean Up Stuff """
    ctx.run("rm -rf build/")
