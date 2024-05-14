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

from .. import Job as _Job_20682b42


@jsii.data_type(
    jsii_type="@gcix/gcix.git.GitMirrorProps",
    jsii_struct_bases=[],
    name_mapping={
        "remote_repository": "remoteRepository",
        "git_config_user_email": "gitConfigUserEmail",
        "git_config_user_name": "gitConfigUserName",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "private_key_variable": "privateKeyVariable",
        "run_only_for_repository_url": "runOnlyForRepositoryUrl",
        "script_hook": "scriptHook",
    },
)
class GitMirrorProps:
    def __init__(
        self,
        *,
        remote_repository: builtins.str,
        git_config_user_email: typing.Optional[builtins.str] = None,
        git_config_user_name: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        private_key_variable: typing.Optional[builtins.str] = None,
        run_only_for_repository_url: typing.Optional[builtins.str] = None,
        script_hook: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param remote_repository: The git repository the code of the pipelines repository should be mirrored to.
        :param git_config_user_email: The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.
        :param git_config_user_name: The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param private_key_variable: DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.
        :param run_only_for_repository_url: When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again. With this variable the job only runs, when its value matches the CI_REPOSITORY_URL of the current repository.
        :param script_hook: This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote. This hook is mostly meant to be for git configuration commands, required to push to the remote repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c77a41e1617691bf259b90c9f123b22689eaf9d80a501ff2c84d6fd4a37c77)
            check_type(argname="argument remote_repository", value=remote_repository, expected_type=type_hints["remote_repository"])
            check_type(argname="argument git_config_user_email", value=git_config_user_email, expected_type=type_hints["git_config_user_email"])
            check_type(argname="argument git_config_user_name", value=git_config_user_name, expected_type=type_hints["git_config_user_name"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument private_key_variable", value=private_key_variable, expected_type=type_hints["private_key_variable"])
            check_type(argname="argument run_only_for_repository_url", value=run_only_for_repository_url, expected_type=type_hints["run_only_for_repository_url"])
            check_type(argname="argument script_hook", value=script_hook, expected_type=type_hints["script_hook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_repository": remote_repository,
        }
        if git_config_user_email is not None:
            self._values["git_config_user_email"] = git_config_user_email
        if git_config_user_name is not None:
            self._values["git_config_user_name"] = git_config_user_name
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if private_key_variable is not None:
            self._values["private_key_variable"] = private_key_variable
        if run_only_for_repository_url is not None:
            self._values["run_only_for_repository_url"] = run_only_for_repository_url
        if script_hook is not None:
            self._values["script_hook"] = script_hook

    @builtins.property
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        result = self._values.get("remote_repository")
        assert result is not None, "Required property 'remote_repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_config_user_email(self) -> typing.Optional[builtins.str]:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        result = self._values.get("git_config_user_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_config_user_name(self) -> typing.Optional[builtins.str]:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        result = self._values.get("git_config_user_name")
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
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        result = self._values.get("private_key_variable")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        result = self._values.get("run_only_for_repository_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_hook(self) -> typing.Optional[typing.List[builtins.str]]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        result = self._values.get("script_hook")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitMirrorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@gcix/gcix.git.IGitMirror")
class IGitMirror(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="gitConfigUserEmail")
    def git_config_user_email(self) -> builtins.str:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        ...

    @git_config_user_email.setter
    def git_config_user_email(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserName")
    def git_config_user_name(self) -> builtins.str:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        ...

    @git_config_user_name.setter
    def git_config_user_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="remoteRepository")
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        ...

    @remote_repository.setter
    def remote_repository(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="scriptHook")
    def script_hook(self) -> typing.List[builtins.str]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        ...

    @script_hook.setter
    def script_hook(self, value: typing.List[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="privateKeyVariable")
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        ...

    @private_key_variable.setter
    def private_key_variable(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="runOnlyForRepositoryUrl")
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        ...

    @run_only_for_repository_url.setter
    def run_only_for_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IGitMirrorProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.git.IGitMirror"

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserEmail")
    def git_config_user_email(self) -> builtins.str:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserEmail"))

    @git_config_user_email.setter
    def git_config_user_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9701fc33a1783754f17b3d0fb4109dade1dadaa97835f19d36a35ebfd889ac17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserEmail", value)

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserName")
    def git_config_user_name(self) -> builtins.str:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserName"))

    @git_config_user_name.setter
    def git_config_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91937795e6200f6c6e3aa9092797313316e78cdee0a5673e6d3302a88cfba20c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserName", value)

    @builtins.property
    @jsii.member(jsii_name="remoteRepository")
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        return typing.cast(builtins.str, jsii.get(self, "remoteRepository"))

    @remote_repository.setter
    def remote_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b732dce8b7cedf5e1e92c3324b5721376d8ec89525c6702821c44096eda49788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteRepository", value)

    @builtins.property
    @jsii.member(jsii_name="scriptHook")
    def script_hook(self) -> typing.List[builtins.str]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scriptHook"))

    @script_hook.setter
    def script_hook(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9624ea25bb887b67d9a982fff580b05d68edff140705193a7cf95781d9e16294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptHook", value)

    @builtins.property
    @jsii.member(jsii_name="privateKeyVariable")
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyVariable"))

    @private_key_variable.setter
    def private_key_variable(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4243c1bc77532e6e998f1ae5266bf69a3868c6aeb23d821b568ec9b0be44d386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyVariable", value)

    @builtins.property
    @jsii.member(jsii_name="runOnlyForRepositoryUrl")
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runOnlyForRepositoryUrl"))

    @run_only_for_repository_url.setter
    def run_only_for_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045ecf3349c29865c8df481f35e34dbdcea71b2c459a24fc73b8cada29b12505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runOnlyForRepositoryUrl", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGitMirror).__jsii_proxy_class__ = lambda : _IGitMirrorProxy


@jsii.implements(IGitMirror)
class GitMirror(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.git.GitMirror",
):
    '''This job clones the CI_COMMIT_REF_NAME of the current repository and forcefully pushes this REF to the ``remote_repository``.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: git-mirror
    - stage: deploy
    - image: PredefinedImages.ALPINE_GIT
    '''

    def __init__(
        self,
        *,
        remote_repository: builtins.str,
        git_config_user_email: typing.Optional[builtins.str] = None,
        git_config_user_name: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        private_key_variable: typing.Optional[builtins.str] = None,
        run_only_for_repository_url: typing.Optional[builtins.str] = None,
        script_hook: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param remote_repository: The git repository the code of the pipelines repository should be mirrored to.
        :param git_config_user_email: The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.
        :param git_config_user_name: The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param private_key_variable: DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.
        :param run_only_for_repository_url: When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again. With this variable the job only runs, when its value matches the CI_REPOSITORY_URL of the current repository.
        :param script_hook: This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote. This hook is mostly meant to be for git configuration commands, required to push to the remote repository.
        '''
        props = GitMirrorProps(
            remote_repository=remote_repository,
            git_config_user_email=git_config_user_email,
            git_config_user_name=git_config_user_name,
            job_name=job_name,
            job_stage=job_stage,
            private_key_variable=private_key_variable,
            run_only_for_repository_url=run_only_for_repository_url,
            script_hook=script_hook,
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
    @jsii.member(jsii_name="gitConfigUserEmail")
    def git_config_user_email(self) -> builtins.str:
        '''The 'user.email' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_EMAIL.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserEmail"))

    @git_config_user_email.setter
    def git_config_user_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6a2dfa91cc4a041bc062497b62a459d9fd533d878ce42e141181715d1c1897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserEmail", value)

    @builtins.property
    @jsii.member(jsii_name="gitConfigUserName")
    def git_config_user_name(self) -> builtins.str:
        '''The 'user.name' with which the commits to the remote repository should be made. Defaults to GITLAB_USER_NAME.'''
        return typing.cast(builtins.str, jsii.get(self, "gitConfigUserName"))

    @git_config_user_name.setter
    def git_config_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1616ac938ff85b3af6f252facf5356fceff39b7c6924de2bac0c3b47dd62fa5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitConfigUserName", value)

    @builtins.property
    @jsii.member(jsii_name="remoteRepository")
    def remote_repository(self) -> builtins.str:
        '''The git repository the code of the pipelines repository should be mirrored to.'''
        return typing.cast(builtins.str, jsii.get(self, "remoteRepository"))

    @remote_repository.setter
    def remote_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5988cc3c07a7a077e3d9ee7419a390eedb6f9a72d955838292bdc4514bf6ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteRepository", value)

    @builtins.property
    @jsii.member(jsii_name="scriptHook")
    def script_hook(self) -> typing.List[builtins.str]:
        '''This list of strings could contain any commands that should be executed between pulling the current repository and pushing it to the remote.

        This hook is mostly meant to be for git configuration commands,
        required to push to the remote repository.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scriptHook"))

    @script_hook.setter
    def script_hook(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8572ceb0f1804fe555e4be9bd114f6e319ad09cc5d3dda31d221cc31a66b605b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptHook", value)

    @builtins.property
    @jsii.member(jsii_name="privateKeyVariable")
    def private_key_variable(self) -> typing.Optional[builtins.str]:
        '''DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes the name of the Gitlab environment variable, which contains the private ssh key used to push to the remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings of your project.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyVariable"))

    @private_key_variable.setter
    def private_key_variable(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2cddea3ae0cccf99b0e8e47b6e654d829b715b4825456c613822df869b5814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyVariable", value)

    @builtins.property
    @jsii.member(jsii_name="runOnlyForRepositoryUrl")
    def run_only_for_repository_url(self) -> typing.Optional[builtins.str]:
        '''When mirroring to a remote Gitlab instance, you don't want to run this mirroring job there again.

        With this variable the job only runs, when its
        value matches the CI_REPOSITORY_URL of the current repository.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runOnlyForRepositoryUrl"))

    @run_only_for_repository_url.setter
    def run_only_for_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebbfcbe4557c1dfced9a3f74ffec98bf9a188f2ea57cee1e2eb632c2fde9fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runOnlyForRepositoryUrl", value)


__all__ = [
    "GitMirror",
    "GitMirrorProps",
    "IGitMirror",
]

publication.publish()

def _typecheckingstub__f5c77a41e1617691bf259b90c9f123b22689eaf9d80a501ff2c84d6fd4a37c77(
    *,
    remote_repository: builtins.str,
    git_config_user_email: typing.Optional[builtins.str] = None,
    git_config_user_name: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    private_key_variable: typing.Optional[builtins.str] = None,
    run_only_for_repository_url: typing.Optional[builtins.str] = None,
    script_hook: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9701fc33a1783754f17b3d0fb4109dade1dadaa97835f19d36a35ebfd889ac17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91937795e6200f6c6e3aa9092797313316e78cdee0a5673e6d3302a88cfba20c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b732dce8b7cedf5e1e92c3324b5721376d8ec89525c6702821c44096eda49788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9624ea25bb887b67d9a982fff580b05d68edff140705193a7cf95781d9e16294(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4243c1bc77532e6e998f1ae5266bf69a3868c6aeb23d821b568ec9b0be44d386(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045ecf3349c29865c8df481f35e34dbdcea71b2c459a24fc73b8cada29b12505(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6a2dfa91cc4a041bc062497b62a459d9fd533d878ce42e141181715d1c1897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1616ac938ff85b3af6f252facf5356fceff39b7c6924de2bac0c3b47dd62fa5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5988cc3c07a7a077e3d9ee7419a390eedb6f9a72d955838292bdc4514bf6ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8572ceb0f1804fe555e4be9bd114f6e319ad09cc5d3dda31d221cc31a66b605b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2cddea3ae0cccf99b0e8e47b6e654d829b715b4825456c613822df869b5814(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebbfcbe4557c1dfced9a3f74ffec98bf9a188f2ea57cee1e2eb632c2fde9fa3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
