class User(object):
    def __init__(self, name, secret_key, able_to=lambda x: True,
                 open_sections=['AbnormalPlayers', 'ChatMonitor', 'SpamModel', 'PostgresStats']):
        self.name = name
        self.secret_key = secret_key
        self.able = able_to
        self.open_sections = open_sections

    def able_to(self, protocol):
        return self.able(protocol)


__all__ = ['User', 'Users']

Users = {
    "lu": User("lu", "8262dec64d4649c8285dcd0c9f3bf8962f98bc3f571a44120bdafd08c6d95d7f"),
    "c19": User("c19", "95ff38af9a2edb7bbcb94baace11ad933192dfe8c40218c9964706839bd8a5e7")
}