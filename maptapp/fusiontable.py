import os
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/fusiontables']
API_NAME = 'fusiontables'
API_VERSION = 'v2'

class Fusiontable:
    """
    the adapter for Google Fusion Tables API, was implemented by Active Record pattern,
    """
    def __init__(self, options, data=None):
        if data:
            self.lat = data.get('lat')
            self.lng = data.get('lng')
            self.address = data.get('address')
        self.__init_service(options)
        self.table_id = options.get('table_id')

    def __init_service(self, options):
        """
        Initializing the service for Google API and authorizing for permitions confirmation
        :param options:
        :return:
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'test.json'
            ),
            scopes=SCOPES
        )
        http = Http()
        credentials.authorize(http)
        if not credentials.access_token:
            credentials.refresh(http)
        self.service = build(API_NAME, API_VERSION, developerKey=options.get('api_key'), http=http)

    @property
    def location(self):
        """
        :return location string:
        """
        return '{}, {}'.format(self.lat, self.lng)

    @property
    def already_exists(self):
        sql = "Select * from {} where address = '{}'".format(self.table_id, self.address)
        result = self.service.query().sql(sql=sql).execute()
        return result is None

    def save(self):
        """
        save new address into Fusion Table
        :return bool:
        """
        sql = "insert into {} (address, Location) values ('{}', '{}')".\
            format(self.table_id, self.address, self.location)
        result = self.service.query().sql(sql=sql).execute()
        return int(result.get('rows')[0][0]) > 0

    def delete_all(self):
        """
        clearing Fusion Table
        :return bool:
        """
        sql = "delete from {}".format(self.table_id)
        result = self.service.query().sql(sql=sql).execute()
        return result.get('rows')[0][0] == 'all rows'

