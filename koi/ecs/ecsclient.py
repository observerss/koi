#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json

from koi.core.client import Client


class ECSClient(Client):
    def create_instance(self, 
                        region_id,
                        image_id,
                        instance_type,
                        zone_id=None,
                        security_group_id=None,
                        instance_name=None,
                        description=None,
                        internet_charge_type='PayByTraffic',
                        internet_max_bandwidth=(200, 100)
                        ):
        data = {
            'RegionId': region_id,
            'ImageId': image_id,
            'InstanceType': instance_type,
            'SecurityGroupId': security_group_id or \
                self.default_security_group_id(region_id),
            'InternetChargeType': internet_charge_type,
            'InternetMaxBandwidthIn': internet_max_bandwidth[0],
            'InternetMaxBandwidthOut': internet_max_bandwidth[1],
        }
        if zone_id:
            data['ZoneId'] = zone_id
        if instance_name:
            data['InstanceName'] = instance_name
        if description:
            data['Description'] = description
        return self.request('CreateInstance', data)

    def start_instance(self, instance_id):
        return self.request('StartInstance', {'InstanceId': instance_id})

    def stop_instance(self, instance_id, force_stop=False):
        force_stop = str(force_stop).lower()
        return self.request('StopInstance',
                            {'InstanceId': instance_id,
                             'ForceStop': force_stop})
    
    def reboot_instance(self, instance_id, force_stop=False):
        force_stop = str(force_stop).lower()
        return self.request('RebootInstance',
                            {'InstanceId': instance_id,
                             'ForceStop': force_stop})

    def delete_instance(self, instance_id):
        return self.request('DeleteInstance', {'InstanceId': instance_id})

    def modify_instance_attribute(self, instance_id, 
                                  instance_name=None, 
                                  description=None,
                                  password=None, 
                                  hostname=None):
        data = {}
        if instance_name:
            data['InstanceName'] = instance_name
        if description:
            data['Description'] = description
        if password:
            data['Password'] = password
        if hostname:
            data['HostName'] = hostname
        if not data:
            raise ValueError('you must specifiy at least one of changed attributes')
        data['InstanceId'] = instance_id
        return self.request('ModifyInstanceAttribute', data)

    def describe_instances(self, region_id, page=1, pagesize=100,
                           instance_ids=None, 
                           image_id=None, 
                           charge_type=None,
                           status=None):
        """
        :param charge_type: PrePaid/PostPaid
        :param status: Running/Starting/Stopping/Stopped
        """
        data = {'RegionId': region_id,
                'PageNumber': page,
                'PageSize': pagesize}
        if instance_ids:
            data['InstanceIds'] = json.dumps(instance_ids)
        if image_id:
            data['ImageId'] = image_id
        if status:
            data['Status'] = status
        if charge_type:
            data['InstanceChargeType'] = charge_type
        return self.request('DescribeInstances', data)

    def describe_images(self, region_id, 
                        image_name=None,
                        image_id=None,
                        snapshot_id=None,
                        owner=None,
                        page=1, pagesize=100):
        data = {'RegionId': region_id,
                'PageNumber': page,
                'PageSize': pagesize}
        if image_name:
            data['ImageName'] = image_name
        if image_id:
            data['ImageId'] = image_id
        if snapshot_id:
            data['SnapshotId'] = snapshot_id
        if owner in ['system', 'self', 'others', 'marketplace']:
            data['ImageOwnerAlias'] = owner
        return self.request('DescribeImages', data)

    def allocate_public_ip_address(self, instance_id):
        return self.request('AllocatePublicIpAddress', {'InstanceId': instance_id})

    def copy_image(self, region_id_from, image_id_from, 
                   region_id_to, image_name, image_description):
        return self.request('CopyImage',
                            {'RegionId': region_id_from,
                             'ImageId': image_id_from,
                             'DestinationRegionId': region_id_to,
                             'DestinationImageName': image_name,
                             'DestinationDescription': image_description})

    def describe_security_group_attribute(self, region_id, security_group_id, 
                                          nic_type='internet'):
        return self.request('DescribeSecurityGroupAttribute',
                            {'RegionId': region_id,
                             'SecurityGroupId': security_group_id,
                             'NicType': nic_type})

    def create_security_group(self, region_id, 
                              security_group_name=None,
                              description=None,
                              vpc_id=None):
        data = {'RegionId': region_id}
        if security_group_name:
            data['SecurityGroupName'] = security_group_name,
        if description:
            data['Description'] = description
        if vpc_id:
            data['VpcId'] = vpc_id
        return self.request('CreateSecurityGroup', data)

    def authorize_security_group(self, region_id, security_group_id,
                                 ip_protocol='all',
                                 port_range='-1/-1',
                                 source_group_id=None,
                                 source_group_owner=None,
                                 source_cidr_ip='0.0.0.0/0',
                                 policy='accept',
                                 priority=100,
                                 nic_type='internet'):
        assert ip_protocol in ['tcp', 'udp', 'icmp', 'gre', 'all']
        assert policy in ['accept', 'drop']
        assert nic_type in ['internet', 'intranet']
        data = {
            'RegionId': region_id,
            'SecurityGroupId': security_group_id,
            'IpProtocol': ip_protocol,
            'PortRange': port_range,
            'SourceCidrIp': source_cidr_ip,
            'Policy': policy,
            'Priority': priority,
            'NicType': nic_type}
        if source_group_id:
            data['SourceGroupId'] = source_group_id
        if source_group_owner:
            data['SourceGroupOwner'] = source_group_owner
        return self.request('AuthorizeSecurityGroup', data)

    def authorize_security_group_egress(self, region_id, security_group_id,
                                        ip_protocol='all',
                                        port_range='-1/-1',
                                        dest_group_id=None,
                                        dest_group_owner=None,
                                        dest_cidr_ip='0.0.0.0/0',
                                        policy='accept',
                                        priority=100,
                                        nic_type='internet'):
        assert ip_protocol in ['tcp', 'udp', 'icmp', 'gre', 'all']
        assert policy in ['accept', 'drop']
        assert nic_type in ['internet', 'intranet']
        data = {
            'RegionId': region_id,
            'SecurityGroupId': security_group_id,
            'IpProtocol': ip_protocol,
            'PortRange': port_range,
            'DestCidrIp': dest_cidr_ip,
            'Policy': policy,
            'Priority': priority,
            'NicType': nic_type}
        if dest_group_id:
            data['DestGroupId'] = dest_group_id
        if dest_group_owner:
            data['DestGroupOwner'] = dest_group_owner
        return self.request('AuthorizeSecurityGroupEgress', data)

    def describe_security_groups(self, region_id):
        return self.request('DescribeSecurityGroups', {'RegionId': region_id})

    def describe_regions(self):
        return self.request('DescribeRegions')

    def describe_zones(self, region_id):
        return self.request('DescribeZones', {'RegionId': region_id})

    # below are sugar methods
    def default_security_group_id(self, region_id):
        """ find a security group that allows everything """
        # First we look for system created security group, which allows all.
        # If you have created one or more instances in web console,
        # Aliyun will then create one for you automatically
        r = self.describe_security_groups(region_id)
        sgs = r['SecurityGroups']['SecurityGroup']
        for sg in sgs:
            if sg['Description'] == 'System created security group.':
                return sg['SecurityGroupId']

        # No "system created" sg, let's fake one
        r = self.create_security_group(region_id, description='System created security group.')
        security_group_id = r['SecurityGroupId']
        self.authorize_security_group(region_id, security_group_id)
        self.authorize_security_group_egress(region_id, security_group_id)
        return security_group_id

    def run_instances(self, region_id, image_id, instance_type, num_instances=1):
        """ create and start public facing instances in batch """
        instance_ids = []
        for _ in range(num_instances):
            r = self.create_instance(region_id, image_id, instance_type) 
            self.allocate_public_ip_address(r['InstanceId'])
            self.start_instance(r['InstanceId'])
            instance_ids.append(r['InstanceId'])
        return instance_ids

    def release_instances(self, region_id, instance_ids, timeout=None):
        """ stop and delete instances """
        waited = 0
        while not timeout or waited < timeout:
            r = self.describe_instances(region_id, instance_ids=instance_ids)
            instances = r['Instances']['Instance']
            if not instances:
                break
            for i in instances:
                if i['Status'] != 'Stopped':
                    self.stop_instance(i['InstanceId'])
                elif i['Status'] == 'Stopped':
                    self.delete_instance(i['InstanceId'])
            time.sleep(1)
            waited += 1
