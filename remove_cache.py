import os

for dirPath, dirNames, fileNames in os.walk("."):
	for name in dirNames:
		if name == "__pycache__":
			os.system("rm -r "+os.path.join(dirPath,name))