import os
import json

#Pass the above JSON file and create a file object
fileObj = open('BuildConfig.json')

#Convert JSON and parse as Python Dictionary
jsonDict = json.load(fileObj)
print(jsonDict)

os.environ["TWSRESULT_PYTHON"] = "FAILED"
#Substitute the value wherever required using os.path.expandvars
TWSResult = os.getenv("tws_result")

print("TWSResult: ", TWSResult)

env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    print("TWSRESULT_GHA=SUCCESS", file=myfile)
