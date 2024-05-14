import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

from .. import Job as _Job_20682b42, JobCollection as _JobCollection_0289800c
from ..git import (
    GitMirror as _GitMirror_6ee7350e,
    GitMirrorProps as _GitMirrorProps_84e02642,
    IGitMirror as _IGitMirror_5d079bec,
)


class AWSAccount(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.aws.AWSAccount"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsAccountId")
    @builtins.classmethod
    def aws_account_id(cls) -> builtins.str:
        '''Retrieves the AWS Account ID associated with the current AWS credentials or environment.

        If available, it uses the environment variable
        ``AWS_ACCOUNT_ID``. Otherwise, it fetches the AWS Account ID from the caller
        identity response obtained via STS.

        :return:

        A promise that resolves to the
        AWS Account ID as a string.

        :throws: {Error} If the AWS Account ID cannot be resolved.
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "awsAccountId", []))

    @jsii.member(jsii_name="awsRegion")
    @builtins.classmethod
    def aws_region(cls) -> builtins.str:
        '''Retrieves the AWS region associated with the current AWS credentials or environment.

        If available, it uses the environment variable
        ``AWS_DEFAULT_REGION``. Otherwise, it fetches the AWS region from the caller
        identity response obtained via STS.

        :return:

        A promise that resolves to the
        AWS region as a string.

        :throws: {Error} If the AWS region cannot be resolved.
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "awsRegion", []))


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.CdkBootstrapProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_account_id": "awsAccountId",
        "aws_region": "awsRegion",
        "qualifier": "qualifier",
        "toolkit_stack_name": "toolkitStackName",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "resource_tags": "resourceTags",
    },
)
class CdkBootstrapProps:
    def __init__(
        self,
        *,
        aws_account_id: builtins.str,
        aws_region: builtins.str,
        qualifier: builtins.str,
        toolkit_stack_name: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Configuration properties for initializing a Bootstrap instance.

        :param aws_account_id: The AWS account ID associated with the Bootstrap configuration.
        :param aws_region: The AWS region in which the Bootstrap will be performed.
        :param qualifier: The qualifier applied to the Bootstrap.
        :param toolkit_stack_name: The name of the toolkit stack used for Bootstrap.
        :param job_name: An optional name for the Bootstrap job.
        :param job_stage: An optional stage for the Bootstrap job.
        :param resource_tags: Optional resource tags that can be applied during Bootstrap.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37398e5dc48fffd8861bcb2c632fe99d18e406672223915a28931a06671d7348)
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
            check_type(argname="argument toolkit_stack_name", value=toolkit_stack_name, expected_type=type_hints["toolkit_stack_name"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_account_id": aws_account_id,
            "aws_region": aws_region,
            "qualifier": qualifier,
            "toolkit_stack_name": toolkit_stack_name,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        result = self._values.get("aws_account_id")
        assert result is not None, "Required property 'aws_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        result = self._values.get("aws_region")
        assert result is not None, "Required property 'aws_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        result = self._values.get("qualifier")
        assert result is not None, "Required property 'qualifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        result = self._values.get("toolkit_stack_name")
        assert result is not None, "Required property 'toolkit_stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkBootstrapProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.CdkDeployProps",
    jsii_struct_bases=[],
    name_mapping={
        "stacks": "stacks",
        "context": "context",
        "deploy_options": "deployOptions",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "strict": "strict",
        "toolkit_stack_name": "toolkitStackName",
        "wait_for_stack": "waitForStack",
        "wait_for_stack_account_id": "waitForStackAccountId",
        "wait_for_stack_assume_role": "waitForStackAssumeRole",
    },
)
class CdkDeployProps:
    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deploy_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        strict: typing.Optional[builtins.bool] = None,
        toolkit_stack_name: typing.Optional[builtins.str] = None,
        wait_for_stack: typing.Optional[builtins.bool] = None,
        wait_for_stack_account_id: typing.Optional[builtins.str] = None,
        wait_for_stack_assume_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration properties for initializing a Deploy instance.

        :param stacks: An array of stack names to be deployed.
        :param context: Optional context values to provide additional information for deployment.
        :param deploy_options: Optional deployment options.
        :param job_name: An optional name for the Deploy job.
        :param job_stage: An optional stage for the Deploy job.
        :param strict: Enable strict deployment mode.
        :param toolkit_stack_name: Optional toolkit stack name used for deployment.
        :param wait_for_stack: Wait for stacks to complete deployment.
        :param wait_for_stack_account_id: AWS account ID for stack waiting.
        :param wait_for_stack_assume_role: AWS assume role for stack waiting.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3340b2b1e95669df6e03e938c9d4de34609cb8a4b0a6ce593d2e1d61615f8f)
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument deploy_options", value=deploy_options, expected_type=type_hints["deploy_options"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
            check_type(argname="argument toolkit_stack_name", value=toolkit_stack_name, expected_type=type_hints["toolkit_stack_name"])
            check_type(argname="argument wait_for_stack", value=wait_for_stack, expected_type=type_hints["wait_for_stack"])
            check_type(argname="argument wait_for_stack_account_id", value=wait_for_stack_account_id, expected_type=type_hints["wait_for_stack_account_id"])
            check_type(argname="argument wait_for_stack_assume_role", value=wait_for_stack_assume_role, expected_type=type_hints["wait_for_stack_assume_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if context is not None:
            self._values["context"] = context
        if deploy_options is not None:
            self._values["deploy_options"] = deploy_options
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if strict is not None:
            self._values["strict"] = strict
        if toolkit_stack_name is not None:
            self._values["toolkit_stack_name"] = toolkit_stack_name
        if wait_for_stack is not None:
            self._values["wait_for_stack"] = wait_for_stack
        if wait_for_stack_account_id is not None:
            self._values["wait_for_stack_account_id"] = wait_for_stack_account_id
        if wait_for_stack_assume_role is not None:
            self._values["wait_for_stack_assume_role"] = wait_for_stack_assume_role

    @builtins.property
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        result = self._values.get("deploy_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''Enable strict deployment mode.'''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        result = self._values.get("toolkit_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_stack(self) -> typing.Optional[builtins.bool]:
        '''Wait for stacks to complete deployment.'''
        result = self._values.get("wait_for_stack")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        result = self._values.get("wait_for_stack_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        result = self._values.get("wait_for_stack_assume_role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkDeployProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.CdkDiffDeployProps",
    jsii_struct_bases=[],
    name_mapping={"stacks": "stacks", "context": "context"},
)
class CdkDiffDeployProps:
    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Configuration properties for initializing a DiffDeploy instance.

        :param stacks: An array of stack names for which to generate a diff and perform deployment.
        :param context: Optional context values to provide additional information for the diff and deployment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cd226a3f0a1593c412a494e12652d95fdd4dc0470e43ecd474e7e86806d03b)
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if context is not None:
            self._values["context"] = context

    @builtins.property
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkDiffDeployProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.CdkDiffProps",
    jsii_struct_bases=[],
    name_mapping={
        "stacks": "stacks",
        "context": "context",
        "diff_options": "diffOptions",
        "job_name": "jobName",
        "job_stage": "jobStage",
    },
)
class CdkDiffProps:
    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        diff_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration properties for initializing a Diff instance.

        :param stacks: An array of stack names for which to generate a diff.
        :param context: Optional context values to provide additional information for the diff.
        :param diff_options: Optional diff options to customize the diff process.
        :param job_name: An optional name for the Diff job.
        :param job_stage: An optional stage for the Diff job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b86e2c006bbf0acd73f9e414ebd393e3c33cdf2a01046a1c4b2b4c98a8dfa3)
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument diff_options", value=diff_options, expected_type=type_hints["diff_options"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if context is not None:
            self._values["context"] = context
        if diff_options is not None:
            self._values["diff_options"] = diff_options
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        result = self._values.get("diff_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkDiffProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.aws.CdkMirrorToCodecommitProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_region": "awsRegion",
        "infrastructure_tags": "infrastructureTags",
        "mirror_opts": "mirrorOpts",
        "repository_name": "repositoryName",
    },
)
class CdkMirrorToCodecommitProps:
    def __init__(
        self,
        *,
        aws_region: typing.Optional[builtins.str] = None,
        infrastructure_tags: typing.Optional[builtins.str] = None,
        mirror_opts: typing.Optional[typing.Union[_GitMirrorProps_84e02642, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_region: The AWS region you want to operate in. When not set, it would be curl'ed from the current EC2 instance metadata.
        :param infrastructure_tags: Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource. Changed values won't change the tags on an already existing ECR. This string must have the pattern: ``Tag1=Value1,Tag2=Value2``
        :param mirror_opts: Options for the upstream Mirror job.
        :param repository_name: The name of the target Codecommit repository. Default: CI_PROJECT_PATH_SLUG.
        '''
        if isinstance(mirror_opts, dict):
            mirror_opts = _GitMirrorProps_84e02642(**mirror_opts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47df810de3c1bf977eee80a71468d65ca8d2a0a68b57bb789ee943a6eb938cb4)
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument infrastructure_tags", value=infrastructure_tags, expected_type=type_hints["infrastructure_tags"])
            check_type(argname="argument mirror_opts", value=mirror_opts, expected_type=type_hints["mirror_opts"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_region is not None:
            self._values["aws_region"] = aws_region
        if infrastructure_tags is not None:
            self._values["infrastructure_tags"] = infrastructure_tags
        if mirror_opts is not None:
            self._values["mirror_opts"] = mirror_opts
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        result = self._values.get("aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        result = self._values.get("infrastructure_tags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mirror_opts(self) -> typing.Optional[_GitMirrorProps_84e02642]:
        '''Options for the upstream Mirror job.'''
        result = self._values.get("mirror_opts")
        return typing.cast(typing.Optional[_GitMirrorProps_84e02642], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name of the target Codecommit repository.

        :default: CI_PROJECT_PATH_SLUG.
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkMirrorToCodecommitProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@gcix/gcix.aws.ICdkBootstrap")
class ICdkBootstrap(typing_extensions.Protocol):
    '''Represents the interface that a Bootstrap instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        ...

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        ...

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the Bootstrap job.'''
        ...

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> builtins.str:
        '''The stage of the Bootstrap job.'''
        ...

    @job_stage.setter
    def job_stage(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        ...

    @qualifier.setter
    def qualifier(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        ...

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        ...

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...


class _ICdkBootstrapProxy:
    '''Represents the interface that a Bootstrap instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.ICdkBootstrap"

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cdf8dd77884f083481be81ff8a5bf909631727ae0a811673be925c92a313fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e5374b3e70f7d635be60f89ad86c1c844e9e384b4e9d94eeca2601984c44c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd7a4807467d24f33c0b0bf3f21392995a28f1164b218050dcfcfa1a09dfdd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> builtins.str:
        '''The stage of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc42b7319ea4890a28b5bd19482cb71300f6c58f55fc98c457da15a6c1e761a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be143a606737bf44a6f59539ad3c58557f2a546c6671149fa2c8e232f1328f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f5c8868e8d57afaccb5ec5629dadc5e40bf1a267cb766873f40dc70be51f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5803f1441ce607f7f23ba7a147b2a6ba8c30e52f63950b3698a09b8c48f192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkBootstrap).__jsii_proxy_class__ = lambda : _ICdkBootstrapProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.ICdkDeploy")
class ICdkDeploy(typing_extensions.Protocol):
    '''Represents the interface that a Deploy instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        ...

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="strict")
    def strict(self) -> builtins.bool:
        '''Flag indicating if strict deployment mode is enabled.'''
        ...

    @strict.setter
    def strict(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="waitForStack")
    def wait_for_stack(self) -> builtins.bool:
        '''Flag indicating if the deployment should wait for stack completion.'''
        ...

    @wait_for_stack.setter
    def wait_for_stack(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        ...

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="deployOptions")
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        ...

    @deploy_options.setter
    def deploy_options(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        ...

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        ...

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        ...

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="waitForStackAccountId")
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        ...

    @wait_for_stack_account_id.setter
    def wait_for_stack_account_id(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="waitForStackAssumeRole")
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        ...

    @wait_for_stack_assume_role.setter
    def wait_for_stack_assume_role(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ICdkDeployProxy:
    '''Represents the interface that a Deploy instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.ICdkDeploy"

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b293dbac332116f63964a664f1b05236fad22ad5706f84791aa853bbbead173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="strict")
    def strict(self) -> builtins.bool:
        '''Flag indicating if strict deployment mode is enabled.'''
        return typing.cast(builtins.bool, jsii.get(self, "strict"))

    @strict.setter
    def strict(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee50b049e139f4e39d17229d2bae7c5e52c7825589b69192e3eaae91d6de09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strict", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStack")
    def wait_for_stack(self) -> builtins.bool:
        '''Flag indicating if the deployment should wait for stack completion.'''
        return typing.cast(builtins.bool, jsii.get(self, "waitForStack"))

    @wait_for_stack.setter
    def wait_for_stack(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14eb3a4ba56e331539230637502241d194a0cb798aae3eb588f2c1fc3b078b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStack", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7684e7e9949953457b93fa92d73e21dc87bf6c7f7afc7fabed03ad20f7f8cf77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="deployOptions")
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deployOptions"))

    @deploy_options.setter
    def deploy_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320b863290e2e36fe94338325bbfa90dac63ec4b4252c53898be07b0b17b6cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdfd97df55ecd6edc7acf50af406acddea1bfbf28a0663d24d8f6f33429d592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f436c92d8c36402e1fe3ba8f7b560562ca6e75027036e00fff2b985612530952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52945067d98fc5230384ceb86f4dc49d9688ed6f4ead42114e17ced244ce94b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAccountId")
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAccountId"))

    @wait_for_stack_account_id.setter
    def wait_for_stack_account_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b14bd4d9690a5f3f5d5fe4ff69f468fe41594ffac4e7fc458fd6156a7021260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAssumeRole")
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAssumeRole"))

    @wait_for_stack_assume_role.setter
    def wait_for_stack_assume_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d132bb77f90f56ac9fde731d714b1ac09a0df849d9febbc3f0248224f38c1948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAssumeRole", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkDeploy).__jsii_proxy_class__ = lambda : _ICdkDeployProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.ICdkDiff")
class ICdkDiff(typing_extensions.Protocol):
    '''Represents the interface that a Diff instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        ...

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        ...

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="diffOptions")
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        ...

    @diff_options.setter
    def diff_options(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        ...

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        ...

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ICdkDiffProxy:
    '''Represents the interface that a Diff instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.ICdkDiff"

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dfbc70949707cb8b4e391c24abd625dcad5bbe1eb9aa2570d5f07d07a87be06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c27569098ca7c11eb215bb1b42d5b7904b65a83dee930b508509ffd4a52347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="diffOptions")
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diffOptions"))

    @diff_options.setter
    def diff_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f6fe2207f2a1bf57e48656d7fbb0aeec1b6cfd7e107cb68932c8a44d3869c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f48a693c4354c3b997392a7f3c401da32929c81cd0b3b8d499452eb14eed8c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe9a510c6a87778dae422141e5174fc42568c85c075d52af77d2765efee0723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkDiff).__jsii_proxy_class__ = lambda : _ICdkDiffProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.ICdkDiffDeploy")
class ICdkDiffDeploy(typing_extensions.Protocol):
    '''Represents the interface that a DiffDeploy instance adheres to.'''

    @builtins.property
    @jsii.member(jsii_name="deployJob")
    def deploy_job(self) -> "CdkDeploy":
        '''The instance of the Deploy job associated with this DiffDeploy instance.'''
        ...

    @deploy_job.setter
    def deploy_job(self, value: "CdkDeploy") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="diffJob")
    def diff_job(self) -> "CdkDiff":
        '''The instance of the Diff job associated with this DiffDeploy instance.'''
        ...

    @diff_job.setter
    def diff_job(self, value: "CdkDiff") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        ...

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        ...

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...


class _ICdkDiffDeployProxy:
    '''Represents the interface that a DiffDeploy instance adheres to.'''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.ICdkDiffDeploy"

    @builtins.property
    @jsii.member(jsii_name="deployJob")
    def deploy_job(self) -> "CdkDeploy":
        '''The instance of the Deploy job associated with this DiffDeploy instance.'''
        return typing.cast("CdkDeploy", jsii.get(self, "deployJob"))

    @deploy_job.setter
    def deploy_job(self, value: "CdkDeploy") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df26671a02e8fd866809787f4f23cce08756f7e0382ad90e7fe6d5aebd1d2abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployJob", value)

    @builtins.property
    @jsii.member(jsii_name="diffJob")
    def diff_job(self) -> "CdkDiff":
        '''The instance of the Diff job associated with this DiffDeploy instance.'''
        return typing.cast("CdkDiff", jsii.get(self, "diffJob"))

    @diff_job.setter
    def diff_job(self, value: "CdkDiff") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175d4f5c9ffa3048843b56a9c4bab323107f99432dc9968b35463da4ad85ccee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffJob", value)

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f48042f605101d4f76c483b8d09f8f4c6f0862a06f30722e2bd23afa4d5617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7c2e624808af6dbcfe1f889566334dd46b47acd8db4ff72a7f4ff92a1cb03f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkDiffDeploy).__jsii_proxy_class__ = lambda : _ICdkDiffDeployProxy


@jsii.interface(jsii_type="@gcix/gcix.aws.ICdkMirrorToCodecommit")
class ICdkMirrorToCodecommit(_IGitMirror_5d079bec, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the target Codecommit repository.

        :default: CI_PROJECT_PATH_SLUG.
        '''
        ...

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        ...

    @aws_region.setter
    def aws_region(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="infrastructureTags")
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        ...

    @infrastructure_tags.setter
    def infrastructure_tags(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ICdkMirrorToCodecommitProxy(
    jsii.proxy_for(_IGitMirror_5d079bec), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.aws.ICdkMirrorToCodecommit"

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the target Codecommit repository.

        :default: CI_PROJECT_PATH_SLUG.
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f929cef14fa91579128711bf0f9ba8e63ad4315f91c22d1e2ad145b559f7d24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20969918eacf1bf43f4097ffa8b39204e30591ee65ff026026f2538177221dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureTags")
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureTags"))

    @infrastructure_tags.setter
    def infrastructure_tags(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc09064ce8e79620db65517d3e3ef1f2663b38a560bb9e4e4f5cf5c6a5a5b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureTags", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkMirrorToCodecommit).__jsii_proxy_class__ = lambda : _ICdkMirrorToCodecommitProxy


@jsii.implements(ICdkBootstrap)
class CdkBootstrap(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.CdkBootstrap",
):
    '''Creates an instance of Bootstrap.'''

    def __init__(
        self,
        *,
        aws_account_id: builtins.str,
        aws_region: builtins.str,
        qualifier: builtins.str,
        toolkit_stack_name: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param aws_account_id: The AWS account ID associated with the Bootstrap configuration.
        :param aws_region: The AWS region in which the Bootstrap will be performed.
        :param qualifier: The qualifier applied to the Bootstrap.
        :param toolkit_stack_name: The name of the toolkit stack used for Bootstrap.
        :param job_name: An optional name for the Bootstrap job.
        :param job_stage: An optional stage for the Bootstrap job.
        :param resource_tags: Optional resource tags that can be applied during Bootstrap.
        '''
        props = CdkBootstrapProps(
            aws_account_id=aws_account_id,
            aws_region=aws_region,
            qualifier=qualifier,
            toolkit_stack_name=toolkit_stack_name,
            job_name=job_name,
            job_stage=job_stage,
            resource_tags=resource_tags,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        '''The AWS account ID associated with the Bootstrap configuration.'''
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81893f35b86aed8fa153c49178978a647cfab30cd214a669295fb222f7bca1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        '''The AWS region in which the Bootstrap will be performed.'''
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a495cac46cfac723d07eec7ee112dc54e4365946b823263c6231cb7c1905eabd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94eddd34834a55a1a396fb6f5bb523ef28cc3482021e210e9cd85a8737b89b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> builtins.str:
        '''The stage of the Bootstrap job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf39e1809aafe676300b9e587e8fc8fbe522422ea90ab03fe6c44060226d05c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> builtins.str:
        '''The qualifier applied to the Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4a5bca8b714f0aaa29c7e7224a9d92a0159cf3580ca396186ea05bc2e9d5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> builtins.str:
        '''The name of the toolkit stack used for Bootstrap.'''
        return typing.cast(builtins.str, jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1120b3e3afcfbb436200d7558d051d6e7743ea7a6ef651feec1a0c2cb7511577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional resource tags that can be applied during Bootstrap.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8ca2392ddd6e52bd22d9f2ea96b5f9458b073f4e78f21cf840693b401030f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)


@jsii.implements(ICdkDeploy)
class CdkDeploy(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.CdkDeploy",
):
    '''A class that manages the configuration and rendering of a Deploy job.

    Inherits from the base Job class and implements the IDeploy interface.
    '''

    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deploy_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        strict: typing.Optional[builtins.bool] = None,
        toolkit_stack_name: typing.Optional[builtins.str] = None,
        wait_for_stack: typing.Optional[builtins.bool] = None,
        wait_for_stack_account_id: typing.Optional[builtins.str] = None,
        wait_for_stack_assume_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates an instance of Deploy.

        :param stacks: An array of stack names to be deployed.
        :param context: Optional context values to provide additional information for deployment.
        :param deploy_options: Optional deployment options.
        :param job_name: An optional name for the Deploy job.
        :param job_stage: An optional stage for the Deploy job.
        :param strict: Enable strict deployment mode.
        :param toolkit_stack_name: Optional toolkit stack name used for deployment.
        :param wait_for_stack: Wait for stacks to complete deployment.
        :param wait_for_stack_account_id: AWS account ID for stack waiting.
        :param wait_for_stack_assume_role: AWS assume role for stack waiting.
        '''
        props = CdkDeployProps(
            stacks=stacks,
            context=context,
            deploy_options=deploy_options,
            job_name=job_name,
            job_stage=job_stage,
            strict=strict,
            toolkit_stack_name=toolkit_stack_name,
            wait_for_stack=wait_for_stack,
            wait_for_stack_account_id=wait_for_stack_account_id,
            wait_for_stack_assume_role=wait_for_stack_assume_role,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Renders the Deploy job's configuration and scripts.

        :return: The rendered configuration and scripts.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names to be deployed.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6464cb0b057c96521149750f1423dc6c0ccb24c01fde252b24888ba02a9ba34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="strict")
    def strict(self) -> builtins.bool:
        '''Flag indicating if strict deployment mode is enabled.'''
        return typing.cast(builtins.bool, jsii.get(self, "strict"))

    @strict.setter
    def strict(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74948b9fe9e56c73081c38335aea9f90fc77c55302673b8af62f7b14a0093878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strict", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStack")
    def wait_for_stack(self) -> builtins.bool:
        '''Flag indicating if the deployment should wait for stack completion.'''
        return typing.cast(builtins.bool, jsii.get(self, "waitForStack"))

    @wait_for_stack.setter
    def wait_for_stack(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0342bb6b52874bc9e06caa20f13c65e6b0b67ceb63608e99e12362c6d411854f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStack", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd0cebcfb45d12848b72214eb34a8821fd2219005dffceb13feaa2feee23f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="deployOptions")
    def deploy_options(self) -> typing.Optional[builtins.str]:
        '''Optional deployment options.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deployOptions"))

    @deploy_options.setter
    def deploy_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafbcc86fc2df8aa0283125ff99a357c5f21d1274d4be4fffb99f739b9b98ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4746e690212058337cff0fa4dfb7ad5920458b05a9c50707a97958df02d14794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Deploy job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7473a8f04bab3b080d916911979d575a72f40a189ab4849be68545aee92ad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)

    @builtins.property
    @jsii.member(jsii_name="toolkitStackName")
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''Optional toolkit stack name used for deployment.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toolkitStackName"))

    @toolkit_stack_name.setter
    def toolkit_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9640b8676c0acb8af5a1fa2b10d101ad594db38bca666f76e91776d13e453074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolkitStackName", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAccountId")
    def wait_for_stack_account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account ID for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAccountId"))

    @wait_for_stack_account_id.setter
    def wait_for_stack_account_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f42e54fdf8eba4082d867dfc259f5250bfc41d4d8921a2e92b41df2856a671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="waitForStackAssumeRole")
    def wait_for_stack_assume_role(self) -> typing.Optional[builtins.str]:
        '''AWS assume role for stack waiting.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitForStackAssumeRole"))

    @wait_for_stack_assume_role.setter
    def wait_for_stack_assume_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2269c901b587b7e1a95901d75e0d40eda3236df3bbe1dda78f30b723dfe693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForStackAssumeRole", value)


@jsii.implements(ICdkDiff)
class CdkDiff(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.CdkDiff",
):
    '''A class that manages the configuration and rendering of a Diff job.

    Inherits from the base Job class and implements the IDiff interface.
    '''

    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        diff_options: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates an instance of Diff.

        :param stacks: An array of stack names for which to generate a diff.
        :param context: Optional context values to provide additional information for the diff.
        :param diff_options: Optional diff options to customize the diff process.
        :param job_name: An optional name for the Diff job.
        :param job_stage: An optional stage for the Diff job.
        '''
        props = CdkDiffProps(
            stacks=stacks,
            context=context,
            diff_options=diff_options,
            job_name=job_name,
            job_stage=job_stage,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a94f797464ad26b46665cecd78cfa6fcdcf6ef8dad9b9d64ad07a245dddbcd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a061adb48b54909f11b4773618703a442c05f2bad276efd9a1a86994bf51e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="diffOptions")
    def diff_options(self) -> typing.Optional[builtins.str]:
        '''Optional diff options to customize the diff process.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diffOptions"))

    @diff_options.setter
    def diff_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd731dba380c9e8d121f5d611ea4da506a584fdc6ed0173beeb5263936ffe66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffOptions", value)

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c837a2eb8848957fbfde4b20e61ca2510dfbca7e10862e87a9d18d5f378eb119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value)

    @builtins.property
    @jsii.member(jsii_name="jobStage")
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''An optional stage for the Diff job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStage"))

    @job_stage.setter
    def job_stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b4fb7a0a582bd77510656287c9e5236d78e847932b25b29e7b72563ed6f555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStage", value)


@jsii.implements(ICdkDiffDeploy)
class CdkDiffDeploy(
    _JobCollection_0289800c,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.CdkDiffDeploy",
):
    '''A class that manages the configuration and execution of combined Diff and Deploy operations.

    Inherits from the base JobCollection class and implements the IDiffDeploy interface.
    '''

    def __init__(
        self,
        *,
        stacks: typing.Sequence[builtins.str],
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Creates an instance of DiffDeploy.

        :param stacks: An array of stack names for which to generate a diff and perform deployment.
        :param context: Optional context values to provide additional information for the diff and deployment.
        '''
        props = CdkDiffDeployProps(stacks=stacks, context=context)

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="deployJob")
    def deploy_job(self) -> CdkDeploy:
        '''The instance of the Deploy job associated with this DiffDeploy instance.'''
        return typing.cast(CdkDeploy, jsii.get(self, "deployJob"))

    @deploy_job.setter
    def deploy_job(self, value: CdkDeploy) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b9d622c7d5af992f1dd4521a6fd7435f2c5c5026c28dc4be64024ed41aa499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployJob", value)

    @builtins.property
    @jsii.member(jsii_name="diffJob")
    def diff_job(self) -> CdkDiff:
        '''The instance of the Diff job associated with this DiffDeploy instance.'''
        return typing.cast(CdkDiff, jsii.get(self, "diffJob"))

    @diff_job.setter
    def diff_job(self, value: CdkDiff) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39accd7f1ad3e0ab041e10f27507cfadbb07134c40408b6fd8d9db3bf569f67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffJob", value)

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[builtins.str]:
        '''An array of stack names for which to generate a diff and perform deployment.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stacks"))

    @stacks.setter
    def stacks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f64485abb2c0684e39aec69517f8c01333d625a995fe65f2f93eadd4480e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stacks", value)

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional context values to provide additional information for the diff and deployment.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "context"))

    @context.setter
    def context(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3eb2a28a361ceff4489d5b57f72300aefcffecbcf3a73057fbe1dc942c4209f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)


@jsii.implements(ICdkMirrorToCodecommit)
class CdkMirrorToCodecommit(
    _GitMirror_6ee7350e,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.aws.CdkMirrorToCodecommit",
):
    '''This job clones the CI_COMMIT_REF_NAME of the current repository and forcefully pushes this REF to a AWS CodeCommit repository.

    This job requires following IAM permissions:

    - codecommit:CreateRepository
    - codecommit:GetRepository
    - codecommit:CreateBranch
    - codecommit:GitPush
    - codecommit:TagResource

    You could also limit the resource to ``!Sub arn:aws:codecommit:${AWS::Region}:${AWS::AccountId}:<repository-name>``.
    '''

    def __init__(
        self,
        *,
        aws_region: typing.Optional[builtins.str] = None,
        infrastructure_tags: typing.Optional[builtins.str] = None,
        mirror_opts: typing.Optional[typing.Union[_GitMirrorProps_84e02642, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_region: The AWS region you want to operate in. When not set, it would be curl'ed from the current EC2 instance metadata.
        :param infrastructure_tags: Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource. Changed values won't change the tags on an already existing ECR. This string must have the pattern: ``Tag1=Value1,Tag2=Value2``
        :param mirror_opts: Options for the upstream Mirror job.
        :param repository_name: The name of the target Codecommit repository. Default: CI_PROJECT_PATH_SLUG.
        '''
        props = CdkMirrorToCodecommitProps(
            aws_region=aws_region,
            infrastructure_tags=infrastructure_tags,
            mirror_opts=mirror_opts,
            repository_name=repository_name,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the target Codecommit repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed4c555820f92912d5d01e582d37dea021eb970f6a4688d06cfd99532501993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region you want to operate in.

        When not set, it would be
        curl'ed from the current EC2 instance metadata.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e7bba4c0156b9b0df8a9d33ed023329508101624745635fec23a3aa67091ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureTags")
    def infrastructure_tags(self) -> typing.Optional[builtins.str]:
        '''Only if the ECR would be created on the first call, these AWS Tags becomes applied to the AWS Codecommit resource.

        Changed values won't
        change the tags on an already existing ECR. This string must have the
        pattern: ``Tag1=Value1,Tag2=Value2``
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureTags"))

    @infrastructure_tags.setter
    def infrastructure_tags(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662a744c2209dff133c67b7498c40695277df5de95e1ca1c777034aee2f46547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureTags", value)

    @builtins.property
    @jsii.member(jsii_name="mirrorOpts")
    def mirror_opts(self) -> typing.Optional[_GitMirrorProps_84e02642]:
        return typing.cast(typing.Optional[_GitMirrorProps_84e02642], jsii.get(self, "mirrorOpts"))

    @mirror_opts.setter
    def mirror_opts(self, value: typing.Optional[_GitMirrorProps_84e02642]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea21c181ffa7fffea1bb0e2a224bd0737fa56cef6dab7e14a5bb05dd719b5036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorOpts", value)


__all__ = [
    "AWSAccount",
    "CdkBootstrap",
    "CdkBootstrapProps",
    "CdkDeploy",
    "CdkDeployProps",
    "CdkDiff",
    "CdkDiffDeploy",
    "CdkDiffDeployProps",
    "CdkDiffProps",
    "CdkMirrorToCodecommit",
    "CdkMirrorToCodecommitProps",
    "ICdkBootstrap",
    "ICdkDeploy",
    "ICdkDiff",
    "ICdkDiffDeploy",
    "ICdkMirrorToCodecommit",
]

publication.publish()

def _typecheckingstub__37398e5dc48fffd8861bcb2c632fe99d18e406672223915a28931a06671d7348(
    *,
    aws_account_id: builtins.str,
    aws_region: builtins.str,
    qualifier: builtins.str,
    toolkit_stack_name: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3340b2b1e95669df6e03e938c9d4de34609cb8a4b0a6ce593d2e1d61615f8f(
    *,
    stacks: typing.Sequence[builtins.str],
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    deploy_options: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    strict: typing.Optional[builtins.bool] = None,
    toolkit_stack_name: typing.Optional[builtins.str] = None,
    wait_for_stack: typing.Optional[builtins.bool] = None,
    wait_for_stack_account_id: typing.Optional[builtins.str] = None,
    wait_for_stack_assume_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cd226a3f0a1593c412a494e12652d95fdd4dc0470e43ecd474e7e86806d03b(
    *,
    stacks: typing.Sequence[builtins.str],
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b86e2c006bbf0acd73f9e414ebd393e3c33cdf2a01046a1c4b2b4c98a8dfa3(
    *,
    stacks: typing.Sequence[builtins.str],
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    diff_options: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47df810de3c1bf977eee80a71468d65ca8d2a0a68b57bb789ee943a6eb938cb4(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    infrastructure_tags: typing.Optional[builtins.str] = None,
    mirror_opts: typing.Optional[typing.Union[_GitMirrorProps_84e02642, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cdf8dd77884f083481be81ff8a5bf909631727ae0a811673be925c92a313fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e5374b3e70f7d635be60f89ad86c1c844e9e384b4e9d94eeca2601984c44c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd7a4807467d24f33c0b0bf3f21392995a28f1164b218050dcfcfa1a09dfdd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc42b7319ea4890a28b5bd19482cb71300f6c58f55fc98c457da15a6c1e761a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be143a606737bf44a6f59539ad3c58557f2a546c6671149fa2c8e232f1328f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f5c8868e8d57afaccb5ec5629dadc5e40bf1a267cb766873f40dc70be51f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5803f1441ce607f7f23ba7a147b2a6ba8c30e52f63950b3698a09b8c48f192(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b293dbac332116f63964a664f1b05236fad22ad5706f84791aa853bbbead173(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee50b049e139f4e39d17229d2bae7c5e52c7825589b69192e3eaae91d6de09d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14eb3a4ba56e331539230637502241d194a0cb798aae3eb588f2c1fc3b078b9b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7684e7e9949953457b93fa92d73e21dc87bf6c7f7afc7fabed03ad20f7f8cf77(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320b863290e2e36fe94338325bbfa90dac63ec4b4252c53898be07b0b17b6cc8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdfd97df55ecd6edc7acf50af406acddea1bfbf28a0663d24d8f6f33429d592(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f436c92d8c36402e1fe3ba8f7b560562ca6e75027036e00fff2b985612530952(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52945067d98fc5230384ceb86f4dc49d9688ed6f4ead42114e17ced244ce94b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b14bd4d9690a5f3f5d5fe4ff69f468fe41594ffac4e7fc458fd6156a7021260(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d132bb77f90f56ac9fde731d714b1ac09a0df849d9febbc3f0248224f38c1948(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dfbc70949707cb8b4e391c24abd625dcad5bbe1eb9aa2570d5f07d07a87be06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c27569098ca7c11eb215bb1b42d5b7904b65a83dee930b508509ffd4a52347(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f6fe2207f2a1bf57e48656d7fbb0aeec1b6cfd7e107cb68932c8a44d3869c8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f48a693c4354c3b997392a7f3c401da32929c81cd0b3b8d499452eb14eed8c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe9a510c6a87778dae422141e5174fc42568c85c075d52af77d2765efee0723(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df26671a02e8fd866809787f4f23cce08756f7e0382ad90e7fe6d5aebd1d2abb(
    value: CdkDeploy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175d4f5c9ffa3048843b56a9c4bab323107f99432dc9968b35463da4ad85ccee(
    value: CdkDiff,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f48042f605101d4f76c483b8d09f8f4c6f0862a06f30722e2bd23afa4d5617(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7c2e624808af6dbcfe1f889566334dd46b47acd8db4ff72a7f4ff92a1cb03f(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f929cef14fa91579128711bf0f9ba8e63ad4315f91c22d1e2ad145b559f7d24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20969918eacf1bf43f4097ffa8b39204e30591ee65ff026026f2538177221dcc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc09064ce8e79620db65517d3e3ef1f2663b38a560bb9e4e4f5cf5c6a5a5b08(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81893f35b86aed8fa153c49178978a647cfab30cd214a669295fb222f7bca1e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a495cac46cfac723d07eec7ee112dc54e4365946b823263c6231cb7c1905eabd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94eddd34834a55a1a396fb6f5bb523ef28cc3482021e210e9cd85a8737b89b28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf39e1809aafe676300b9e587e8fc8fbe522422ea90ab03fe6c44060226d05c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4a5bca8b714f0aaa29c7e7224a9d92a0159cf3580ca396186ea05bc2e9d5e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1120b3e3afcfbb436200d7558d051d6e7743ea7a6ef651feec1a0c2cb7511577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8ca2392ddd6e52bd22d9f2ea96b5f9458b073f4e78f21cf840693b401030f9(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6464cb0b057c96521149750f1423dc6c0ccb24c01fde252b24888ba02a9ba34(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74948b9fe9e56c73081c38335aea9f90fc77c55302673b8af62f7b14a0093878(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0342bb6b52874bc9e06caa20f13c65e6b0b67ceb63608e99e12362c6d411854f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd0cebcfb45d12848b72214eb34a8821fd2219005dffceb13feaa2feee23f99(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafbcc86fc2df8aa0283125ff99a357c5f21d1274d4be4fffb99f739b9b98ee6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4746e690212058337cff0fa4dfb7ad5920458b05a9c50707a97958df02d14794(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7473a8f04bab3b080d916911979d575a72f40a189ab4849be68545aee92ad4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9640b8676c0acb8af5a1fa2b10d101ad594db38bca666f76e91776d13e453074(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f42e54fdf8eba4082d867dfc259f5250bfc41d4d8921a2e92b41df2856a671(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2269c901b587b7e1a95901d75e0d40eda3236df3bbe1dda78f30b723dfe693(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a94f797464ad26b46665cecd78cfa6fcdcf6ef8dad9b9d64ad07a245dddbcd3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a061adb48b54909f11b4773618703a442c05f2bad276efd9a1a86994bf51e5(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd731dba380c9e8d121f5d611ea4da506a584fdc6ed0173beeb5263936ffe66(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c837a2eb8848957fbfde4b20e61ca2510dfbca7e10862e87a9d18d5f378eb119(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b4fb7a0a582bd77510656287c9e5236d78e847932b25b29e7b72563ed6f555(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b9d622c7d5af992f1dd4521a6fd7435f2c5c5026c28dc4be64024ed41aa499(
    value: CdkDeploy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39accd7f1ad3e0ab041e10f27507cfadbb07134c40408b6fd8d9db3bf569f67e(
    value: CdkDiff,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f64485abb2c0684e39aec69517f8c01333d625a995fe65f2f93eadd4480e13(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3eb2a28a361ceff4489d5b57f72300aefcffecbcf3a73057fbe1dc942c4209f(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed4c555820f92912d5d01e582d37dea021eb970f6a4688d06cfd99532501993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e7bba4c0156b9b0df8a9d33ed023329508101624745635fec23a3aa67091ba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662a744c2209dff133c67b7498c40695277df5de95e1ca1c777034aee2f46547(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea21c181ffa7fffea1bb0e2a224bd0737fa56cef6dab7e14a5bb05dd719b5036(
    value: typing.Optional[_GitMirrorProps_84e02642],
) -> None:
    """Type checking stubs"""
    pass
