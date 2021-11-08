import requests
import json
from time import sleep, time

# Reqeust headers
headers={
  "Content-Type": "application/json",
  "Accept": "application/json",
  "Travis-API-Version": "3",
  "Authorization": "token <add-api-token-here>"
}

# Request body
body={
  "request": {
  "message": "Override the commit message: this is an api request",
  "branch":"main"
  }
}

# Make a build request
response = requests.post("https://api.travis-ci.com/repo/Rohan-Shinde-98%2Ftravis-build-monitor/requests", data=json.dumps(body), headers=headers)

# Get the response body
data = response.json()
	
# Get the request number to get the build info
request_no = data["request"]["id"]

# Make a request to get the build numbers wait some time to spin up the build
sleep(10)
response = requests.get("https://api.travis-ci.com/repo/20274855/request/"+str(request_no),headers=headers)  

# Get the build number from the request number
sleep(1)
build_number = response.json()["builds"][0]["id"]

print("Starting the polllll.....")

# Poll till 3 seconds
start = time()
flag = False
while (time() - start) < 3:
  response = requests.get("https://api.travis-ci.com/build/"+str(build_number), headers=headers)
  data = response.json()["state"]
  if data == "started" or data == "failed" or data == "passed" or data == "canceled":
    print("Build triggered in", str(time()-start), " seconds")
    flag = True
    break
  # Sleep for some time to avoid the too many request call 
  sleep(0.5)

# If build didn't start
if not flag:
  print("Time limit exceeded")
