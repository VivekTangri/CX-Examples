import json

import logging
from ldap3 import Server, Connection

from proxy.response import Response
from resources.base import Resource


log = logging.getLogger(__name__)

class EDirUsersResource(Resource):
    def __init__(self, service):
        super().__init__(service)

    def create_user(self, request):
        log.info("Create user body:{}".format(request.data))
        data = json.loads(request.data)        
        
        server = Server('10.120.46.80')
        conn = Connection(server, "cn=zgrossbart,ou=services,o=corp", "N0v3ll123")
        conn.bind()
        attrs = {}
        attrs['cn'] = 'zacktest'
        attrs['sn'] = data["sName"]
        attrs['userPassword'] = data["password"]
        attrs['mail'] = data["email"]
        attrs['postalCode'] = data["postalCode"]
        attrs['fullName'] = data["fName"] + ' ' + data["sName"]
        attrs['givenName'] = data["fName"]
        attrs['description'] = data["description"]
        dn = "cn=zacktest,ou=SA,ou=CanadaLife,o=corp"
        result = conn.add(dn, ','.join(['inetOrgPerson']), attrs)
        
        if result:
            return Response(json.dumps({"result": True}), headers={'Content-type': 'application/json'})
            
        log.error('Failed to add user: {}'.format(conn.result))
        return Response(json.dumps({"result": False, "error": conn.result}),
                        headers={'Content-type': 'application/json'}, status_code=500)
