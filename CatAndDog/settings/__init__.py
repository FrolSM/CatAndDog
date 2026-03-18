import os

env = os.getenv("ENVIRONMENT", "local")

if env == "docker":
    from .docker import *
elif env == "production":
    from .production import *
else:
    from .local import *