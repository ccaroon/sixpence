from invoke import task, Collection

import app
import check
import dev



ns = Collection(
    app,
    check,
    dev
)
