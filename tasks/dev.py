from invoke import task


@task
def run(ctx):
    """ Run in Dev Mode """
    ctx.run("flet run")
