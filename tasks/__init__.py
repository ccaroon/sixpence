from invoke import task, Collection

import build
import check
import dev



ns = Collection(
    build,
    check,
    dev
)
