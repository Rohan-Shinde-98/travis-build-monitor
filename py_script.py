import requests
import json
from time import sleep, time

TRAVIS_API_TOKEN=""
GITHUB_USERNAME=""
GITHUB_REPOSITORY_NAME=""
REPOSITORY_ID=

# Reqeust headers
headers={
  "Content-Type": "application/json",
  "Accept": "application/json",
  "Travis-API-Version": "3",
  "Authorization": "token " + TRAVIS_API_TOKEN
}

# Request body
body={
  "request": {
  "message": "Override the commit message: this is an api request",
  "branch":"main"
  }
}

try:
   # Make a build request
   response = requests.post("https://api.travis-ci.com/repo/"+ GITHUB_USERNAME + "%2F" + GITHUB_REPOSITORY_NAME + "/requests", data=json.dumps(body), headers=headers)
except:
   print("Error occured while making the api request")

# Get the response body
data = response.json()
	
# Get the request number to get the build info
request_no = data["request"]["id"]

# Make a request to get the build numbers wait some time to spin up the build
sleep(2)
try:
   response = requests.get("https://api.travis-ci.com/repo/" + str(REPOSITORY_ID) + "/request/"+ str(request_no),headers=headers)  
except:
   print("Error occured while getting the build number")

# Get the build number from the request number
sleep(1)
build_number = response.json()["builds"][0]["id"]

print("Starting the polllll.....")

# Time Limit for builds to allowed to run
TIME_LIMIT = 3

# Poll till specified in TIME_LIMIT variable
start = time()
flag = False
while (time() - start) < TIME_LIMIT:
  try:  
     response = requests.get("https://api.travis-ci.com/build/"+str(build_number), headers=headers)
  except:
     print("Error occured while polling")
  data = response.json()["state"]
  if data == "started" or data == "failed" or data == "passed" or data == "canceled":
    print("Build triggered in", str(time()-start), " seconds")
    flag = True
    break
  # Sleep for some time to avoid the too many request call 
  sleep(0.5)

# If build didn't start
if not flag:
  try:
     response = requests.post("https://api.travis-ci.com/build/" + str(build_number) + "/cancel", headers=headers)
     print("Time limit exceeded, Build Cancelled!")
  except Exception as e:
     print("Error while canceliing the build")
     print(e)
