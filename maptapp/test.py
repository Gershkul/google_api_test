# clientId: 650250597316-k3tbnc42edk6evvtrs97vm9iop289mr6.apps.googleusercontent.com
#client secret: kHz5cj3mZDePCUHUEs914V3S
import urllib3
import json, os
from oauth2client.service_account  import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build





# # r = http.request('GET', 'https://www.googleapis.com/fusiontables/v2/query?sql=SELECT%20*%20FROM%201L2MC8G8_HsloPzVPtajkBsWkC_bPQdL9BjVrwDjN&key=AIzaSyAsCTUUgf20880DF1y8B5WXLSQwi6Q79qw')
# # print(r.status)
# # print(r.data)
#
# fields = {
#     'address': 'trulala',
#     'Location': '-34.0116885991085000, 149.470214843750000'
# }
# urllib3.disable_warnings()
# data = {
#     'sql': 'INSERT INTO 1L2MC8G8_HsloPzVPtajkBsWkC_bPQdL9BjVrwDjN (address, Location) VALUES ("trulala", "-34.0116885991085000, 149.4470214843750000")',
#
# }

scopes = ['https://www.googleapis.com/auth/fusiontables']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test.json'
    ),
    scopes=scopes
)
http = Http()
credentials.authorize(http)
if not credentials.access_token:
    credentials.refresh(http)

print(credentials.access_token)

ft = build('fusiontables', 'v2', developerKey='AIzaSyAsCTUUgf20880DF1y8B5WXLSQwi6Q79qw', http=http)
tb = ft.query().sql(sql="insert into  1L2MC8G8_HsloPzVPtajkBsWkC_bPQdL9BjVrwDjN (address, Location) VALUES ('trulala', '-34.4767480034781000, 149.0944726562500000')").execute()

print(tb)

