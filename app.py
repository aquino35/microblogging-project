#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.user import UsrController
from controller.msg import MsgController

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to Twitter!"

@app.route('/MicrobloggingApp/users', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        return UsrController().register(request.json)
    elif request.method == 'GET':
        return UsrController().getAllUsers()
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/users/<int:uid>', methods=['GET','PUT','DELETE'])
def userById(uid):
    if request.method == 'GET':
        return UsrController().getUserById(uid)
    if request.method == 'PUT':
        request.json["uid"] = uid
        return UsrController().updateUserById(request.json)
    elif request.method == 'DELETE':
        return UsrController().removeUser(uid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/users/<string:uname>', methods=['GET'])
def userByUname(uname):
    if request.method == 'GET':
        return UsrController().getUserByUname(uname)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/users/email/<string:email>', methods=['GET']) #needs tunning
def userByEmail(email):
    if request.method == 'GET':
        return UsrController().getUserByEmail(email)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/follow/<int:uid2>', methods=['POST'])
def followUser(uid2):
    if request.method == 'POST':
        request.json["uid2"] = uid2
        return UsrController().follow(request.json)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/unfollow/<int:uid2>', methods=['POST'])
def unfollowUser(uid2):
    if request.method == 'POST':
        request.json["uid2"] = uid2
        return UsrController().unfollow(request.json)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/followedBy/<int:uid>', methods=['GET'])
def followedByUser(uid):
    if request.method == 'GET':
        return UsrController().followedBy(uid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/follows/<int:uid>', methods=['GET'])
def followsUser(uid):
    if request.method == 'GET':
        return UsrController().follows(uid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/posts', methods=['POST'])
def post():
    if request.method == 'POST':
        return MsgController().post(request.json, False)

@app.route('/MicrobloggingApp/msg/<int:mid>', methods=['GET'])
def msgByMId(mid):
    if request.method == 'GET':
        return MsgController().getMsgByMId(mid)
    return jsonify("Method not allowed"), 405


@app.route('/MicrobloggingApp/users/msg/<int:uid>', methods=['GET'])
def msgsByUId(uid):
    if request.method == 'GET':
        return MsgController().getMsgsByUId(uid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/users/msg/<string:uname>', methods=['GET'])
def msgsByUname(uname):
    if request.method == 'GET':
        return MsgController().getMsgsByUname(uname)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/msg')
def seeAllMsgs():
    return MsgController().getAllMsgs()

@app.route('/MicrobloggingApp/block/<int:uid2>', methods=['POST'])
def blockUser(uid2):
    if request.method == 'POST':
        request.json["uid2"] = uid2
        return UsrController().block(request.json)
    return jsonify("Method not allowed"), 405


@app.route('/MicrobloggingApp/unblock/<int:uid2>', methods=['POST'])
def unblockUser(uid2):
    if request.method == 'POST':
        request.json["uid2"] = uid2
        return UsrController().unblock(request.json)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/blockedBy/<int:uid>', methods=['GET'])
def blockedByUser(uid):
    if request.method == 'GET':
        return UsrController().blockedBy(uid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/blocking/<int:uid>', methods=['GET'])
def blockingUser(uid):
    if request.method == 'GET':
        return UsrController().blocking(uid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/reply', methods=['POST'])
def reply():
    if request.method == 'POST':
        return MsgController().reply(request.json)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/reply/msg/<int:repliesToid>', methods=['POST'])
def replyByMId(repliesToid):
    if request.method == 'POST':
        request.json["repliesToid"] = repliesToid
        return MsgController().reply(request.json)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/like/<int:mid>', methods=['POST','DELETE','GET'])
def like(mid):
    if request.method == 'POST':
        request.json["mid"] = mid
        MsgController().removeUnlike(request.json)
        return MsgController().like(request.json)
    elif request.method == 'DELETE':
        request.json["mid"] = mid
        return MsgController().removeLike(request.json)
    elif request.method == 'GET':
        return MsgController().getAllLikesByUsers(mid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/unlike/<int:mid>', methods=['POST','DELETE','GET'])
def unlike(mid):
    if request.method == 'POST':
        request.json["mid"] = mid
        MsgController().removeLike(request.json)
        return MsgController().unlike(request.json)
    elif request.method == 'DELETE':
        request.json["mid"] = mid
        return MsgController().removeUnlike(request.json)
    elif request.method == 'GET':
        return MsgController().getAllUnlikesByUsers(mid)
    return jsonify("Method not allowed"), 405

@app.route('/MicrobloggingApp/share', methods=['POST','DELETE','GET'])
def share():
    if request.method == 'POST':
        return MsgController().share(request.json)
    elif request.method == 'DELETE':
        return MsgController().unshare(request.json)
    elif request.method == 'GET':
        return MsgController().getShares(request.json)
    return jsonify("Method not allowed"), 405

if __name__ == '__main__':
    app.run(debug=True)
