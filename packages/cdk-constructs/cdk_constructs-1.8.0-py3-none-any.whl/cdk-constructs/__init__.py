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
        primary_output_directory: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Constructs a new instance of the PipelineCdk class.

        :param scope: The parent construct.
        :param id: The name of the construct.
        :param pipeline_name: The name of the pipeline.
        :param repo_branch: The branch of the repository to use.
        :param repo_name: The name of the repository.
        :param primary_output_directory: The primary output directory.
        :param synth_command: The command to run in the synth step.

        :default: - No default properties.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e764fe86eddba1990c2a10a0ac6f2a79d290cf0db7a8e80f31cc11f6cca412)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PipelineProps(
            pipeline_name=pipeline_name,
            repo_branch=repo_branch,
            repo_name=repo_name,
            primary_output_directory=primary_output_directory,
            synth_command=synth_command,
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
        "primary_output_directory": "primaryOutputDirectory",
        "synth_command": "synthCommand",
    },
)
class PipelineProps:
    def __init__(
        self,
        *,
        pipeline_name: builtins.str,
        repo_branch: builtins.str,
        repo_name: builtins.str,
        primary_output_directory: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param pipeline_name: The name of the pipeline.
        :param repo_branch: The branch of the repository to use.
        :param repo_name: The name of the repository.
        :param primary_output_directory: The primary output directory.
        :param synth_command: The command to run in the synth step.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdce3e5d311d928440bba572fce978fa088acf413153800cbdad001ff72e65cd)
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument repo_branch", value=repo_branch, expected_type=type_hints["repo_branch"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            check_type(argname="argument primary_output_directory", value=primary_output_directory, expected_type=type_hints["primary_output_directory"])
            check_type(argname="argument synth_command", value=synth_command, expected_type=type_hints["synth_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pipeline_name": pipeline_name,
            "repo_branch": repo_branch,
            "repo_name": repo_name,
        }
        if primary_output_directory is not None:
            self._values["primary_output_directory"] = primary_output_directory
        if synth_command is not None:
            self._values["synth_command"] = synth_command

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

    @builtins.property
    def primary_output_directory(self) -> typing.Optional[builtins.str]:
        '''The primary output directory.'''
        result = self._values.get("primary_output_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synth_command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command to run in the synth step.'''
        result = self._values.get("synth_command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-constructs.TmVpcProps",
    jsii_struct_bases=[_aws_cdk_aws_ec2_ceddda9d.VpcProps],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "create_internet_gateway": "createInternetGateway",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "ip_addresses": "ipAddresses",
        "ip_protocol": "ipProtocol",
        "ipv6_addresses": "ipv6Addresses",
        "max_azs": "maxAzs",
        "nat_gateway_provider": "natGatewayProvider",
        "nat_gateways": "natGateways",
        "nat_gateway_subnets": "natGatewaySubnets",
        "reserved_azs": "reservedAzs",
        "restrict_default_security_group": "restrictDefaultSecurityGroup",
        "subnet_configuration": "subnetConfiguration",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
        "range_cidr": "rangeCidr",
        "enable_endpoints": "enableEndpoints",
    },
)
class TmVpcProps(_aws_cdk_aws_ec2_ceddda9d.VpcProps):
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        create_internet_gateway: typing.Optional[builtins.bool] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        ip_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses] = None,
        ip_protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IpProtocol] = None,
        ipv6_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpv6Addresses] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        reserved_azs: typing.Optional[jsii.Number] = None,
        restrict_default_security_group: typing.Optional[builtins.bool] = None,
        subnet_configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        range_cidr: builtins.str,
        enable_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Represents the configuration for a VPC.

        :param availability_zones: Availability zones this VPC spans. Specify this option only if you do not specify ``maxAzs``. Default: - a subset of AZs of the stack
        :param cidr: (deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'. Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone. Default: Vpc.DEFAULT_CIDR_RANGE
        :param create_internet_gateway: If set to false then disable the creation of the default internet gateway. Default: true
        :param default_instance_tenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
        :param enable_dns_support: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
        :param flow_logs: Flow logs to add to this VPC. Default: - No flow logs.
        :param gateway_endpoints: Gateway endpoints to add to this VPC. Default: - None.
        :param ip_addresses: The Provider to use to allocate IPv4 Space to your VPC. Options include static allocation or from a pool. Note this is specific to IPv4 addresses. Default: ec2.IpAddresses.cidr
        :param ip_protocol: The protocol of the vpc. Options are IPv4 only or dual stack. Default: IpProtocol.IPV4_ONLY
        :param ipv6_addresses: The Provider to use to allocate IPv6 Space to your VPC. Options include amazon provided CIDR block. Note this is specific to IPv6 addresses. Default: Ipv6Addresses.amazonProvided
        :param max_azs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack. Specify this option only if you do not specify ``availabilityZones``. Default: 3
        :param nat_gateway_provider: What type of NAT provider to use. Select between NAT gateways or NAT instances. NAT gateways may not be available in all AWS regions. Default: NatProvider.gateway()
        :param nat_gateways: The number of NAT Gateways/Instances to create. The type of NAT gateway or instance will be determined by the ``natGatewayProvider`` parameter. You can set this number lower than the number of Availability Zones in your VPC in order to save on NAT cost. Be aware you may be charged for cross-AZ data traffic instead. Default: - One NAT gateway/instance per Availability Zone
        :param nat_gateway_subnets: Configures the subnets which will have NAT Gateways/Instances. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Only necessary if you have more than one public subnet group. Default: - All public subnets.
        :param reserved_azs: Define the number of AZs to reserve. When specified, the IP space is reserved for the azs but no actual resources are provisioned. Default: 0
        :param restrict_default_security_group: If set to true then the default inbound & outbound rules will be removed from the default security group. Default: true if '@aws-cdk/aws-ec2:restrictDefaultSecurityGroup' is enabled, false otherwise
        :param subnet_configuration: Configure the subnets to build for each AZ. Each entry in this list configures a Subnet Group; each group will contain a subnet for each Availability Zone. For example, if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following:: new ec2.Vpc(this, 'VPC', { subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: ec2.SubnetType.PUBLIC, }, { cidrMask: 24, name: 'application', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, }, { cidrMask: 28, name: 'rds', subnetType: ec2.SubnetType.PRIVATE_ISOLATED, } ] }); Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
        :param vpc_name: The VPC name. Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag Default: this.node.path
        :param vpn_connections: VPN connections to this VPC. Default: - No connections.
        :param vpn_gateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified
        :param vpn_gateway_asn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
        :param vpn_route_propagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets. If no private subnets exists, isolated subnets are used. If no isolated subnets exists, public subnets are used.
        :param range_cidr: The CIDR block for the VPC.
        :param enable_endpoints: Indicates whether to enable the S3 endpoint for the VPC.
        '''
        if isinstance(nat_gateway_subnets, dict):
            nat_gateway_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**nat_gateway_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4305830cfac56f9525ce1d343bcbad2f9851c8cff92425568f94a971a4c150c6)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument create_internet_gateway", value=create_internet_gateway, expected_type=type_hints["create_internet_gateway"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument ipv6_addresses", value=ipv6_addresses, expected_type=type_hints["ipv6_addresses"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument nat_gateway_provider", value=nat_gateway_provider, expected_type=type_hints["nat_gateway_provider"])
            check_type(argname="argument nat_gateways", value=nat_gateways, expected_type=type_hints["nat_gateways"])
            check_type(argname="argument nat_gateway_subnets", value=nat_gateway_subnets, expected_type=type_hints["nat_gateway_subnets"])
            check_type(argname="argument reserved_azs", value=reserved_azs, expected_type=type_hints["reserved_azs"])
            check_type(argname="argument restrict_default_security_group", value=restrict_default_security_group, expected_type=type_hints["restrict_default_security_group"])
            check_type(argname="argument subnet_configuration", value=subnet_configuration, expected_type=type_hints["subnet_configuration"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
            check_type(argname="argument range_cidr", value=range_cidr, expected_type=type_hints["range_cidr"])
            check_type(argname="argument enable_endpoints", value=enable_endpoints, expected_type=type_hints["enable_endpoints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range_cidr": range_cidr,
        }
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if create_internet_gateway is not None:
            self._values["create_internet_gateway"] = create_internet_gateway
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if ip_protocol is not None:
            self._values["ip_protocol"] = ip_protocol
        if ipv6_addresses is not None:
            self._values["ipv6_addresses"] = ipv6_addresses
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if nat_gateway_provider is not None:
            self._values["nat_gateway_provider"] = nat_gateway_provider
        if nat_gateways is not None:
            self._values["nat_gateways"] = nat_gateways
        if nat_gateway_subnets is not None:
            self._values["nat_gateway_subnets"] = nat_gateway_subnets
        if reserved_azs is not None:
            self._values["reserved_azs"] = reserved_azs
        if restrict_default_security_group is not None:
            self._values["restrict_default_security_group"] = restrict_default_security_group
        if subnet_configuration is not None:
            self._values["subnet_configuration"] = subnet_configuration
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation
        if enable_endpoints is not None:
            self._values["enable_endpoints"] = enable_endpoints

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Availability zones this VPC spans.

        Specify this option only if you do not specify ``maxAzs``.

        :default: - a subset of AZs of the stack
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'.

        Should be a minimum of /28 and maximum size of /16. The range will be
        split across all subnets per Availability Zone.

        :default: Vpc.DEFAULT_CIDR_RANGE

        :deprecated: Use ipAddresses instead

        :stability: deprecated
        '''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_internet_gateway(self) -> typing.Optional[builtins.bool]:
        '''If set to false then disable the creation of the default internet gateway.

        :default: true
        '''
        result = self._values.get("create_internet_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        '''The default tenancy of instances launched into the VPC.

        By setting this to dedicated tenancy, instances will be launched on
        hardware dedicated to a single AWS customer, unless specifically specified
        at instance launch time. Please note, not all instance types are usable
        with Dedicated tenancy.

        :default: DefaultInstanceTenancy.Default (shared) tenancy
        '''
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the instances launched in the VPC get public DNS hostnames.

        If this attribute is true, instances in the VPC get public DNS hostnames,
        but only if the enableDnsSupport attribute is also set to true.

        :default: true
        '''
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DNS resolution is supported for the VPC.

        If this attribute is false, the Amazon-provided DNS server in the VPC that
        resolves public DNS hostnames to IP addresses is not enabled. If this
        attribute is true, queries to the Amazon provided DNS server at the
        169.254.169.253 IP address, or the reserved IP address at the base of the
        VPC IPv4 network range plus two will succeed.

        :default: true
        '''
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]]:
        '''Flow logs to add to this VPC.

        :default: - No flow logs.
        '''
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        '''Gateway endpoints to add to this VPC.

        :default: - None.
        '''
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses]:
        '''The Provider to use to allocate IPv4 Space to your VPC.

        Options include static allocation or from a pool.

        Note this is specific to IPv4 addresses.

        :default: ec2.IpAddresses.cidr
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses], result)

    @builtins.property
    def ip_protocol(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IpProtocol]:
        '''The protocol of the vpc.

        Options are IPv4 only or dual stack.

        :default: IpProtocol.IPV4_ONLY
        '''
        result = self._values.get("ip_protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IpProtocol], result)

    @builtins.property
    def ipv6_addresses(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpv6Addresses]:
        '''The Provider to use to allocate IPv6 Space to your VPC.

        Options include amazon provided CIDR block.

        Note this is specific to IPv6 addresses.

        :default: Ipv6Addresses.amazonProvided
        '''
        result = self._values.get("ipv6_addresses")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpv6Addresses], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        '''Define the maximum number of AZs to use in this region.

        If the region has more AZs than you want to use (for example, because of
        EIP limits), pick a lower number here. The AZs will be sorted and picked
        from the start of the list.

        If you pick a higher number than the number of AZs in the region, all AZs
        in the region will be selected. To use "all AZs" available to your
        account, use a high number (such as 99).

        Be aware that environment-agnostic stacks will be created with access to
        only 2 AZs, so to use more than 2 AZs, be sure to specify the account and
        region on your stack.

        Specify this option only if you do not specify ``availabilityZones``.

        :default: 3
        '''
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider]:
        '''What type of NAT provider to use.

        Select between NAT gateways or NAT instances. NAT gateways
        may not be available in all AWS regions.

        :default: NatProvider.gateway()
        '''
        result = self._values.get("nat_gateway_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider], result)

    @builtins.property
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        '''The number of NAT Gateways/Instances to create.

        The type of NAT gateway or instance will be determined by the
        ``natGatewayProvider`` parameter.

        You can set this number lower than the number of Availability Zones in your
        VPC in order to save on NAT cost. Be aware you may be charged for
        cross-AZ data traffic instead.

        :default: - One NAT gateway/instance per Availability Zone
        '''
        result = self._values.get("nat_gateways")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Configures the subnets which will have NAT Gateways/Instances.

        You can pick a specific group of subnets by specifying the group name;
        the picked subnets must be public subnets.

        Only necessary if you have more than one public subnet group.

        :default: - All public subnets.
        '''
        result = self._values.get("nat_gateway_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def reserved_azs(self) -> typing.Optional[jsii.Number]:
        '''Define the number of AZs to reserve.

        When specified, the IP space is reserved for the azs but no actual
        resources are provisioned.

        :default: 0
        '''
        result = self._values.get("reserved_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def restrict_default_security_group(self) -> typing.Optional[builtins.bool]:
        '''If set to true then the default inbound & outbound rules will be removed from the default security group.

        :default: true if '@aws-cdk/aws-ec2:restrictDefaultSecurityGroup' is enabled, false otherwise
        '''
        result = self._values.get("restrict_default_security_group")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet_configuration(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration]]:
        '''Configure the subnets to build for each AZ.

        Each entry in this list configures a Subnet Group; each group will contain a
        subnet for each Availability Zone.

        For example, if you want 1 public subnet, 1 private subnet, and 1 isolated
        subnet in each AZ provide the following::

           new ec2.Vpc(this, 'VPC', {
             subnetConfiguration: [
                {
                  cidrMask: 24,
                  name: 'ingress',
                  subnetType: ec2.SubnetType.PUBLIC,
                },
                {
                  cidrMask: 24,
                  name: 'application',
                  subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
                },
                {
                  cidrMask: 28,
                  name: 'rds',
                  subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
                }
             ]
           });

        :default:

        - The VPC CIDR will be evenly divided between 1 public and 1
        private subnet per AZ.
        '''
        result = self._values.get("subnet_configuration")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration]], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        '''The VPC name.

        Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag

        :default: this.node.path
        '''
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        '''VPN connections to this VPC.

        :default: - No connections.
        '''
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether a VPN gateway should be created and attached to this VPC.

        :default: - true when vpnGatewayAsn or vpnConnections is specified
        '''
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        '''The private Autonomous System Number (ASN) for the VPN gateway.

        :default: - Amazon default ASN.
        '''
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        '''Where to propagate VPN routes.

        :default:

        - On the route tables associated with private subnets. If no
        private subnets exists, isolated subnets are used. If no isolated subnets
        exists, public subnets are used.
        '''
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    @builtins.property
    def range_cidr(self) -> builtins.str:
        '''The CIDR block for the VPC.'''
        result = self._values.get("range_cidr")
        assert result is not None, "Required property 'range_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Indicates whether to enable the S3 endpoint for the VPC.'''
        result = self._values.get("enable_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TmVpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcBase(
    _aws_cdk_aws_ec2_ceddda9d.Vpc,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-constructs.VpcBase",
):
    '''A VPC construct that creates a VPC with public and private subnets.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        range_cidr: builtins.str,
        enable_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        create_internet_gateway: typing.Optional[builtins.bool] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        ip_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses] = None,
        ip_protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IpProtocol] = None,
        ipv6_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpv6Addresses] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        reserved_azs: typing.Optional[jsii.Number] = None,
        restrict_default_security_group: typing.Optional[builtins.bool] = None,
        subnet_configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''The VPC created by the construct.

        :param scope: -
        :param id: -
        :param range_cidr: The CIDR block for the VPC.
        :param enable_endpoints: Indicates whether to enable the S3 endpoint for the VPC.
        :param availability_zones: Availability zones this VPC spans. Specify this option only if you do not specify ``maxAzs``. Default: - a subset of AZs of the stack
        :param cidr: (deprecated) The CIDR range to use for the VPC, e.g. '10.0.0.0/16'. Should be a minimum of /28 and maximum size of /16. The range will be split across all subnets per Availability Zone. Default: Vpc.DEFAULT_CIDR_RANGE
        :param create_internet_gateway: If set to false then disable the creation of the default internet gateway. Default: true
        :param default_instance_tenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
        :param enable_dns_support: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
        :param flow_logs: Flow logs to add to this VPC. Default: - No flow logs.
        :param gateway_endpoints: Gateway endpoints to add to this VPC. Default: - None.
        :param ip_addresses: The Provider to use to allocate IPv4 Space to your VPC. Options include static allocation or from a pool. Note this is specific to IPv4 addresses. Default: ec2.IpAddresses.cidr
        :param ip_protocol: The protocol of the vpc. Options are IPv4 only or dual stack. Default: IpProtocol.IPV4_ONLY
        :param ipv6_addresses: The Provider to use to allocate IPv6 Space to your VPC. Options include amazon provided CIDR block. Note this is specific to IPv6 addresses. Default: Ipv6Addresses.amazonProvided
        :param max_azs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Be aware that environment-agnostic stacks will be created with access to only 2 AZs, so to use more than 2 AZs, be sure to specify the account and region on your stack. Specify this option only if you do not specify ``availabilityZones``. Default: 3
        :param nat_gateway_provider: What type of NAT provider to use. Select between NAT gateways or NAT instances. NAT gateways may not be available in all AWS regions. Default: NatProvider.gateway()
        :param nat_gateways: The number of NAT Gateways/Instances to create. The type of NAT gateway or instance will be determined by the ``natGatewayProvider`` parameter. You can set this number lower than the number of Availability Zones in your VPC in order to save on NAT cost. Be aware you may be charged for cross-AZ data traffic instead. Default: - One NAT gateway/instance per Availability Zone
        :param nat_gateway_subnets: Configures the subnets which will have NAT Gateways/Instances. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Only necessary if you have more than one public subnet group. Default: - All public subnets.
        :param reserved_azs: Define the number of AZs to reserve. When specified, the IP space is reserved for the azs but no actual resources are provisioned. Default: 0
        :param restrict_default_security_group: If set to true then the default inbound & outbound rules will be removed from the default security group. Default: true if '@aws-cdk/aws-ec2:restrictDefaultSecurityGroup' is enabled, false otherwise
        :param subnet_configuration: Configure the subnets to build for each AZ. Each entry in this list configures a Subnet Group; each group will contain a subnet for each Availability Zone. For example, if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following:: new ec2.Vpc(this, 'VPC', { subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: ec2.SubnetType.PUBLIC, }, { cidrMask: 24, name: 'application', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, }, { cidrMask: 28, name: 'rds', subnetType: ec2.SubnetType.PRIVATE_ISOLATED, } ] }); Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
        :param vpc_name: The VPC name. Since the VPC resource doesn't support providing a physical name, the value provided here will be recorded in the ``Name`` tag Default: this.node.path
        :param vpn_connections: VPN connections to this VPC. Default: - No connections.
        :param vpn_gateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified
        :param vpn_gateway_asn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
        :param vpn_route_propagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets. If no private subnets exists, isolated subnets are used. If no isolated subnets exists, public subnets are used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d531e6e4ad3ba7357a68fce4020bd67376f02ea8949ac0f6df52c63d66bc911d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TmVpcProps(
            range_cidr=range_cidr,
            enable_endpoints=enable_endpoints,
            availability_zones=availability_zones,
            cidr=cidr,
            create_internet_gateway=create_internet_gateway,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            ip_addresses=ip_addresses,
            ip_protocol=ip_protocol,
            ipv6_addresses=ipv6_addresses,
            max_azs=max_azs,
            nat_gateway_provider=nat_gateway_provider,
            nat_gateways=nat_gateways,
            nat_gateway_subnets=nat_gateway_subnets,
            reserved_azs=reserved_azs,
            restrict_default_security_group=restrict_default_security_group,
            subnet_configuration=subnet_configuration,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "PipelineCdk",
    "PipelineProps",
    "TmVpcProps",
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
    primary_output_directory: typing.Optional[builtins.str] = None,
    synth_command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdce3e5d311d928440bba572fce978fa088acf413153800cbdad001ff72e65cd(
    *,
    pipeline_name: builtins.str,
    repo_branch: builtins.str,
    repo_name: builtins.str,
    primary_output_directory: typing.Optional[builtins.str] = None,
    synth_command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4305830cfac56f9525ce1d343bcbad2f9851c8cff92425568f94a971a4c150c6(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    create_internet_gateway: typing.Optional[builtins.bool] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses] = None,
    ip_protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IpProtocol] = None,
    ipv6_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpv6Addresses] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
    nat_gateways: typing.Optional[jsii.Number] = None,
    nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    reserved_azs: typing.Optional[jsii.Number] = None,
    restrict_default_security_group: typing.Optional[builtins.bool] = None,
    subnet_configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    range_cidr: builtins.str,
    enable_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d531e6e4ad3ba7357a68fce4020bd67376f02ea8949ac0f6df52c63d66bc911d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    range_cidr: builtins.str,
    enable_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    create_internet_gateway: typing.Optional[builtins.bool] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpAddresses] = None,
    ip_protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IpProtocol] = None,
    ipv6_addresses: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IIpv6Addresses] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
    nat_gateways: typing.Optional[jsii.Number] = None,
    nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    reserved_azs: typing.Optional[jsii.Number] = None,
    restrict_default_security_group: typing.Optional[builtins.bool] = None,
    subnet_configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
