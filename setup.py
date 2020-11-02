import subprocess
import sys


def install(package):
    # try:
    #     subprocess.call([sys.executable, "-m", "pip", "install", "-U", package, "--user"])
    # except:
    #     subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])
    subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])


# Base
install("pip")

# Base de données
install("tinydb")
install("pysqlite3")

# Communication
install("pyzmq")
install("PyYAML")

# Gestion des événements
install("apscheduler")
