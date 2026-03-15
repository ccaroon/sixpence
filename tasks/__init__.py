import dev
from invoke import Collection

import app

ns = Collection(
    app,
    dev,
)
