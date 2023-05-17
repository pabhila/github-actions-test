import os
import json

#Pass the above JSON file and create a file object

fileObj = open('BuildConfig.json',)

#Convert JSON and parse as Python Dictionary

jsonDict = json.load(fileObj)

print(jsonDict)

#Substitute the value wherever required using os.path.expandvars
KlocworkProject = os.getenv("KlocworkProject")
KlocworkCSharpProject = os.getenv("KlocworkCSharpProject")
CoverityStream = os.getenv("CoverityStream")
CoverityCSharpStream = os.getenv("CoverityCSharpStream")
CoverityStream1 = os.getenv("CoverityStream1")
CHROME_BIN = os.getenv("CHROME_BIN")

print("KlocworkProject: ", KlocworkProject)
print("KlocworkCSharpProject: ", KlocworkCSharpProject)
print("CoverityStream: ", CoverityStream)
print("CoverityCSharpStream: ", CoverityCSharpStream)
print("CoverityCSharpStream1: ", CoverityStream1)
print("CHROME_BIN: ", CHROME_BIN)
print(os.environ)
