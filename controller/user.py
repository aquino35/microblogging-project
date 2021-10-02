from flask import jsonify
from DAOs.user import UsersDao

class UsrController:

    def build_map_dic(self, row):
        result = {}
        result['uid'] = row[0]
        result['fname'] = row[1]
        result['lname'] = row[2]
        result['uname'] = row[3]
        result['pword'] = row[4]
        result['email'] = row[5]
        result['phone'] = row[6]
        result['uage'] = row[7]
        result['is_Active'] = row[8]
        return result

    def __build_attr_dic(self, uid, fname, lname, uname, pword, email, phone, uage):
        result = {}
        result['uid'] = uid
        result['fname'] = fname
        result['lname'] = lname
        result['uname'] = uname
        result['pword'] = pword
        result['email'] = email
        result['phone'] = phone
        result['uage'] = uage
        return result

    def getAllUsers(self):
        dao = UsersDao()
        usr_list = dao.getAllUsers()
        result_list = []
        for row in usr_list:
            obj = self.build_map_dic(row)
            result_list.append(obj)
        return jsonify(Users = result_list)

    def getUserById(self, uid):
        dao = UsersDao()
        usr_tupple = dao.getUserById(uid)
        if not usr_tupple:
            return jsonify("Not found"), 404
        else:
            result = self.build_map_dic(usr_tupple)
            return jsonify(User=result), 200

    def updateUserById(self, json):
        if json == None or len(json) != 2:
            return jsonify(Error= "Malformed result"), 200
        try:
            json_body = json[0].values()
            body = list(json_body)
            fname = body[0]
            lname = body[1]
            uname = body[2]
            pword = body[3]
            email = body[4]
            phone = body[5]
            uage = body[6]
            uid = json[1]
            uid = list(uid.values())
            dao = UsersDao()
            usr_tupple = dao.updateUserById(fname, lname, uname, pword, email, phone, uage, uid[0])
            if not usr_tupple:
                return jsonify("Not found"), 404
            else:
                result = self.build_map_dic(usr_tupple)
                return jsonify(User=result), 200
        except:
            return jsonify(Error="Incorrect parameters inserted or "
                                 "ID not found"), 400

    def getUserByUname(self, uname):
        dao = UsersDao()
        usr_tupple = dao.getUserByUname(uname)
        if not usr_tupple:
            return jsonify("Not found"), 404
        else:
            result = self.build_map_dic(usr_tupple)
            return jsonify(User=result), 200

    def getUserByEmail(self, email):
        dao = UsersDao()
        usr_tupple = dao.getUserByEmail(email)
        if not usr_tupple:
            return jsonify("Not found"), 404
        else:
            result = self.build_map_dic(usr_tupple)
            return jsonify(User=result), 200

    def register(self, json):
        fname = json['fname']
        lname = json['lname']
        uname = json['uname']
        pword = json['pword']
        email = json['email']
        phone = json['phone']
        uage = json['uage']
        dao = UsersDao()
        uid = dao.register(fname, lname, uname, pword, email, phone, uage)
        result = self.__build_attr_dic(uid, fname, lname, uname, pword, email, phone, uage)
        return jsonify(User = result), 201

    def removeUser(self, uid):
        dao = UsersDao()
        successful = dao.removeUser(uid)
        if not dao.is_Active(uid):
            return jsonify("User already removed"), 403
        if not successful:
            return jsonify("Not found"), 404
        else:
            return jsonify("User removed succesfully"), 200

    def follow(self, json):
        try:
            uid1 = json['uid1']
            uid2 = json['uid2']
            dao = UsersDao()
            if not dao.is_Active(uid1) or not dao.is_Active(uid2):
                return jsonify("Inactive users cannot follow or be followed"), 403
            if dao.is_Blocking(uid1,uid2) or dao.is_Blocking(uid2, uid1):
                return jsonify("Cannot follow blocked user or blocking user"), 403
            fid = dao.follow(uid1, uid2)
            return jsonify(Followed=f"User {uid2} followed by {uid1}"), 200
        except:
            return jsonify("Incorrect parameters or user is already followed"), 400

    def unfollow(self, json):
        try:
            uid1 = json['uid1']
            uid2 = json['uid2']
            dao = UsersDao()
            if not dao.is_Active(uid1) or not dao.is_Active(uid2):
                return jsonify("Inactive users cannot unfollow or be unfollowed"), 403
            fid = dao.unfollow(uid1, uid2)
            return jsonify(Unfollowed=f"User {uid2} unfollowed by {uid1}"), 200
        except:
            return jsonify("Incorrect parameters or user is not followed"), 400

    def followedBy(self, uid):
        dao = UsersDao()
        follow_list = dao.followedBy(uid)
        result_list = []
        for row in follow_list:
            obj = self.build_map_dic(row)
            result_list.append(obj)
        return jsonify(FollowedBy = result_list), 200

    def follows(self, uid):
        dao = UsersDao()
        follow_list = dao.follows(uid)
        result_list = []
        for row in follow_list:
            obj = self.build_map_dic(row)
            result_list.append(obj)
        return jsonify(Follows = result_list), 200

    def block(self, json):
        try:
            uid1 = json['uid1']
            uid2 = json['uid2']
            dao = UsersDao()
            if not dao.is_Active(uid1) or not dao.is_Active(uid2):
                return jsonify("Inactive users cannot block or be blocked"), 403
            bid = dao.block(uid1, uid2)
            dao.unfollow(uid1, uid2)
            dao.unfollow(uid2,uid1)
            return jsonify(Blocked = f"User {uid2} blocked by {uid1}"), 200
        except:
            return jsonify("Incorrect parameters or user is already blocked"), 400

    def unblock(self, json):
        try:
            uid1 = json['uid1']
            uid2 = json['uid2']
            dao = UsersDao()
            if not dao.is_Active(uid1) or not dao.is_Active(uid2):
                return jsonify("Inactive users cannot unblock or be unblocked"), 403
            bid = dao.unblock(uid1, uid2)
            return jsonify(Unblocked=f"User {uid2} unblocked by {uid1}"), 200
        except:
            return jsonify("Incorrect parameters or user is not blocked"), 400

    def blockedBy(self, uid):
        dao = UsersDao()
        blocker_list = dao.blockedBy(uid)
        result_list = []
        for row in blocker_list:
            obj = self.build_map_dic(row)
            result_list.append(obj)
        return jsonify(BlockedBy = result_list), 200

    def blocking(self, uid):
        dao = UsersDao()
        follow_list = dao.blocking(uid)
        result_list = []
        for row in follow_list:
            obj = self.build_map_dic(row)
            result_list.append(obj)
        return jsonify(Blocking=result_list), 200
