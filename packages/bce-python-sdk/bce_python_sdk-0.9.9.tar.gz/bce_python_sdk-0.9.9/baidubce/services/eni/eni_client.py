# -*- coding: utf-8 -*-

# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
#  of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions
# and limitations under the License.
"""
This module provides a client class for ENI.
"""

import copy
import json
import logging
import uuid

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import utils
from baidubce.utils import required
from baidubce import compat

_logger = logging.getLogger(__name__)


class EniClient(bce_base_client.BceBaseClient):
    """
    ENI base sdk client
    """

    prefix = b'/v1'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if headers is None:
            headers = {b'Accept': b'*/*', b'Content-Type': b'application/json;charset=utf-8'}
        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, EniClient.prefix + path, body, headers, params)

    @required(name=(bytes, str), subnet_id=(bytes, str), security_group_ids=list, 
              enterprise_security_group_ids=list, eni_ip_address_list=list, eni_ipv6_address_list=list)
    def create_eni(self, name, subnet_id, security_group_ids=None, enterprise_security_group_ids=None,
                   eni_ip_address_list=None, eni_ipv6_address_list=None, description=None, 
                   client_token=None, config=None):
        """
        :param name:
            The name of eni to be created.
        :type name: string

        :param subnet_id:
            The parameter to specify the id of subnet from vpc
        :type subnet_id: string

        :param security_group_ids:
            security_group_ids
        :type security_group_ids: list<string>

        :param enterprise_security_group_ids:
            enterprise_security_group_ids
        :type enterprise_security_group_ids: list<string>

        :param eni_ip_address_list:
            The parameter to specify the ipv4 address list of eni
        :type eni_ip_address_list: eni_model.EniIPSet

        :param eni_ipv6_address_list:
            The parameter to specify the ipv6 address list of eni
        :type eni_ip_address_list: eni_model.EniIPSet

        :param description:
            The description of the eni.
        :type description: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/eni'
        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {
            'name': compat.convert_to_string(name),
            'subnetId': compat.convert_to_string(subnet_id),
        }
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if enterprise_security_group_ids is not None:
            body['enterpriseSecurityGroupIds'] = enterprise_security_group_ids
        if eni_ip_address_list is not None:
            pri_ip_set = []
            for ip_set in eni_ip_address_list:
                pri_ip_set.append({"publicIpAddress":ip_set.public_ip, "primary":ip_set.primary,
                                   "privateIpAddress":ip_set.private_ip})
            body['privateIpSet'] = pri_ip_set
        if eni_ipv6_address_list is not None:
            pri_ipv6_set = []
            for ip_set in eni_ipv6_address_list:
                pri_ipv6_set.append({"publicIpAddress":ip_set.public_ip, "primary":ip_set.primary,
                                     "privateIpAddress":ip_set.private_ip})
            body['ipv6PrivateIpSet'] = pri_ipv6_set
        if description is not None:
            body['description'] = compat.convert_to_string(description)

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params,
                                  config=config)
    
    @required(eni_id=(bytes, str))
    def delete_eni(self, eni_id, client_token=None, config=None):
        """
        release the eni(delete operation)
        if the eni has been bound, must unbind before releasing.

        :type eni_id: string
        :param eni_id: eni to be released

        :type client_token: string
        :param client_token: if the clientToken is not specified by the user,
         a random String generated by default algorithm will be used.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }
        return self._send_request(http_methods.DELETE, path, params=params,
                                  config=config)

    @required(eni_id=(bytes, str), name=(bytes, str))
    def update_eni(self, eni_id, name=None, description=None, client_token=None, config=None):
        """
        :param eni_id: eni to be updated
        :type eni_id: string

        :param name: eni name to be updated
        :type name: string

        :param description:
            The description of the eni.
        :type description: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'modifyAttribute': None,
            b'clientToken': client_token
        }
        body = {}
        if name is not None:
            body['name'] = compat.convert_to_string(name)
        if description is not None:
            body['description'] = compat.convert_to_string(description)
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(vpc_id=(bytes, str), instance_id=(bytes, str), name=(bytes, str), private_ip_address_list=list, 
              marker=(bytes, str), max_keys=int)
    def list_eni(self, vpc_id, instance_id=None, name=None, private_ip_address_list=None, 
                 marker=None, max_keys=None, client_token=None, config=None):
        """
        :param vpc_id: The parameter to specify the vpc id
        :type vpc_id: string

        :param instance_id: The parameter to specify the id of instance
        :type instance_id: string

        :param name: eni name to be updated
        :type name: string

        :param private_ip_address_list: The parameter to specify the private ip address list
        :type private_ip_address_list: list

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specify the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specify the max number of list result to return.
            The default value is 1000.
        :type max_keys: int

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni'
        params = {}
        params[b'vpcId'] = compat.convert_to_string(vpc_id)
        if instance_id is not None:
            params[b'instanceId'] = compat.convert_to_string(instance_id)
        if name is not None:
            params[b'name'] = compat.convert_to_string(name)
        if private_ip_address_list is not None:
            params[b'privateIpAddress'] = (",").join(private_ip_address_list)
        if marker is not None:
            params[b'marker'] = compat.convert_to_string(marker)
        if max_keys is None:
            params[b'maxKeys'] = 1000
        else:
            params[b'maxKeys'] = max_keys
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        return self._send_request(http_methods.GET, path, params=params,
                                  config=config)

    @required(eni_id=(bytes, str), is_ipv6=bool, private_ip_address=(bytes, str))
    def add_private_ip(self, eni_id, private_ip_address, is_ipv6=None, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param is_ipv6: The parameter to specify the ipv6 flag
        :type is_ipv6: bool

        :param private_ip_address:
            The parameter to specify the private ip address.
            if is_ipv6 is True, the private ip address must be a valid ipv6 address.
        :type private_ip_address: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s/privateIp' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }
        body = {}
        body['privateIpAddress'] = compat.convert_to_string(private_ip_address)
        if is_ipv6 is not None:
            body['isIpv6'] = is_ipv6
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str), private_ip_address=(bytes, str))
    def delete_private_ip(self, eni_id, private_ip_address, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param private_ip_address:
            The parameter to specify the private ip address.
        :type private_ip_address: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s/privateIp/%s' % (compat.convert_to_bytes(eni_id), 
                                          utils.normalize_string(private_ip_address))
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }

        return self._send_request(http_methods.DELETE, path, params=params,
                                  config=config)

    @required(eni_id=(bytes, str))
    def get_eni_details(self, eni_id, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }
        return self._send_request(http_methods.GET, path, params=params,
                                  config=config)

    @required(eni_id=(bytes, str), instance_id=(bytes, str))
    def attach_eni_instance(self, eni_id, instance_id, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param instance_id: The parameter to specify the id of instance
        :type instance_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'attach': None,
            b'clientToken': client_token
        }
        body = {}
        if instance_id is not None:
            body['instanceId'] = compat.convert_to_string(instance_id)
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str), instance_id=(bytes, str))
    def detach_eni_instance(self, eni_id, instance_id, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param instance_id: The parameter to specify the id of instance
        :type instance_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'detach': None,
            b'clientToken': client_token
        }
        body = {}
        if instance_id is not None:
            body['instanceId'] = compat.convert_to_string(instance_id)
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str), security_group_ids=list)
    def update_eni_security_group(self, eni_id, security_group_ids, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param security_group_ids: security group ids
        :type security_group_ids: list

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'bindSg': None,
            b'clientToken': client_token
        }
        body = {}
        body['securityGroupIds'] = security_group_ids
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str), security_group_ids=list)
    def update_eni_enterprise_security_group(self, eni_id, enterprise_security_group_ids, 
                                             client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param enterprise_security_group_ids: enterprise security group ids
        :type enterprise_security_group_ids: list

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'bindEsg': None,
            b'clientToken': client_token
        }
        body = {}
        body['enterpriseSecurityGroupIds'] = enterprise_security_group_ids
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str), is_ipv6=bool, private_ip_address_list=list, private_ip_address_count=int)
    def batch_add_private_ip(self, eni_id, is_ipv6=None, private_ip_address_list=None, 
                             private_ip_address_count=None, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param is_ipv6: The parameter to specify the ipv6 flag
        :type is_ipv6: bool

        :param private_ip_address_list: 
            The parameter to specify the private ip address list.
            if is_ipv6 is True, the private ip address must be a valid ipv6 address.
        :type private_ip_address_list: list

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s/privateIp/batchAdd' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }
        body = {}
        if private_ip_address_list is not None:
            body['privateIpAddresses'] = private_ip_address_list
        if is_ipv6 is not None:
            body['isIpv6'] = is_ipv6
        if private_ip_address_count is not None:
            body['privateIpAddressCount'] = private_ip_address_count
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str), private_ip_address_list=list)
    def batch_delete_private_ip(self, eni_id, private_ip_address_list, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param private_ip_address_list: 
            The parameter to specify the private ip address list.
            if is_ipv6 is True, the private ip address must be a valid ipv6 address.
        :type private_ip_address_list: list

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s/privateIp/batchDel' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }
        body = {}
        body['privateIpAddresses'] = private_ip_address_list
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str))
    def get_eni_status(self, eni_id, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s/status' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }
        return self._send_request(http_methods.GET, path, params=params,
                                  config=config)

    @required(eni_id=(bytes, str), private_ip_address=(bytes, str), public_ip_address=(bytes, str))
    def bind_eni_public_ip(self, eni_id, privat_ip_address, public_ip_address, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param private_ip_address:
            The parameter to specify the private ip address.
        :type private_ip_address: string

        :param public_ip_address:
            The parameter to specify the public ip address.
        :type public_ip_address: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'bind': None,
            b'clientToken': client_token
        }

        body = {}
        body['privateIpAddress'] = compat.convert_to_string(privat_ip_address)
        body['publicIpAddress'] = compat.convert_to_string(public_ip_address)
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)

    @required(eni_id=(bytes, str), private_ip_address=(bytes, str), public_ip_address=(bytes, str))
    def unbind_eni_public_ip(self, eni_id, public_ip_address, client_token=None, config=None):
        """
        :param eni_id: The parameter to specify the id of eni
        :type eni_id: string

        :param public_ip_address:
            The parameter to specify the public ip address.
        :type public_ip_address: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = b'/eni/%s' % compat.convert_to_bytes(eni_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'unBind': None,
            b'clientToken': client_token
        }

        body = {}
        body['publicIpAddress'] = compat.convert_to_string(public_ip_address)
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.

    :return:
    :rtype string
    """
    return str(uuid.uuid4())

generate_client_token = generate_client_token_by_uuid
