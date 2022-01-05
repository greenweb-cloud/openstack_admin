#!/usr/bin/python3

from flask import Flask, jsonify, request, Response, json, abort
import subprocess
import sys

app = Flask(__name__)
class OpenstackAdmin:
    def __init__(self,project_id="null"):
        self.project_id = project_id
        self.command_reset_status= f"source /root/openrc; nova reset-state %s"%(project_id)
        self.command_active= f"source /root/openrc; nova reset-state --active %s"%(project_id)
        self.host="infra1_utility_container_ip"

    

    def reste_status(self):
        status = connect_to_server(self.host, self.command_reset_status)
        if status == True:
            return True
        else:
            return False

    def reset_state_active(self):
        status = connect_to_server(self.host, self.command_active)
        if status == True:
            return True
        else:
            return False




@app.route('/v1/server/reset_status',methods=['POST'])
def reset_status():
    try:
        res = request.get_json()["server"]
        print("request",res)
        server = OpenstackAdmin(res["project_id"])
        res = server.reste_status()
        if res:
            return success_result("success","Reset status")
        else:
            return error_result("error","Not found project id"),404

    except Exception as e:
#        return error_result("fail","key error missing %s"%e) 
        raise InvalidUsage(error_result("fail","key error missing %s"%e),status_code=400)



@app.route('/v1/server/reset_states_active',methods=['POST'])
def reset_states_active():
    try:
        res = request.get_json()["server"]
        print("request",res)
        server = OpenstackAdmin(res["project_id"])
        res = server.reset_state_active()
        if res:
            return success_result("success","reset status")
        else:
            return error_result("error","ee")

    except Exception as e:
#        return error_result("fail","key error missing %s"%e) 
        raise InvalidUsage(error_result("fail","key error missing %s"%e),status_code=400)




class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
        
# this function used to buffer stdout of remote terminal.
def line_buffered(f):
    line_buf = ""
    while not f.channel.exit_status_ready():
        line_buf = f.readline()
        yield line_buf
        line_buf = ''

# create error result structure
def error_result(status,message):
    results={}
    results["error"]={}
    results["error"]["status"]=status
    results["error"]['message']=message
    return jsonify(results)

# create success result structure
def success_result(status,message,types=""):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    if types !="":
        results["data"]["type"]=types
    results["data"]['message']=message
    return jsonify(results)

def connect_to_server(host,command):
    ssh = subprocess.Popen(["ssh", "%s" % host, command],
    shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print (sys.stderr, "ERROR: %s" % error)
        return False
    else:
        for i in result:
            if "No server with a name" in str(i):
                return False
            else:
                return True

        return True


if __name__ == '__main__':
	app.run(host= '0.0.0.0',debug=True,port=8586)



