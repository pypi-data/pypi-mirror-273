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

from .. import (
    Image as _Image_e46ac833,
    Job as _Job_20682b42,
    JobCollection as _JobCollection_0289800c,
)


@jsii.data_type(
    jsii_type="@gcix/gcix.container.AWSRegistryProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "region": "region"},
)
class AWSRegistryProps:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: AWS account id. Default: AWSAccount.awsAccountId()
        :param region: AWS region where the ECR repository lives in. Default: AWSAccount.awsRegion()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70690165055af01ed6463f1d83e17300344a1a45d59ec7b9f16882e9308da882)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account id.

        :default: AWSAccount.awsAccountId()
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''AWS region where the ECR repository lives in.

        :default: AWSAccount.awsRegion()
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AWSRegistryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.BuildContainerCollectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "docker_client_config": "dockerClientConfig",
        "do_crane_push": "doCranePush",
        "do_dive_scan": "doDiveScan",
        "do_trivyignore_check": "doTrivyignoreCheck",
        "do_trivy_scan": "doTrivyScan",
        "image_name": "imageName",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "registry": "registry",
    },
)
class BuildContainerCollectionProps:
    def __init__(
        self,
        *,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        do_crane_push: typing.Optional[builtins.bool] = None,
        do_dive_scan: typing.Optional[builtins.bool] = None,
        do_trivyignore_check: typing.Optional[builtins.bool] = None,
        do_trivy_scan: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        registry: typing.Optional[typing.Union[builtins.str, "Registry"]] = None,
    ) -> None:
        '''
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param do_crane_push: Set to ``false`` to skip the Crane push job. Default: true
        :param do_dive_scan: Set to ``false`` to skip the Dive scan job. Default: true
        :param do_trivyignore_check: Set to ``false`` to skip the existance check of the ``.trivyignore`` file. Default: true
        :param do_trivy_scan: Set to ``false`` to skip the Trivy scan job. Default: true
        :param image_name: Image name with stage in the registry. e.g. username/imageName. Default: PredefinedVariables.ciProjectName
        :param image_tag: Image tag. Depending of the build it defaults either to the git tag or to the actual branch name. Default: PredefinedVariables.ciCommitRefName
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param registry: Container registry to push the image to. If the container registry needs authentication, you have to provide a ``DockerClientConfig`` object with credentials. Default: Registry.DOCKER
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ff9c385c6297e1a0adfb206009578373904ad51c5a0e329f1a46947138992b)
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument do_crane_push", value=do_crane_push, expected_type=type_hints["do_crane_push"])
            check_type(argname="argument do_dive_scan", value=do_dive_scan, expected_type=type_hints["do_dive_scan"])
            check_type(argname="argument do_trivyignore_check", value=do_trivyignore_check, expected_type=type_hints["do_trivyignore_check"])
            check_type(argname="argument do_trivy_scan", value=do_trivy_scan, expected_type=type_hints["do_trivy_scan"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if do_crane_push is not None:
            self._values["do_crane_push"] = do_crane_push
        if do_dive_scan is not None:
            self._values["do_dive_scan"] = do_dive_scan
        if do_trivyignore_check is not None:
            self._values["do_trivyignore_check"] = do_trivyignore_check
        if do_trivy_scan is not None:
            self._values["do_trivy_scan"] = do_trivy_scan
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if registry is not None:
            self._values["registry"] = registry

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def do_crane_push(self) -> typing.Optional[builtins.bool]:
        '''Set to ``false`` to skip the Crane push job.

        :default: true
        '''
        result = self._values.get("do_crane_push")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def do_dive_scan(self) -> typing.Optional[builtins.bool]:
        '''Set to ``false`` to skip the Dive scan job.

        :default: true
        '''
        result = self._values.get("do_dive_scan")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def do_trivyignore_check(self) -> typing.Optional[builtins.bool]:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.

        :default: true
        '''
        result = self._values.get("do_trivyignore_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def do_trivy_scan(self) -> typing.Optional[builtins.bool]:
        '''Set to ``false`` to skip the Trivy scan job.

        :default: true
        '''
        result = self._values.get("do_trivy_scan")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Image name with stage in the registry.

        e.g. username/imageName.

        :default: PredefinedVariables.ciProjectName
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''Image tag.

        Depending of the build it defaults either to the git tag or
        to the actual branch name.

        :default: PredefinedVariables.ciCommitRefName
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry(self) -> typing.Optional[typing.Union[builtins.str, "Registry"]]:
        '''Container registry to push the image to.

        If the container registry
        needs authentication, you have to provide a ``DockerClientConfig`` object
        with credentials.

        :default: Registry.DOCKER
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "Registry"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildContainerCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.CopyContainerCollectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_name": "imageName",
        "image_tag": "imageTag",
        "docker_client_config": "dockerClientConfig",
        "do_dive_scan": "doDiveScan",
        "do_trivyignore_check": "doTrivyignoreCheck",
        "do_trivy_scan": "doTrivyScan",
        "dst_registry": "dstRegistry",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "src_registry": "srcRegistry",
    },
)
class CopyContainerCollectionProps:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        image_tag: builtins.str,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        do_dive_scan: typing.Optional[builtins.bool] = None,
        do_trivyignore_check: typing.Optional[builtins.bool] = None,
        do_trivy_scan: typing.Optional[builtins.bool] = None,
        dst_registry: typing.Optional[typing.Union[builtins.str, "Registry"]] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        src_registry: typing.Optional[typing.Union[builtins.str, "Registry"]] = None,
    ) -> None:
        '''
        :param image_name: Image name with stage in the registry. e.g. username/image_name.
        :param image_tag: Container image tag to pull from ``srcRegistry`` and push to ``dstRegistry``.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param do_dive_scan: Set to ``false`` to skip the Dive scan job. Default: true
        :param do_trivyignore_check: Set to ``false`` to skip the existance check of the ``.trivyignore`` file. Default: true
        :param do_trivy_scan: Set to ``false`` to skip the Trivy scan job. Default: true
        :param dst_registry: Container registry to push the image to. If the container registry needs authentication, you have to provide a ``DockerClientConfig`` object with credentials. Default: Registry.DOCKER
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param src_registry: Container registry to pull the image from. If the container registry needs authentication, you have to provide a ``DockerClientConfig`` object with credentials. Default: Registry.DOCKER
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3db202194708972a921f7bd23b4b2751374f8e11c927c45e43ca01e05e57e3)
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument do_dive_scan", value=do_dive_scan, expected_type=type_hints["do_dive_scan"])
            check_type(argname="argument do_trivyignore_check", value=do_trivyignore_check, expected_type=type_hints["do_trivyignore_check"])
            check_type(argname="argument do_trivy_scan", value=do_trivy_scan, expected_type=type_hints["do_trivy_scan"])
            check_type(argname="argument dst_registry", value=dst_registry, expected_type=type_hints["dst_registry"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument src_registry", value=src_registry, expected_type=type_hints["src_registry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_name": image_name,
            "image_tag": image_tag,
        }
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if do_dive_scan is not None:
            self._values["do_dive_scan"] = do_dive_scan
        if do_trivyignore_check is not None:
            self._values["do_trivyignore_check"] = do_trivyignore_check
        if do_trivy_scan is not None:
            self._values["do_trivy_scan"] = do_trivy_scan
        if dst_registry is not None:
            self._values["dst_registry"] = dst_registry
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if src_registry is not None:
            self._values["src_registry"] = src_registry

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Image name with stage in the registry.

        e.g. username/image_name.
        '''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''Container image tag to pull from ``srcRegistry`` and push to ``dstRegistry``.'''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def do_dive_scan(self) -> typing.Optional[builtins.bool]:
        '''Set to ``false`` to skip the Dive scan job.

        :default: true
        '''
        result = self._values.get("do_dive_scan")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def do_trivyignore_check(self) -> typing.Optional[builtins.bool]:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.

        :default: true
        '''
        result = self._values.get("do_trivyignore_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def do_trivy_scan(self) -> typing.Optional[builtins.bool]:
        '''Set to ``false`` to skip the Trivy scan job.

        :default: true
        '''
        result = self._values.get("do_trivy_scan")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dst_registry(self) -> typing.Optional[typing.Union[builtins.str, "Registry"]]:
        '''Container registry to push the image to.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.

        :default: Registry.DOCKER
        '''
        result = self._values.get("dst_registry")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "Registry"]], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def src_registry(self) -> typing.Optional[typing.Union[builtins.str, "Registry"]]:
        '''Container registry to pull the image from.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.

        :default: Registry.DOCKER
        '''
        result = self._values.get("src_registry")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "Registry"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CopyContainerCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.CraneCopyProps",
    jsii_struct_bases=[],
    name_mapping={
        "dst_registry": "dstRegistry",
        "src_registry": "srcRegistry",
        "docker_client_config": "dockerClientConfig",
        "job_name": "jobName",
        "job_stage": "jobStage",
    },
)
class CraneCopyProps:
    def __init__(
        self,
        *,
        dst_registry: typing.Union[builtins.str, "Registry"],
        src_registry: typing.Union[builtins.str, "Registry"],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param src_registry: Registry URL to copy container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283b893e3831d11cacf41e61a68451d11197db97ea7dbe634f0b7a1c8a4b2556)
            check_type(argname="argument dst_registry", value=dst_registry, expected_type=type_hints["dst_registry"])
            check_type(argname="argument src_registry", value=src_registry, expected_type=type_hints["src_registry"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dst_registry": dst_registry,
            "src_registry": src_registry,
        }
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image to.'''
        result = self._values.get("dst_registry")
        assert result is not None, "Required property 'dst_registry' is missing"
        return typing.cast(typing.Union[builtins.str, "Registry"], result)

    @builtins.property
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image from.'''
        result = self._values.get("src_registry")
        assert result is not None, "Required property 'src_registry' is missing"
        return typing.cast(typing.Union[builtins.str, "Registry"], result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CraneCopyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.CranePullProps",
    jsii_struct_bases=[],
    name_mapping={
        "src_registry": "srcRegistry",
        "docker_client_config": "dockerClientConfig",
        "image_name": "imageName",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "tar_path": "tarPath",
    },
)
class CranePullProps:
    def __init__(
        self,
        *,
        src_registry: typing.Union[builtins.str, "Registry"],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param src_registry: Registry URL to pull container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image with namespace to pull from ``srcRegistry``. Default: PredefinedVariables.ciProjectName
        :param image_tag: Tag of the image which will be pulled. Default: latest
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to save the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af47f2a968c387561169d8e4411bcf7ea9b8f70b4ae889ba5979fa2cf9b927b)
            check_type(argname="argument src_registry", value=src_registry, expected_type=type_hints["src_registry"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument tar_path", value=tar_path, expected_type=type_hints["tar_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "src_registry": src_registry,
        }
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if tar_path is not None:
            self._values["tar_path"] = tar_path

    @builtins.property
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to pull container image from.'''
        result = self._values.get("src_registry")
        assert result is not None, "Required property 'src_registry' is missing"
        return typing.cast(typing.Union[builtins.str, "Registry"], result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Container image with namespace to pull from ``srcRegistry``.

        :default: PredefinedVariables.ciProjectName
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''Tag of the image which will be pulled.

        :default: latest
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Path where to save the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        result = self._values.get("tar_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CranePullProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.CranePushProps",
    jsii_struct_bases=[],
    name_mapping={
        "dst_registry": "dstRegistry",
        "docker_client_config": "dockerClientConfig",
        "image_name": "imageName",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "tar_path": "tarPath",
    },
)
class CranePushProps:
    def __init__(
        self,
        *,
        dst_registry: typing.Union[builtins.str, "Registry"],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Defaults to a ``DockerClientConfig`` with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image name, searched for in ``imagePath`` and gets ``.tar`` appended. Default: PredefinedVariables.ciProjectName
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.ciCommitTag
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to find the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f279a64e767394ea6f700643ba7fa4e3c39b4660a7236b0921fdbf6d52462b4)
            check_type(argname="argument dst_registry", value=dst_registry, expected_type=type_hints["dst_registry"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument tar_path", value=tar_path, expected_type=type_hints["tar_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dst_registry": dst_registry,
        }
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if tar_path is not None:
            self._values["tar_path"] = tar_path

    @builtins.property
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image to.'''
        result = self._values.get("dst_registry")
        assert result is not None, "Required property 'dst_registry' is missing"
        return typing.cast(typing.Union[builtins.str, "Registry"], result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.ciProjectName
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Path where to find the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        result = self._values.get("tar_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CranePushProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.DiveScanProps",
    jsii_struct_bases=[],
    name_mapping={
        "highest_user_wasted_percent": "highestUserWastedPercent",
        "highest_wasted_bytes": "highestWastedBytes",
        "ignore_errors": "ignoreErrors",
        "image_name": "imageName",
        "image_path": "imagePath",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "lowest_efficiency": "lowestEfficiency",
        "source": "source",
    },
)
class DiveScanProps:
    def __init__(
        self,
        *,
        highest_user_wasted_percent: typing.Optional[jsii.Number] = None,
        highest_wasted_bytes: typing.Optional[jsii.Number] = None,
        ignore_errors: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_path: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        lowest_efficiency: typing.Optional[jsii.Number] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param highest_user_wasted_percent: Highest allowable percentage of bytes wasted (as a ratio between 0-1), otherwise CI validation will fail. Default: 0.1
        :param highest_wasted_bytes: Highest allowable bytes wasted, otherwise CI validation will fail.
        :param ignore_errors: Ignore image parsing errors and run the analysis anyway. Default: false
        :param image_name: Name of the container image to scan, if ``source`` is ``docker-archive`` argument gets prefix ``.tar``. Default: PredefinedVariables.ciProjectName
        :param image_path: Path to the image can be either a remote container registry, as well as a local path to an image. Default: PredefinedVariables.ciProjectPath
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.ciCommitTag
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param lowest_efficiency: Lowest allowable image efficiency (as a ratio between 0-1), otherwise CI validation will fail. Default: 0.9
        :param source: The container engine to fetch the image from. Allowed values: docker, podman, docker-archive Default: "docker-archive
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af56cecc923ccf6759959ff9339129db7a8008203f8a2629f79606ebf173cd8e)
            check_type(argname="argument highest_user_wasted_percent", value=highest_user_wasted_percent, expected_type=type_hints["highest_user_wasted_percent"])
            check_type(argname="argument highest_wasted_bytes", value=highest_wasted_bytes, expected_type=type_hints["highest_wasted_bytes"])
            check_type(argname="argument ignore_errors", value=ignore_errors, expected_type=type_hints["ignore_errors"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_path", value=image_path, expected_type=type_hints["image_path"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument lowest_efficiency", value=lowest_efficiency, expected_type=type_hints["lowest_efficiency"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if highest_user_wasted_percent is not None:
            self._values["highest_user_wasted_percent"] = highest_user_wasted_percent
        if highest_wasted_bytes is not None:
            self._values["highest_wasted_bytes"] = highest_wasted_bytes
        if ignore_errors is not None:
            self._values["ignore_errors"] = ignore_errors
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_path is not None:
            self._values["image_path"] = image_path
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if lowest_efficiency is not None:
            self._values["lowest_efficiency"] = lowest_efficiency
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def highest_user_wasted_percent(self) -> typing.Optional[jsii.Number]:
        '''Highest allowable percentage of bytes wasted (as a ratio between 0-1), otherwise CI validation will fail.

        :default: 0.1
        '''
        result = self._values.get("highest_user_wasted_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def highest_wasted_bytes(self) -> typing.Optional[jsii.Number]:
        '''Highest allowable bytes wasted, otherwise CI validation will fail.'''
        result = self._values.get("highest_wasted_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_errors(self) -> typing.Optional[builtins.bool]:
        '''Ignore image parsing errors and run the analysis anyway.

        :default: false
        '''
        result = self._values.get("ignore_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Name of the container image to scan, if ``source`` is ``docker-archive`` argument gets prefix ``.tar``.

        :default: PredefinedVariables.ciProjectName
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_path(self) -> typing.Optional[builtins.str]:
        '''Path to the image can be either a remote container registry, as well as a local path to an image.

        :default: PredefinedVariables.ciProjectPath
        '''
        result = self._values.get("image_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lowest_efficiency(self) -> typing.Optional[jsii.Number]:
        '''Lowest allowable image efficiency (as a ratio between 0-1), otherwise CI validation will fail.

        :default: 0.9
        '''
        result = self._values.get("lowest_efficiency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The container engine to fetch the image from.

        Allowed values: docker, podman, docker-archive

        :default: "docker-archive
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiveScanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.DockerBuildProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository": "repository",
        "context": "context",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "tag": "tag",
    },
)
class DockerBuildProps:
    def __init__(
        self,
        *,
        repository: builtins.str,
        context: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The Docker repository name ``([<registry>/]<image>)``.
        :param context: The Docker build context (the directory containing the Dockerfile). Default: ``.``
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tag: A Docker image tag applied to the image. If not set docker uses ``latest``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6a99ea530ccaf32750baa4c78f8f420c32d204f1eb43121e53d4baa06a37a7)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if context is not None:
            self._values["context"] = context
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def repository(self) -> builtins.str:
        '''The Docker repository name ``([<registry>/]<image>)``.'''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''The Docker build context (the directory containing the Dockerfile).

        :default: ``.``
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''A Docker image tag applied to the image.

        If not set docker uses ``latest``
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerBuildProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.DockerClientConfigProps",
    jsii_struct_bases=[],
    name_mapping={"config_file_path": "configFilePath"},
)
class DockerClientConfigProps:
    def __init__(
        self,
        *,
        config_file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_file_path: Docker client config path. Default: $HOME/.docker/config.json
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206d2b583e918e93a1ff212d6af4cd76afeb3ac91bd0bf5e2193df801f76b70d)
            check_type(argname="argument config_file_path", value=config_file_path, expected_type=type_hints["config_file_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_file_path is not None:
            self._values["config_file_path"] = config_file_path

    @builtins.property
    def config_file_path(self) -> typing.Optional[builtins.str]:
        '''Docker client config path.

        :default: $HOME/.docker/config.json
        '''
        result = self._values.get("config_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerClientConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.container.DockerPushProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_image": "containerImage",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "login_env_var": "loginEnvVar",
        "registry": "registry",
        "tag": "tag",
        "user_env_var": "userEnvVar",
    },
)
class DockerPushProps:
    def __init__(
        self,
        *,
        container_image: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        login_env_var: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        user_env_var: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_image: The name of the Docker image to push to the ``registry``.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param login_env_var: If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the password or token, here. **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        :param registry: The Docker registry the image should be pushed to. Default: index.docker.io/v1
        :param tag: The Docker image tag that should be pushed to the ``registry``. Default: ``latest``
        :param user_env_var: If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the username value, here. **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607c48baa8d826d3aaedac3a174f21f61ae4e3e0b0a832478a9aab984f42de22)
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument login_env_var", value=login_env_var, expected_type=type_hints["login_env_var"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument user_env_var", value=user_env_var, expected_type=type_hints["user_env_var"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_image": container_image,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if login_env_var is not None:
            self._values["login_env_var"] = login_env_var
        if registry is not None:
            self._values["registry"] = registry
        if tag is not None:
            self._values["tag"] = tag
        if user_env_var is not None:
            self._values["user_env_var"] = user_env_var

    @builtins.property
    def container_image(self) -> builtins.str:
        '''The name of the Docker image to push to the ``registry``.'''
        result = self._values.get("container_image")
        assert result is not None, "Required property 'container_image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the password or token, here.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        '''
        result = self._values.get("login_env_var")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry(self) -> typing.Optional[builtins.str]:
        '''The Docker registry the image should be pushed to.

        :default: index.docker.io/v1
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The Docker image tag that should be pushed to the ``registry``.

        :default: ``latest``
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the username value, here.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        '''
        result = self._values.get("user_env_var")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerPushProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@gcix/gcix.container.IBuildContainerCollection")
class IBuildContainerCollection(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="cranePushJob")
    def crane_push_job(self) -> "CranePush":
        '''Crane push job.'''
        ...

    @crane_push_job.setter
    def crane_push_job(self, value: "CranePush") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="diveScanJob")
    def dive_scan_job(self) -> "DiveScan":
        '''Dive scan job.'''
        ...

    @dive_scan_job.setter
    def dive_scan_job(self, value: "DiveScan") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        ...

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="doCranePush")
    def do_crane_push(self) -> builtins.bool:
        '''Set to ``false`` to skip the Crane push job.

        :default: true
        '''
        ...

    @do_crane_push.setter
    def do_crane_push(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="doDiveScan")
    def do_dive_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Dive scan job.

        :default: true
        '''
        ...

    @do_dive_scan.setter
    def do_dive_scan(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="doTrivyignoreCheck")
    def do_trivyignore_check(self) -> builtins.bool:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.

        :default: true
        '''
        ...

    @do_trivyignore_check.setter
    def do_trivyignore_check(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="doTrivyScan")
    def do_trivy_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Trivy scan job.

        :default: true
        '''
        ...

    @do_trivy_scan.setter
    def do_trivy_scan(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name with stage in the registry.

        e.g. username/imageName.

        :default: PredefinedVariables.ciProjectDir
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Image tag.

        Depending of the build it defaults either to the git tag or
        to the actual branch name.

        :default: PredefinedVariables.ciCommitRefName
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="kanikoExecuteJob")
    def kaniko_execute_job(self) -> "KanikoExecute":
        '''Kaniko execute job.'''
        ...

    @kaniko_execute_job.setter
    def kaniko_execute_job(self, value: "KanikoExecute") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Container registry to push the image to.

        If the container registry
        needs authentication, you have to provide a ``DockerClientConfig`` object
        with credentials.

        :default: Registry.DOCKER
        '''
        ...

    @registry.setter
    def registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trivyIgnoreFileCheckJob")
    def trivy_ignore_file_check_job(self) -> "TrivyIgnoreFileCheck":
        '''Trivy ignore file check job.'''
        ...

    @trivy_ignore_file_check_job.setter
    def trivy_ignore_file_check_job(self, value: "TrivyIgnoreFileCheck") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trivyScanLocalImageJob")
    def trivy_scan_local_image_job(self) -> "TrivyScanLocalImage":
        '''Trivy scan local image job.'''
        ...

    @trivy_scan_local_image_job.setter
    def trivy_scan_local_image_job(self, value: "TrivyScanLocalImage") -> None:
        ...


class _IBuildContainerCollectionProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IBuildContainerCollection"

    @builtins.property
    @jsii.member(jsii_name="cranePushJob")
    def crane_push_job(self) -> "CranePush":
        '''Crane push job.'''
        return typing.cast("CranePush", jsii.get(self, "cranePushJob"))

    @crane_push_job.setter
    def crane_push_job(self, value: "CranePush") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0116523456ff706c1377a152fde5fe35683cdffa8ccac7b83af0ed04168db58e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cranePushJob", value)

    @builtins.property
    @jsii.member(jsii_name="diveScanJob")
    def dive_scan_job(self) -> "DiveScan":
        '''Dive scan job.'''
        return typing.cast("DiveScan", jsii.get(self, "diveScanJob"))

    @dive_scan_job.setter
    def dive_scan_job(self, value: "DiveScan") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0fb2d88304bf5cc561b1ab15b81b9add0917cd2f367d5d0ffd6ac3a708f6f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diveScanJob", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746261fcfe25d21c1421f3c65f118ded186f03ab7b94d8df37f5d9ac75554b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="doCranePush")
    def do_crane_push(self) -> builtins.bool:
        '''Set to ``false`` to skip the Crane push job.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "doCranePush"))

    @do_crane_push.setter
    def do_crane_push(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da94f33e04ac9bc8665968417f85fd7e09ed24f5571b9390407aae9d1c11a334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doCranePush", value)

    @builtins.property
    @jsii.member(jsii_name="doDiveScan")
    def do_dive_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Dive scan job.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "doDiveScan"))

    @do_dive_scan.setter
    def do_dive_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427629879567738d70e65ab56ac3776a98e6af570e9fa519271b1fc019064927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doDiveScan", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyignoreCheck")
    def do_trivyignore_check(self) -> builtins.bool:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyignoreCheck"))

    @do_trivyignore_check.setter
    def do_trivyignore_check(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9357a747b76ebaa830adf801712ece723718e77dc329ce0830354923de5e6844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyignoreCheck", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyScan")
    def do_trivy_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Trivy scan job.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyScan"))

    @do_trivy_scan.setter
    def do_trivy_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d3b984aeda16e11797c209a33b2c0d2e2aa060fcfe72baf2e5c74192e21c77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyScan", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name with stage in the registry.

        e.g. username/imageName.

        :default: PredefinedVariables.ciProjectDir
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36058c9f7ee07328c959e1627cd79ceac781ae81f7b3ae49b8e9bbb9c707ec35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Image tag.

        Depending of the build it defaults either to the git tag or
        to the actual branch name.

        :default: PredefinedVariables.ciCommitRefName
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7daa0536f8f39a3f3d41f62cbf3ed6443b03b9bcd7422f85836df6cc8cc06fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="kanikoExecuteJob")
    def kaniko_execute_job(self) -> "KanikoExecute":
        '''Kaniko execute job.'''
        return typing.cast("KanikoExecute", jsii.get(self, "kanikoExecuteJob"))

    @kaniko_execute_job.setter
    def kaniko_execute_job(self, value: "KanikoExecute") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948de3d6f36852424a280596b72941071f34bac514d195427d22d709e98ff45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kanikoExecuteJob", value)

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Container registry to push the image to.

        If the container registry
        needs authentication, you have to provide a ``DockerClientConfig`` object
        with credentials.

        :default: Registry.DOCKER
        '''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "registry"))

    @registry.setter
    def registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef285394371971c730d00b57a4fa74506459cf73a548d80099e21b461faf8ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registry", value)

    @builtins.property
    @jsii.member(jsii_name="trivyIgnoreFileCheckJob")
    def trivy_ignore_file_check_job(self) -> "TrivyIgnoreFileCheck":
        '''Trivy ignore file check job.'''
        return typing.cast("TrivyIgnoreFileCheck", jsii.get(self, "trivyIgnoreFileCheckJob"))

    @trivy_ignore_file_check_job.setter
    def trivy_ignore_file_check_job(self, value: "TrivyIgnoreFileCheck") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a604e69d9a3619b65703566a521f561cd7378490a5e61a74f94790ee7d27393d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyIgnoreFileCheckJob", value)

    @builtins.property
    @jsii.member(jsii_name="trivyScanLocalImageJob")
    def trivy_scan_local_image_job(self) -> "TrivyScanLocalImage":
        '''Trivy scan local image job.'''
        return typing.cast("TrivyScanLocalImage", jsii.get(self, "trivyScanLocalImageJob"))

    @trivy_scan_local_image_job.setter
    def trivy_scan_local_image_job(self, value: "TrivyScanLocalImage") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aea3c85b9f24b12424e7e389c2071b59bf07bfc76ca3c60ed970d2cf6a8d8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyScanLocalImageJob", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBuildContainerCollection).__jsii_proxy_class__ = lambda : _IBuildContainerCollectionProxy


