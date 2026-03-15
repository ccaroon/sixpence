from invoke import task, Collection

import app
import dev


ns = Collection(
    app,
    dev,
)
