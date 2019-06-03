#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, urllib, operator
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

URI_PREFIX='/api/arsys/v1/entry'
RESULT_STATUS          = 200
RECORD_CREATED_STATUS  = 201
RECORD_UPDATED_STATUS  = 204


class RemedyClient(object):
    def __init__(self, httpConnection, username=None, password=None):
        self.headers        = {}
        self.accessToken    = None
        self.httpConnection = httpConnection

        self.username = username if username else httpConnection['username']
        self.password = password if password else httpConnection['password']
        
        # clear username/password so underlying library doesn't try to do basic authentication
        del httpConnection['username']
        del httpConnection['password']

        self.httpRequest = HttpRequest(self.httpConnection)

        self.issue_token()

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return RemedyClient(httpConnection, username, password)

    # see https://docs.bmc.com/docs/display/public/ars9000/Login+information
    def issue_token(self):
        api_url = '/api/jwt/login';
        form_data = urllib.urlencode({'username': self.username, 'password': self.password});
        response = self.httpRequest.post(api_url, body=form_data, contentType='application/x-www-form-urlencoded', headers = {'Accept': 'text/plain'})

        if response.getStatus() != RESULT_STATUS:
            self.throw_error(response)

        token = response.getResponse()
        self.headers['Authorization'] = 'AR-JWT ' + token

    # task functions -----------------------------------------------------------
    def verify_connection(self):
        '''
        Remedy AR Common Forms

        HPD:IncidentInterface_Create - to create or submit new incident
        HPD:IncidentInterface - to perform SEARCH,READ,UPDATE/MODIFY on existing incident
        CHG:ChangeInterface - to create change request
        CHG:ChangeInterface_Create - update and modify change request
        CHG:CRQ:Worklog - for work Info/log
        HPD:INC:Worklog - for Incident work log
        '''
        self.query_entrys('User', '')

    # https://docs.bmc.com/docs/pages/releaseview.action?pageId=517036472#id-/entry/{formName}-Createanentry
    def create_entry(self, form_name, form_data):
        remedy_api_url = '%s/%s' % (URI_PREFIX, form_name)
 
        entry_str = '''{
            "values": %s
        }''' % form_data
 
        response = self.httpRequest.post(remedy_api_url, body=entry_str.encode('utf-8'), contentType='application/json; charset=utf-8', headers = self.headers)
 
        if response.getStatus() in [RECORD_CREATED_STATUS, RECORD_UPDATED_STATUS]: # both can be returned according to the api docs
            location = response.getHeaders()["Location"]
            print "Entry created, url [%s]" % location
            return location.split('/')[-1]
        else:
            print "create_entry error %s" % (response)
            self.throw_error(response)

    # https://docs.bmc.com/docs/pages/releaseview.action?pageId=517036478#id-/entry/{formName}/{entryId}-Updateanentry
    def update_entry(self, form_name, entry_id, form_data):
        remedy_api_url = '%s/%s/%s' % (URI_PREFIX, form_name, entry_id)

        entry_str = '''{
            "values": %s
        }''' % form_data

        response = self.httpRequest.put(remedy_api_url, body=entry_str.encode('utf-8'), contentType='application/json; charset=utf-8', headers = self.headers)

        if response.getStatus() == RECORD_UPDATED_STATUS:
            return self.get_entry(form_name, entry_id)
        else:
            print "update_entry error %s" % (response)
            self.throw_error(response)

    # https://docs.bmc.com/docs/pages/releaseview.action?pageId=517036478#id-/entry/{formName}/{entryId}-Getsingleentry
    def get_entry(self, form_name, entry_id):
        # example: /api/arsys/v1/entry/SimpleForm/000000000000103
        remedy_api_url = '%s/%s/%s' % (URI_PREFIX, form_name, entry_id)
        response = self.httpRequest.get(remedy_api_url, contentType='application/json; charset=utf-8', headers = self.headers)

        if response.getStatus() == RESULT_STATUS:
            data = json.loads(response.getResponse())
            print 'Remedy response is: %s' % data
            return data['values']
        else:
            print "get_entry error %s" % (response)
            self.throw_error(response)

    # https://docs.bmc.com/docs/pages/releaseview.action?pageId=517036478#id-/entry/{formName}/{entryId}-Getsingleentry
    def get_change_request(self, form_name, change_id):
        # example: /api/arsys/v1/entry/CHG:ChangeInterface?q=%27Infrastructure%20Change%20ID%27%3d%22CRQ000000152848%22
        remedy_api_url = '%s/%s?q=%%27Infrastructure%%20Change%%20ID%%27%%3d%%22%s%%22' % (URI_PREFIX, form_name, change_id)
        print 'Remedy CR API is: %s' % remedy_api_url
        response = self.httpRequest.get(remedy_api_url, contentType='application/json; charset=utf-8', headers = self.headers)

        if response.getStatus() == RESULT_STATUS:
            data = json.loads(response.getResponse())['entries']
            print 'Remedy response is: %s' % data
            return map(operator.itemgetter('values'), data)
        else:
            print "get_entry error %s" % (response)
            self.throw_error(response)

    # https://docs.bmc.com/docs/pages/releaseview.action?pageId=517036472#id-/entry/{formName}-GETmultipleentries
    def query_entrys(self, form_name, query):
        remedy_api_url = '%s/%s?q=%s' % (URI_PREFIX, form_name, urllib.quote_plus(query))
        response = self.httpRequest.get(remedy_api_url, contentType='application/json; charset=utf-8', headers = self.headers)

        if response.getStatus() == RESULT_STATUS:
            data = json.loads(response.getResponse())['entries']
            return map(operator.itemgetter('values'), data)
        else:
            print "query_entrys error %s" % (response)
            self.throw_error(response)

    # Utility functions ========================================================
    def throw_error(self, response):
        print "Error from Remedy, HTTP Return: %s\n" % (response.getStatus())
        print "Detailed error: %s\n" % response.getResponse()
        sys.exit([response.getStatus(), response.getResponse()])