@jsii.interface(jsii_type="@gcix/gcix.container.ICopyContainerCollection")
class ICopyContainerCollection(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="cranePullJob")
    def crane_pull_job(self) -> "CranePull":
        '''CranPull job.'''
        ...

    @crane_pull_job.setter
    def crane_pull_job(self, value: "CranePull") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="cranePushJob")
    def crane_push_job(self) -> "CranePush":
        ...

    @crane_push_job.setter
    def crane_push_job(self, value: "CranePush") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        ...

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="doDiveScan")
    def do_dive_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Dive scan job.

        :default: true
        '''
        ...

    @do_dive_scan.setter
    def do_dive_scan(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="doTrivyignoreCheck")
    def do_trivyignore_check(self) -> builtins.bool:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.

        :default: true
        '''
        ...

    @do_trivyignore_check.setter
    def do_trivyignore_check(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="doTrivyScan")
    def do_trivy_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Trivy scan job.

        :default: true
        '''
        ...

    @do_trivy_scan.setter
    def do_trivy_scan(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Container registry to push the image to.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.

        :default: Registry.DOCKER
        '''
        ...

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name with stage in the registry.

        e.g. username/image_name.
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Container image tag to pull from ``srcRegistry`` and push to ``dstRegistry``.'''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Container registry to pull the image from.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.

        :default: Registry.DOCKER
        '''
        ...

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="diveScanJob")
    def dive_scan_job(self) -> typing.Optional["DiveScan"]:
        '''Dive scan job.'''
        ...

    @dive_scan_job.setter
    def dive_scan_job(self, value: typing.Optional["DiveScan"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trivyIgnoreFileCheckJob")
    def trivy_ignore_file_check_job(self) -> typing.Optional["TrivyIgnoreFileCheck"]:
        '''Trivy ignore file check job.'''
        ...

    @trivy_ignore_file_check_job.setter
    def trivy_ignore_file_check_job(
        self,
        value: typing.Optional["TrivyIgnoreFileCheck"],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trivyScanLocalImageJob")
    def trivy_scan_local_image_job(self) -> typing.Optional["TrivyScanLocalImage"]:
        '''Trivy scan local image job.'''
        ...

    @trivy_scan_local_image_job.setter
    def trivy_scan_local_image_job(
        self,
        value: typing.Optional["TrivyScanLocalImage"],
    ) -> None:
        ...


class _ICopyContainerCollectionProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.ICopyContainerCollection"

    @builtins.property
    @jsii.member(jsii_name="cranePullJob")
    def crane_pull_job(self) -> "CranePull":
        '''CranPull job.'''
        return typing.cast("CranePull", jsii.get(self, "cranePullJob"))

    @crane_pull_job.setter
    def crane_pull_job(self, value: "CranePull") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f70d3fad8673833b2c8fed070cb2921a7493bf0d4bb0adb56df39cfeb43784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cranePullJob", value)

    @builtins.property
    @jsii.member(jsii_name="cranePushJob")
    def crane_push_job(self) -> "CranePush":
        return typing.cast("CranePush", jsii.get(self, "cranePushJob"))

    @crane_push_job.setter
    def crane_push_job(self, value: "CranePush") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4283bacb47bb921dcfdb531bab8ce5cc5b89580936030ebd193145094339345c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cranePushJob", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee8d038b73c3aaa63ba95c493db064287e1663d01cf8681d501f46dd20cce1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="doDiveScan")
    def do_dive_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Dive scan job.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "doDiveScan"))

    @do_dive_scan.setter
    def do_dive_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b392df5662373fd9c18ce8bfb3821a721ad141e60545a66cb7a7ab7ff1ff7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doDiveScan", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyignoreCheck")
    def do_trivyignore_check(self) -> builtins.bool:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyignoreCheck"))

    @do_trivyignore_check.setter
    def do_trivyignore_check(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2687c0184c9a9b888ce969ed872eb2bb6185df142b016b04a2778b755d2fa951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyignoreCheck", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyScan")
    def do_trivy_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Trivy scan job.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyScan"))

    @do_trivy_scan.setter
    def do_trivy_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad564cc88fd5c116ad6269a596679f594a0fddc450165c9effe162a97620b82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyScan", value)

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Container registry to push the image to.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.

        :default: Registry.DOCKER
        '''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292f9682734eb6bc8f1fe0e28bfd2473c4dbf27b42a3297be6a91b5e59e56e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name with stage in the registry.

        e.g. username/image_name.
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2177b7c9a8f60ea34287f1db828576bc2c110f869fb1ca123cab951c945373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Container image tag to pull from ``srcRegistry`` and push to ``dstRegistry``.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e4b69135ef78283b8302414edf06c7ea0228c0453a9cb92a22c36d27b36fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Container registry to pull the image from.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.

        :default: Registry.DOCKER
        '''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ee07f847778f249471fed60cb36083c0ace9ba27419870e2c74b2d0a149844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="diveScanJob")
    def dive_scan_job(self) -> typing.Optional["DiveScan"]:
        '''Dive scan job.'''
        return typing.cast(typing.Optional["DiveScan"], jsii.get(self, "diveScanJob"))

    @dive_scan_job.setter
    def dive_scan_job(self, value: typing.Optional["DiveScan"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4c012c9759ba283e975a61aeb8b2fe10705104aaa8441498be8ddbe28fa00d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diveScanJob", value)

    @builtins.property
    @jsii.member(jsii_name="trivyIgnoreFileCheckJob")
    def trivy_ignore_file_check_job(self) -> typing.Optional["TrivyIgnoreFileCheck"]:
        '''Trivy ignore file check job.'''
        return typing.cast(typing.Optional["TrivyIgnoreFileCheck"], jsii.get(self, "trivyIgnoreFileCheckJob"))

    @trivy_ignore_file_check_job.setter
    def trivy_ignore_file_check_job(
        self,
        value: typing.Optional["TrivyIgnoreFileCheck"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3934c339c5eb70b4b32dc76ce257b78827bcc3d98cbd495bb27b778a33bf482e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyIgnoreFileCheckJob", value)

    @builtins.property
    @jsii.member(jsii_name="trivyScanLocalImageJob")
    def trivy_scan_local_image_job(self) -> typing.Optional["TrivyScanLocalImage"]:
        '''Trivy scan local image job.'''
        return typing.cast(typing.Optional["TrivyScanLocalImage"], jsii.get(self, "trivyScanLocalImageJob"))

    @trivy_scan_local_image_job.setter
    def trivy_scan_local_image_job(
        self,
        value: typing.Optional["TrivyScanLocalImage"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec493b51d2332c76141026bb84f26885492bf54dd685fee6f5897261cfa0f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyScanLocalImageJob", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICopyContainerCollection).__jsii_proxy_class__ = lambda : _ICopyContainerCollectionProxy


@jsii.interface(jsii_type="@gcix/gcix.container.ICraneCopy")
class ICraneCopy(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image to.'''
        ...

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image from.'''
        ...

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        ...

    @docker_client_config.setter
    def docker_client_config(
        self,
        value: typing.Optional["DockerClientConfig"],
    ) -> None:
        ...


class _ICraneCopyProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.ICraneCopy"

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image to.'''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca99b3afd8175b7d4f020c4c9e008e634a6bf8ee72b9349f778e54a8100523a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image from.'''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dd0fd5c0a2473ae269ae3cbacd9ed5a8efef8426c98b32c6336a169029edf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        return typing.cast(typing.Optional["DockerClientConfig"], jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(
        self,
        value: typing.Optional["DockerClientConfig"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572a8f78cc2839ffe9780649d73c01c2c2eeaedbebde024e455caea88ec08560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICraneCopy).__jsii_proxy_class__ = lambda : _ICraneCopyProxy


@jsii.interface(jsii_type="@gcix/gcix.container.ICranePull")
class ICranePull(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        ...

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image with namespace to pull from ``srcRegistry``.

        :default: PredefinedVariables.ciProjectName
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Tag of the image which will be pulled.

        :default: latest
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to pull container image from.'''
        ...

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to save the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        ...

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        ...


class _ICranePullProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.ICranePull"

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        :default:

        DockerClientConfig with login to the official Docker Hub
        and expecting credentials given as environment variables
        ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b26b506fdcc8eaa9939599dd8489a2249519cb16cc776239041a52106891cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image with namespace to pull from ``srcRegistry``.

        :default: PredefinedVariables.ciProjectName
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bed8506136c090c0a09432835eef1925ccb69f3d751dffb59027f5366e32d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Tag of the image which will be pulled.

        :default: latest
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce4f64fff958d19283260f72458ea249140b49ba9e1e05a0e7cfe370cb34970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to pull container image from.'''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5baeec5ec1b0e913e04e73cc573a5be67b6200667837d053dc99c81f8136f8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to save the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dae25943a7ff0eebcd64fbee4b63d00d9ab3a05fc8dfd0368df7dc5c1c61f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICranePull).__jsii_proxy_class__ = lambda : _ICranePullProxy


@jsii.interface(jsii_type="@gcix/gcix.container.ICranePush")
class ICranePush(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        ...

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image to.'''
        ...

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.ciProjectName
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to find the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        ...

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        ...


class _ICranePushProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.ICranePush"

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ec746d6937d9d03d7509b01e47b2584cf0ada28b0820ce9d91dff6652f83e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, "Registry"]:
        '''Registry URL to copy container image to.'''
        return typing.cast(typing.Union[builtins.str, "Registry"], jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, "Registry"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427ddd0e70a8eae02188adb4ddaefd1934bf84dacc91f364a9ac0ff3b603db37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.ciProjectName
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d134ee48b532e485915f3ee98f970d1363ce9cb16e110f85033b752fe51e001e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853d7fe77aaa83cac92bdda53480c907e1f13eb8e7fb19f4219d21e175d5faa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to find the container image tarball.

        :default: PredefinedVariables.ciProjectDir
        '''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2e53be5f9d444680eea46c38ae9a84c2ea75ecc5f0917f19a459210b7d2f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICranePush).__jsii_proxy_class__ = lambda : _ICranePushProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IDiveScan")
class IDiveScan(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="highestUserWastedPercent")
    def highest_user_wasted_percent(self) -> jsii.Number:
        '''Highest allowable percentage of bytes wasted (as a ratio between 0-1), otherwise CI validation will fail.

        :default: 0.1
        '''
        ...

    @highest_user_wasted_percent.setter
    def highest_user_wasted_percent(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignoreErrors")
    def ignore_errors(self) -> builtins.bool:
        '''Ignore image parsing errors and run the analysis anyway.

        :default: false
        '''
        ...

    @ignore_errors.setter
    def ignore_errors(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Name of the container image to scan, if ``source`` is ``docker-archive`` argument gets prefix ``.tar``.

        :default: PredefinedVariables.ciProjectName
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imagePath")
    def image_path(self) -> builtins.str:
        '''Path to the image can be either a remote container registry, as well as a local path to an image.

        :default: PredefinedVariables.ciProjectPath
        '''
        ...

    @image_path.setter
    def image_path(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lowestEfficiency")
    def lowest_efficiency(self) -> jsii.Number:
        '''Lowest allowable image efficiency (as a ratio between 0-1), otherwise CI validation will fail.

        :default: 0.9
        '''
        ...

    @lowest_efficiency.setter
    def lowest_efficiency(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''The container engine to fetch the image from.

        Allowed values: docker, podman, docker-archive

        :default: docker-archive
        '''
        ...

    @source.setter
    def source(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="highestWastedBytes")
    def highest_wasted_bytes(self) -> typing.Optional[jsii.Number]:
        '''Highest allowable bytes wasted, otherwise CI validation will fail.'''
        ...

    @highest_wasted_bytes.setter
    def highest_wasted_bytes(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IDiveScanProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IDiveScan"

    @builtins.property
    @jsii.member(jsii_name="highestUserWastedPercent")
    def highest_user_wasted_percent(self) -> jsii.Number:
        '''Highest allowable percentage of bytes wasted (as a ratio between 0-1), otherwise CI validation will fail.

        :default: 0.1
        '''
        return typing.cast(jsii.Number, jsii.get(self, "highestUserWastedPercent"))

    @highest_user_wasted_percent.setter
    def highest_user_wasted_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe71cb94e2e06adab49f829f2ebfdbea30b54bf73742ece0aded57e3b47f4121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highestUserWastedPercent", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreErrors")
    def ignore_errors(self) -> builtins.bool:
        '''Ignore image parsing errors and run the analysis anyway.

        :default: false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "ignoreErrors"))

    @ignore_errors.setter
    def ignore_errors(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81db5595c647596525c7ee87df16f1a9f3e201fe62d545ab09354b1658ca7794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreErrors", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Name of the container image to scan, if ``source`` is ``docker-archive`` argument gets prefix ``.tar``.

        :default: PredefinedVariables.ciProjectName
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad28a33ef8749b49df20b2504a2caf1791478806d44864e45f63b7613c0ae87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imagePath")
    def image_path(self) -> builtins.str:
        '''Path to the image can be either a remote container registry, as well as a local path to an image.

        :default: PredefinedVariables.ciProjectPath
        '''
        return typing.cast(builtins.str, jsii.get(self, "imagePath"))

    @image_path.setter
    def image_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde47e48e379e35ebb11187e5bddde8752550725efd4e56c78a39234e3fa8340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePath", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.ciCommitTag
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd27df3a863d7d63829bfe23a67ede3f1b30fe48682433e92cf585833ee9bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="lowestEfficiency")
    def lowest_efficiency(self) -> jsii.Number:
        '''Lowest allowable image efficiency (as a ratio between 0-1), otherwise CI validation will fail.

        :default: 0.9
        '''
        return typing.cast(jsii.Number, jsii.get(self, "lowestEfficiency"))

    @lowest_efficiency.setter
    def lowest_efficiency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be88fcd6aff5e5b4d57e11d1636301dd72fe2a84d3f18f1b405a131cc2321849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lowestEfficiency", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''The container engine to fetch the image from.

        Allowed values: docker, podman, docker-archive

        :default: docker-archive
        '''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e1c3f3ab655b91291ea50630f1e7f412162f94756023c5596cdbc349155585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="highestWastedBytes")
    def highest_wasted_bytes(self) -> typing.Optional[jsii.Number]:
        '''Highest allowable bytes wasted, otherwise CI validation will fail.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "highestWastedBytes"))

    @highest_wasted_bytes.setter
    def highest_wasted_bytes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd759d2dcce813e15442e74e2118677cf9eec201f2b3c60db19d44e56e4092cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highestWastedBytes", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDiveScan).__jsii_proxy_class__ = lambda : _IDiveScanProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IDockerBuild")
class IDockerBuild(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        '''The Docker build context (the directory containing the Dockerfile).

        :default: ``.``
        '''
        ...

    @context.setter
    def context(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        '''The Docker repository name ``([<registry>/]<image>)``.'''
        ...

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        '''A Docker image tag applied to the image.

        :default: "latest"
        '''
        ...

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        ...


class _IDockerBuildProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IDockerBuild"

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        '''The Docker build context (the directory containing the Dockerfile).

        :default: ``.``
        '''
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d88bc47be0b26a05c11e5a808fbc99281da1b2fc3013c8b9796a6f097526f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        '''The Docker repository name ``([<registry>/]<image>)``.'''
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203470e55e08328fb006328448b04c1b19c7764bcda6c071c1251dc39def4997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        '''A Docker image tag applied to the image.

        :default: "latest"
        '''
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcf03ccb02d5412b838d7587b6db059f9f57c60f993cad32fb6745bf72cafe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerBuild).__jsii_proxy_class__ = lambda : _IDockerBuildProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IDockerClientConfig")
class IDockerClientConfig(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "IDockerClientConfigType":
        '''Docker client configuration.'''
        ...

    @config.setter
    def config(self, value: "IDockerClientConfigType") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        '''Docker client config path.

        :default: $HOME/.docker/config.json
        '''
        ...

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        ...


class _IDockerClientConfigProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IDockerClientConfig"

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "IDockerClientConfigType":
        '''Docker client configuration.'''
        return typing.cast("IDockerClientConfigType", jsii.get(self, "config"))

    @config.setter
    def config(self, value: "IDockerClientConfigType") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e083816c6ae221d335e5ff8ce0e91aa7f1e31492a64baf65024fe45cd17037fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        '''Docker client config path.

        :default: $HOME/.docker/config.json
        '''
        return typing.cast(builtins.str, jsii.get(self, "configFilePath"))

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7a975cf87bb5d079e0e97120574ec688b6767aedfbaacb31d43ca74d1e4788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configFilePath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerClientConfig).__jsii_proxy_class__ = lambda : _IDockerClientConfigProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IDockerClientConfigType")
class IDockerClientConfigType(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="auths")
    def auths(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        ...

    @auths.setter
    def auths(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="credHelpers")
    def cred_helpers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @cred_helpers.setter
    def cred_helpers(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="credsStore")
    def creds_store(self) -> typing.Optional[builtins.str]:
        ...

    @creds_store.setter
    def creds_store(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rawInput")
    def raw_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @raw_input.setter
    def raw_input(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...


class _IDockerClientConfigTypeProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IDockerClientConfigType"

    @builtins.property
    @jsii.member(jsii_name="auths")
    def auths(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "auths"))

    @auths.setter
    def auths(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c06e68bf27701f47e2c6385823c047b7c48641502ed2b70c2e6cb00bf4ff745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auths", value)

    @builtins.property
    @jsii.member(jsii_name="credHelpers")
    def cred_helpers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "credHelpers"))

    @cred_helpers.setter
    def cred_helpers(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbecbff16e0ecee4e2f306a4eaf894e4c91614f6ff695a7a129b9ea08b16ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credHelpers", value)

    @builtins.property
    @jsii.member(jsii_name="credsStore")
    def creds_store(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credsStore"))

    @creds_store.setter
    def creds_store(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82864bc1bc4d58efa2a54428508f6ebc1c52cfd22adf629cbd02e1c714987e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credsStore", value)

    @builtins.property
    @jsii.member(jsii_name="rawInput")
    def raw_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "rawInput"))

    @raw_input.setter
    def raw_input(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f757d69a2d460924dab774a4f874fe7a6bcc483a62e890ea65eaa6e060088dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawInput", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerClientConfigType).__jsii_proxy_class__ = lambda : _IDockerClientConfigTypeProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IDockerPush")
class IDockerPush(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        '''The name of the Docker image to push to the ``registry``.'''
        ...

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> builtins.str:
        '''The Docker registry the image should be pushed to.

        :default: index.docker.io/v1
        '''
        ...

    @registry.setter
    def registry(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        '''The Docker image tag that should be pushed to the ``registry``.

        :default: ``latest``
        '''
        ...

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="loginEnvVar")
    def login_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the password or token, here.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        '''
        ...

    @login_env_var.setter
    def login_env_var(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="userEnvVar")
    def user_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the username value, here.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        '''
        ...

    @user_env_var.setter
    def user_env_var(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IDockerPushProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IDockerPush"

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        '''The name of the Docker image to push to the ``registry``.'''
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634532a050c76b1a285c937d782cef38a6eedbd04d15c9d69780dff08a87973e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value)

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> builtins.str:
        '''The Docker registry the image should be pushed to.

        :default: index.docker.io/v1
        '''
        return typing.cast(builtins.str, jsii.get(self, "registry"))

    @registry.setter
    def registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fae0979d9292c572e6ef2b3250f490948b0b92cc67fa9f0a91accafa7b7f155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registry", value)

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        '''The Docker image tag that should be pushed to the ``registry``.

        :default: ``latest``
        '''
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460f6268d66f75afd35020e7abb6634e22eaeb10c18535885522c7fde478d5e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value)

    @builtins.property
    @jsii.member(jsii_name="loginEnvVar")
    def login_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the password or token, here.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginEnvVar"))

    @login_env_var.setter
    def login_env_var(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbe3f1fa312eaf653de6f0d6b7ee92868a4b1de025a151375ec50875a47de25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="userEnvVar")
    def user_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the username value, here.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userEnvVar"))

    @user_env_var.setter
    def user_env_var(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9cc3a57a43fe3c80a7424fa92d0662b8af3d87c372e6993fdd57cba98e24a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEnvVar", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerPush).__jsii_proxy_class__ = lambda : _IDockerPushProxy


@jsii.interface(jsii_type="@gcix/gcix.container.IKanikoExecute")
class IKanikoExecute(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        '''Context which will be send to kaniko.

        :default: PredefinedVariables.CI_PROJECT_DIR
        '''
        ...

    @context.setter
    def context(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        ...

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dockerfile")
    def dockerfile(self) -> builtins.str:
        '''Name of the dockerfile to use.

        File is relative to context.

        :default: "Dockerfile"
        '''
        ...

    @dockerfile.setter
    def dockerfile(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enablePush")
    def enable_push(self) -> builtins.bool:
        '''Enable push to container registry, disabled to allow subsequent jobs to act on container tarball.

        :default: false
        '''
        ...

    @enable_push.setter
    def enable_push(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name which will be created.

        :default: PredefinedVariables.CI_PROJECT_NAME.
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.CI_COMMIT_TAG
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="verbosity")
    def verbosity(self) -> builtins.str:
        '''Verbosity of kaniko logging.

        :default: "info"
        '''
        ...

    @verbosity.setter
    def verbosity(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="buildArgs")
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Container build arguments, used to instrument the container image build.'''
        ...

    @build_args.setter
    def build_args(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="buildTarget")
    def build_target(self) -> typing.Optional[builtins.str]:
        '''For container multistage builds name of the build stage you want to create.

        Image tag will be appended with the build_target. e.g. latest-buildtarget.
        '''
        ...

    @build_target.setter
    def build_target(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="registries")
    def registries(
        self,
    ) -> typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]]:
        '''List of container registries to push created image to.'''
        ...

    @registries.setter
    def registries(
        self,
        value: typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Container images created by kaniko are tarball files.

        This is the path where to store the image, will be named with suffix ``.tar``.
        This path will be created if not present.
        '''
        ...

    @tar_path.setter
    def tar_path(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IKanikoExecuteProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.IKanikoExecute"

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        '''Context which will be send to kaniko.

        :default: PredefinedVariables.CI_PROJECT_DIR
        '''
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960f544c37478e03e6c13e2105577d33d5c657009865df4102475d57639ac5cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f4dbd81fe06b79b591fe9cf35b8d320de110a35d4abf8ee7a04085c6a8ab93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="dockerfile")
    def dockerfile(self) -> builtins.str:
        '''Name of the dockerfile to use.

        File is relative to context.

        :default: "Dockerfile"
        '''
        return typing.cast(builtins.str, jsii.get(self, "dockerfile"))

    @dockerfile.setter
    def dockerfile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0204504365c6c1fdf207e611880f54b89fbfcd7cee0d7ed59d09fefe9c763259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerfile", value)

    @builtins.property
    @jsii.member(jsii_name="enablePush")
    def enable_push(self) -> builtins.bool:
        '''Enable push to container registry, disabled to allow subsequent jobs to act on container tarball.

        :default: false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enablePush"))

    @enable_push.setter
    def enable_push(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e49220b641e8d014fcb4f82e4acdfa83e37bf1025c611b88b6ec478e4b4694b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePush", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name which will be created.

        :default: PredefinedVariables.CI_PROJECT_NAME.
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835bc659f95de56020a6aabda657d6184bfb6e4ef0d54ba1dcaf03aeec0c4d49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.CI_COMMIT_TAG
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9537120dfd5a81dd138c75109bedfc46b2c4d0625afe620e09a3d25f899168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="verbosity")
    def verbosity(self) -> builtins.str:
        '''Verbosity of kaniko logging.

        :default: "info"
        '''
        return typing.cast(builtins.str, jsii.get(self, "verbosity"))

    @verbosity.setter
    def verbosity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff39590d779bee9ef114aac8a3286ad1701b76c3ae4bf15fe7d65f9f887ed19b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verbosity", value)

    @builtins.property
    @jsii.member(jsii_name="buildArgs")
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Container build arguments, used to instrument the container image build.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "buildArgs"))

    @build_args.setter
    def build_args(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10c717f02fa8d39199986400366b6397188bf90d0c4478b4c67ce222512a7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildArgs", value)

    @builtins.property
    @jsii.member(jsii_name="buildTarget")
    def build_target(self) -> typing.Optional[builtins.str]:
        '''For container multistage builds name of the build stage you want to create.

        Image tag will be appended with the build_target. e.g. latest-buildtarget.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildTarget"))

    @build_target.setter
    def build_target(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7775e186dbb617d4940a35b327f0e7d0139ef0cfe8786740c5aa6b17e3bb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildTarget", value)

    @builtins.property
    @jsii.member(jsii_name="registries")
    def registries(
        self,
    ) -> typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]]:
        '''List of container registries to push created image to.'''
        return typing.cast(typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]], jsii.get(self, "registries"))

    @registries.setter
    def registries(
        self,
        value: typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a997093041cfd9d7d6400b88e572ecb673325c07ac8d667e0651e3db78818118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registries", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Container images created by kaniko are tarball files.

        This is the path where to store the image, will be named with suffix ``.tar``.
        This path will be created if not present.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad9231cd7938be92768dfb0b13a59083fa4bd15f2326d1f5837eed5df5736ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IKanikoExecute).__jsii_proxy_class__ = lambda : _IKanikoExecuteProxy


@jsii.interface(jsii_type="@gcix/gcix.container.ITrivyIgnoreFileCheck")
class ITrivyIgnoreFileCheck(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="trivyignorePath")
    def trivyignore_path(self) -> builtins.str:
        '''Path to the ``.trivyignore`` file.

        :default: PredefinedVariables.ciProjectDir/.trivyignore
        '''
        ...

    @trivyignore_path.setter
    def trivyignore_path(self, value: builtins.str) -> None:
        ...


class _ITrivyIgnoreFileCheckProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.ITrivyIgnoreFileCheck"

    @builtins.property
    @jsii.member(jsii_name="trivyignorePath")
    def trivyignore_path(self) -> builtins.str:
        '''Path to the ``.trivyignore`` file.

        :default: PredefinedVariables.ciProjectDir/.trivyignore
        '''
        return typing.cast(builtins.str, jsii.get(self, "trivyignorePath"))

    @trivyignore_path.setter
    def trivyignore_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9b14b6da43ef0a63a4e33d17019ecb0cb5094821bc439b5b645f611fc7dd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyignorePath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITrivyIgnoreFileCheck).__jsii_proxy_class__ = lambda : _ITrivyIgnoreFileCheckProxy


@jsii.interface(jsii_type="@gcix/gcix.container.ITrivyScanLocalImage")
class ITrivyScanLocalImage(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="debug")
    def debug(self) -> builtins.bool:
        '''If trivy should run in debug mode.

        :default: false
        '''
        ...

    @debug.setter
    def debug(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="exitIfVulnerable")
    def exit_if_vulnerable(self) -> builtins.bool:
        '''Exit code when vulnerabilities were found.

        If true exit code is 1 else 0.

        :default: true
        '''
        ...

    @exit_if_vulnerable.setter
    def exit_if_vulnerable(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.CI_PROJECT_NAME
        '''
        ...

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imagePath")
    def image_path(self) -> builtins.str:
        '''Path where to find the container image.

        :default: PredefinedVariables.CI_PROJECT_DIR
        '''
        ...

    @image_path.setter
    def image_path(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.CI_COMMIT_TAG
        '''
        ...

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        '''Scan output format, possible values (table, json).

        :default: "table"
        '''
        ...

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        '''Severities of vulnerabilities to be displayed (comma separated).

        :default: "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL"
        '''
        ...

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityTypes")
    def vulnerability_types(self) -> builtins.str:
        '''List of vulnerability types (comma separated).

        :default: "os,library"
        '''
        ...

    @vulnerability_types.setter
    def vulnerability_types(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trivyConfig")
    def trivy_config(self) -> typing.Optional[builtins.str]:
        '''Additional options to pass to ``trivy`` binary.'''
        ...

    @trivy_config.setter
    def trivy_config(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ITrivyScanLocalImageProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.container.ITrivyScanLocalImage"

    @builtins.property
    @jsii.member(jsii_name="debug")
    def debug(self) -> builtins.bool:
        '''If trivy should run in debug mode.

        :default: false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "debug"))

    @debug.setter
    def debug(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3c03cbdfd88f243b2a021cfea7bae2aec22d673a96bee2b3ee4a572e8233d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "debug", value)

    @builtins.property
    @jsii.member(jsii_name="exitIfVulnerable")
    def exit_if_vulnerable(self) -> builtins.bool:
        '''Exit code when vulnerabilities were found.

        If true exit code is 1 else 0.

        :default: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "exitIfVulnerable"))

    @exit_if_vulnerable.setter
    def exit_if_vulnerable(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c264b4fd7f342e70577e3bd1ab7176dfd66fa96178f8fd734cad331b949418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exitIfVulnerable", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.CI_PROJECT_NAME
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a720a7b8311dda5bbd35347a36418e7f3d677c9efffc9a7f6fde5665861f93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imagePath")
    def image_path(self) -> builtins.str:
        '''Path where to find the container image.

        :default: PredefinedVariables.CI_PROJECT_DIR
        '''
        return typing.cast(builtins.str, jsii.get(self, "imagePath"))

    @image_path.setter
    def image_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49dca41c09e4104d51824907b4d0a0f8b37b33fd721e724ecbf5794d0fcb6509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePath", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.CI_COMMIT_TAG
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a287bb09ff02b901fe6f9e3f5c2ca8283fa5bfbb1708d08e967397deb02cfd60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        '''Scan output format, possible values (table, json).

        :default: "table"
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdfa2df4221b9e73051d6df9dc7faa117504c6f0bedcb3e38b01bac7420a64d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value)

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        '''Severities of vulnerabilities to be displayed (comma separated).

        :default: "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL"
        '''
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be88e0b5945f5ff3ccc1f91e16defded980aedafa87ccfe7e6b19858787586d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value)

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityTypes")
    def vulnerability_types(self) -> builtins.str:
        '''List of vulnerability types (comma separated).

        :default: "os,library"
        '''
        return typing.cast(builtins.str, jsii.get(self, "vulnerabilityTypes"))

    @vulnerability_types.setter
    def vulnerability_types(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75525ed276b934a24dfcee6d0abba57de42d5e160c092c4cfff7df3ef90f4f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerabilityTypes", value)

    @builtins.property
    @jsii.member(jsii_name="trivyConfig")
    def trivy_config(self) -> typing.Optional[builtins.str]:
        '''Additional options to pass to ``trivy`` binary.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trivyConfig"))

    @trivy_config.setter
    def trivy_config(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7990b578c250d41dce4ab20a226a12f9d45cecf909467c75ee46c4b89122b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyConfig", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITrivyScanLocalImage).__jsii_proxy_class__ = lambda : _ITrivyScanLocalImageProxy


@jsii.implements(IKanikoExecute)
class KanikoExecute(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.KanikoExecute",
):
    '''Creates a job which builds container images.

    This job creates images depending on git branches.
    e.g If the branch which gets pushed to the remote is named
    ``my_awsome_feature`` the image will be tagged with ``my-awsome-feature``.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: kaniko
    - stage: build
    - image: PredefinedImages.KANIKO
    '''

    def __init__(
        self,
        *,
        build_args: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        build_target: typing.Optional[builtins.str] = None,
        context: typing.Optional[builtins.str] = None,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        enable_push: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        registries: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Sequence["Registry"]]] = None,
        tar_path: typing.Optional[builtins.str] = None,
        verbosity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_args: Container build arguments, used to instrument the container image build.
        :param build_target: For container multistage builds name of the build stage you want to create. Image tag will be appended with the build_target. e.g. latest-buildtarget.
        :param context: Context which will be send to kaniko. Defaults to ``None`` which implies the local directory is the context.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Defaults to a ``DockerClientConfig`` with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param dockerfile: Name of the dockerfile to use. File is relative to context. Default: "Dockerfile"
        :param enable_push: Enable push to container registry, disabled to allow subsequent jobs to. Default: false act on container tarball.
        :param image_name: Image name which will be created. Default: PredefinedVariables.CI_PROJECT_NAME.
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.CI_COMMIT_TAG
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param registries: List of container registries to push created image to.
        :param tar_path: Container images created by kaniko are tarball files. This is the path where to store the image, will be named with suffix ``.tar``. This path will be created if not present.
        :param verbosity: Verbosity of kaniko logging. Default: "info"
        '''
        props = KanikoExecuteProps(
            build_args=build_args,
            build_target=build_target,
            context=context,
            docker_client_config=docker_client_config,
            dockerfile=dockerfile,
            enable_push=enable_push,
            image_name=image_name,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            registries=registries,
            tar_path=tar_path,
            verbosity=verbosity,
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
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        '''Context which will be send to kaniko.'''
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65dfbf74ad05f2261adfd845689fcaab7fde4974223a697ad48653f6406ebf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9764c5c99a60e2b94882581dbb58e909133d3e658a672d57dc5b4a693a82c685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="dockerfile")
    def dockerfile(self) -> builtins.str:
        '''Name of the dockerfile to use.

        File is relative to context.
        '''
        return typing.cast(builtins.str, jsii.get(self, "dockerfile"))

    @dockerfile.setter
    def dockerfile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d642c8384f282964aa63d3e05faa23df50ae48c028f601b497a63336e211bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerfile", value)

    @builtins.property
    @jsii.member(jsii_name="enablePush")
    def enable_push(self) -> builtins.bool:
        '''Enable push to container registry, disabled to allow subsequent jobs to act on container tarball.'''
        return typing.cast(builtins.bool, jsii.get(self, "enablePush"))

    @enable_push.setter
    def enable_push(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13f68f262149a1e20f5b9466e051e439f36ed22b8a7c10ef7a6c45c8ebfd9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePush", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name which will be created.'''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e423cc24374e30697505b9794984faa425c7e2e4e61270ada43c5b35d633c603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0efb9c3ae7881742c6b8e4f525d9c290b6ac74ba69322645f9859a8256b795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="verbosity")
    def verbosity(self) -> builtins.str:
        '''Verbosity of kaniko logging.'''
        return typing.cast(builtins.str, jsii.get(self, "verbosity"))

    @verbosity.setter
    def verbosity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d951aba997bdde6677b256cac5c2605ea0f56ecd520a54110a59cdc1415096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verbosity", value)

    @builtins.property
    @jsii.member(jsii_name="buildArgs")
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Container build arguments, used to instrument the container image build.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "buildArgs"))

    @build_args.setter
    def build_args(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7f6efc6a9b488baa9919952461cefe3522ec89661a2a59e001eecf759b9e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildArgs", value)

    @builtins.property
    @jsii.member(jsii_name="buildTarget")
    def build_target(self) -> typing.Optional[builtins.str]:
        '''For container multistage builds name of the build stage you want to create.

        Image tag will be appended with the build_target. e.g. latest-buildtarget.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildTarget"))

    @build_target.setter
    def build_target(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a1f91eaa5e923d8c937825ba8538a1b298236f81e36c6c7b1f694b62a0ab78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildTarget", value)

    @builtins.property
    @jsii.member(jsii_name="registries")
    def registries(
        self,
    ) -> typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]]:
        '''List of container registries to push created image to.'''
        return typing.cast(typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]], jsii.get(self, "registries"))

    @registries.setter
    def registries(
        self,
        value: typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63a3207114011d319800e8a8450d28abfcb485b8ca87f88369b295e36012f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registries", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Container images created by kaniko are tarball files.

        This is the path where to store the image, will be named with suffix ``.tar``.
        This path will be created if not present.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a7d1cb7b08aca5e734ae386a2ad2d5dc9483e9d629e50913f2ee5798314e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.container.KanikoExecuteProps",
    jsii_struct_bases=[],
    name_mapping={
        "build_args": "buildArgs",
        "build_target": "buildTarget",
        "context": "context",
        "docker_client_config": "dockerClientConfig",
        "dockerfile": "dockerfile",
        "enable_push": "enablePush",
        "image_name": "imageName",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "registries": "registries",
        "tar_path": "tarPath",
        "verbosity": "verbosity",
    },
)
class KanikoExecuteProps:
    def __init__(
        self,
        *,
        build_args: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        build_target: typing.Optional[builtins.str] = None,
        context: typing.Optional[builtins.str] = None,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        enable_push: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        registries: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Sequence["Registry"]]] = None,
        tar_path: typing.Optional[builtins.str] = None,
        verbosity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_args: Container build arguments, used to instrument the container image build.
        :param build_target: For container multistage builds name of the build stage you want to create. Image tag will be appended with the build_target. e.g. latest-buildtarget.
        :param context: Context which will be send to kaniko. Defaults to ``None`` which implies the local directory is the context.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Defaults to a ``DockerClientConfig`` with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param dockerfile: Name of the dockerfile to use. File is relative to context. Default: "Dockerfile"
        :param enable_push: Enable push to container registry, disabled to allow subsequent jobs to. Default: false act on container tarball.
        :param image_name: Image name which will be created. Default: PredefinedVariables.CI_PROJECT_NAME.
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.CI_COMMIT_TAG
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param registries: List of container registries to push created image to.
        :param tar_path: Container images created by kaniko are tarball files. This is the path where to store the image, will be named with suffix ``.tar``. This path will be created if not present.
        :param verbosity: Verbosity of kaniko logging. Default: "info"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2495b5e88ddaa0512109b982431d7841daef797033c03c01af360aac76d62fbf)
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument build_target", value=build_target, expected_type=type_hints["build_target"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument docker_client_config", value=docker_client_config, expected_type=type_hints["docker_client_config"])
            check_type(argname="argument dockerfile", value=dockerfile, expected_type=type_hints["dockerfile"])
            check_type(argname="argument enable_push", value=enable_push, expected_type=type_hints["enable_push"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument registries", value=registries, expected_type=type_hints["registries"])
            check_type(argname="argument tar_path", value=tar_path, expected_type=type_hints["tar_path"])
            check_type(argname="argument verbosity", value=verbosity, expected_type=type_hints["verbosity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_args is not None:
            self._values["build_args"] = build_args
        if build_target is not None:
            self._values["build_target"] = build_target
        if context is not None:
            self._values["context"] = context
        if docker_client_config is not None:
            self._values["docker_client_config"] = docker_client_config
        if dockerfile is not None:
            self._values["dockerfile"] = dockerfile
        if enable_push is not None:
            self._values["enable_push"] = enable_push
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if registries is not None:
            self._values["registries"] = registries
        if tar_path is not None:
            self._values["tar_path"] = tar_path
        if verbosity is not None:
            self._values["verbosity"] = verbosity

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Container build arguments, used to instrument the container image build.'''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def build_target(self) -> typing.Optional[builtins.str]:
        '''For container multistage builds name of the build stage you want to create.

        Image tag will be appended with the build_target. e.g. latest-buildtarget.
        '''
        result = self._values.get("build_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''Context which will be send to kaniko.

        Defaults to ``None`` which implies
        the local directory is the context.
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        result = self._values.get("docker_client_config")
        return typing.cast(typing.Optional["DockerClientConfig"], result)

    @builtins.property
    def dockerfile(self) -> typing.Optional[builtins.str]:
        '''Name of the dockerfile to use.

        File is relative to context.

        :default: "Dockerfile"
        '''
        result = self._values.get("dockerfile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_push(self) -> typing.Optional[builtins.bool]:
        '''Enable push to container registry, disabled to allow subsequent jobs to.

        :default:

        false
        act on container tarball.
        '''
        result = self._values.get("enable_push")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Image name which will be created.

        :default: PredefinedVariables.CI_PROJECT_NAME.
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.CI_COMMIT_TAG
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registries(
        self,
    ) -> typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]]:
        '''List of container registries to push created image to.'''
        result = self._values.get("registries")
        return typing.cast(typing.Optional[typing.Union[typing.List[builtins.str], typing.List["Registry"]]], result)

    @builtins.property
    def tar_path(self) -> typing.Optional[builtins.str]:
        '''Container images created by kaniko are tarball files.

        This is the path where to store the image, will be named with suffix ``.tar``.
        This path will be created if not present.
        '''
        result = self._values.get("tar_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verbosity(self) -> typing.Optional[builtins.str]:
        '''Verbosity of kaniko logging.

        :default: "info"
        '''
        result = self._values.get("verbosity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KanikoExecuteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PredefinedImages(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.PredefinedImages",
):
    '''The PredefinedImages collection supplies commonly utilized container image objects within the gcix framework.'''

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALPINE_GIT")
    def ALPINE_GIT(cls) -> _Image_e46ac833:
        '''A predefined Alpine Git container image object.

        This image is useful for Git operations within containers.
        '''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "ALPINE_GIT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BUSYBOX")
    def BUSYBOX(cls) -> _Image_e46ac833:
        '''A predefined Busybox container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "BUSYBOX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CRANE")
    def CRANE(cls) -> _Image_e46ac833:
        '''A predefined Crane container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "CRANE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DIVE")
    def DIVE(cls) -> _Image_e46ac833:
        '''A predefined Dive container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "DIVE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GCIP")
    def GCIP(cls) -> _Image_e46ac833:
        '''A predefined GCIP container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "GCIP"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GCIX")
    def GCIX(cls) -> _Image_e46ac833:
        '''A predefined GCIX container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "GCIX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="KANIKO")
    def KANIKO(cls) -> _Image_e46ac833:
        '''A predefined Kaniko container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "KANIKO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRIVY")
    def TRIVY(cls) -> _Image_e46ac833:
        '''A predefined Trivy container image object.'''
        return typing.cast(_Image_e46ac833, jsii.sget(cls, "TRIVY"))


class Registry(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.container.Registry"):
    '''Container registry urls constants.'''

    @jsii.member(jsii_name="aws")
    @builtins.classmethod
    def aws(
        cls,
        *,
        account_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Amazon Elastic Container Registry (ECR).

        If neither ``accountId`` nor ``region`` is given, the method attempts to
        evaluate ``accountId`` and ``region`` using helper functions from ``aws.AWSAccount``.
        If either of the helper functions does provide a valid value, a ``ValueError`` or ``KeyError`` exception will be raised.

        :param account_id: AWS account id. Default: AWSAccount.awsAccountId()
        :param region: AWS region where the ECR repository lives in. Default: AWSAccount.awsRegion()

        :return:

        Elastic Container Registry URL in the format of
        **${awsAccountId}.dkr.ecr.${region}.amazonaws.com**.

        :throws: {Error} If no region was found in ``aws.AWSAccount.awsRegion()``.
        '''
        props = AWSRegistryProps(account_id=account_id, region=region)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "aws", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOCKER")
    def DOCKER(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "DOCKER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GCR")
    def GCR(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "GCR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="QUAY")
    def QUAY(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "QUAY"))


@jsii.implements(ITrivyIgnoreFileCheck)
class TrivyIgnoreFileCheck(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.TrivyIgnoreFileCheck",
):
    '''This job checks if a .trivyignore file exists and is not empty and fails if so.

    If a .trivyignore file is found and not empty, by default the job fails with ``exit 1``,
    the job is configured to allow failures so that the pipeline keeps running.
    This ensures the visibility of acknowledged CVE's in the .trivyignore
    file inside the pipeline.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: trivyignore
    - stage: check
    - image: PredefinedImages.BUSYBOX
    - allow_failure: 1
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        trivyignore_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param trivyignore_path: Path to the ``.trivyignore`` file. Default: PredefinedVariables.ciProjectDir/.trivyignore
        '''
        props = TrivyIgnoreFileCheckProps(
            job_name=job_name, job_stage=job_stage, trivyignore_path=trivyignore_path
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
    @jsii.member(jsii_name="trivyignorePath")
    def trivyignore_path(self) -> builtins.str:
        '''Path to the ``.trivyignore`` file.'''
        return typing.cast(builtins.str, jsii.get(self, "trivyignorePath"))

    @trivyignore_path.setter
    def trivyignore_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2391e9fdda74757a01c75df1e8d9ae6b9f644b8b8e4223cd2dbcad6a1a9b32a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyignorePath", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.container.TrivyIgnoreFileCheckProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "job_stage": "jobStage",
        "trivyignore_path": "trivyignorePath",
    },
)
class TrivyIgnoreFileCheckProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        trivyignore_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param trivyignore_path: Path to the ``.trivyignore`` file. Default: PredefinedVariables.ciProjectDir/.trivyignore
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac108d7e6f4ffbd2bf8d4f7f494d032718e1af6cd51a15b5c8eb075fde4dda23)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument trivyignore_path", value=trivyignore_path, expected_type=type_hints["trivyignore_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if trivyignore_path is not None:
            self._values["trivyignore_path"] = trivyignore_path

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trivyignore_path(self) -> typing.Optional[builtins.str]:
        '''Path to the ``.trivyignore`` file.

        :default: PredefinedVariables.ciProjectDir/.trivyignore
        '''
        result = self._values.get("trivyignore_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrivyIgnoreFileCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITrivyScanLocalImage)
class TrivyScanLocalImage(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.TrivyScanLocalImage",
):
    '''This job scanns container images to find vulnerabilities.

    This job fails with exit code 1 if severities are found.
    The scan output is printed to stdout and uploaded to the artifacts of GitLab.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: trivy
    - stage: check
    - image: PredefinedImages.TRIVY
    - artifacts: Path 'trivy.txt'
    '''

    def __init__(
        self,
        *,
        debug: typing.Optional[builtins.bool] = None,
        exit_if_vulnerable: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_path: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        output_format: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        trivy_config: typing.Optional[builtins.str] = None,
        vulnerability_types: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param debug: If trivy should run in debug mode. Default: false
        :param exit_if_vulnerable: Exit code when vulnerabilities were found. If true exit code is 1 else 0. Default: true
        :param image_name: Container image name, searched for in ``imagePath`` and gets ``.tar`` appended. Default: PredefinedVariables.CI_PROJECT_NAME
        :param image_path: Path where to find the container image. Default: PredefinedVariables.CI_PROJECT_DIR
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.CI_COMMIT_TAG
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param output_format: Scan output format, possible values (table, json). Default: "table"
        :param severity: Severities of vulnerabilities to be displayed (comma separated). Default: "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL"
        :param trivy_config: Additional options to pass to ``trivy`` binary.
        :param vulnerability_types: List of vulnerability types (comma separated). Default: "os,library"
        '''
        props = TrivyScanLocalImageProps(
            debug=debug,
            exit_if_vulnerable=exit_if_vulnerable,
            image_name=image_name,
            image_path=image_path,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            output_format=output_format,
            severity=severity,
            trivy_config=trivy_config,
            vulnerability_types=vulnerability_types,
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
    @jsii.member(jsii_name="debug")
    def debug(self) -> builtins.bool:
        '''If trivy should run in debug mode.'''
        return typing.cast(builtins.bool, jsii.get(self, "debug"))

    @debug.setter
    def debug(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e101f33839bc4fb0ae0fec94ae271a7489431391d0ed499559772b55838ef03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "debug", value)

    @builtins.property
    @jsii.member(jsii_name="exitIfVulnerable")
    def exit_if_vulnerable(self) -> builtins.bool:
        '''Exit code when vulnerabilities were found.

        If true exit code is 1 else 0.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "exitIfVulnerable"))

    @exit_if_vulnerable.setter
    def exit_if_vulnerable(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae26370b5edf10ea29fa9027e615ceabe36b3abc8a24c17635e901eb67c298b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exitIfVulnerable", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.'''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aab1e201cbc866a99843185b3e01d2e3e7786903e0a6e93262618f0fe87784d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imagePath")
    def image_path(self) -> builtins.str:
        '''Path where to find the container image.'''
        return typing.cast(builtins.str, jsii.get(self, "imagePath"))

    @image_path.setter
    def image_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9771ae954b212495dc580964dbc93f312fc145fe5d07db1f6ed15c4b75d71c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePath", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c758bd9cf3aadf62ed365904bc5137bb64d48be2dc6676efad9350366d315def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        '''Scan output format, possible values (table, json).'''
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f521d09fb95c2c9a00b8aa644706b1543e537ddade19b740202100e97a473b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value)

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        '''Severities of vulnerabilities to be displayed (comma separated).'''
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dcf05aff049477f8d44f169f6558561d67c50ab9f0143f3c670f273a9926d91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value)

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityTypes")
    def vulnerability_types(self) -> builtins.str:
        '''List of vulnerability types (comma separated).'''
        return typing.cast(builtins.str, jsii.get(self, "vulnerabilityTypes"))

    @vulnerability_types.setter
    def vulnerability_types(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51f6e7d50ce8feb0288a91a7fb2d67560d4e8f8f7e79b334c7ab0c663fe0b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerabilityTypes", value)

    @builtins.property
    @jsii.member(jsii_name="trivyConfig")
    def trivy_config(self) -> typing.Optional[builtins.str]:
        '''Additional options to pass to ``trivy`` binary.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trivyConfig"))

    @trivy_config.setter
    def trivy_config(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c555dd23c3fde2604d322813b03b387ae9ae51392342b82e47f0ae4e94fc07f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyConfig", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.container.TrivyScanLocalImageProps",
    jsii_struct_bases=[],
    name_mapping={
        "debug": "debug",
        "exit_if_vulnerable": "exitIfVulnerable",
        "image_name": "imageName",
        "image_path": "imagePath",
        "image_tag": "imageTag",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "output_format": "outputFormat",
        "severity": "severity",
        "trivy_config": "trivyConfig",
        "vulnerability_types": "vulnerabilityTypes",
    },
)
class TrivyScanLocalImageProps:
    def __init__(
        self,
        *,
        debug: typing.Optional[builtins.bool] = None,
        exit_if_vulnerable: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_path: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        output_format: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        trivy_config: typing.Optional[builtins.str] = None,
        vulnerability_types: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param debug: If trivy should run in debug mode. Default: false
        :param exit_if_vulnerable: Exit code when vulnerabilities were found. If true exit code is 1 else 0. Default: true
        :param image_name: Container image name, searched for in ``imagePath`` and gets ``.tar`` appended. Default: PredefinedVariables.CI_PROJECT_NAME
        :param image_path: Path where to find the container image. Default: PredefinedVariables.CI_PROJECT_DIR
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.CI_COMMIT_TAG
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param output_format: Scan output format, possible values (table, json). Default: "table"
        :param severity: Severities of vulnerabilities to be displayed (comma separated). Default: "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL"
        :param trivy_config: Additional options to pass to ``trivy`` binary.
        :param vulnerability_types: List of vulnerability types (comma separated). Default: "os,library"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f200764796df1b9fe91b8b4a8ee168d4d8529391b2df7073a2026c74a6e5af9d)
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
            check_type(argname="argument exit_if_vulnerable", value=exit_if_vulnerable, expected_type=type_hints["exit_if_vulnerable"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_path", value=image_path, expected_type=type_hints["image_path"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument trivy_config", value=trivy_config, expected_type=type_hints["trivy_config"])
            check_type(argname="argument vulnerability_types", value=vulnerability_types, expected_type=type_hints["vulnerability_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if debug is not None:
            self._values["debug"] = debug
        if exit_if_vulnerable is not None:
            self._values["exit_if_vulnerable"] = exit_if_vulnerable
        if image_name is not None:
            self._values["image_name"] = image_name
        if image_path is not None:
            self._values["image_path"] = image_path
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if output_format is not None:
            self._values["output_format"] = output_format
        if severity is not None:
            self._values["severity"] = severity
        if trivy_config is not None:
            self._values["trivy_config"] = trivy_config
        if vulnerability_types is not None:
            self._values["vulnerability_types"] = vulnerability_types

    @builtins.property
    def debug(self) -> typing.Optional[builtins.bool]:
        '''If trivy should run in debug mode.

        :default: false
        '''
        result = self._values.get("debug")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exit_if_vulnerable(self) -> typing.Optional[builtins.bool]:
        '''Exit code when vulnerabilities were found.

        If true exit code is 1 else 0.

        :default: true
        '''
        result = self._values.get("exit_if_vulnerable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.

        :default: PredefinedVariables.CI_PROJECT_NAME
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_path(self) -> typing.Optional[builtins.str]:
        '''Path where to find the container image.

        :default: PredefinedVariables.CI_PROJECT_DIR
        '''
        result = self._values.get("image_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''The tag the image will be tagged with.

        :default: PredefinedVariables.CI_COMMIT_TAG
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Bootstrap job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the Bootstrap job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''Scan output format, possible values (table, json).

        :default: "table"
        '''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Severities of vulnerabilities to be displayed (comma separated).

        :default: "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL"
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trivy_config(self) -> typing.Optional[builtins.str]:
        '''Additional options to pass to ``trivy`` binary.'''
        result = self._values.get("trivy_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vulnerability_types(self) -> typing.Optional[builtins.str]:
        '''List of vulnerability types (comma separated).

        :default: "os,library"
        '''
        result = self._values.get("vulnerability_types")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrivyScanLocalImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IBuildContainerCollection)
class BuildContainerCollection(
    _JobCollection_0289800c,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.BuildContainerCollection",
):
    '''Creates a ``gcip.Sequence`` to build, scan and push a container image.

    The build step is executed by ``KanikoExecute``,  it will build the container
    image an outputs it to a tarball. There are two scan's, optimization scan
    with ``DiveScan`` to scan storage wasting in container image and a
    vulnerability scan with ``TrivyScanLocalImage``. Both outputs are uploaded
    as an artifact to the GitLab instance. The container image is uploaded
    with ``CranePush``.
    '''

    def __init__(
        self,
        *,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        do_crane_push: typing.Optional[builtins.bool] = None,
        do_dive_scan: typing.Optional[builtins.bool] = None,
        do_trivyignore_check: typing.Optional[builtins.bool] = None,
        do_trivy_scan: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        registry: typing.Optional[typing.Union[builtins.str, Registry]] = None,
    ) -> None:
        '''
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param do_crane_push: Set to ``false`` to skip the Crane push job. Default: true
        :param do_dive_scan: Set to ``false`` to skip the Dive scan job. Default: true
        :param do_trivyignore_check: Set to ``false`` to skip the existance check of the ``.trivyignore`` file. Default: true
        :param do_trivy_scan: Set to ``false`` to skip the Trivy scan job. Default: true
        :param image_name: Image name with stage in the registry. e.g. username/imageName. Default: PredefinedVariables.ciProjectName
        :param image_tag: Image tag. Depending of the build it defaults either to the git tag or to the actual branch name. Default: PredefinedVariables.ciCommitRefName
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param registry: Container registry to push the image to. If the container registry needs authentication, you have to provide a ``DockerClientConfig`` object with credentials. Default: Registry.DOCKER
        '''
        props = BuildContainerCollectionProps(
            docker_client_config=docker_client_config,
            do_crane_push=do_crane_push,
            do_dive_scan=do_dive_scan,
            do_trivyignore_check=do_trivyignore_check,
            do_trivy_scan=do_trivy_scan,
            image_name=image_name,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            registry=registry,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="cranePushJob")
    def crane_push_job(self) -> "CranePush":
        '''Crane push job.'''
        return typing.cast("CranePush", jsii.get(self, "cranePushJob"))

    @crane_push_job.setter
    def crane_push_job(self, value: "CranePush") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888eec956f281f618d8ffd959134518ea8f309867e78dd804ec16fab3c8df7c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cranePushJob", value)

    @builtins.property
    @jsii.member(jsii_name="diveScanJob")
    def dive_scan_job(self) -> "DiveScan":
        '''Dive scan job.'''
        return typing.cast("DiveScan", jsii.get(self, "diveScanJob"))

    @dive_scan_job.setter
    def dive_scan_job(self, value: "DiveScan") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6404340127e815431a1d0d8296a99cce47e0b506d0b0aa26f75b378e84e25b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diveScanJob", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.'''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96dbbd08ea310657684ba0791f1ea24f5a6cbbfe9520c5bd67b9108b4e82304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="doCranePush")
    def do_crane_push(self) -> builtins.bool:
        '''Set to ``false`` to skip the Crane push job.'''
        return typing.cast(builtins.bool, jsii.get(self, "doCranePush"))

    @do_crane_push.setter
    def do_crane_push(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d92e7c6562f0d2aefd66dd0fc3d421d91bd76838eefd22a1323f65d06e865ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doCranePush", value)

    @builtins.property
    @jsii.member(jsii_name="doDiveScan")
    def do_dive_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Dive scan job.'''
        return typing.cast(builtins.bool, jsii.get(self, "doDiveScan"))

    @do_dive_scan.setter
    def do_dive_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f66366dcad131b08e1a18db166da11b846e104fdc9d0e7ca28bd4efbb86d188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doDiveScan", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyignoreCheck")
    def do_trivyignore_check(self) -> builtins.bool:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.'''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyignoreCheck"))

    @do_trivyignore_check.setter
    def do_trivyignore_check(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7151a6e56dca5f037236fe6e9e3711b8cc7a78f44c9ade48077b6b0f714ffb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyignoreCheck", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyScan")
    def do_trivy_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Trivy scan job.'''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyScan"))

    @do_trivy_scan.setter
    def do_trivy_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00c06589c0157c19232ea1c1d063eff5355db3077e2295200c8e17ca5f35081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyScan", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name with stage in the registry.

        e.g. username/imageName.
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4913c762c8fe6cfa9daaea47e73ff22f08e7f1c9a8a4892734ebd03efa87630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Image tag.

        Depending of the build it defaults either to the git tag or
        to the actual branch name.
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e60fb8a421e27f3024da332ca1799416f057c17744fe40dbdef1f2c67f7c35e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="kanikoExecuteJob")
    def kaniko_execute_job(self) -> KanikoExecute:
        '''Kaniko execute job.'''
        return typing.cast(KanikoExecute, jsii.get(self, "kanikoExecuteJob"))

    @kaniko_execute_job.setter
    def kaniko_execute_job(self, value: KanikoExecute) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2922369fb367be38dba77bd09f32f3ca31226c1f0ffe59bb8035ab2b095c1c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kanikoExecuteJob", value)

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> typing.Union[builtins.str, Registry]:
        '''Container registry to push the image to.

        If the container registry
        needs authentication, you have to provide a ``DockerClientConfig`` object
        with credentials.
        '''
        return typing.cast(typing.Union[builtins.str, Registry], jsii.get(self, "registry"))

    @registry.setter
    def registry(self, value: typing.Union[builtins.str, Registry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fde6aeeb273678c9d3d4d9df2d0a4803531986ac8bca58b504663bd5b1aa97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registry", value)

    @builtins.property
    @jsii.member(jsii_name="trivyIgnoreFileCheckJob")
    def trivy_ignore_file_check_job(self) -> TrivyIgnoreFileCheck:
        '''Trivy ignore file check job.'''
        return typing.cast(TrivyIgnoreFileCheck, jsii.get(self, "trivyIgnoreFileCheckJob"))

    @trivy_ignore_file_check_job.setter
    def trivy_ignore_file_check_job(self, value: TrivyIgnoreFileCheck) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a6038b17e0b2bd969d867a443dea17e29b89352e2fb1575e29494455e52ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyIgnoreFileCheckJob", value)

    @builtins.property
    @jsii.member(jsii_name="trivyScanLocalImageJob")
    def trivy_scan_local_image_job(self) -> TrivyScanLocalImage:
        '''Trivy scan local image job.'''
        return typing.cast(TrivyScanLocalImage, jsii.get(self, "trivyScanLocalImageJob"))

    @trivy_scan_local_image_job.setter
    def trivy_scan_local_image_job(self, value: TrivyScanLocalImage) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b292ca715a4c414a39b03b17baacf023dccd452ebb7ae378b91b637b896105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyScanLocalImageJob", value)


class BuildGitlabContainerCollection(
    BuildContainerCollection,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.BuildGitlabContainerCollection",
):
    '''BuildGitlabContainerCollection class.

    Orchestrates a GitLab-specific CI/CD pipeline for building, scanning,
    and pushing container images. Extends the BuildContainerCollection class.
    Handles GitLab-specific configurations, such as image name, registry,
    and Docker client authentication.

    :class: BuildGitlabContainerCollection
    :extends: BuildContainerCollection
    '''

    def __init__(
        self,
        *,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        do_crane_push: typing.Optional[builtins.bool] = None,
        do_dive_scan: typing.Optional[builtins.bool] = None,
        do_trivyignore_check: typing.Optional[builtins.bool] = None,
        do_trivy_scan: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        registry: typing.Optional[typing.Union[builtins.str, Registry]] = None,
    ) -> None:
        '''Constructor for BuildGitlabContainerCollection.

        Overrides the parent constructor to handle GitLab-specific configurations.
        Throws an error if the ``CI_REGISTRY`` environment variable is not set.
        Initializes Docker client authentication using CI_REGISTRY_USER and CI_REGISTRY_PASSWORD.

        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param do_crane_push: Set to ``false`` to skip the Crane push job. Default: true
        :param do_dive_scan: Set to ``false`` to skip the Dive scan job. Default: true
        :param do_trivyignore_check: Set to ``false`` to skip the existance check of the ``.trivyignore`` file. Default: true
        :param do_trivy_scan: Set to ``false`` to skip the Trivy scan job. Default: true
        :param image_name: Image name with stage in the registry. e.g. username/imageName. Default: PredefinedVariables.ciProjectName
        :param image_tag: Image tag. Depending of the build it defaults either to the git tag or to the actual branch name. Default: PredefinedVariables.ciCommitRefName
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param registry: Container registry to push the image to. If the container registry needs authentication, you have to provide a ``DockerClientConfig`` object with credentials. Default: Registry.DOCKER

        :throws: {Error} Throws an error if CI_REGISTRY environment variable is not set.
        '''
        props = BuildContainerCollectionProps(
            docker_client_config=docker_client_config,
            do_crane_push=do_crane_push,
            do_dive_scan=do_dive_scan,
            do_trivyignore_check=do_trivyignore_check,
            do_trivy_scan=do_trivy_scan,
            image_name=image_name,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            registry=registry,
        )

        jsii.create(self.__class__, self, [props])


@jsii.implements(ICopyContainerCollection)
class CopyContainerCollection(
    _JobCollection_0289800c,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.CopyContainerCollection",
):
    '''Creates a ``gcip.Sequence`` to pull, scan and push a container image.

    The pull step is executed by ``CranePull``, it will pull the container image
    and outputs it to a tarball. There are two scan's, optimization scan with
    ``DiveScan`` to scan storage wasting in container image and a vulnerability
    scan with ``TrivyScanLocalImage``.  Both outputs are uploaded as an artifact
    to the GitLab instance. Built container image is uploaded with ``CranePush``.

    NOTE:
    We decided to use caches instead of artifacts to pass the Docker image tar
    archive from one job to another. This is because those tar archives could
    become very large - especially larger then the maximum artifact size limit.
    This limit can just be adjusted by the admin of the gitlab instance, so
    your pipeline would never work, your Gitlab provider would not adjust this
    limit for you. For caches on the other hand you can define storage backends
    at the base of your Gitlab runners.

    Furthermore we set the cache key to the pipeline ID. This is because the
    name and tag of the image does not ensure that the downloaded tar is unique,
    as the image behind the image tag could be overridden.  So we ensure
    uniqueness by downloading the image once per pipeline.
    '''

    def __init__(
        self,
        *,
        image_name: builtins.str,
        image_tag: builtins.str,
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        do_dive_scan: typing.Optional[builtins.bool] = None,
        do_trivyignore_check: typing.Optional[builtins.bool] = None,
        do_trivy_scan: typing.Optional[builtins.bool] = None,
        dst_registry: typing.Optional[typing.Union[builtins.str, Registry]] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        src_registry: typing.Optional[typing.Union[builtins.str, Registry]] = None,
    ) -> None:
        '''
        :param image_name: Image name with stage in the registry. e.g. username/image_name.
        :param image_tag: Container image tag to pull from ``srcRegistry`` and push to ``dstRegistry``.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param do_dive_scan: Set to ``false`` to skip the Dive scan job. Default: true
        :param do_trivyignore_check: Set to ``false`` to skip the existance check of the ``.trivyignore`` file. Default: true
        :param do_trivy_scan: Set to ``false`` to skip the Trivy scan job. Default: true
        :param dst_registry: Container registry to push the image to. If the container registry needs authentication, you have to provide a ``DockerClientConfig`` object with credentials. Default: Registry.DOCKER
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param src_registry: Container registry to pull the image from. If the container registry needs authentication, you have to provide a ``DockerClientConfig`` object with credentials. Default: Registry.DOCKER
        '''
        props = CopyContainerCollectionProps(
            image_name=image_name,
            image_tag=image_tag,
            docker_client_config=docker_client_config,
            do_dive_scan=do_dive_scan,
            do_trivyignore_check=do_trivyignore_check,
            do_trivy_scan=do_trivy_scan,
            dst_registry=dst_registry,
            job_name=job_name,
            job_stage=job_stage,
            src_registry=src_registry,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="cranePullJob")
    def crane_pull_job(self) -> "CranePull":
        '''CranPull job.'''
        return typing.cast("CranePull", jsii.get(self, "cranePullJob"))

    @crane_pull_job.setter
    def crane_pull_job(self, value: "CranePull") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc64a201767458b70da09d48d00f2d51c93ae8bdc860e62c913f8daa9929699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cranePullJob", value)

    @builtins.property
    @jsii.member(jsii_name="cranePushJob")
    def crane_push_job(self) -> "CranePush":
        return typing.cast("CranePush", jsii.get(self, "cranePushJob"))

    @crane_push_job.setter
    def crane_push_job(self, value: "CranePush") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fce608add90049af352328b3004b52675ccaf523a1caded85630603d1079ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cranePushJob", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.'''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef05e812b15f5cead6f9a6d7641bdec5076f2a2ec000e1580fee6ae2219cf72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="doDiveScan")
    def do_dive_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Dive scan job.'''
        return typing.cast(builtins.bool, jsii.get(self, "doDiveScan"))

    @do_dive_scan.setter
    def do_dive_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a74e44774373fc2a574495e05a09af481a5f04e6f25929d5cc85cf9966738e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doDiveScan", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyignoreCheck")
    def do_trivyignore_check(self) -> builtins.bool:
        '''Set to ``false`` to skip the existance check of the ``.trivyignore`` file.'''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyignoreCheck"))

    @do_trivyignore_check.setter
    def do_trivyignore_check(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e0ea527e36d5f07a4aee8d21f6b098dab3c0a90a2f5c336a815ea233fd0bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyignoreCheck", value)

    @builtins.property
    @jsii.member(jsii_name="doTrivyScan")
    def do_trivy_scan(self) -> builtins.bool:
        '''Set to ``false`` to skip the Trivy scan job.'''
        return typing.cast(builtins.bool, jsii.get(self, "doTrivyScan"))

    @do_trivy_scan.setter
    def do_trivy_scan(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e924e58f07211f8686fa15bfec64e9d8a12427d23174c31e91e602a5607a0ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doTrivyScan", value)

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, Registry]:
        '''Container registry to push the image to.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.
        '''
        return typing.cast(typing.Union[builtins.str, Registry], jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, Registry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a3239a551f7f0703d9aab14c886cb157af9b03977c6b5fe98e66f5a9a7b5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Image name with stage in the registry.

        e.g. username/image_name.
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeac6577989dfdc99efd5e906fe59dabdfcbbb30b46df3a6f4d800ca9bf4e2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Container image tag to pull from ``srcRegistry`` and push to ``dstRegistry``.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaed0b8f4aac0fb320bc7fb8fb796cb3625bf0b54d4bf18e18161b4707e4b1e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, Registry]:
        '''Container registry to pull the image from.

        If the container registry needs
        authentication, you have to provide a ``DockerClientConfig`` object with
        credentials.
        '''
        return typing.cast(typing.Union[builtins.str, Registry], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, Registry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024d89a78a509a20b217d9df674764a58481361f4379657687b8e5470c0562c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="diveScanJob")
    def dive_scan_job(self) -> typing.Optional["DiveScan"]:
        '''Dive scan job.'''
        return typing.cast(typing.Optional["DiveScan"], jsii.get(self, "diveScanJob"))

    @dive_scan_job.setter
    def dive_scan_job(self, value: typing.Optional["DiveScan"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84440b4fdd289d6ca9352a972a14b65917c4d1e9e96df75ba1230589d37f2366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diveScanJob", value)

    @builtins.property
    @jsii.member(jsii_name="trivyIgnoreFileCheckJob")
    def trivy_ignore_file_check_job(self) -> typing.Optional[TrivyIgnoreFileCheck]:
        '''Trivy ignore file check job.'''
        return typing.cast(typing.Optional[TrivyIgnoreFileCheck], jsii.get(self, "trivyIgnoreFileCheckJob"))

    @trivy_ignore_file_check_job.setter
    def trivy_ignore_file_check_job(
        self,
        value: typing.Optional[TrivyIgnoreFileCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acaac19a024798d356530addcfb675d00e7718fa15592b52a0bd3d18d5c5b0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyIgnoreFileCheckJob", value)

    @builtins.property
    @jsii.member(jsii_name="trivyScanLocalImageJob")
    def trivy_scan_local_image_job(self) -> typing.Optional[TrivyScanLocalImage]:
        '''Trivy scan local image job.'''
        return typing.cast(typing.Optional[TrivyScanLocalImage], jsii.get(self, "trivyScanLocalImageJob"))

    @trivy_scan_local_image_job.setter
    def trivy_scan_local_image_job(
        self,
        value: typing.Optional[TrivyScanLocalImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1036f13aa2d377d6ce01902136e04ccdee48bbd061144df33038fd886a738b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trivyScanLocalImageJob", value)


@jsii.implements(ICraneCopy)
class CraneCopy(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.CraneCopy",
):
    '''Creates a job to copy container images with ``crane``. See ```crane`` <https://github.com/google/go-containerregistry/tree/main/cmd/crane>`_.

    Copying an image is useful, if you want to have container images as close
    as possible to your cluster or servers.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: crane-copy
    - stage: deploy
    - image: PredefinedImages.CRANE
    '''

    def __init__(
        self,
        *,
        dst_registry: typing.Union[builtins.str, Registry],
        src_registry: typing.Union[builtins.str, Registry],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param src_registry: Registry URL to copy container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        '''
        props = CraneCopyProps(
            dst_registry=dst_registry,
            src_registry=src_registry,
            docker_client_config=docker_client_config,
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
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, Registry]:
        '''Registry URL to copy container image to.'''
        return typing.cast(typing.Union[builtins.str, Registry], jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, Registry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f253d7757bc4254083e30859b29145202b6682b597a7317be2303f85edaed0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, Registry]:
        '''Registry URL to copy container image from.'''
        return typing.cast(typing.Union[builtins.str, Registry], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, Registry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c4b4b3430b6882f7fce62f48611ac8b4160a793c02c7e2d390d91f5342c8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> typing.Optional["DockerClientConfig"]:
        '''Creates the Docker configuration file base on objects settings, used by crane to authenticate against given registries.'''
        return typing.cast(typing.Optional["DockerClientConfig"], jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(
        self,
        value: typing.Optional["DockerClientConfig"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853cf50eb2cf5284e5f43ff03be1857f10d0f46c3e97c0dbfa69004467ccd865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)


@jsii.implements(ICranePull)
class CranePull(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.CranePull",
):
    '''Creates a job to pull container image from remote container registry with ``crane``.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: crane
    - stage: pull
    - image: PredefinedImages.CRANE
    '''

    def __init__(
        self,
        *,
        src_registry: typing.Union[builtins.str, Registry],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param src_registry: Registry URL to pull container image from.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Default: DockerClientConfig with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image with namespace to pull from ``srcRegistry``. Default: PredefinedVariables.ciProjectName
        :param image_tag: Tag of the image which will be pulled. Default: latest
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to save the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        props = CranePullProps(
            src_registry=src_registry,
            docker_client_config=docker_client_config,
            image_name=image_name,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            tar_path=tar_path,
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
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.'''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f05f9ede43dbf97af83473670a3028d41eb17c74c0a35998790dfcbcf7779f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image with namespace to pull from ``srcRegistry``.'''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c04f6d7e0856ea05e199b824d1fef5e77743333145a563615df3b6e24e38a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''Tag of the image which will be pulled.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc52d1cbcbb774ca91c8fe7b76204e751812162fa4f52451e91b4a7dd2c00219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="srcRegistry")
    def src_registry(self) -> typing.Union[builtins.str, Registry]:
        '''Registry URL to pull container image from.'''
        return typing.cast(typing.Union[builtins.str, Registry], jsii.get(self, "srcRegistry"))

    @src_registry.setter
    def src_registry(self, value: typing.Union[builtins.str, Registry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92b854c26778a2e53e5fd7d02e43103e86f5c58f3a4965d756f1c1db56dc9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to save the container image tarball.'''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710f217da8e365150a4d44b7525ded0d915488f00e3eba17d7d4aaf3bc2ca7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)


@jsii.implements(ICranePush)
class CranePush(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.CranePush",
):
    '''Creates a job to push container image to remote container registry with ``crane``.

    The image to copy must be in a ``tarball`` format. It gets validated with crane
    and is pushed to ``dst_registry`` destination registry.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: crane-push
    - stage: deploy
    - image: PredefinedImages.CRANE
    '''

    def __init__(
        self,
        *,
        dst_registry: typing.Union[builtins.str, Registry],
        docker_client_config: typing.Optional["DockerClientConfig"] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tar_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dst_registry: Registry URL to copy container image to.
        :param docker_client_config: Creates the Docker configuration file base on objects settings, to authenticate against given registries. Defaults to a ``DockerClientConfig`` with login to the official Docker Hub and expecting credentials given as environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        :param image_name: Container image name, searched for in ``imagePath`` and gets ``.tar`` appended. Default: PredefinedVariables.ciProjectName
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.ciCommitTag
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tar_path: Path where to find the container image tarball. Default: PredefinedVariables.ciProjectDir
        '''
        props = CranePushProps(
            dst_registry=dst_registry,
            docker_client_config=docker_client_config,
            image_name=image_name,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            tar_path=tar_path,
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
    @jsii.member(jsii_name="dockerClientConfig")
    def docker_client_config(self) -> "DockerClientConfig":
        '''Creates the Docker configuration file base on objects settings, to authenticate against given registries.

        Defaults to a ``DockerClientConfig``
        with login to the official Docker Hub and expecting credentials given as
        environment variables ``REGISTRY_USER`` and ``REGISTRY_LOGIN``.
        '''
        return typing.cast("DockerClientConfig", jsii.get(self, "dockerClientConfig"))

    @docker_client_config.setter
    def docker_client_config(self, value: "DockerClientConfig") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b240e50c52eeff890833592e36cd4323ce92803e128ca9f1d211521ad7823a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerClientConfig", value)

    @builtins.property
    @jsii.member(jsii_name="dstRegistry")
    def dst_registry(self) -> typing.Union[builtins.str, Registry]:
        '''Registry URL to copy container image to.'''
        return typing.cast(typing.Union[builtins.str, Registry], jsii.get(self, "dstRegistry"))

    @dst_registry.setter
    def dst_registry(self, value: typing.Union[builtins.str, Registry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e69659a083b47f4fcb86bc9dba5e55c5feff7c5a98afba50b0345f9250655ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dstRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Container image name, searched for in ``imagePath`` and gets ``.tar`` appended.'''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964f4192a0d90ea2897d6b0177a51f2e018be9de3f7838e0eeae353375d3b6fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe70150d68a7adbc49d4b4cef8662ee7abe851bc67419fbbe29f96728a645c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="tarPath")
    def tar_path(self) -> builtins.str:
        '''Path where to find the container image tarball.'''
        return typing.cast(builtins.str, jsii.get(self, "tarPath"))

    @tar_path.setter
    def tar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72be2fe328749fcc98e785a7c9bd4a8947866df926aeca145e7ac0d5c4e374b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tarPath", value)


@jsii.implements(IDiveScan)
class DiveScan(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.DiveScan",
):
    '''Scan your images with `wagoodman/dive <https://github.com/wagoodman/dive>`_.

    ``dive`` will scan your container image layers and will output the efficency
    of each layer. You can see which layer and which file is consuming the most
    storage and optimize the layers if possible. It prevents container images
    and its layers beeing polluted with files like apt or yum cache's.
    The output produced by ``dive`` is uploaded as an artifact to the
    GitLab instance.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: dive
    - stage: check
    - image: PredefinedImages.DIVE
    - artifacts: Path 'dive.txt'
    '''

    def __init__(
        self,
        *,
        highest_user_wasted_percent: typing.Optional[jsii.Number] = None,
        highest_wasted_bytes: typing.Optional[jsii.Number] = None,
        ignore_errors: typing.Optional[builtins.bool] = None,
        image_name: typing.Optional[builtins.str] = None,
        image_path: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        lowest_efficiency: typing.Optional[jsii.Number] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param highest_user_wasted_percent: Highest allowable percentage of bytes wasted (as a ratio between 0-1), otherwise CI validation will fail. Default: 0.1
        :param highest_wasted_bytes: Highest allowable bytes wasted, otherwise CI validation will fail.
        :param ignore_errors: Ignore image parsing errors and run the analysis anyway. Default: false
        :param image_name: Name of the container image to scan, if ``source`` is ``docker-archive`` argument gets prefix ``.tar``. Default: PredefinedVariables.ciProjectName
        :param image_path: Path to the image can be either a remote container registry, as well as a local path to an image. Default: PredefinedVariables.ciProjectPath
        :param image_tag: The tag the image will be tagged with. Default: PredefinedVariables.ciCommitTag
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param lowest_efficiency: Lowest allowable image efficiency (as a ratio between 0-1), otherwise CI validation will fail. Default: 0.9
        :param source: The container engine to fetch the image from. Allowed values: docker, podman, docker-archive Default: "docker-archive
        '''
        props = DiveScanProps(
            highest_user_wasted_percent=highest_user_wasted_percent,
            highest_wasted_bytes=highest_wasted_bytes,
            ignore_errors=ignore_errors,
            image_name=image_name,
            image_path=image_path,
            image_tag=image_tag,
            job_name=job_name,
            job_stage=job_stage,
            lowest_efficiency=lowest_efficiency,
            source=source,
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
    @jsii.member(jsii_name="highestUserWastedPercent")
    def highest_user_wasted_percent(self) -> jsii.Number:
        '''Highest allowable percentage of bytes wasted (as a ratio between 0-1), otherwise CI validation will fail.'''
        return typing.cast(jsii.Number, jsii.get(self, "highestUserWastedPercent"))

    @highest_user_wasted_percent.setter
    def highest_user_wasted_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00feadced743630d8fff9e0c98a5aa109a170f97e0798c875aee4ba3138e5d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highestUserWastedPercent", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreErrors")
    def ignore_errors(self) -> builtins.bool:
        '''Ignore image parsing errors and run the analysis anyway.'''
        return typing.cast(builtins.bool, jsii.get(self, "ignoreErrors"))

    @ignore_errors.setter
    def ignore_errors(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2101e114e5cb63051f57e91cd6b02ae1803c957432f222515e1291bf93699e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreErrors", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        '''Name of the container image to scan, if ``source`` is ``docker-archive`` argument gets prefix ``.tar``.'''
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc74e395f342425d17a81a5aa0b965fa5cff57253448e9f008c16d64bffeacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imagePath")
    def image_path(self) -> builtins.str:
        '''Path to the image can be either a remote container registry, as well as a local path to an image.'''
        return typing.cast(builtins.str, jsii.get(self, "imagePath"))

    @image_path.setter
    def image_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2d9f92ed7ed2479318fd3de66586a822f474479721e44c9dcb83573a6520ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePath", value)

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''The tag the image will be tagged with.'''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6382aba1f79203bc03e3e7469cb71fda2ad0ba7a71dc2d4ada1f3b95efadd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value)

    @builtins.property
    @jsii.member(jsii_name="lowestEfficiency")
    def lowest_efficiency(self) -> jsii.Number:
        '''Lowest allowable image efficiency (as a ratio between 0-1), otherwise CI validation will fail.'''
        return typing.cast(jsii.Number, jsii.get(self, "lowestEfficiency"))

    @lowest_efficiency.setter
    def lowest_efficiency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67dfbfb7975e89718235bb870ef7c02c5757d22d2a1599c9432ad7cfdd3bf64a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lowestEfficiency", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''The container engine to fetch the image from.

        Allowed values: docker, podman, docker-archive
        '''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c5856866591955ea5a6bceb75c2ac2cbff9be938475dd0c6f00861d3d4f974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="highestWastedBytes")
    def highest_wasted_bytes(self) -> typing.Optional[jsii.Number]:
        '''Highest allowable bytes wasted, otherwise CI validation will fail.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "highestWastedBytes"))

    @highest_wasted_bytes.setter
    def highest_wasted_bytes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9e7f9db878dcbed1cf0192862548a658efdec7bba7166accfc20e0ace60e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highestWastedBytes", value)


@jsii.implements(IDockerBuild)
class DockerBuild(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.DockerBuild",
):
    '''Runs ```docker build`` <https://docs.docker.com/engine/reference/commandline/build/>`_.

    Example::

       import { Build } from "@gcix/gcix"
       const buildJob = Build({repository: "myrepo/myimage", tag: "v0.1.0"})

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: docker
    - stage: build
    '''

    def __init__(
        self,
        *,
        repository: builtins.str,
        context: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The Docker repository name ``([<registry>/]<image>)``.
        :param context: The Docker build context (the directory containing the Dockerfile). Default: ``.``
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param tag: A Docker image tag applied to the image. If not set docker uses ``latest``
        '''
        props = DockerBuildProps(
            repository=repository,
            context=context,
            job_name=job_name,
            job_stage=job_stage,
            tag=tag,
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
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        '''The Docker build context (the directory containing the Dockerfile).'''
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7dd223446f8a1bed867b3129855c805c207ef714bc77959fb18f49622c298f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        '''The Docker repository name ``([<registry>/]<image>)``.'''
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce61caecd628475462cd8b2f997d630e835b4375399caadff660c37070d322af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        '''A Docker image tag applied to the image.'''
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2d0597a159a3258bdd5ff50805a879cb9a016ccd7458e1b28c2aa1429c3c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value)


@jsii.implements(IDockerClientConfig)
class DockerClientConfig(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.DockerClientConfig",
):
    '''Class which represents a docker client configuration.

    After creating an instance of this class you can add new credential helper,
    basic authentication settings or default credential store.
    '''

    def __init__(
        self,
        *,
        config_file_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_file_path: Docker client config path. Default: $HOME/.docker/config.json
        '''
        props = DockerClientConfigProps(config_file_path=config_file_path)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addAuth")
    def add_auth(
        self,
        registry: builtins.str,
        username_env_var: typing.Optional[builtins.str] = None,
        password_env_var: typing.Optional[builtins.str] = None,
    ) -> "DockerClientConfig":
        '''Adds basic authentication ``auths`` setting to the configuration.

        This method acts a little special, because of some security aspects.
        The method, takse three arguments, ``registry``, ``username_env_var`` and ``password_env_var``.
        Arguments ending wit *_env_var, are ment to be available as a ``gcip.Job`` variable.

        :param registry: Name of the container registry to set ``creds_helper`` for.
        :param username_env_var: Name of the environment variable which as the registry username stored.
        :param password_env_var: Name of the environment variable which as the registry password stored.

        :default: REGISTRY_PASSWORD
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a16b4dbc6af5a7a4ba47b59ec2cb53f8fb6ed6b5c3898839e49ed85d425ea61)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument username_env_var", value=username_env_var, expected_type=type_hints["username_env_var"])
            check_type(argname="argument password_env_var", value=password_env_var, expected_type=type_hints["password_env_var"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "addAuth", [registry, username_env_var, password_env_var]))

    @jsii.member(jsii_name="addCredHelper")
    def add_cred_helper(
        self,
        registry: builtins.str,
        cred_helper: builtins.str,
    ) -> "DockerClientConfig":
        '''Adds a Credentials helper ``credHelpers`` for a registry.

        See `docker login#credential-helpers <https://docs.docker.com/engine/reference/commandline/login/#credential-helpers>`_

        :param registry: Name of the container registry to set ``creds_helper`` for.
        :param cred_helper: Name of the credential helper to use together with the ``registry``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfca338a2c1a05056f09278d2f0db7b0ce9db5c5286249628fdd525526c4db40)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument cred_helper", value=cred_helper, expected_type=type_hints["cred_helper"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "addCredHelper", [registry, cred_helper]))

    @jsii.member(jsii_name="addRaw")
    def add_raw(
        self,
        raw_input: typing.Mapping[builtins.str, typing.Any],
    ) -> "DockerClientConfig":
        '''Adds arbitrary settings to configuration.

        Be aware and warned! You can overwrite any predefined settings with this method.
        This method is intendet to be used, if non suitable method is available and you
        have to set a configuration setting.

        :param raw_input: Dictionary of non-available settings to be set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135e6468f74e369fb5865e1eab067d96d6111ef919e2616630228a8d67e6568f)
            check_type(argname="argument raw_input", value=raw_input, expected_type=type_hints["raw_input"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "addRaw", [raw_input]))

    @jsii.member(jsii_name="assignCredsStore")
    def assign_creds_store(self, creds_store: builtins.str) -> "DockerClientConfig":
        '''Sets the ``credsStore`` setting for clients. See `docker login#credentials-store <https://docs.docker.com/engine/reference/commandline/login/#credentials-store>`_.

        Be aware, that if you set the ``credsStore`` and add creds_helper or
        username and password authentication, those authentication methods
        are not used.

        Clients which can authenticate against a registry can handle the credential
        store itself, mostly you do not want to set the ``credsStore``.
        Use ``credsHelpers`` instead.

        :param creds_store: Should be the suffix of the program to use (i.e. everything after docker-credential-). ``osxkeychain``, to use docker-credential-osxkeychain or ``ecr-login``, to use docker-crendential-ecr-login.

        :return: DockerClientConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfa1b99ea08ac61e5f6cae6f49e0cfd6be19103a30962e4a55d362648a7c6ad)
            check_type(argname="argument creds_store", value=creds_store, expected_type=type_hints["creds_store"])
        return typing.cast("DockerClientConfig", jsii.invoke(self, "assignCredsStore", [creds_store]))

    @jsii.member(jsii_name="shellCommand")
    def shell_command(self) -> typing.List[builtins.str]:
        '''Renders the shell command for creating the docker client config.

        The render method uses ``json.dumps()`` to dump the configuration as a json
        string and escapes it for the shell. In Jobs which needed the
        configuration the rendered output should be redirected to the appropriate
        destination e.g. ~/.docker/config.json. This ensures, that environment
        variables are substituted.

        :return:

        Returns a list with ``mkdir -p config_file_path`` and a shell escaped JSON string
        echoed to ``config_file_path``/``config_file_name``
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "shellCommand", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> IDockerClientConfigType:
        '''Docker client configuration.'''
        return typing.cast(IDockerClientConfigType, jsii.get(self, "config"))

    @config.setter
    def config(self, value: IDockerClientConfigType) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956c622101e4f8531772774959f890318bfeac5a399ea3bd389ef92cdbd4fa4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        '''Docker client config path.'''
        return typing.cast(builtins.str, jsii.get(self, "configFilePath"))

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed52c1fe7e09eedf49e79aea025fe55bde8cc4141e6dbcb7aa1eb47b6c5c261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configFilePath", value)


@jsii.implements(IDockerPush)
class DockerPush(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.container.DockerPush",
):
    '''Runs ```docker push`` <https://docs.docker.com/engine/reference/commandline/push/>`_ and optionally ```docker login`` <https://docs.docker.com/engine/reference/commandline/login/>`_ before.

    Example::

       import { Push } from "@gcix/gcix"

       const pushJob = new Push({
                       registry: "index.docker.io/v1/gcix/gcix",
                       image: "gcip",
                       tag: "v0.1.0",
                       userEnvVar: "DOCKER_USER",
                       loginEnvVar: "DOCKER_TOKEN"
                   })

    The ``userEnvVar`` and ``loginEnvVar`` should be created as
    *protected* and *masked* `custom environment variable configured in the UI <https://git.tech.rz.db.de/help/ci/variables/README#create-a-custom-variable-in-the-ui>`_.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: docker
    - stage: deploy
    '''

    def __init__(
        self,
        *,
        container_image: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        login_env_var: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        user_env_var: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_image: The name of the Docker image to push to the ``registry``.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param login_env_var: If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the password or token, here. **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        :param registry: The Docker registry the image should be pushed to. Default: index.docker.io/v1
        :param tag: The Docker image tag that should be pushed to the ``registry``. Default: ``latest``
        :param user_env_var: If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the username value, here. **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        '''
        props = DockerPushProps(
            container_image=container_image,
            job_name=job_name,
            job_stage=job_stage,
            login_env_var=login_env_var,
            registry=registry,
            tag=tag,
            user_env_var=user_env_var,
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
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        '''The name of the Docker image to push to the ``registry``.'''
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9912e5991b7cfe7edef84cbe5388f448461932e968e4162d3226de2a56a674ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value)

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> builtins.str:
        '''The Docker registry the image should be pushed to.'''
        return typing.cast(builtins.str, jsii.get(self, "registry"))

    @registry.setter
    def registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d55b9735ff0a137581ce437613a1e5f0193807936d693eabccb9ac2bd9a08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registry", value)

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        '''The Docker image tag that should be pushed to the ``registry``.'''
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8b75083f7ea3b36776156e76e404773697a7fdef2b0730c40df9558ffdbbf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value)

    @builtins.property
    @jsii.member(jsii_name="loginEnvVar")
    def login_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the password or token, here.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginEnvVar"))

    @login_env_var.setter
    def login_env_var(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4923b13383053a5da73a01b9db70079b084ecdf3700adff7ecbfc855d5eed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="userEnvVar")
    def user_env_var(self) -> typing.Optional[builtins.str]:
        '''If you have to login to the registry before the push, you have to provide the name of the environment variable, which contains the username value, here.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userEnvVar"))

    @user_env_var.setter
    def user_env_var(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14a151f781182bacb686f0db17d4feb44a1601d69ed05a920a7dbcbff3e2a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEnvVar", value)


__all__ = [
    "AWSRegistryProps",
    "BuildContainerCollection",
    "BuildContainerCollectionProps",
    "BuildGitlabContainerCollection",
    "CopyContainerCollection",
    "CopyContainerCollectionProps",
    "CraneCopy",
    "CraneCopyProps",
    "CranePull",
    "CranePullProps",
    "CranePush",
    "CranePushProps",
    "DiveScan",
    "DiveScanProps",
    "DockerBuild",
    "DockerBuildProps",
    "DockerClientConfig",
    "DockerClientConfigProps",
    "DockerPush",
    "DockerPushProps",
    "IBuildContainerCollection",
    "ICopyContainerCollection",
    "ICraneCopy",
    "ICranePull",
    "ICranePush",
    "IDiveScan",
    "IDockerBuild",
    "IDockerClientConfig",
    "IDockerClientConfigType",
    "IDockerPush",
    "IKanikoExecute",
    "ITrivyIgnoreFileCheck",
    "ITrivyScanLocalImage",
    "KanikoExecute",
    "KanikoExecuteProps",
    "PredefinedImages",
    "Registry",
    "TrivyIgnoreFileCheck",
    "TrivyIgnoreFileCheckProps",
    "TrivyScanLocalImage",
    "TrivyScanLocalImageProps",
]

publication.publish()

def _typecheckingstub__70690165055af01ed6463f1d83e17300344a1a45d59ec7b9f16882e9308da882(
    *,
    account_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ff9c385c6297e1a0adfb206009578373904ad51c5a0e329f1a46947138992b(
    *,
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    do_crane_push: typing.Optional[builtins.bool] = None,
    do_dive_scan: typing.Optional[builtins.bool] = None,
    do_trivyignore_check: typing.Optional[builtins.bool] = None,
    do_trivy_scan: typing.Optional[builtins.bool] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    registry: typing.Optional[typing.Union[builtins.str, Registry]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3db202194708972a921f7bd23b4b2751374f8e11c927c45e43ca01e05e57e3(
    *,
    image_name: builtins.str,
    image_tag: builtins.str,
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    do_dive_scan: typing.Optional[builtins.bool] = None,
    do_trivyignore_check: typing.Optional[builtins.bool] = None,
    do_trivy_scan: typing.Optional[builtins.bool] = None,
    dst_registry: typing.Optional[typing.Union[builtins.str, Registry]] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    src_registry: typing.Optional[typing.Union[builtins.str, Registry]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283b893e3831d11cacf41e61a68451d11197db97ea7dbe634f0b7a1c8a4b2556(
    *,
    dst_registry: typing.Union[builtins.str, Registry],
    src_registry: typing.Union[builtins.str, Registry],
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af47f2a968c387561169d8e4411bcf7ea9b8f70b4ae889ba5979fa2cf9b927b(
    *,
    src_registry: typing.Union[builtins.str, Registry],
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    tar_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f279a64e767394ea6f700643ba7fa4e3c39b4660a7236b0921fdbf6d52462b4(
    *,
    dst_registry: typing.Union[builtins.str, Registry],
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    tar_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af56cecc923ccf6759959ff9339129db7a8008203f8a2629f79606ebf173cd8e(
    *,
    highest_user_wasted_percent: typing.Optional[jsii.Number] = None,
    highest_wasted_bytes: typing.Optional[jsii.Number] = None,
    ignore_errors: typing.Optional[builtins.bool] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_path: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    lowest_efficiency: typing.Optional[jsii.Number] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6a99ea530ccaf32750baa4c78f8f420c32d204f1eb43121e53d4baa06a37a7(
    *,
    repository: builtins.str,
    context: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206d2b583e918e93a1ff212d6af4cd76afeb3ac91bd0bf5e2193df801f76b70d(
    *,
    config_file_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607c48baa8d826d3aaedac3a174f21f61ae4e3e0b0a832478a9aab984f42de22(
    *,
    container_image: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    login_env_var: typing.Optional[builtins.str] = None,
    registry: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    user_env_var: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0116523456ff706c1377a152fde5fe35683cdffa8ccac7b83af0ed04168db58e(
    value: CranePush,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fb2d88304bf5cc561b1ab15b81b9add0917cd2f367d5d0ffd6ac3a708f6f2d(
    value: DiveScan,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746261fcfe25d21c1421f3c65f118ded186f03ab7b94d8df37f5d9ac75554b06(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da94f33e04ac9bc8665968417f85fd7e09ed24f5571b9390407aae9d1c11a334(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427629879567738d70e65ab56ac3776a98e6af570e9fa519271b1fc019064927(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9357a747b76ebaa830adf801712ece723718e77dc329ce0830354923de5e6844(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d3b984aeda16e11797c209a33b2c0d2e2aa060fcfe72baf2e5c74192e21c77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36058c9f7ee07328c959e1627cd79ceac781ae81f7b3ae49b8e9bbb9c707ec35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7daa0536f8f39a3f3d41f62cbf3ed6443b03b9bcd7422f85836df6cc8cc06fa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948de3d6f36852424a280596b72941071f34bac514d195427d22d709e98ff45e(
    value: KanikoExecute,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef285394371971c730d00b57a4fa74506459cf73a548d80099e21b461faf8ac(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a604e69d9a3619b65703566a521f561cd7378490a5e61a74f94790ee7d27393d(
    value: TrivyIgnoreFileCheck,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aea3c85b9f24b12424e7e389c2071b59bf07bfc76ca3c60ed970d2cf6a8d8e3(
    value: TrivyScanLocalImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f70d3fad8673833b2c8fed070cb2921a7493bf0d4bb0adb56df39cfeb43784(
    value: CranePull,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4283bacb47bb921dcfdb531bab8ce5cc5b89580936030ebd193145094339345c(
    value: CranePush,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee8d038b73c3aaa63ba95c493db064287e1663d01cf8681d501f46dd20cce1c(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b392df5662373fd9c18ce8bfb3821a721ad141e60545a66cb7a7ab7ff1ff7c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2687c0184c9a9b888ce969ed872eb2bb6185df142b016b04a2778b755d2fa951(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad564cc88fd5c116ad6269a596679f594a0fddc450165c9effe162a97620b82e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292f9682734eb6bc8f1fe0e28bfd2473c4dbf27b42a3297be6a91b5e59e56e8e(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2177b7c9a8f60ea34287f1db828576bc2c110f869fb1ca123cab951c945373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e4b69135ef78283b8302414edf06c7ea0228c0453a9cb92a22c36d27b36fcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ee07f847778f249471fed60cb36083c0ace9ba27419870e2c74b2d0a149844(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4c012c9759ba283e975a61aeb8b2fe10705104aaa8441498be8ddbe28fa00d(
    value: typing.Optional[DiveScan],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3934c339c5eb70b4b32dc76ce257b78827bcc3d98cbd495bb27b778a33bf482e(
    value: typing.Optional[TrivyIgnoreFileCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec493b51d2332c76141026bb84f26885492bf54dd685fee6f5897261cfa0f1a(
    value: typing.Optional[TrivyScanLocalImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca99b3afd8175b7d4f020c4c9e008e634a6bf8ee72b9349f778e54a8100523a5(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dd0fd5c0a2473ae269ae3cbacd9ed5a8efef8426c98b32c6336a169029edf0(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572a8f78cc2839ffe9780649d73c01c2c2eeaedbebde024e455caea88ec08560(
    value: typing.Optional[DockerClientConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b26b506fdcc8eaa9939599dd8489a2249519cb16cc776239041a52106891cc(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bed8506136c090c0a09432835eef1925ccb69f3d751dffb59027f5366e32d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce4f64fff958d19283260f72458ea249140b49ba9e1e05a0e7cfe370cb34970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5baeec5ec1b0e913e04e73cc573a5be67b6200667837d053dc99c81f8136f8bb(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dae25943a7ff0eebcd64fbee4b63d00d9ab3a05fc8dfd0368df7dc5c1c61f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ec746d6937d9d03d7509b01e47b2584cf0ada28b0820ce9d91dff6652f83e2(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427ddd0e70a8eae02188adb4ddaefd1934bf84dacc91f364a9ac0ff3b603db37(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d134ee48b532e485915f3ee98f970d1363ce9cb16e110f85033b752fe51e001e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853d7fe77aaa83cac92bdda53480c907e1f13eb8e7fb19f4219d21e175d5faa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2e53be5f9d444680eea46c38ae9a84c2ea75ecc5f0917f19a459210b7d2f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe71cb94e2e06adab49f829f2ebfdbea30b54bf73742ece0aded57e3b47f4121(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81db5595c647596525c7ee87df16f1a9f3e201fe62d545ab09354b1658ca7794(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad28a33ef8749b49df20b2504a2caf1791478806d44864e45f63b7613c0ae87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde47e48e379e35ebb11187e5bddde8752550725efd4e56c78a39234e3fa8340(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd27df3a863d7d63829bfe23a67ede3f1b30fe48682433e92cf585833ee9bb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be88fcd6aff5e5b4d57e11d1636301dd72fe2a84d3f18f1b405a131cc2321849(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e1c3f3ab655b91291ea50630f1e7f412162f94756023c5596cdbc349155585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd759d2dcce813e15442e74e2118677cf9eec201f2b3c60db19d44e56e4092cc(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d88bc47be0b26a05c11e5a808fbc99281da1b2fc3013c8b9796a6f097526f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203470e55e08328fb006328448b04c1b19c7764bcda6c071c1251dc39def4997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcf03ccb02d5412b838d7587b6db059f9f57c60f993cad32fb6745bf72cafe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e083816c6ae221d335e5ff8ce0e91aa7f1e31492a64baf65024fe45cd17037fd(
    value: IDockerClientConfigType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7a975cf87bb5d079e0e97120574ec688b6767aedfbaacb31d43ca74d1e4788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c06e68bf27701f47e2c6385823c047b7c48641502ed2b70c2e6cb00bf4ff745(
    value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbecbff16e0ecee4e2f306a4eaf894e4c91614f6ff695a7a129b9ea08b16ed3(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82864bc1bc4d58efa2a54428508f6ebc1c52cfd22adf629cbd02e1c714987e18(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f757d69a2d460924dab774a4f874fe7a6bcc483a62e890ea65eaa6e060088dfe(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634532a050c76b1a285c937d782cef38a6eedbd04d15c9d69780dff08a87973e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fae0979d9292c572e6ef2b3250f490948b0b92cc67fa9f0a91accafa7b7f155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460f6268d66f75afd35020e7abb6634e22eaeb10c18535885522c7fde478d5e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbe3f1fa312eaf653de6f0d6b7ee92868a4b1de025a151375ec50875a47de25(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9cc3a57a43fe3c80a7424fa92d0662b8af3d87c372e6993fdd57cba98e24a5b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960f544c37478e03e6c13e2105577d33d5c657009865df4102475d57639ac5cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f4dbd81fe06b79b591fe9cf35b8d320de110a35d4abf8ee7a04085c6a8ab93(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0204504365c6c1fdf207e611880f54b89fbfcd7cee0d7ed59d09fefe9c763259(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e49220b641e8d014fcb4f82e4acdfa83e37bf1025c611b88b6ec478e4b4694b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835bc659f95de56020a6aabda657d6184bfb6e4ef0d54ba1dcaf03aeec0c4d49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9537120dfd5a81dd138c75109bedfc46b2c4d0625afe620e09a3d25f899168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff39590d779bee9ef114aac8a3286ad1701b76c3ae4bf15fe7d65f9f887ed19b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10c717f02fa8d39199986400366b6397188bf90d0c4478b4c67ce222512a7de(
    value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7775e186dbb617d4940a35b327f0e7d0139ef0cfe8786740c5aa6b17e3bb4a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a997093041cfd9d7d6400b88e572ecb673325c07ac8d667e0651e3db78818118(
    value: typing.Optional[typing.Union[typing.List[builtins.str], typing.List[Registry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad9231cd7938be92768dfb0b13a59083fa4bd15f2326d1f5837eed5df5736ab(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9b14b6da43ef0a63a4e33d17019ecb0cb5094821bc439b5b645f611fc7dd0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3c03cbdfd88f243b2a021cfea7bae2aec22d673a96bee2b3ee4a572e8233d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c264b4fd7f342e70577e3bd1ab7176dfd66fa96178f8fd734cad331b949418(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a720a7b8311dda5bbd35347a36418e7f3d677c9efffc9a7f6fde5665861f93f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49dca41c09e4104d51824907b4d0a0f8b37b33fd721e724ecbf5794d0fcb6509(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a287bb09ff02b901fe6f9e3f5c2ca8283fa5bfbb1708d08e967397deb02cfd60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdfa2df4221b9e73051d6df9dc7faa117504c6f0bedcb3e38b01bac7420a64d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be88e0b5945f5ff3ccc1f91e16defded980aedafa87ccfe7e6b19858787586d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75525ed276b934a24dfcee6d0abba57de42d5e160c092c4cfff7df3ef90f4f48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7990b578c250d41dce4ab20a226a12f9d45cecf909467c75ee46c4b89122b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65dfbf74ad05f2261adfd845689fcaab7fde4974223a697ad48653f6406ebf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9764c5c99a60e2b94882581dbb58e909133d3e658a672d57dc5b4a693a82c685(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d642c8384f282964aa63d3e05faa23df50ae48c028f601b497a63336e211bfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13f68f262149a1e20f5b9466e051e439f36ed22b8a7c10ef7a6c45c8ebfd9ba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e423cc24374e30697505b9794984faa425c7e2e4e61270ada43c5b35d633c603(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0efb9c3ae7881742c6b8e4f525d9c290b6ac74ba69322645f9859a8256b795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d951aba997bdde6677b256cac5c2605ea0f56ecd520a54110a59cdc1415096(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7f6efc6a9b488baa9919952461cefe3522ec89661a2a59e001eecf759b9e1c(
    value: typing.Optional[typing.Mapping[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a1f91eaa5e923d8c937825ba8538a1b298236f81e36c6c7b1f694b62a0ab78(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63a3207114011d319800e8a8450d28abfcb485b8ca87f88369b295e36012f18(
    value: typing.Optional[typing.Union[typing.List[builtins.str], typing.List[Registry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a7d1cb7b08aca5e734ae386a2ad2d5dc9483e9d629e50913f2ee5798314e62(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2495b5e88ddaa0512109b982431d7841daef797033c03c01af360aac76d62fbf(
    *,
    build_args: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    build_target: typing.Optional[builtins.str] = None,
    context: typing.Optional[builtins.str] = None,
    docker_client_config: typing.Optional[DockerClientConfig] = None,
    dockerfile: typing.Optional[builtins.str] = None,
    enable_push: typing.Optional[builtins.bool] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    registries: typing.Optional[typing.Union[typing.Sequence[builtins.str], typing.Sequence[Registry]]] = None,
    tar_path: typing.Optional[builtins.str] = None,
    verbosity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2391e9fdda74757a01c75df1e8d9ae6b9f644b8b8e4223cd2dbcad6a1a9b32a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac108d7e6f4ffbd2bf8d4f7f494d032718e1af6cd51a15b5c8eb075fde4dda23(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    trivyignore_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e101f33839bc4fb0ae0fec94ae271a7489431391d0ed499559772b55838ef03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae26370b5edf10ea29fa9027e615ceabe36b3abc8a24c17635e901eb67c298b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aab1e201cbc866a99843185b3e01d2e3e7786903e0a6e93262618f0fe87784d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9771ae954b212495dc580964dbc93f312fc145fe5d07db1f6ed15c4b75d71c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c758bd9cf3aadf62ed365904bc5137bb64d48be2dc6676efad9350366d315def(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f521d09fb95c2c9a00b8aa644706b1543e537ddade19b740202100e97a473b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dcf05aff049477f8d44f169f6558561d67c50ab9f0143f3c670f273a9926d91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51f6e7d50ce8feb0288a91a7fb2d67560d4e8f8f7e79b334c7ab0c663fe0b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c555dd23c3fde2604d322813b03b387ae9ae51392342b82e47f0ae4e94fc07f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f200764796df1b9fe91b8b4a8ee168d4d8529391b2df7073a2026c74a6e5af9d(
    *,
    debug: typing.Optional[builtins.bool] = None,
    exit_if_vulnerable: typing.Optional[builtins.bool] = None,
    image_name: typing.Optional[builtins.str] = None,
    image_path: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    output_format: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
    trivy_config: typing.Optional[builtins.str] = None,
    vulnerability_types: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888eec956f281f618d8ffd959134518ea8f309867e78dd804ec16fab3c8df7c4(
    value: CranePush,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6404340127e815431a1d0d8296a99cce47e0b506d0b0aa26f75b378e84e25b2(
    value: DiveScan,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96dbbd08ea310657684ba0791f1ea24f5a6cbbfe9520c5bd67b9108b4e82304(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d92e7c6562f0d2aefd66dd0fc3d421d91bd76838eefd22a1323f65d06e865ff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f66366dcad131b08e1a18db166da11b846e104fdc9d0e7ca28bd4efbb86d188(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7151a6e56dca5f037236fe6e9e3711b8cc7a78f44c9ade48077b6b0f714ffb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00c06589c0157c19232ea1c1d063eff5355db3077e2295200c8e17ca5f35081(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4913c762c8fe6cfa9daaea47e73ff22f08e7f1c9a8a4892734ebd03efa87630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e60fb8a421e27f3024da332ca1799416f057c17744fe40dbdef1f2c67f7c35e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2922369fb367be38dba77bd09f32f3ca31226c1f0ffe59bb8035ab2b095c1c85(
    value: KanikoExecute,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fde6aeeb273678c9d3d4d9df2d0a4803531986ac8bca58b504663bd5b1aa97e(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a6038b17e0b2bd969d867a443dea17e29b89352e2fb1575e29494455e52ebc(
    value: TrivyIgnoreFileCheck,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b292ca715a4c414a39b03b17baacf023dccd452ebb7ae378b91b637b896105(
    value: TrivyScanLocalImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc64a201767458b70da09d48d00f2d51c93ae8bdc860e62c913f8daa9929699(
    value: CranePull,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fce608add90049af352328b3004b52675ccaf523a1caded85630603d1079ee(
    value: CranePush,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef05e812b15f5cead6f9a6d7641bdec5076f2a2ec000e1580fee6ae2219cf72(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a74e44774373fc2a574495e05a09af481a5f04e6f25929d5cc85cf9966738e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e0ea527e36d5f07a4aee8d21f6b098dab3c0a90a2f5c336a815ea233fd0bad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e924e58f07211f8686fa15bfec64e9d8a12427d23174c31e91e602a5607a0ee9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a3239a551f7f0703d9aab14c886cb157af9b03977c6b5fe98e66f5a9a7b5be(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeac6577989dfdc99efd5e906fe59dabdfcbbb30b46df3a6f4d800ca9bf4e2a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaed0b8f4aac0fb320bc7fb8fb796cb3625bf0b54d4bf18e18161b4707e4b1e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024d89a78a509a20b217d9df674764a58481361f4379657687b8e5470c0562c7(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84440b4fdd289d6ca9352a972a14b65917c4d1e9e96df75ba1230589d37f2366(
    value: typing.Optional[DiveScan],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acaac19a024798d356530addcfb675d00e7718fa15592b52a0bd3d18d5c5b0f5(
    value: typing.Optional[TrivyIgnoreFileCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1036f13aa2d377d6ce01902136e04ccdee48bbd061144df33038fd886a738b(
    value: typing.Optional[TrivyScanLocalImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f253d7757bc4254083e30859b29145202b6682b597a7317be2303f85edaed0b(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c4b4b3430b6882f7fce62f48611ac8b4160a793c02c7e2d390d91f5342c8ea(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853cf50eb2cf5284e5f43ff03be1857f10d0f46c3e97c0dbfa69004467ccd865(
    value: typing.Optional[DockerClientConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f05f9ede43dbf97af83473670a3028d41eb17c74c0a35998790dfcbcf7779f(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c04f6d7e0856ea05e199b824d1fef5e77743333145a563615df3b6e24e38a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc52d1cbcbb774ca91c8fe7b76204e751812162fa4f52451e91b4a7dd2c00219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92b854c26778a2e53e5fd7d02e43103e86f5c58f3a4965d756f1c1db56dc9c1(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710f217da8e365150a4d44b7525ded0d915488f00e3eba17d7d4aaf3bc2ca7dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b240e50c52eeff890833592e36cd4323ce92803e128ca9f1d211521ad7823a(
    value: DockerClientConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e69659a083b47f4fcb86bc9dba5e55c5feff7c5a98afba50b0345f9250655ba(
    value: typing.Union[builtins.str, Registry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964f4192a0d90ea2897d6b0177a51f2e018be9de3f7838e0eeae353375d3b6fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe70150d68a7adbc49d4b4cef8662ee7abe851bc67419fbbe29f96728a645c70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72be2fe328749fcc98e785a7c9bd4a8947866df926aeca145e7ac0d5c4e374b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00feadced743630d8fff9e0c98a5aa109a170f97e0798c875aee4ba3138e5d3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2101e114e5cb63051f57e91cd6b02ae1803c957432f222515e1291bf93699e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc74e395f342425d17a81a5aa0b965fa5cff57253448e9f008c16d64bffeacf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2d9f92ed7ed2479318fd3de66586a822f474479721e44c9dcb83573a6520ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6382aba1f79203bc03e3e7469cb71fda2ad0ba7a71dc2d4ada1f3b95efadd3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67dfbfb7975e89718235bb870ef7c02c5757d22d2a1599c9432ad7cfdd3bf64a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c5856866591955ea5a6bceb75c2ac2cbff9be938475dd0c6f00861d3d4f974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9e7f9db878dcbed1cf0192862548a658efdec7bba7166accfc20e0ace60e2a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7dd223446f8a1bed867b3129855c805c207ef714bc77959fb18f49622c298f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce61caecd628475462cd8b2f997d630e835b4375399caadff660c37070d322af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2d0597a159a3258bdd5ff50805a879cb9a016ccd7458e1b28c2aa1429c3c11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a16b4dbc6af5a7a4ba47b59ec2cb53f8fb6ed6b5c3898839e49ed85d425ea61(
    registry: builtins.str,
    username_env_var: typing.Optional[builtins.str] = None,
    password_env_var: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfca338a2c1a05056f09278d2f0db7b0ce9db5c5286249628fdd525526c4db40(
    registry: builtins.str,
    cred_helper: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135e6468f74e369fb5865e1eab067d96d6111ef919e2616630228a8d67e6568f(
    raw_input: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfa1b99ea08ac61e5f6cae6f49e0cfd6be19103a30962e4a55d362648a7c6ad(
    creds_store: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956c622101e4f8531772774959f890318bfeac5a399ea3bd389ef92cdbd4fa4c(
    value: IDockerClientConfigType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed52c1fe7e09eedf49e79aea025fe55bde8cc4141e6dbcb7aa1eb47b6c5c261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9912e5991b7cfe7edef84cbe5388f448461932e968e4162d3226de2a56a674ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d55b9735ff0a137581ce437613a1e5f0193807936d693eabccb9ac2bd9a08d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8b75083f7ea3b36776156e76e404773697a7fdef2b0730c40df9558ffdbbf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4923b13383053a5da73a01b9db70079b084ecdf3700adff7ecbfc855d5eed0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14a151f781182bacb686f0db17d4feb44a1601d69ed05a920a7dbcbff3e2a4a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
