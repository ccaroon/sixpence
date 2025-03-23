import os
from app.config import Config

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

cfg = Config.initialize(
    f"{TEST_DIR}/data/test_config.yml",
    transient=["session"]
)
cfg.set("session:env", "test")
cfg.set("session:docs_dir", f"{TEST_DIR}/data")
