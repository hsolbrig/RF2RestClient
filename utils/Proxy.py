# -*- coding: utf-8 -*-
# Copyright (c) 2014, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the <ORGANIZATION> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
import requests
from time import gmtime, strftime

from utils.JSONWrapper import JSONWrapper


class Proxy:
    """ REST proxy for RF2 Changesets
    """

    def __init__(self, url, changeset, effectivetime, debugging=False):
        """
        @param url: Base URL of REST service (example:  http://service.org/rf2)
        @param changeset: Name or UUID of an existing changeset or None if this is an atomic operation
        """
        self._debugging = debugging
        self.ok, self._url, self.changeset, self._effectivetime = False, url, None, None
        r = self.get('status')
        self.rf2_release = r.val.rf2_release if r.ok else None
        self.changeset, self.locked = changeset, 0
        self._commitRequired = changeset is None
        self._effectivetime = effectivetime if effectivetime else strftime("%Y%m%d", gmtime())

    def establish_changeset(self, csname):
        """ Establish the changeset context for subsequent operations
        :param csname: Change set name if it needs to be created.  None means use server default
        """
        if self.changeset:
            r = self.get('changeset/')
        else:
            r = self.post('changeset', csname=csname)
        self.changeset, self.locked = (r.ChangeSetReferenceSetEntry.referencedComponentId.uuid,
                                       1 if r.ChangeSetReferenceSetEntry.isFinal == 0 else 0) if r.ok else (None, None)

    def get(self, root, **args):
        if self._debugging:
            print("GET ", end='')
        return self._doaccess(requests.get, root, **args)

    def post(self, root, **args):
        if self._debugging:
            print("POST ", end='')
        return self._doaccess(requests.post, root, **args)

    def put(self, root, **args):
        if self._debugging:
            print("PUT ", end='')
        return self._doaccess(requests.put, root, **args)

    def delete(self, root, **args):
        if self._debugging:
            print("DELETE ", end='')
        try:
            r = requests.delete(self._urlfor(root), params=args)
            return r
        except requests.ConnectionError as e:
            print(e.strerror, file=sys.stderr)
        return JSONWrapper(None, 200)

    def commit(self, force=False):
        """ Commit the changeset if we're doing a one shot
        @return: changeset id that was commited or None if it wasn't needed
        """
        if self._commitRequired or force:
            return self.put('changeset/%s/commit' % self.changeset).ok
        return None

    def rollback(self, force=False):
        """ Rollback the changeset because an error occurred.  Can only be done on one shots
        """
        if self._commitRequired or force:
            return self.delete('changeset/%s' % self.changeset)
            # TODO manually undo the changes if we can't use the rollback mechanism

    @staticmethod
    def camelcase(text):
        return ''.join(x.capitalize() for x in text.split(' '))

    def changeset_info(self):
        return '\t' + str(self.changeset) + '\t' + str(self.locked)

    def _urlfor(self, root, format_='json', parms=None):
        """ URL constructor
        @param root: base URL
        @param format_: return format
        @return:
        """
        rval = self._url + '/' + root + "?bypass=1&format=" + format_ + \
            (('&effectiveTime=%s' % self._effectivetime) if self._effectivetime else '') + \
            (('&changeset=%s' % self.changeset) if self.changeset else '')
        if self._debugging:
            print(rval + '&' + ('&'.join('%s=%s' % (k, ' '.join(v) if isinstance(v, list) else v)
                                         for k, v in (parms.items() if parms else {}))))
        return rval

    def _doaccess(self, op, root, format='json', **args):
        """ REST access with error handling
        @param op: requests function to invoke
        @param root: root URL
        @param format_:  expected return format
        @param args: arguments to add to line
        @return: JSON wrapper
        """
        try:
            response = op(self._urlfor(root, format_=format, parms=args), params=args)
            if self._debugging:
                print("%s: %s" % (response.status_code, response.reason))
            return self._rslt(response) if format == "json" else response
        except requests.ConnectionError as e:
            print(str(e), file=sys.stderr)
            return self._rslt(None)

    def _rslt(self, response):
        """ Evaluate the response data
        @param response: http response
        @return: python wrapper for resulting data or None if an error ocurred
        """
        if not response or not response.ok:
            self.ok = False
            data = None
            if self._debugging:
                print("No response" if not response else "%s: %s" % (response.status_code, response.reason),
                      file=sys.stderr)
                if response is not None:
                    print(response.content.decode())
        else:
            self.ok = True
            data = response.json()
            if self._debugging:
                print("%s: %s" % (response.status_code, response.reason))
        return JSONWrapper(data, response.status_code if response else 404)
