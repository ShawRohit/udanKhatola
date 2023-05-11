import os
from config_env.development_config import Development
from config_env.production_config import Production
from config_env.qa_config import QaDevelepment
from config_env.stagging_config import Stagging

if os.environ['ENV'] == "dev":
    config = Development()
elif os.environ['ENV'] == "stage":
    print("============stag=============")
    config = Stagging()
elif os.environ['ENV'] == "qa":
    print("============qa=============")
    config = QaDevelepment()
elif os.environ['ENV'] == "prod":
    print("============prod=============")
    config = Production()

else:
    print("============dev=============")
    config = Development()
