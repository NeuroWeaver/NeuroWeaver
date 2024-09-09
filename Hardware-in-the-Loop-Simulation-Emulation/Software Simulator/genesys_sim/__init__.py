import os
currPath = os.getcwd()
print (currPath)
os.execute(f'export PYTHONPATH={currPath}')