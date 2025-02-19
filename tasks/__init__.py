from invoke import task, Collection

import build
import dev



ns = Collection(
    build,
    dev
)
