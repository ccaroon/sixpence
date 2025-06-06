import arrow
import platform

from invoke import task

os_map = {
    "Linux": {
        "target": "linux",
        "exe": "sixpence",
        "install_path": "~/local/sixpence"
    },
    "Darwin": {
        "target": "macos",
        "exe": "Sixpence.app",
        "install_path": "/Applications"
    },
}


@task
def build(ctx, target=None):
    """ Build The Application for `target` Platform """
    if not target:
        os_name = platform.system()
        target = os_map.get(os_name).get("target")
    ctx.run(f"flet build {target}", echo=True)
    print("=> Build Complete")


@task
def run(ctx):
    """ Run the built Application """
    os_name = platform.system()
    target = os_map.get(os_name).get("target")
    exe = os_map.get(os_name).get("exe")
    if target and exe:
        prefix = "open" if os_name == "Darwin" else ""
        ctx.run(f"{prefix} build/{target}/{exe}", echo=True)
    else:
        print(f"=> Error: Don't know to run on {os_name}.")


@task
def install(ctx):
    """ Install the Application """
    os_name = platform.system()
    target = os_map.get(os_name).get("target")
    install_path = os_map.get(os_name).get("install_path")

    if os_name == "Linux":
        date_stamp = arrow.now().format("YYYYMMDD_HHmmss")
        ctx.run(f"mv {install_path} {install_path}-{date_stamp}", echo=True)
        ctx.run(f"cp -a build/{target} {install_path}", echo=True)
        ctx.run(f"cp etc/sixpence.desktop ~/.local/share/applications")
        ctx.run(f"cp src/assets/icon.png ~/.local/share/icons")
        ctx.run("update-desktop-database ~/.local/share/icons/ ~/.local/share/applications/")
    elif os_name == "Darwin":
        exe = os_map.get(os_name).get("exe")
        ctx.run(f"cp -a build/{target}/{exe} {install_path}", echo=True)
    else:
        print(f"=> Error: Don't know to install for {os_name}.")


@task(
    aliases=["build-clean"]
)
def clean_build(ctx):
    """ Clean Up Stuff """
    ctx.run("rm -rf build/")
