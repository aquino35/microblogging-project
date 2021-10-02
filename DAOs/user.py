from config.dbconfig import pg_config
import psycopg2

class UsersDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
            pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = 'select * from users where is_Active = \'True\';'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getUserById(self, uid):
        cursor = self.conn.cursor()
        query = 'select * from "users" where uid = %s;'
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        self.conn.close()
        return result

    def updateUserById(self, fname, lname, uname, pword, email, phone, uage, uid):
        cursor = self.conn.cursor()
        query = 'update users set fname = %s,lname = %s,uname = %s,pword = %s,email = %s,phone = %s,uage = %s' \
                'where uid = %s returning *;'
        cursor.execute(query, (fname, lname, uname, pword, email, phone, uage, uid,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def getUserByUname(self, uname):
        cursor = self.conn.cursor()
        query = 'select * from "users" where uname = %s;'
        cursor.execute(query, (uname,))
        result = cursor.fetchone()
        return result

    def getUserByEmail(self, email):
        cursor = self.conn.cursor()
        query = 'select * from "users" where email = %s;'
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def register(self, fname, lname, uname, pword, email, phone, uage):
        cursor = self.conn.cursor()
        query = ('insert into users(fname,lname,uname,pword,email,phone,uage) '
                      'values (%s, %s, %s, %s, %s, %s, %s) returning uid;')
        cursor.execute(query, (fname, lname, uname, pword, email, phone, uage))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid

    def removeUser(self, uid):
        cursor = self.conn.cursor()
        query = 'update users set is_Active = \'false\' where uid = %s returning uid'
        cursor.execute(query, ([uid]))
        test = cursor.fetchone() is not None
        self.conn.commit()
        return test

    def follow(self, uid1, uid2):
        cursor = self.conn.cursor()
        query = 'insert into follows(uid1,uid2) values (%s, %s) returning uid1'
        cursor.execute(query, ([uid1, uid2]))
        uid1 = cursor.fetchone()[0]
        self.conn.commit()
        return uid1

    def unfollow(self, uid1, uid2):
        cursor = self.conn.cursor()
        query = 'delete from follows where (uid1 = %s and uid2 = %s);'
        cursor.execute(query, ([uid1, uid2]))
        self.conn.commit()
        return uid1

    def followedBy(self, uid):
        cursor = self.conn.cursor()
        query = 'select * from users inner join follows on follows.uid2 = users.uid where follows.uid1 = %s;'
        cursor.execute(query, ([uid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def follows(self, uid):
        cursor = self.conn.cursor()
        query = 'select * from users inner join follows on follows.uid1 = users.uid where follows.uid2 = %s;'
        cursor.execute(query, ([uid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def block(self, uid1, uid2):
        cursor = self.conn.cursor()
        query = 'insert into Blocked(uid1,uid2) values (%s, %s) returning uid1'
        cursor.execute(query, ([uid1, uid2]))
        uid1 = cursor.fetchone()[0]
        self.conn.commit()
        return uid1

    def unblock(self, uid1, uid2):
        cursor = self.conn.cursor()
        query = 'delete from Blocked where (uid1 = %s and uid2 = %s);'
        cursor.execute(query, ([uid1, uid2]))
        self.conn.commit()
        return uid1

    def blockedBy(self, uid):
        cursor = self.conn.cursor()
        query = 'select * from users inner join Blocked on Blocked.uid2 = users.uid where Blocked.uid1 = %s;'
        cursor.execute(query, ([uid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def blocking(self, uid):
        cursor = self.conn.cursor()
        query = 'select * from users inner join Blocked on Blocked.uid1 = users.uid where Blocked.uid2 = %s;'
        cursor.execute(query, ([uid]))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def is_Active(self, uid):
        cursor = self.conn.cursor()
        query = 'select is_Active from users where uid = %s'
        cursor.execute(query, [uid])
        is_Active = cursor.fetchone()[0]
        self.conn.commit()
        return is_Active

    def is_Blocking(self, uid1, uid2):
        cursor = self.conn.cursor()
        query = 'select uid1 from Blocked where uid1 = %s and uid2 = %s'
        cursor.execute(query, [uid1, uid2])
        is_Blocked = cursor.fetchone() is not None
        self.conn.commit()
        return is_Blocked