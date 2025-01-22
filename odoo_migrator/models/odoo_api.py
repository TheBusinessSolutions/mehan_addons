import xmlrpc.client


class OdooApi:

    def __init__(self, host, database, username, password):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.host))
        self.db = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.host))
        self.uid = self.common.authenticate(self.database, self.username, self.password, {})

    def getVersion(self):
        print(self.common.version())

    def getUid(self):
        print(self.uid)

    def checkAccessRights(self):
        print(self.db.execute_kw(self.database, self.uid, self.password,
                                  'res.partner', 'check_access_rights', ['read'],
                                {'raise_exception': False}))

    def search1(self, model, conditions):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'search', conditions)

    def search2(self, model, conditions, fields):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'search_read', conditions,
                                  {'fields': fields})

    def search3(self, model, conditions, offset=0):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'search', conditions, {'offset': offset})

    def search4(self, model, conditions, fields, offset=0):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'search_read', conditions,
                                  {'fields': fields, 'offset': offset})

    def search5(self, model, conditions, offset=0, limit=5):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'search', conditions,
                                  {'offset': offset, 'limit': limit})

    def search6(self, model, conditions, fields, offset=0, limit=0):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'search_read', conditions,
                                  {'fields': fields, 'offset': offset, 'limit': limit})

    def count(self, model, conditions):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'search_count', conditions)





    def read(self, model, ids, fields):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'read', [ids], {'fields':fields})

    def create(self, model, data):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'create', [data])

    def delete(self, model, ids):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'unlink', [ids])
    def button_immediate_uninstall(self, model, ids):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'button_immediate_uninstall', [ids])

    def update(self, model, id, new_data):
        self.db.execute_kw(self.database, self.uid, self.password, model, 'write', [[id], new_data])
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'name_get', [[id]])

    def getMetaData(self, model, ids, attributes):
        return self.db.execute_kw(self.database, self.uid, self.password, model, 'fields_get', ids,
                                  {'attributes': attributes})
