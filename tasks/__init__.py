from invoke import task, Collection


@task
def clean(ctx):
    """ Clean Up Stuff """
    ctx.run("rm -rf build/")


ns = Collection(
    clean
)
