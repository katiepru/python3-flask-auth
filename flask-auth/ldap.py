from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC, \
        STRATEGY_ASYNC_THREADED, SEARCH_SCOPE_WHOLE_SUBTREE, GET_ALL_INFO, Tls

class LDAP:

    def __init__(self, ldap_args, logger=None):
        """Set up LDAP object. Throws exceptions on invalid config"""

        required_fields = ['host', 'port', 'uid', 'encryption', 'base_dn']
        optional_fields = ['bind_dn', 'bind_pass']

        for field in required_fields:
            setattr(self, field, ldap_args[field] or raise_KeyError(msg='%s \
                cannot be None' % (field)))

        for field in optional_fields:
            setattr(self, field, ldap_args[field])

        self.setUp()

    def authenticate(self, username, password):
        self.start_conn(self.conn_init)
        self.conn_init.bind()

        user_conn = Connection(self.server, auto_bind=False,
                client_strategy=STRATEGY_SYNC, user='%s=%s,%s' % (self.uid,
                username, self.base_dn), password = password)
        self.start_conn(user_conn)
        res = user_conn.bind()

        e = user_conn.last_error

        user_conn.unbind()
        self.conn_init.unbind()

        return (res, e)

    def setUp(self):
        if self.encryption == 'ssl':
            self.server = Server(self.host, port=self.port,
                    get_info=GET_ALL_INFO, use_ssl=True)
        elif self.encryption == 'tls':
            #TODO: Cert stuff
            self.server = Server(self.host, port=self.port,
                    get_info=GET_ALL_INFO, tls=Tls())
        else:
            self.server = Server(self.host, port=self.port,
                    get_info=GET_ALL_INFO)

        # Set up initial connection
        if self.bind_dn:
            # Simple auth
            self.conn_init = Connection(self.server, auto_bind=False,
                    client_strategy=STRATEGY_SYNC, user=self.bind_dn,
                    password=self.bind_pass)
        else:
            # Anonymous bind
            self.conn_init = Connection(self.server, auto_bind=False,
                    client_strategy=STRATEGY_SYNC)


    def start_conn(self, conn):
        conn.open()

        if self.encryption == 'tls':
            conn.start_tls()

    def raise_KeyError(msg=''):
        raise KeyError(msg)
