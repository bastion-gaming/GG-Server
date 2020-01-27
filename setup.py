import subprocess
import sys

def install(package):
	# try:
	# 	subprocess.call([sys.executable, "-m", "pip", "install", "-U", package, "--user"])
	# except:
	# 	subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])
	subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])

install("pip")
install("tinydb")
install("pysqlite3")
install("pyzmq")
install("PyYAML")
install("termcolor")
