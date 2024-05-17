'''
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-wordpress

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-wordpress)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-wordpress/)

> CDK Construct to deploy wordpress

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-wordpress
```

Python:

```bash
pip install cloudcomponents.cdk-wordpress
```

## How to use

```python
import { Wordpress } from '@cloudcomponents/cdk-wordpress';
import { RemovalPolicy, Stack, StackProps, aws_route53 } from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class WordpressStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    const hostedZone = aws_route53.PublicHostedZone.fromLookup(this, 'HostedZone', {
      domainName: 'cloudcomponents.org',
    });

    new Wordpress(this, 'Wordpress', {
      domainName: 'blog.cloudcomponents.org',
      domainZone: hostedZone,
      removalPolicy: RemovalPolicy.DESTROY,
      offloadStaticContent: true, // Support for plugin e.g. `WP Offload Media for Amazon S3`
    });
  }
}
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-wordpress/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-wordpress/LICENSE)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_backup as _aws_cdk_aws_backup_ceddda9d
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_rds as _aws_cdk_aws_rds_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


class Application(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-wordpress.Application",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
        database: "Database",
        domain_name: builtins.str,
        domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        volume: "EfsVolume",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        cloud_front_hash_header: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param certificate: -
        :param database: -
        :param domain_name: -
        :param domain_zone: -
        :param volume: -
        :param vpc: -
        :param cloud_front_hash_header: -
        :param environment: -
        :param image: -
        :param log_driver: -
        :param memory_limit_mib: -
        :param removal_policy: -
        :param secrets: -
        :param service_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86a85f9d40e4aae581d066ec69d9258b766fcc5e3895bb4e792644d14b6eae4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationProps(
            certificate=certificate,
            database=database,
            domain_name=domain_name,
            domain_zone=domain_zone,
            volume=volume,
            vpc=vpc,
            cloud_front_hash_header=cloud_front_hash_header,
            environment=environment,
            image=image,
            log_driver=log_driver,
            memory_limit_mib=memory_limit_mib,
            removal_policy=removal_policy,
            secrets=secrets,
            service_name=service_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="enableStaticContentOffload")
    def enable_static_content_offload(
        self,
        domain_name: builtins.str,
        certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
    ) -> "StaticContentOffload":
        '''
        :param domain_name: -
        :param certificate: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ee60cfba8a8304c2550763d548c2896ebeb289d5a52da58cb1bc776f559167)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
        return typing.cast("StaticContentOffload", jsii.invoke(self, "enableStaticContentOffload", [domain_name, certificate]))

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.IDistribution:
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.IDistribution, jsii.get(self, "distribution"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="domainZone")
    def domain_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, jsii.get(self, "domainZone"))

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener, jsii.get(self, "listener"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_ceddda9d.FargateService:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.FargateService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup, jsii.get(self, "targetGroup"))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-wordpress.ApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "database": "database",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "volume": "volume",
        "vpc": "vpc",
        "cloud_front_hash_header": "cloudFrontHashHeader",
        "environment": "environment",
        "image": "image",
        "log_driver": "logDriver",
        "memory_limit_mib": "memoryLimitMiB",
        "removal_policy": "removalPolicy",
        "secrets": "secrets",
        "service_name": "serviceName",
    },
)
class ApplicationProps:
    def __init__(
        self,
        *,
        certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
        database: "Database",
        domain_name: builtins.str,
        domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        volume: "EfsVolume",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        cloud_front_hash_header: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param certificate: -
        :param database: -
        :param domain_name: -
        :param domain_zone: -
        :param volume: -
        :param vpc: -
        :param cloud_front_hash_header: -
        :param environment: -
        :param image: -
        :param log_driver: -
        :param memory_limit_mib: -
        :param removal_policy: -
        :param secrets: -
        :param service_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4147338ead91bc36469c53b2d36a8ab77fa49f96220544ab8cb34091570cab5c)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cloud_front_hash_header", value=cloud_front_hash_header, expected_type=type_hints["cloud_front_hash_header"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "database": database,
            "domain_name": domain_name,
            "domain_zone": domain_zone,
            "volume": volume,
            "vpc": vpc,
        }
        if cloud_front_hash_header is not None:
            self._values["cloud_front_hash_header"] = cloud_front_hash_header
        if environment is not None:
            self._values["environment"] = environment
        if image is not None:
            self._values["image"] = image
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if secrets is not None:
            self._values["secrets"] = secrets
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def certificate(self) -> _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate:
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate, result)

    @builtins.property
    def database(self) -> "Database":
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast("Database", result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        result = self._values.get("domain_zone")
        assert result is not None, "Required property 'domain_zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, result)

    @builtins.property
    def volume(self) -> "EfsVolume":
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast("EfsVolume", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def cloud_front_hash_header(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_front_hash_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage]:
        result = self._values.get("image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver]:
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]]:
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Database(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-wordpress.Database",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allocated_storage: typing.Optional[jsii.Number] = None,
        database_name: typing.Optional[builtins.str] = None,
        engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: -
        :param allocated_storage: -
        :param database_name: -
        :param engine: -
        :param instance_type: -
        :param removal_policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0f90ad3b873dc10c55d35dcb77299b48d7f5a855b7385d7a7f0e8520743193)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatabaseProps(
            vpc=vpc,
            allocated_storage=allocated_storage,
            database_name=database_name,
            engine=engine,
            instance_type=instance_type,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="allowDefaultPortFrom")
    def allow_default_port_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param other: -
        :param description: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8708b646c3357a09c1cf4af2315e06de78f4287f6da3be38238f4a932d799e1a)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(None, jsii.invoke(self, "allowDefaultPortFrom", [other, description]))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]:
        return typing.cast(typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret], jsii.get(self, "secrets"))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-wordpress.DatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "allocated_storage": "allocatedStorage",
        "database_name": "databaseName",
        "engine": "engine",
        "instance_type": "instanceType",
        "removal_policy": "removalPolicy",
    },
)
class DatabaseProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allocated_storage: typing.Optional[jsii.Number] = None,
        database_name: typing.Optional[builtins.str] = None,
        engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param vpc: -
        :param allocated_storage: -
        :param database_name: -
        :param engine: -
        :param instance_type: -
        :param removal_policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f713415f72ab350ff686b08ae9de6c1bfc84e9a8aa1f3783e65be96fb7a5ac)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if database_name is not None:
            self._values["database_name"] = database_name
        if engine is not None:
            self._values["engine"] = engine
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine]:
        result = self._values.get("engine")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Dns(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-wordpress.Dns",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        distribution: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
        domain_name: builtins.str,
        domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param distribution: -
        :param domain_name: -
        :param domain_zone: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade5099f5ef2799e23fa1c82ef30dbf0982ccb84a613c08a28b19390dc1fcb6b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DnsProps(
            distribution=distribution, domain_name=domain_name, domain_zone=domain_zone
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-wordpress.DnsProps",
    jsii_struct_bases=[],
    name_mapping={
        "distribution": "distribution",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
    },
)
class DnsProps:
    def __init__(
        self,
        *,
        distribution: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
        domain_name: builtins.str,
        domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    ) -> None:
        '''
        :param distribution: -
        :param domain_name: -
        :param domain_zone: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171baceec1b06361edb267b5fc8e1b7003d5df804b53b9464565e0aa6d67ef83)
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "distribution": distribution,
            "domain_name": domain_name,
            "domain_zone": domain_zone,
        }

    @builtins.property
    def distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.IDistribution:
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.IDistribution, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        result = self._values.get("domain_zone")
        assert result is not None, "Required property 'domain_zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EfsVolume(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-wordpress.EfsVolume",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: -
        :param name: -
        :param removal_policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8bf09fbce1843c5d6c99b9abd4cbed9b7abe2d852c44734b03d81c821201bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EfsVolumeProps(vpc=vpc, name=name, removal_policy=removal_policy)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="allowDefaultPortFrom")
    def allow_default_port_from(
        self,
        other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param other: -
        :param description: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cce58fae21555ec2e6b1880e78653e363df34d2e4d3871787dc952ed0b02f7)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(None, jsii.invoke(self, "allowDefaultPortFrom", [other, description]))

    @builtins.property
    @jsii.member(jsii_name="efsVolumeConfiguration")
    def efs_volume_configuration(
        self,
    ) -> _aws_cdk_aws_ecs_ceddda9d.EfsVolumeConfiguration:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.EfsVolumeConfiguration, jsii.get(self, "efsVolumeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-wordpress.EfsVolumeProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "name": "name", "removal_policy": "removalPolicy"},
)
class EfsVolumeProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param vpc: -
        :param name: -
        :param removal_policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d99d26186a349dd082e89b5911b980d1301c8ccce5a0258e0ddea682eb91163)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if name is not None:
            self._values["name"] = name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EfsVolumeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-wordpress.StaticContentOffload",
    jsii_struct_bases=[],
    name_mapping={"distribution": "distribution", "domain_name": "domainName"},
)
class StaticContentOffload:
    def __init__(
        self,
        *,
        distribution: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
        domain_name: builtins.str,
    ) -> None:
        '''
        :param distribution: -
        :param domain_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fd3e05dff74ae35ae4299736e2468d15a81f8398f08c123e2553fc189fca3a)
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "distribution": distribution,
            "domain_name": domain_name,
        }

    @builtins.property
    def distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.IDistribution:
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.IDistribution, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticContentOffload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wordpress(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-wordpress.Wordpress",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        backup_plan: typing.Optional[_aws_cdk_aws_backup_ceddda9d.BackupPlan] = None,
        cloud_front_hash_header: typing.Optional[builtins.str] = None,
        database: typing.Optional[Database] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        offload_static_content: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        volume: typing.Optional[EfsVolume] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain_name: -
        :param domain_zone: -
        :param backup_plan: -
        :param cloud_front_hash_header: -
        :param database: -
        :param environment: -
        :param image: -
        :param log_driver: -
        :param memory_limit_mib: -
        :param offload_static_content: -
        :param removal_policy: -
        :param secrets: -
        :param service_name: -
        :param subject_alternative_names: -
        :param volume: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3412748298cfdca097da6a07ff0371c3bd1a29b7c3e3be86d6809884802c4c26)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WordpressProps(
            domain_name=domain_name,
            domain_zone=domain_zone,
            backup_plan=backup_plan,
            cloud_front_hash_header=cloud_front_hash_header,
            database=database,
            environment=environment,
            image=image,
            log_driver=log_driver,
            memory_limit_mib=memory_limit_mib,
            offload_static_content=offload_static_content,
            removal_policy=removal_policy,
            secrets=secrets,
            service_name=service_name,
            subject_alternative_names=subject_alternative_names,
            volume=volume,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> Application:
        return typing.cast(Application, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> Database:
        return typing.cast(Database, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> EfsVolume:
        return typing.cast(EfsVolume, jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="staticContentOffload")
    def static_content_offload(self) -> typing.Optional[StaticContentOffload]:
        return typing.cast(typing.Optional[StaticContentOffload], jsii.get(self, "staticContentOffload"))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-wordpress.WordpressProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "backup_plan": "backupPlan",
        "cloud_front_hash_header": "cloudFrontHashHeader",
        "database": "database",
        "environment": "environment",
        "image": "image",
        "log_driver": "logDriver",
        "memory_limit_mib": "memoryLimitMiB",
        "offload_static_content": "offloadStaticContent",
        "removal_policy": "removalPolicy",
        "secrets": "secrets",
        "service_name": "serviceName",
        "subject_alternative_names": "subjectAlternativeNames",
        "volume": "volume",
        "vpc": "vpc",
    },
)
class WordpressProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        backup_plan: typing.Optional[_aws_cdk_aws_backup_ceddda9d.BackupPlan] = None,
        cloud_front_hash_header: typing.Optional[builtins.str] = None,
        database: typing.Optional[Database] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        offload_static_content: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        volume: typing.Optional[EfsVolume] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param domain_name: -
        :param domain_zone: -
        :param backup_plan: -
        :param cloud_front_hash_header: -
        :param database: -
        :param environment: -
        :param image: -
        :param log_driver: -
        :param memory_limit_mib: -
        :param offload_static_content: -
        :param removal_policy: -
        :param secrets: -
        :param service_name: -
        :param subject_alternative_names: -
        :param volume: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c30ad270ad0eb8786ffd4bbaa9f8ed89f0d9b7eac5fcc8282c6e9e914e3431)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument backup_plan", value=backup_plan, expected_type=type_hints["backup_plan"])
            check_type(argname="argument cloud_front_hash_header", value=cloud_front_hash_header, expected_type=type_hints["cloud_front_hash_header"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument offload_static_content", value=offload_static_content, expected_type=type_hints["offload_static_content"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "domain_zone": domain_zone,
        }
        if backup_plan is not None:
            self._values["backup_plan"] = backup_plan
        if cloud_front_hash_header is not None:
            self._values["cloud_front_hash_header"] = cloud_front_hash_header
        if database is not None:
            self._values["database"] = database
        if environment is not None:
            self._values["environment"] = environment
        if image is not None:
            self._values["image"] = image
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if offload_static_content is not None:
            self._values["offload_static_content"] = offload_static_content
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if secrets is not None:
            self._values["secrets"] = secrets
        if service_name is not None:
            self._values["service_name"] = service_name
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names
        if volume is not None:
            self._values["volume"] = volume
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def domain_name(self) -> builtins.str:
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        result = self._values.get("domain_zone")
        assert result is not None, "Required property 'domain_zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, result)

    @builtins.property
    def backup_plan(self) -> typing.Optional[_aws_cdk_aws_backup_ceddda9d.BackupPlan]:
        result = self._values.get("backup_plan")
        return typing.cast(typing.Optional[_aws_cdk_aws_backup_ceddda9d.BackupPlan], result)

    @builtins.property
    def cloud_front_hash_header(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_front_hash_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[Database]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[Database], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage]:
        result = self._values.get("image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver]:
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def offload_static_content(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("offload_static_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]]:
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def volume(self) -> typing.Optional[EfsVolume]:
        result = self._values.get("volume")
        return typing.cast(typing.Optional[EfsVolume], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WordpressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Application",
    "ApplicationProps",
    "Database",
    "DatabaseProps",
    "Dns",
    "DnsProps",
    "EfsVolume",
    "EfsVolumeProps",
    "StaticContentOffload",
    "Wordpress",
    "WordpressProps",
]

publication.publish()

def _typecheckingstub__d86a85f9d40e4aae581d066ec69d9258b766fcc5e3895bb4e792644d14b6eae4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
    database: Database,
    domain_name: builtins.str,
    domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    volume: EfsVolume,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    cloud_front_hash_header: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ee60cfba8a8304c2550763d548c2896ebeb289d5a52da58cb1bc776f559167(
    domain_name: builtins.str,
    certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4147338ead91bc36469c53b2d36a8ab77fa49f96220544ab8cb34091570cab5c(
    *,
    certificate: _aws_cdk_aws_certificatemanager_ceddda9d.ICertificate,
    database: Database,
    domain_name: builtins.str,
    domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    volume: EfsVolume,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    cloud_front_hash_header: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0f90ad3b873dc10c55d35dcb77299b48d7f5a855b7385d7a7f0e8520743193(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allocated_storage: typing.Optional[jsii.Number] = None,
    database_name: typing.Optional[builtins.str] = None,
    engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8708b646c3357a09c1cf4af2315e06de78f4287f6da3be38238f4a932d799e1a(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f713415f72ab350ff686b08ae9de6c1bfc84e9a8aa1f3783e65be96fb7a5ac(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allocated_storage: typing.Optional[jsii.Number] = None,
    database_name: typing.Optional[builtins.str] = None,
    engine: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IInstanceEngine] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade5099f5ef2799e23fa1c82ef30dbf0982ccb84a613c08a28b19390dc1fcb6b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    distribution: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
    domain_name: builtins.str,
    domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171baceec1b06361edb267b5fc8e1b7003d5df804b53b9464565e0aa6d67ef83(
    *,
    distribution: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
    domain_name: builtins.str,
    domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8bf09fbce1843c5d6c99b9abd4cbed9b7abe2d852c44734b03d81c821201bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cce58fae21555ec2e6b1880e78653e363df34d2e4d3871787dc952ed0b02f7(
    other: _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d99d26186a349dd082e89b5911b980d1301c8ccce5a0258e0ddea682eb91163(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fd3e05dff74ae35ae4299736e2468d15a81f8398f08c123e2553fc189fca3a(
    *,
    distribution: _aws_cdk_aws_cloudfront_ceddda9d.IDistribution,
    domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3412748298cfdca097da6a07ff0371c3bd1a29b7c3e3be86d6809884802c4c26(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    backup_plan: typing.Optional[_aws_cdk_aws_backup_ceddda9d.BackupPlan] = None,
    cloud_front_hash_header: typing.Optional[builtins.str] = None,
    database: typing.Optional[Database] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    offload_static_content: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume: typing.Optional[EfsVolume] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c30ad270ad0eb8786ffd4bbaa9f8ed89f0d9b7eac5fcc8282c6e9e914e3431(
    *,
    domain_name: builtins.str,
    domain_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    backup_plan: typing.Optional[_aws_cdk_aws_backup_ceddda9d.BackupPlan] = None,
    cloud_front_hash_header: typing.Optional[builtins.str] = None,
    database: typing.Optional[Database] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ContainerImage] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    offload_static_content: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_ceddda9d.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume: typing.Optional[EfsVolume] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass
