from config.dbconfig import pg_config
import psycopg2

class MsgDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
            pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2.connect(connection_url)

    def getAllMsgs(self):
        cursor = self.conn.cursor()
        query = 'select * from messages;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getMsgByMId(self, mid):
        cursor = self.conn.cursor()
        query = 'select * from messages where mid = %s;'
        cursor.execute(query, ([mid]))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def getMsgsByUId(self, uid):
        cursor = self.conn.cursor()
        query = 'select * from messages where uid = %s;'
        cursor.execute(query, ([uid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getMsgsByUname(self, uname):
        cursor = self.conn.cursor()
        query = 'select * from messages natural inner join users where uname =  %s;'
        cursor.execute(query, ([uname]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getAuthorid(self):
        return self.uid

# -- engagements of a msg (post,shares,likes,unlikes,shares)

    def post(self, uid, date, msg, is_Reply):
        self.uid = uid
        cursor = self.conn.cursor()
        replystr = str(is_Reply).lower()
        query = 'insert into messages(uid, date, msg, is_Reply) values (%s, %s, %s, %s) returning mid;'
        cursor.execute(query, ([uid, date, msg, replystr]))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        return mid

    def reply(self, replyid, repliesToid):
        cursor = self.conn.cursor()
        query = 'insert into replies(replyid, repliesToid) values (%s, %s)'
        cursor.execute(query, ([replyid, repliesToid]))
        self.conn.commit()

    def like(self, uid, mid):
        cursor = self.conn.cursor()
        query = 'insert into "likes"(uid,mid) values (%s, %s);'
        cursor.execute(query, ([uid,mid]))
        self.conn.commit()

    def getAllLikesByUsers(self, mid):
        cursor = self.conn.cursor()
        query = 'select uid from likes where mid = %s;'
        cursor.execute(query, ([mid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def removeLike(self, uid, mid):
        cursor = self.conn.cursor()
        query = 'delete from likes where (uid = %s and mid = %s);'
        cursor.execute(query, ([uid, mid]))
        self.conn.commit()

    def unlike(self, uid, mid):
        cursor = self.conn.cursor()
        query = 'insert into "unlikes"(uid,mid) values (%s, %s);'
        cursor.execute(query, ([uid,mid]))
        self.conn.commit()

    def getAllUnlikesByUsers(self, mid):
        cursor = self.conn.cursor()
        query = 'select uid from unlikes where mid = %s;'
        cursor.execute(query, ([mid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def removeUnlike(self, uid, mid):
        cursor = self.conn.cursor()
        query = 'delete from unlikes where (uid = %s and mid = %s);'
        cursor.execute(query, ([uid, mid]))
        self.conn.commit()

    def share(self, uid, mid):
        cursor = self.conn.cursor()
        query = 'insert into shares(uid,mid) values (%s, %s)'
        cursor.execute(query, ([uid, mid]))
        self.conn.commit()

    def unshare(self, uid, mid):
        cursor = self.conn.cursor()
        query = 'delete from shares where (uid = %s and mid = %s);'
        cursor.execute(query, ([uid, mid]))
        self.conn.commit()

    def getShares(self, mid):
        cursor = self.conn.cursor()
        query = 'select uid from shares where mid = %s;'
        cursor.execute(query, ([mid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getUidfromPost(self, mid):
        cursor = self.conn.cursor()
        query = 'select uid from messages where mid = %s;'
        cursor.execute(query, ([mid]))
        self.conn.commit()
        return cursor.fetchone()[0]
