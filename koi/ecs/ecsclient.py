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
                        internet_charge_type='PayByBandwidth',
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

    def describe_instances(self, region_id, page=1, pagesize=100,
                           instance_ids=None, 
                           image_id=None, 
                           status=None):
        """
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
        return self.request('DescribeInstances', data)

    def describe_images(self, region_id, image_name=None):
        data = {'RegionId': region_id}
        if image_name:
            data['ImageName'] = image_name
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

    def describe_security_groups(self, region_id):
        return self.request('DescribeSecurityGroups', {'RegionId': region_id})

    def describe_regions(self):
        return self.request('DescribeRegions')

    def describe_zones(self, region_id):
        return self.request('DescribeZones', {'RegionId': region_id})

    # diy methods
    def default_security_group_id(self, region_id):
        r = self.describe_security_groups(region_id)
        return r['SecurityGroups']['SecurityGroup'][0]['SecurityGroupId']

    def run_instances(region_id, image_id, instance_type, num_instances=1):
        """ create and start instances in batch """
        instance_ids = []
        for _ in range(num_instances):
            r = self.create_instance(region_id, image_id, instance_type) 
            self.allocate_public_ip_address(r['InstanceId'])
            self.start_instance(r['InstanceId'])
            instance_ids.append(r['InstanceId'])
        return instance_ids

    def release_instances(self, region_id, instance_ids):
        while True:
            r = self.describe_instances(region_id, instance_ids=instance_ids)
            instances = r['Instances']['Instance']
            if not instances:
                break
            for i in instances:
                if i['Status'] == 'Running':
                    self.stop_instance(i['InstanceId'])
                elif i['Status'] == 'Stopped':
                    self.delete_instance(i['InstanceId'])
                else:
                    # just let Starting/Stopping finish
                    pass
            time.sleep(1)
