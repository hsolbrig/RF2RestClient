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
#     Redistributions in binary form must reproduce the above copyright notice,
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

from utils.Proxy import Proxy

""" Common utilities for adding various flavors of concepts
"""


def valid_concept_add(url, changeset, effectivetime, parent, name, override=False):
    """
    :param url: URL of service
    :param changeset: Changeset name or URI.  If none, create one for this transaction
    :param effectivetime: Effective time for record. If none, use today
    :param parent: parent concept identifier. If None, do not validate
    :param name: concept name
    :param override: do not check for concept with same name existing
    :return: (urlproxy, fsn) or (None, error message)
    """
    # Make sure the url is valid and points at a RF2 service
    urlproxy = Proxy(url, changeset, effectivetime)
    if not urlproxy.ok:
        return None, "Invalid URL: %s" % url

    # Make sure the parent concept is valid
    if parent and not urlproxy.get('concept/%s' % parent).Concept.id:
        return None, "Invalid parent concept: %s" % parent

    # Create the FSN from the name and the base
    fsn = name + ' ' + urlproxy.get('concept/%s/base' % parent).val

    # Make sure FSN doesn't already exist
    r = urlproxy.get('descriptions/', matchalgorithm='exactmatch', matchvalue=fsn, maxtoreturn=0)
    if not r.ok:
        return None, "Server access error"
    if int(r.DescriptionList.numEntries) > 0:
        return None, "Concept with the FSN of %s already exists" % fsn

    # Make sure the name doesn't already exist
    if not override:
        r = urlproxy.get('descriptions/', matchalgorithm='exactmatch', matchvalue=name, maxtoreturn=0)
        if not r.ok:
            return None, "Server access error"
        if int(r.DescriptionList.numEntries) > 0:
            return None, "Concept with the same name (%s) already exists - use override flag to add" % name

    # Validate the changeset or create a new one if needed
    urlproxy.establish_changeset("Add%s" % Proxy.camelcase(name))
    if not urlproxy.ok:
        return None, "Changeset is not valid"
    
    return urlproxy, fsn

