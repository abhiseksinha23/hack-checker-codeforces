from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route("/test_api", methods = ["GET"])
def test_func():
  u = request.args.get("user")
  sol = {
    "FAILED": 0,
    "OK": 0,
    "PARTIAL": 0,
    "COMPILATION_ERROR": 0,
    "RUNTIME_ERROR": 0,
    "WRONG_ANSWER": 0,
    "PRESENTATION_ERROR": 0,
    "TIME_LIMIT_EXCEEDED": 0,
    "MEMORY_LIMIT_EXCEEDED": 0,
    "IDLENESS_LIMIT_EXCEEDED": 0,
    "SECURITY_VIOLATED": 0,
    "CRASHED": 0,
    "INPUT_PREPARATION_CRASHED": 0,
    "CHALLENGED": 0,
    "SKIPPED": 0,
    "TESTING": 0,
    "REJECTED": 0,
    "ABSENT": 0,
    "successfulHackCount": 0,
    "unsuccessfulHackCount": 0
  }
  res = requests.get("https://codeforces.com/api/user.status?", params={"handle": u})
  jdata = res.json()
  jres = jdata["result"]
  for i in jres:
    try:
      sol[i["verdict"]] += 1
    except IndexError:
      sol["ABSENT"] += 1
  res = requests.get("https://codeforces.com/api/user.rating?", params={"handle": u})
  jdata = res.json()
  jres = jdata["result"]
  for i in jres:
    res2 = requests.get("https://codeforces.com/api/contest.standings?", params = {"contestId": i["contestId"], "handles": u})
    jdata2 = res2.json()
    jres2 = jdata2["result"]["rows"]
    if jres2:
      sol["successfulHackCount"] += jres2[0]["successfulHackCount"]
      sol["unsuccessfulHackCount"] += jres2[0]["unsuccessfulHackCount"]  
  return jsonify(sol)

if __name__=="__main__":
    app.run(debug = True)