import os
import importlib

schema_dir = 'bots.VK_API.Schema'

modules = [f.replace('.py', '') for f in os.listdir(schema_dir) if f.endswith('.py')]

for module in modules:
    globals()[module] = importlib.import_module(f'{schema_dir}.{module}')

