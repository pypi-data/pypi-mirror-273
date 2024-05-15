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
import aws_cdk.pipelines as _aws_cdk_pipelines_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="cdk-constructs.IVpcBase")
class IVpcBase(typing_extensions.Protocol):
    '''Represents the configuration for a VPC.'''

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        '''The CIDR block for the VPC.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="enableEndpointDynamoDB")
    def enable_endpoint_dynamo_db(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to enable the DynamoDB endpoint for the VPC.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="enableEndpointS3")
    def enable_endpoint_s3(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to enable the S3 endpoint for the VPC.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of availability zones to use for the VPC.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        '''The number of NAT gateways to create for the VPC.'''
        ...


class _IVpcBaseProxy:
    '''Represents the configuration for a VPC.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-constructs.IVpcBase"

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        '''The CIDR block for the VPC.'''
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="enableEndpointDynamoDB")
    def enable_endpoint_dynamo_db(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to enable the DynamoDB endpoint for the VPC.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableEndpointDynamoDB"))

    @builtins.property
    @jsii.member(jsii_name="enableEndpointS3")
    def enable_endpoint_s3(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to enable the S3 endpoint for the VPC.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableEndpointS3"))

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of availability zones to use for the VPC.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAzs"))

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        '''The number of NAT gateways to create for the VPC.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "natGateways"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcBase).__jsii_proxy_class__ = lambda : _IVpcBaseProxy


class PipelineCdk(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-constructs.PipelineCdk",
):
    '''A CDK construct that creates a CodePipeline.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        pipeline_name: builtins.str,
        repo_branch: builtins.str,
        repo_name: builtins.str,
    ) -> None:
        '''Constructs a new instance of the PipelineCdk class.

        :param scope: The parent construct.
        :param id: The name of the construct.
        :param pipeline_name: The name of the pipeline.
        :param repo_branch: The branch of the repository to use.
        :param repo_name: The name of the repository.

        :default: - No default properties.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e764fe86eddba1990c2a10a0ac6f2a79d290cf0db7a8e80f31cc11f6cca412)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PipelineProps(
            pipeline_name=pipeline_name, repo_branch=repo_branch, repo_name=repo_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> _aws_cdk_pipelines_ceddda9d.CodePipeline:
        '''The CodePipeline created by the construct.'''
        return typing.cast(_aws_cdk_pipelines_ceddda9d.CodePipeline, jsii.get(self, "pipeline"))


@jsii.data_type(
    jsii_type="cdk-constructs.PipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipeline_name": "pipelineName",
        "repo_branch": "repoBranch",
        "repo_name": "repoName",
    },
)
class PipelineProps:
    def __init__(
        self,
        *,
        pipeline_name: builtins.str,
        repo_branch: builtins.str,
        repo_name: builtins.str,
    ) -> None:
        '''
        :param pipeline_name: The name of the pipeline.
        :param repo_branch: The branch of the repository to use.
        :param repo_name: The name of the repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdce3e5d311d928440bba572fce978fa088acf413153800cbdad001ff72e65cd)
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument repo_branch", value=repo_branch, expected_type=type_hints["repo_branch"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pipeline_name": pipeline_name,
            "repo_branch": repo_branch,
            "repo_name": repo_name,
        }

    @builtins.property
    def pipeline_name(self) -> builtins.str:
        '''The name of the pipeline.'''
        result = self._values.get("pipeline_name")
        assert result is not None, "Required property 'pipeline_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_branch(self) -> builtins.str:
        '''The branch of the repository to use.'''
        result = self._values.get("repo_branch")
        assert result is not None, "Required property 'repo_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_name(self) -> builtins.str:
        '''The name of the repository.'''
        result = self._values.get("repo_name")
        assert result is not None, "Required property 'repo_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-constructs.VpcBase",
):
    '''A VPC construct that creates a VPC with public and private subnets.'''

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
        '''The VPC created by the construct.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, jsii.get(self, "vpc"))


__all__ = [
    "IVpcBase",
    "PipelineCdk",
    "PipelineProps",
    "VpcBase",
]

publication.publish()

def _typecheckingstub__10e764fe86eddba1990c2a10a0ac6f2a79d290cf0db7a8e80f31cc11f6cca412(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    pipeline_name: builtins.str,
    repo_branch: builtins.str,
    repo_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdce3e5d311d928440bba572fce978fa088acf413153800cbdad001ff72e65cd(
    *,
    pipeline_name: builtins.str,
    repo_branch: builtins.str,
    repo_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d531e6e4ad3ba7357a68fce4020bd67376f02ea8949ac0f6df52c63d66bc911d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IVpcBase,
) -> None:
    """Type checking stubs"""
    pass
