from flask import jsonify
from DAOs.msg import MsgDao
from DAOs.user import UsersDao


class MsgController:

    def build_map_dic(self,row):
        result = {}
        result['mid'] = row[0]
        result['hasNotified'] = row[1]
        result['isReply'] = row[2]
        result['uid'] = row[3]
        result['date'] = row[4]
        result['msg'] = row[5]
        return result

    def __build_attr_dic(self, mid, uid, date , msg):
        result = {}
        result['mid'] = mid
        result['uid'] = uid
        result['date'] = date
        result['msg'] = msg
        return result

    def __build_reply_attr_dic(self, replyid, repliesToid):
        result = {}
        result['replyid'] = replyid
        result['repliesToid'] = repliesToid
        return result

    def getAllMsgs(self):
        dao = MsgDao()
        msg_list = dao.getAllMsgs()
        result_list = []
        for row in msg_list:
            obj = self.build_map_dic(row)
            result_list.append(obj)
        return jsonify(Messages = result_list)

    def getMsgByMId(self, mid):
        try:
            dao = MsgDao()
            msg = dao.getMsgByMId(mid)
            result = self.build_map_dic(msg)
            return jsonify(Message=result)
        except:
            return jsonify("Message does not exist"), 404

    def getMsgsByUId(self, uid):
        try:
            dao = MsgDao()
            msg_list = dao.getMsgsByUId(uid)
            result_list = []
            for row in msg_list:
                obj = self.build_map_dic(row)
                result_list.append(obj)
            return jsonify(Messages=result_list)
        except:
            return jsonify("User does not exist"), 404

    def getMsgsByUname(self, uname):
        try:
            dao = MsgDao()
            msg_list = dao.getMsgsByUname(uname)
            result_list = []
            for row in msg_list:
                obj = self.build_map_dic(row)
                result_list.append(obj)
            return jsonify(Messages=result_list)
        except:
            return jsonify("Username does not exist"), 404

    # -- engagements of a msg (post,shares,likes,unlikes,shares)

    def post(self, json, is_Reply):
        if json is None or len(json) != 3:
            return jsonify(Error=" Malformed result"), 200
        try:
            uid = json['uid']
            date = json['date']
            msg = json['msg']
            udao = UsersDao()
            if not udao.is_Active(uid):
                return jsonify("Inactive users cannot post"), 403
            dao = MsgDao()
            mid = dao.post(uid, date, msg, is_Reply)
            json['mid'] = mid
            return jsonify(Message = json), 201
        except:
            return jsonify(Error = "Incorrect parameters inserted"), 400

    def reply(self, json, repliesToid = None):
        udao = UsersDao()
        dao = MsgDao()

        if not udao.is_Active(json['uid']):
            return jsonify("Inactive users cannot reply"), 403
        if (udao.is_Blocking(json['uid'],dao.getUidfromPost(json['repliesToid'])) or
                udao.is_Blocking(dao.getUidfromPost(json['repliesToid']),json['uid'])):
            return jsonify("Cannot interact with blocked users or users blocking you"), 403

        if json is None or len(json) != 4:
            return jsonify(Error=" Malformed result"), 200
        try:
            if (repliesToid is None):
                repliesToid = json.pop("repliesToid")
            midResponse = self.post(json, True)
            midstr = str(midResponse[0].get_data())
            midint = int(midstr[midstr.find("\"mid\"")+7: midstr.find(",", midstr.find("\"mid\""))])
            replyid = int(midint)
            rid = dao.reply(replyid, repliesToid)
            result = self.__build_reply_attr_dic(replyid, repliesToid)
            return jsonify(Message = result), 201
        except:
            return jsonify(Error = "Incorrect parameters inserted"), 400

    def usr_engagement_dic(self, row):
        result = {}
        result['uid'] = row[0]
        return result

    def __build_engagement_attr_dic(self, mid, uid):
        result = {}
        result['mid'] = mid
        result['uid'] = uid
        return result

    def like(self, json):
        if json is None or len(json) != 2:
            return jsonify(Error= "Malformed result"), 200
        try:
            uid = json['uid']
            mid = json['mid']

            udao = UsersDao()
            dao = MsgDao()
            if not udao.is_Active(uid):
                return jsonify("Inactive users cannot like or unlike posts"), 403
            if (udao.is_Blocking(json['uid'], dao.getUidfromPost(mid)) or
                    udao.is_Blocking(dao.getUidfromPost(mid), json['uid'])):
                return jsonify("Cannot interact with blocked users or users blocking you"), 403
            if dao.getMsgByMId(mid) is None:
                return jsonify("Message not found"), 404

            dao.like(uid, mid)
            return jsonify("Like inserted succesfully"), 201
        except:
            return jsonify(Error="Incorrect parameters inserted or "
                                 "User has already liked this message"), 400

    def getAllLikesByUsers(self, mid):
        dao = MsgDao()
        if dao.getMsgByMId(mid) is None:
            return jsonify("Message not found"), 404
        usr_list = dao.getAllLikesByUsers(mid)
        result_list = []
        for row in usr_list:
            obj = self.usr_engagement_dic(row)
            result_list.append(obj)
        return jsonify(Users=result_list)

    def removeLike(self, json):
        if json is None or len(json) != 2:
            return jsonify(Error= "Malformed result"), 200
        try:
            uid = json['uid']
            mid = json['mid']

            udao = UsersDao()
            dao = MsgDao()
            if not udao.is_Active(uid):
                return jsonify("Inactive users cannot like or unlike posts"), 403
            if dao.getMsgByMId(mid) is None:
                return jsonify("Message not found"), 404

            dao.removeLike(uid, mid)
            return jsonify("Removed like succesfully"), 201
        except:
            return jsonify(Error = "Incorrect parameters inserted,  "
                                   "User has already disliked this message"), 400

    def unlike(self, json):
        if json is None or len(json) != 2:
            return jsonify(Error= "Malformed result"), 200
        try:
            uid = json['uid']
            mid = json['mid']

            udao = UsersDao()
            dao = MsgDao()
            if not udao.is_Active(uid):
                return jsonify("Inactive users cannot like or unlike posts"), 403
            if dao.getMsgByMId(mid) is None:
                return jsonify("Message not found"), 404

            dao.unlike(uid, mid)
            return jsonify("Unlike inserted succesfully"), 201
        except:
            return jsonify(Error="Incorrect parameters inserted or "
                                 "User has already disliked this message"), 400

    def getAllUnlikesByUsers(self, mid):
        dao = MsgDao()
        if dao.getMsgByMId(mid) is None:
            return jsonify("Message not found"), 404
        usr_list = dao.getAllUnlikesByUsers(mid)
        result_list = []
        for row in usr_list:
            obj = self.usr_engagement_dic(row)
            result_list.append(obj)
        return jsonify(Users=result_list)

    def removeUnlike(self, json):
        if json is None or len(json) != 2:
            return jsonify(Error= "Malformed result"), 200
        try:
            uid = json['uid']
            mid = json['mid']

            udao = UsersDao()
            dao = MsgDao()
            if not udao.is_Active(uid):
                return jsonify("Inactive users cannot like or unlike posts"), 403
            if dao.getMsgByMId(mid) is None:
                return jsonify("Message not found"), 404

            dao.removeUnlike(uid, mid)
            return jsonify("Removed like succesfully"), 201
        except:
            return jsonify(Error = "Incorrect parameters inserted,  "
                                   "User has already disliked this message"), 400

    def share(self, json):
        if json is None or len(json) != 2:
            return jsonify(Error= "Malformed result"), 200
        try:
            uid = json['uid']
            mid = json['mid']

            udao = UsersDao()
            dao = MsgDao()
            if not udao.is_Active(uid):
                return jsonify("Inactive users cannot share"), 403
            if (udao.is_Blocking(json['uid'], dao.getUidfromPost(mid)) or
                    udao.is_Blocking(dao.getUidfromPost(mid), json['uid'])):
                return jsonify("Cannot interact with blocked users or users blocking you"), 403
            if dao.getMsgByMId(mid) is None:
                return jsonify("Message not found"), 404

            dao.share(uid, mid)
            return jsonify("Post has been shared succesfully"), 201
        except:
            return jsonify(Error="Incorrect parameters inserted or "
                                 "User has already shared this message"), 400

    def unshare(self, json):
        if json is None or len(json) != 2:
            return jsonify(Error= "Malformed result"), 200
        try:
            uid = json['uid']
            mid = json['mid']

            udao = UsersDao()
            dao = MsgDao()
            if not udao.is_Active(uid):
                return jsonify("Inactive users cannot unshare"), 403
            if dao.getMsgByMId(mid) is None:
                return jsonify("Message not found"), 404

            dao.unshare(uid, mid)
            return jsonify("Unshared succesfully"), 201
        except:
            return jsonify(Error = "Incorrect parameters inserted,  "
                                   "User has already disliked this message"), 400

    def getShares(self, json):
        mid = json['mid']
        dao = MsgDao()
        if dao.getMsgByMId(mid) is None:
            return jsonify("Message not found"), 404
        usr_list = dao.getShares(mid)
        result_list = []
        for row in usr_list:
            obj = self.usr_engagement_dic(row)
            result_list.append(obj)
        return jsonify(Shares=result_list)
    