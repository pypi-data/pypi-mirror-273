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


class GitlabScripts(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.gitlab.GitlabScripts",
):
    '''GitlabScripts Class Documentation.

    The ``GitlabScripts`` class provides utility methods for performing various Git-related actions in the context of GitLab.
    '''

    @jsii.member(jsii_name="cloneRepository")
    @builtins.classmethod
    def clone_repository(
        cls,
        path: builtins.str,
        branch: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Clones a repository from a remote Git server using the Git command.

        :param path: - The path of the repository to clone. Should start with a forward slash ("/").
        :param branch: - (Optional) The branch name to clone from the remote repository. Currently, only "main" is supported.

        :return: A Git clone command as a string with the provided branch and repository path.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd5b76126699d26330d7dfeb3122212a724ea05dd5a006bbd12e60b24819200)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "cloneRepository", [path, branch]))


@jsii.interface(jsii_type="@gcix/gcix.gitlab.IPagesAsciiDoctor")
class IPagesAsciiDoctor(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="outFile")
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        ...

    @out_file.setter
    def out_file(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        ...

    @source.setter
    def source(self, value: builtins.str) -> None:
        ...


class _IPagesAsciiDoctorProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.gitlab.IPagesAsciiDoctor"

    @builtins.property
    @jsii.member(jsii_name="outFile")
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        return typing.cast(builtins.str, jsii.get(self, "outFile"))

    @out_file.setter
    def out_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd96129bc7b3ec7f5fc2b940829e9c4525d97ed64c6ca6556ea8b654fc40adfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outFile", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa927abf8a1764801389a1d4bd5ceda060dc48e44bd8f849427f25a3ac33cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPagesAsciiDoctor).__jsii_proxy_class__ = lambda : _IPagesAsciiDoctorProxy


@jsii.implements(IPagesAsciiDoctor)
class PagesAsciiDoctor(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.gitlab.PagesAsciiDoctor",
):
    '''Translate the AsciiDoc source FILE as Gitlab Pages HTML5 file.

    Runs ``asciidoctor {source} -o public{out_file}``and stores the output
    as artifact under the ``public`` directory.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: asciidoctor-pages
    - stage: build
    - image: ruby:3-alpine
    - artifacts: Path 'public'
    '''

    def __init__(
        self,
        *,
        out_file: builtins.str,
        source: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param out_file: Output HTML file.
        :param source: Source .adoc files to translate to HTML files.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        props = PagesAsciiDoctorProps(
            out_file=out_file, source=source, job_name=job_name, job_stage=job_stage
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
    @jsii.member(jsii_name="outFile")
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        return typing.cast(builtins.str, jsii.get(self, "outFile"))

    @out_file.setter
    def out_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d1861ba62c52ef1ac9c3754a95089b61216ff321934e5ba1b2bc9104bdf509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outFile", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ff6c14a34079cce033a8c3100ab964fdb9ef73fc55907e821517e61c45e512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.gitlab.PagesAsciiDoctorProps",
    jsii_struct_bases=[],
    name_mapping={
        "out_file": "outFile",
        "source": "source",
        "job_name": "jobName",
        "job_stage": "jobStage",
    },
)
class PagesAsciiDoctorProps:
    def __init__(
        self,
        *,
        out_file: builtins.str,
        source: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param out_file: Output HTML file.
        :param source: Source .adoc files to translate to HTML files.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785bd136cb09e7394e3fa254707c0bc4b01b6bf4298c7ac058f2e52f44acf94c)
            check_type(argname="argument out_file", value=out_file, expected_type=type_hints["out_file"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "out_file": out_file,
            "source": source,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

    @builtins.property
    def out_file(self) -> builtins.str:
        '''Output HTML file.'''
        result = self._values.get("out_file")
        assert result is not None, "Required property 'out_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Source .adoc files to translate to HTML files.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job.'''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        '''The stage of the job.'''
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesAsciiDoctorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GitlabScripts",
    "IPagesAsciiDoctor",
    "PagesAsciiDoctor",
    "PagesAsciiDoctorProps",
]

publication.publish()

def _typecheckingstub__2bd5b76126699d26330d7dfeb3122212a724ea05dd5a006bbd12e60b24819200(
    path: builtins.str,
    branch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd96129bc7b3ec7f5fc2b940829e9c4525d97ed64c6ca6556ea8b654fc40adfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa927abf8a1764801389a1d4bd5ceda060dc48e44bd8f849427f25a3ac33cd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d1861ba62c52ef1ac9c3754a95089b61216ff321934e5ba1b2bc9104bdf509(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ff6c14a34079cce033a8c3100ab964fdb9ef73fc55907e821517e61c45e512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785bd136cb09e7394e3fa254707c0bc4b01b6bf4298c7ac058f2e52f44acf94c(
    *,
    out_file: builtins.str,
    source: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
