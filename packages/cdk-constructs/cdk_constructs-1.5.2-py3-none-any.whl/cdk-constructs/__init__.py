'''
# CDK construct lib

Welcome to Toumoro's AWS Service Wrapper CDK Construct Library! This library is designed to make it easy and efficient to deploy and manage AWS services within your CDK projects. Whether you're provisioning infrastructure for a simple web application or orchestrating a complex cloud-native architecture, this library aims to streamline your development process by providing high-level constructs for common AWS services.

## Features

* Simplified Service Provisioning: Easily create and configure AWS services using intuitive CDK constructs.
* Best Practices Built-In: Leverage pre-configured settings and defaults based on AWS best practices to ensure reliable and secure deployments.
* Modular and Extensible: Compose your infrastructure using modular constructs, allowing for flexibility and reusability across projects.

# Contributing to CDK Construct Toumoro

[Contributing](CONTRIBUTING.md)

# Examples

[Examples](examples/README.md)

# Documentation API

[API](API.md)

# Developpement Guide

[AWS CDK Design Guidelines](https://github.com/aws/aws-cdk/blob/main/docs/DESIGN_GUIDELINES.md)

## Naming Conventions

1. *Prefixes*:

   * *Cfn* for CloudFormation resources.
   * *Fn* for constructs generating CloudFormation functions.
   * *As* for abstract classes.
   * *I* for interfaces.
   * *Vpc* for constructs related to Virtual Private Cloud.
   * *Lambda* for constructs related to AWS Lambda.
   * Example: CfnStack, FnSub, Aspects, IVpc, VpcNetwork, LambdaFunction.
2. *Construct Names*:

   * Use descriptive names that reflect the purpose of the construct.
   * CamelCase for multi-word names.
   * Avoid abbreviations unless they are widely understood.
   * Example: BucketStack, RestApiConstruct, DatabaseCluster.
3. *Property Names*:

   * Follow AWS resource naming conventions where applicable.
   * Use camelCase for property names.
   * Use clear and concise names that reflect the purpose of the property.
   * Example: bucketName, vpcId, functionName.
4. *Method Names*:

   * Use verbs or verb phrases to describe actions performed by methods.
   * Use camelCase.
   * Example: addBucketPolicy, createVpc, invokeLambda.
5. *Interface Names*:

   * Start with an uppercase I.
   * Use clear and descriptive names.
   * Example: IInstance, ISecurityGroup, IVpc.
6. *Module Names*:

   * Use lowercase with hyphens for separating words.
   * Be descriptive but concise.
   * Follow a hierarchy if necessary, e.g., aws-cdk.aws_s3 for S3-related constructs.
   * Example: aws-cdk.aws_s3, aws-cdk.aws_ec2, aws-cdk.aws_lambda.
7. *Variable Names*:

   * Use descriptive names.
   * CamelCase for multi-word names.
   * Keep variable names concise but meaningful.
   * Example: instanceCount, subnetIds, roleArn.
8. *Enum and Constant Names*:

   * Use uppercase for constants.
   * CamelCase for multi-word names.
   * Be descriptive about the purpose of the constant or enum.
   * Example: MAX_RETRIES, HTTP_STATUS_CODES, VPC_CONFIG.
9. *File Names*:

   * Use lowercase with hyphens for separating words.
   * Reflect the content of the file.
   * Include version numbers if necessary.
   * Example: s3-bucket-stack.ts, vpc-network.ts, lambda-function.ts.
10. *Documentation Comments*:

    * Use JSDoc or similar conventions to provide clear documentation for each construct, method, property, etc.
    * Ensure that the documentation is up-to-date and accurately reflects the purpose and usage of the code.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="cdk-constructs.IVpcBase")
class IVpcBase(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        ...

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        ...


class _IVpcBaseProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-constructs.IVpcBase"

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAzs"))

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "natGateways"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcBase).__jsii_proxy_class__ = lambda : _IVpcBaseProxy


class VpcBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-constructs.VpcBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IVpcBase,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d531e6e4ad3ba7357a68fce4020bd67376f02ea8949ac0f6df52c63d66bc911d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, jsii.get(self, "vpc"))


__all__ = [
    "IVpcBase",
    "VpcBase",
]

publication.publish()

def _typecheckingstub__d531e6e4ad3ba7357a68fce4020bd67376f02ea8949ac0f6df52c63d66bc911d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IVpcBase,
) -> None:
    """Type checking stubs"""
    pass
