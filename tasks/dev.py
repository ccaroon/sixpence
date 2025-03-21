from invoke import task

import util

OLD_DATA_DIR = "~/workspace/sixpence/old_data"
NEW_DATA_DIR = "~/workspace/sixpence/new_data"

@task
def run(ctx):
    """ Run in Dev Mode """
    ctx.run("flet run")

@task
def migrate(ctx, data_type):
    """
    Migrate Data v1 to Data v2
    """
    old_db = None
    new_db = None
    if data_type in ("budget", "budgets"):
        old_db = f"{OLD_DATA_DIR}/budget.sxp"
        out_db = "Budget.sxp.json"
        new_db = "Budgets.json"
    elif data_type in ("expense", "expenses"):
        old_db = f"{OLD_DATA_DIR}/expenses.sxp"
        out_db = "Expenses.sxp.json"
        new_db = "Expenses.json"

    ctx.run(f"{util.ROOT_DIR}/bin/migrate.py {old_db} {NEW_DATA_DIR}")

    ctx.run(f"cp {NEW_DATA_DIR}/{out_db} ~/Documents/sixpence/{new_db}")
    ctx.run(f"cp {NEW_DATA_DIR}/Tags.json ~/Documents/sixpence/Tags.json")
