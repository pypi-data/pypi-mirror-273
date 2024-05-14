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


@jsii.interface(jsii_type="@gcix/gcix.python.IPagesPdoc3")
class IPagesPdoc3(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        ...

    @module.setter
    def module(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(self) -> builtins.str:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        ...

    @output_path.setter
    def output_path(self, value: builtins.str) -> None:
        ...


class _IPagesPdoc3Proxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPagesPdoc3"

    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        return typing.cast(builtins.str, jsii.get(self, "module"))

    @module.setter
    def module(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140d454e9594d840e53743eb2b20130db9bb7ec52f62f97bbe46e14b9f204a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "module", value)

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(self) -> builtins.str:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputPath"))

    @output_path.setter
    def output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8c65cef894cbe4a5cc2330b3f4cd77e69fc7ea7d99d31ac9db843f30bf42ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputPath", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPagesPdoc3).__jsii_proxy_class__ = lambda : _IPagesPdoc3Proxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPagesSphinx")
class IPagesSphinx(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="pip")
    def pip(self) -> typing.Optional["PipInstallRequirementsProps"]:
        ...

    @pip.setter
    def pip(self, value: typing.Optional["PipInstallRequirementsProps"]) -> None:
        ...


class _IPagesSphinxProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPagesSphinx"

    @builtins.property
    @jsii.member(jsii_name="pip")
    def pip(self) -> typing.Optional["PipInstallRequirementsProps"]:
        return typing.cast(typing.Optional["PipInstallRequirementsProps"], jsii.get(self, "pip"))

    @pip.setter
    def pip(self, value: typing.Optional["PipInstallRequirementsProps"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354586cef6fc67c1f9a319458092fb865de861b541ca2058a4b6a161ef851c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pip", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPagesSphinx).__jsii_proxy_class__ = lambda : _IPagesSphinxProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPythonBuildBdistWheel")
class IPythonBuildBdistWheel(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="requirementsFile")
    def requirements_file(self) -> typing.Optional[builtins.str]:
        ...


class _IPythonBuildBdistWheelProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonBuildBdistWheel"

    @builtins.property
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipenvVersionSpecifier"))

    @builtins.property
    @jsii.member(jsii_name="requirementsFile")
    def requirements_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementsFile"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonBuildBdistWheel).__jsii_proxy_class__ = lambda : _IPythonBuildBdistWheelProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPythonDeployTwineUpload")
class IPythonDeployTwineUpload(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="twinePasswordEnvVar")
    def twine_password_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        ...

    @twine_password_env_var.setter
    def twine_password_env_var(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="twineUsernameEnvVar")
    def twine_username_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        ...

    @twine_username_env_var.setter
    def twine_username_env_var(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="twineRepositoryUrl")
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        ...

    @twine_repository_url.setter
    def twine_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IPythonDeployTwineUploadProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonDeployTwineUpload"

    @builtins.property
    @jsii.member(jsii_name="twinePasswordEnvVar")
    def twine_password_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twinePasswordEnvVar"))

    @twine_password_env_var.setter
    def twine_password_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9660a6af6f0331d5ef0889cb13f6b84c3b288609572c9b9a2155101f25277f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twinePasswordEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineUsernameEnvVar")
    def twine_username_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twineUsernameEnvVar"))

    @twine_username_env_var.setter
    def twine_username_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7400741906b0c3800b5a650a2bc50a84d537d16ed2deb183a26d6ea86779b55c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineUsernameEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineRepositoryUrl")
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "twineRepositoryUrl"))

    @twine_repository_url.setter
    def twine_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294991e35b11dd0a55e271a2d164d4c0f8ec6a83386fd51042dc0650ea48d84b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineRepositoryUrl", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonDeployTwineUpload).__jsii_proxy_class__ = lambda : _IPythonDeployTwineUploadProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPythonFullStack")
class IPythonFullStack(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="bDistWheelJob")
    def b_dist_wheel_job(self) -> "PythonBuildBdistWheel":
        ...

    @b_dist_wheel_job.setter
    def b_dist_wheel_job(self, value: "PythonBuildBdistWheel") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="evaluateGitTagPep440ConformityJob")
    def evaluate_git_tag_pep440_conformity_job(
        self,
    ) -> "PythonTestEvaluateGitTagPep440Conformity":
        ...

    @evaluate_git_tag_pep440_conformity_job.setter
    def evaluate_git_tag_pep440_conformity_job(
        self,
        value: "PythonTestEvaluateGitTagPep440Conformity",
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="flake8Job")
    def flake8_job(self) -> "PythonLintFlake8":
        ...

    @flake8_job.setter
    def flake8_job(self, value: "PythonLintFlake8") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="isortJob")
    def isort_job(self) -> "PythonLintIsort":
        ...

    @isort_job.setter
    def isort_job(self, value: "PythonLintIsort") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="pytestJob")
    def pytest_job(self) -> "PythonTestPytest":
        ...

    @pytest_job.setter
    def pytest_job(self, value: "PythonTestPytest") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="twineProdJob")
    def twine_prod_job(self) -> "PythonDeployTwineUpload":
        ...

    @twine_prod_job.setter
    def twine_prod_job(self, value: "PythonDeployTwineUpload") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="mypyJob")
    def mypy_job(self) -> typing.Optional["PythonLintMyPy"]:
        ...

    @mypy_job.setter
    def mypy_job(self, value: typing.Optional["PythonLintMyPy"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="sphinxJob")
    def sphinx_job(self) -> typing.Optional["PagesSphinx"]:
        ...

    @sphinx_job.setter
    def sphinx_job(self, value: typing.Optional["PagesSphinx"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="twineDevJob")
    def twine_dev_job(self) -> typing.Optional["PythonDeployTwineUpload"]:
        ...

    @twine_dev_job.setter
    def twine_dev_job(self, value: typing.Optional["PythonDeployTwineUpload"]) -> None:
        ...


class _IPythonFullStackProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonFullStack"

    @builtins.property
    @jsii.member(jsii_name="bDistWheelJob")
    def b_dist_wheel_job(self) -> "PythonBuildBdistWheel":
        return typing.cast("PythonBuildBdistWheel", jsii.get(self, "bDistWheelJob"))

    @b_dist_wheel_job.setter
    def b_dist_wheel_job(self, value: "PythonBuildBdistWheel") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568861bbd1fe7d87d974cb539dc8d64587c42d630a1bed30a2346845d5da0f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bDistWheelJob", value)

    @builtins.property
    @jsii.member(jsii_name="evaluateGitTagPep440ConformityJob")
    def evaluate_git_tag_pep440_conformity_job(
        self,
    ) -> "PythonTestEvaluateGitTagPep440Conformity":
        return typing.cast("PythonTestEvaluateGitTagPep440Conformity", jsii.get(self, "evaluateGitTagPep440ConformityJob"))

    @evaluate_git_tag_pep440_conformity_job.setter
    def evaluate_git_tag_pep440_conformity_job(
        self,
        value: "PythonTestEvaluateGitTagPep440Conformity",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf9ed1a47cec1b7ef35c54489f3d54ba6bf92e52a8de57510b769e9fbf18629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateGitTagPep440ConformityJob", value)

    @builtins.property
    @jsii.member(jsii_name="flake8Job")
    def flake8_job(self) -> "PythonLintFlake8":
        return typing.cast("PythonLintFlake8", jsii.get(self, "flake8Job"))

    @flake8_job.setter
    def flake8_job(self, value: "PythonLintFlake8") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23465dc6f8fa6651d5a80d748cf1134c2d4d93bd7e8d7a25c5bf6f9a3aabc5e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flake8Job", value)

    @builtins.property
    @jsii.member(jsii_name="isortJob")
    def isort_job(self) -> "PythonLintIsort":
        return typing.cast("PythonLintIsort", jsii.get(self, "isortJob"))

    @isort_job.setter
    def isort_job(self, value: "PythonLintIsort") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bbff723efb147305eaa84407b2ddb9cb0968fe0b941f788a7f45dc32941da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isortJob", value)

    @builtins.property
    @jsii.member(jsii_name="pytestJob")
    def pytest_job(self) -> "PythonTestPytest":
        return typing.cast("PythonTestPytest", jsii.get(self, "pytestJob"))

    @pytest_job.setter
    def pytest_job(self, value: "PythonTestPytest") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973a2ce3390bca53c20e2327ebcc03fc74f2eec2fb457d80227bca310a868247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pytestJob", value)

    @builtins.property
    @jsii.member(jsii_name="twineProdJob")
    def twine_prod_job(self) -> "PythonDeployTwineUpload":
        return typing.cast("PythonDeployTwineUpload", jsii.get(self, "twineProdJob"))

    @twine_prod_job.setter
    def twine_prod_job(self, value: "PythonDeployTwineUpload") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085b971628c10b30ceed12ea1d639c048da63ba5e606d5233d7191e8fbddf797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineProdJob", value)

    @builtins.property
    @jsii.member(jsii_name="mypyJob")
    def mypy_job(self) -> typing.Optional["PythonLintMyPy"]:
        return typing.cast(typing.Optional["PythonLintMyPy"], jsii.get(self, "mypyJob"))

    @mypy_job.setter
    def mypy_job(self, value: typing.Optional["PythonLintMyPy"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c692346485d0e6ac60b5980eebdd8ceeabdabf81d594b089ba738b040d11029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mypyJob", value)

    @builtins.property
    @jsii.member(jsii_name="sphinxJob")
    def sphinx_job(self) -> typing.Optional["PagesSphinx"]:
        return typing.cast(typing.Optional["PagesSphinx"], jsii.get(self, "sphinxJob"))

    @sphinx_job.setter
    def sphinx_job(self, value: typing.Optional["PagesSphinx"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd60dad551f973eec4ba18b03eead5b07aceee826705f356cab33c000eb6599a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sphinxJob", value)

    @builtins.property
    @jsii.member(jsii_name="twineDevJob")
    def twine_dev_job(self) -> typing.Optional["PythonDeployTwineUpload"]:
        return typing.cast(typing.Optional["PythonDeployTwineUpload"], jsii.get(self, "twineDevJob"))

    @twine_dev_job.setter
    def twine_dev_job(self, value: typing.Optional["PythonDeployTwineUpload"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c120af49a66b6d3e55e57d49aa1a97fffb5581661b87336df9701e82d7ca74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineDevJob", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonFullStack).__jsii_proxy_class__ = lambda : _IPythonFullStackProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPythonLintFlake8")
class IPythonLintFlake8(typing_extensions.Protocol):
    pass


class _IPythonLintFlake8Proxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonLintFlake8"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonLintFlake8).__jsii_proxy_class__ = lambda : _IPythonLintFlake8Proxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPythonLintIsort")
class IPythonLintIsort(typing_extensions.Protocol):
    pass


class _IPythonLintIsortProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonLintIsort"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonLintIsort).__jsii_proxy_class__ = lambda : _IPythonLintIsortProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPythonLintMyPy")
class IPythonLintMyPy(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="packageDir")
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        ...

    @package_dir.setter
    def package_dir(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="myPyOptions")
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        ...

    @my_py_options.setter
    def my_py_options(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="myPyVersion")
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        ...

    @my_py_version.setter
    def my_py_version(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IPythonLintMyPyProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonLintMyPy"

    @builtins.property
    @jsii.member(jsii_name="packageDir")
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        return typing.cast(builtins.str, jsii.get(self, "packageDir"))

    @package_dir.setter
    def package_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0292cf04a9fe7832e1972e0fb59b0afb40652a5aa4df5a8b31013bda0c15775e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageDir", value)

    @builtins.property
    @jsii.member(jsii_name="myPyOptions")
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyOptions"))

    @my_py_options.setter
    def my_py_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f7dc13926bf2901d954705eb2b2080131744bd1c1a9a463e2bf9f300b786be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyOptions", value)

    @builtins.property
    @jsii.member(jsii_name="myPyVersion")
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyVersion"))

    @my_py_version.setter
    def my_py_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cbe14da8069cbd2b9aa386715ffaa435bade1cd81e19ab0cf2cbd0628bd7ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyVersion", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonLintMyPy).__jsii_proxy_class__ = lambda : _IPythonLintMyPyProxy


@jsii.interface(
    jsii_type="@gcix/gcix.python.IPythonTestEvaluateGitTagPep440Conformity"
)
class IPythonTestEvaluateGitTagPep440Conformity(typing_extensions.Protocol):
    pass


class _IPythonTestEvaluateGitTagPep440ConformityProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonTestEvaluateGitTagPep440Conformity"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonTestEvaluateGitTagPep440Conformity).__jsii_proxy_class__ = lambda : _IPythonTestEvaluateGitTagPep440ConformityProxy


@jsii.interface(jsii_type="@gcix/gcix.python.IPythonTestPytest")
class IPythonTestPytest(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> builtins.str:
        '''The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to latest package version.'''
        ...

    @pipenv_version_specifier.setter
    def pipenv_version_specifier(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="pytestCommand")
    def pytest_command(self) -> builtins.str:
        '''This argument is only required if you have a custom command to call pytest.'''
        ...

    @pytest_command.setter
    def pytest_command(self, value: builtins.str) -> None:
        ...


class _IPythonTestPytestProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.python.IPythonTestPytest"

    @builtins.property
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> builtins.str:
        '''The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to latest package version.'''
        return typing.cast(builtins.str, jsii.get(self, "pipenvVersionSpecifier"))

    @pipenv_version_specifier.setter
    def pipenv_version_specifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e080d65e55a5fcd2b8fbb2f7646143710ebe547d295afc0517d92c4e3f925b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipenvVersionSpecifier", value)

    @builtins.property
    @jsii.member(jsii_name="pytestCommand")
    def pytest_command(self) -> builtins.str:
        '''This argument is only required if you have a custom command to call pytest.'''
        return typing.cast(builtins.str, jsii.get(self, "pytestCommand"))

    @pytest_command.setter
    def pytest_command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0098dec7df0df3581a75e389645e9d96d409c81950b610da666da7a525675862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pytestCommand", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPythonTestPytest).__jsii_proxy_class__ = lambda : _IPythonTestPytestProxy


@jsii.implements(IPagesPdoc3)
class PagesPdoc3(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PagesPdoc3",
):
    '''Generate a HTML API documentation of you python code as Gitlab Pages.

    Runs ``pdoc3 --html -f --skip-errors --output-dir public{path} {module}`` and stores the output
    as artifact under the ``public`` directory.

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: pdoc3-pages
    - stage: build
    - artifacts: Path 'public'
    '''

    def __init__(
        self,
        *,
        module: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module: The Python module name. This may be an import path resolvable in the current environment, or a file path to a Python module or package.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param output_path: A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to. Defaults to "/".
        '''
        props = PagesPdoc3Props(
            module=module,
            job_name=job_name,
            job_stage=job_stage,
            output_path=output_path,
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
    @jsii.member(jsii_name="module")
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        return typing.cast(builtins.str, jsii.get(self, "module"))

    @module.setter
    def module(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b6b36665ee5b05eca589deb7b94bd312d8af22e49daa6f7529cca7dc750378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "module", value)

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(self) -> builtins.str:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputPath"))

    @output_path.setter
    def output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56ae18de1241a2206a8b1a05e8029fe7706c1529d8a3e316d8024cbfaa7c747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputPath", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PagesPdoc3Props",
    jsii_struct_bases=[],
    name_mapping={
        "module": "module",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "output_path": "outputPath",
    },
)
class PagesPdoc3Props:
    def __init__(
        self,
        *,
        module: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module: The Python module name. This may be an import path resolvable in the current environment, or a file path to a Python module or package.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param output_path: A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to. Defaults to "/".
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90380030d730957ebee8c04fce8a4e8295ce646c15825b4e27ae670fa482475)
            check_type(argname="argument module", value=module, expected_type=type_hints["module"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument output_path", value=output_path, expected_type=type_hints["output_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "module": module,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if output_path is not None:
            self._values["output_path"] = output_path

    @builtins.property
    def module(self) -> builtins.str:
        '''The Python module name.

        This may be an import path resolvable in the
        current environment, or a file path to a Python module or package.
        '''
        result = self._values.get("module")
        assert result is not None, "Required property 'module' is missing"
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

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''A sub path of the Gitlab Pages ``public`` directory to output generated HTML/markdown files to.

        Defaults to "/".
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesPdoc3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPagesSphinx)
class PagesSphinx(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PagesSphinx",
):
    '''Runs ``sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}`` and installs project requirements. Uses: (``PythonScripts.PipInstallRequirements()``).

    - Requires a ``docs/requirements.txt`` in your project folder``containing at least``sphinx`
    - Creates artifacts for Gitlab Pages under ``pages``

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: sphinx-pages
    - stage: build
    - artifacts: Path 'public'
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip: typing.Optional[typing.Union["PipInstallRequirementsProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param pip: 
        '''
        props = PagesSphinxProps(job_name=job_name, job_stage=job_stage, pip=pip)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="pip")
    def pip(self) -> typing.Optional["PipInstallRequirementsProps"]:
        return typing.cast(typing.Optional["PipInstallRequirementsProps"], jsii.get(self, "pip"))

    @pip.setter
    def pip(self, value: typing.Optional["PipInstallRequirementsProps"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ce70a659a919456b0d69440802e137492954b2b045a49b622d4c0df19eb4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pip", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PagesSphinxProps",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "job_stage": "jobStage", "pip": "pip"},
)
class PagesSphinxProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip: typing.Optional[typing.Union["PipInstallRequirementsProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param pip: 
        '''
        if isinstance(pip, dict):
            pip = PipInstallRequirementsProps(**pip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b81e438f09bb67ab84286db25b1f9401359e060552f35868b18dc62e8feb7e)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument pip", value=pip, expected_type=type_hints["pip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if pip is not None:
            self._values["pip"] = pip

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

    @builtins.property
    def pip(self) -> typing.Optional["PipInstallRequirementsProps"]:
        result = self._values.get("pip")
        return typing.cast(typing.Optional["PipInstallRequirementsProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagesSphinxProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PipInstallRequirementsProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipenv_version_specifier": "pipenvVersionSpecifier",
        "requirements_file": "requirementsFile",
    },
)
class PipInstallRequirementsProps:
    def __init__(
        self,
        *,
        pipenv_version_specifier: typing.Optional[builtins.str] = None,
        requirements_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents the properties for the ``pipInstallRequirements`` static method.

        :param pipenv_version_specifier: The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to an empty string, indicating installation of the latest version. Default: ""
        :param requirements_file: The location and name of the requirements file. Default: "requirements.txt"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f23b66d8083ae889fbd949745fd77545b924a5aebcc1c180cd20b8e4f447ea)
            check_type(argname="argument pipenv_version_specifier", value=pipenv_version_specifier, expected_type=type_hints["pipenv_version_specifier"])
            check_type(argname="argument requirements_file", value=requirements_file, expected_type=type_hints["requirements_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pipenv_version_specifier is not None:
            self._values["pipenv_version_specifier"] = pipenv_version_specifier
        if requirements_file is not None:
            self._values["requirements_file"] = requirements_file

    @builtins.property
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        '''The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to an empty string, indicating installation of the latest version.

        :default: ""
        '''
        result = self._values.get("pipenv_version_specifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requirements_file(self) -> typing.Optional[builtins.str]:
        '''The location and name of the requirements file.

        :default: "requirements.txt"
        '''
        result = self._values.get("requirements_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipInstallRequirementsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPythonBuildBdistWheel)
class PythonBuildBdistWheel(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonBuildBdistWheel",
):
    '''Runs ``python3 setup.py bdist_wheel`` and installs project requirements Requirements are installed by ``LinuxScripts.pipInstallRequirements()``.

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: bdist_wheel
    - stage: build
    - artifacts: Path 'dist/'

    Requires a ``Pipfile.lock`` or ``requirements.txt`` in your project folder
    containing at least ``setuptools``. Creates artifacts under the path 'dist/'.

    :default:

    to an empty string, indicating
    installation of the latest version.
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip_requirements: typing.Optional[typing.Union[PipInstallRequirementsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: 
        :param job_stage: 
        :param pip_requirements: 
        '''
        props = PythonBuildBdistWheelProps(
            job_name=job_name, job_stage=job_stage, pip_requirements=pip_requirements
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
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipenvVersionSpecifier"))

    @builtins.property
    @jsii.member(jsii_name="requirementsFile")
    def requirements_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementsFile"))


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonBuildBdistWheelProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "job_stage": "jobStage",
        "pip_requirements": "pipRequirements",
    },
)
class PythonBuildBdistWheelProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pip_requirements: typing.Optional[typing.Union[PipInstallRequirementsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_name: 
        :param job_stage: 
        :param pip_requirements: 
        '''
        if isinstance(pip_requirements, dict):
            pip_requirements = PipInstallRequirementsProps(**pip_requirements)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176b3c5202655c2120b1f4797286db6e2cf925b6ff78468974e3b96185c2a1bf)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument pip_requirements", value=pip_requirements, expected_type=type_hints["pip_requirements"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if pip_requirements is not None:
            self._values["pip_requirements"] = pip_requirements

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_stage(self) -> typing.Optional[builtins.str]:
        result = self._values.get("job_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pip_requirements(self) -> typing.Optional[PipInstallRequirementsProps]:
        result = self._values.get("pip_requirements")
        return typing.cast(typing.Optional[PipInstallRequirementsProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonBuildBdistWheelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPythonDeployTwineUpload)
class PythonDeployTwineUpload(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonDeployTwineUpload",
):
    '''Runs:.

    Example::

       pip3 install --upgrade twine
       python3 -m twine upload --non-interactive --disable-progress-bar dist/*

    Requires artifacts from a build job under ``dist/`` (e.g. from ``BdistWheel()``)

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: twine
    - stage: deploy
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        twine_password_env_var: typing.Optional[builtins.str] = None,
        twine_repository_url: typing.Optional[builtins.str] = None,
        twine_username_env_var: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param twine_password_env_var: The name of the environment variable containing the password. **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_PASSWORD'.
        :param twine_repository_url: The URL to the PyPI repository to which the Python artifacts will be deployed. If ``undefined`` the package is published to ``https://pypi.org``.
        :param twine_username_env_var: The name of the environment variable containing the username value. **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_USERNAME'.
        '''
        props = PythonDeployTwineUploadProps(
            job_name=job_name,
            job_stage=job_stage,
            twine_password_env_var=twine_password_env_var,
            twine_repository_url=twine_repository_url,
            twine_username_env_var=twine_username_env_var,
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
    @jsii.member(jsii_name="twinePasswordEnvVar")
    def twine_password_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twinePasswordEnvVar"))

    @twine_password_env_var.setter
    def twine_password_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6504026af919021f131594420a0ecb8e9b7c1bbca0d584ac11b14a76489fcef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twinePasswordEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineUsernameEnvVar")
    def twine_username_env_var(self) -> builtins.str:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "twineUsernameEnvVar"))

    @twine_username_env_var.setter
    def twine_username_env_var(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404330b5ddcd370372addc52f78f0c934baa8fce06f1d597f9354cfc0c17c577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineUsernameEnvVar", value)

    @builtins.property
    @jsii.member(jsii_name="twineRepositoryUrl")
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "twineRepositoryUrl"))

    @twine_repository_url.setter
    def twine_repository_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92058c1de881895984a14b99b9a3ac64d8e008e965bde3c19d2d83e2f2664ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineRepositoryUrl", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonDeployTwineUploadProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "job_stage": "jobStage",
        "twine_password_env_var": "twinePasswordEnvVar",
        "twine_repository_url": "twineRepositoryUrl",
        "twine_username_env_var": "twineUsernameEnvVar",
    },
)
class PythonDeployTwineUploadProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        twine_password_env_var: typing.Optional[builtins.str] = None,
        twine_repository_url: typing.Optional[builtins.str] = None,
        twine_username_env_var: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Represents the properties for the ``TwineUpload`` class.

        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param twine_password_env_var: The name of the environment variable containing the password. **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_PASSWORD'.
        :param twine_repository_url: The URL to the PyPI repository to which the Python artifacts will be deployed. If ``undefined`` the package is published to ``https://pypi.org``.
        :param twine_username_env_var: The name of the environment variable containing the username value. **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue! Defaults to 'TWINE_USERNAME'.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5dce1ff6466e0829306594500898f7fd88c82d1a07c636e777f4d6baa0e4e43)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument twine_password_env_var", value=twine_password_env_var, expected_type=type_hints["twine_password_env_var"])
            check_type(argname="argument twine_repository_url", value=twine_repository_url, expected_type=type_hints["twine_repository_url"])
            check_type(argname="argument twine_username_env_var", value=twine_username_env_var, expected_type=type_hints["twine_username_env_var"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if twine_password_env_var is not None:
            self._values["twine_password_env_var"] = twine_password_env_var
        if twine_repository_url is not None:
            self._values["twine_repository_url"] = twine_repository_url
        if twine_username_env_var is not None:
            self._values["twine_username_env_var"] = twine_username_env_var

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

    @builtins.property
    def twine_password_env_var(self) -> typing.Optional[builtins.str]:
        '''The name of the environment variable containing the password.

        **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_PASSWORD'.
        '''
        result = self._values.get("twine_password_env_var")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_repository_url(self) -> typing.Optional[builtins.str]:
        '''The URL to the PyPI repository to which the Python artifacts will be deployed.

        If ``undefined`` the package is published to ``https://pypi.org``.
        '''
        result = self._values.get("twine_repository_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_username_env_var(self) -> typing.Optional[builtins.str]:
        '''The name of the environment variable containing the username value.

        **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
        Defaults to 'TWINE_USERNAME'.
        '''
        result = self._values.get("twine_username_env_var")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonDeployTwineUploadProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPythonFullStack)
class PythonFullStack(
    _JobCollection_0289800c,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonFullStack",
):
    '''Returns a sequence containing following jobs: - isort - flake8 - pytest - evaluating CI_COMMIT_TAG as valid PyPI version string (if exists) - bdist_wheel - Gitlab Pages sphinx - twine upload  Optional jobs: - mypy  The ``varname_dev_password`` and ``varname_stable_password`` arguments are **only** used to specify the variable name and **not** the actuall password.

    The variable name has to be set outside of the pipeline itself,
    if you set it within the pipline, that would be a security risk.
    '''

    def __init__(
        self,
        *,
        twine_prod_job_props: typing.Union[PythonDeployTwineUploadProps, typing.Dict[builtins.str, typing.Any]],
        b_dist_wheel_job_props: typing.Optional[typing.Union[PythonBuildBdistWheelProps, typing.Dict[builtins.str, typing.Any]]] = None,
        evaluate_git_tag_pep440_conformity_job_props: typing.Optional[typing.Union["PythonTestEvaluateGitTagPep440ConformityProps", typing.Dict[builtins.str, typing.Any]]] = None,
        flake8_job_props: typing.Optional[typing.Union["PythonLintFlake8Props", typing.Dict[builtins.str, typing.Any]]] = None,
        isort_job_props: typing.Optional[typing.Union["PythonLintIsortProps", typing.Dict[builtins.str, typing.Any]]] = None,
        mypy_job_props: typing.Optional[typing.Union["PythonLintMyPyProps", typing.Dict[builtins.str, typing.Any]]] = None,
        pytest_job_props: typing.Optional[typing.Union["PythonTestPytestProps", typing.Dict[builtins.str, typing.Any]]] = None,
        sphinx_props_job_props: typing.Optional[typing.Union[PagesSphinxProps, typing.Dict[builtins.str, typing.Any]]] = None,
        twine_dev_job_props: typing.Optional[typing.Union[PythonDeployTwineUploadProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param twine_prod_job_props: 
        :param b_dist_wheel_job_props: 
        :param evaluate_git_tag_pep440_conformity_job_props: 
        :param flake8_job_props: 
        :param isort_job_props: 
        :param mypy_job_props: 
        :param pytest_job_props: 
        :param sphinx_props_job_props: 
        :param twine_dev_job_props: 
        '''
        props = PythonFullStackProps(
            twine_prod_job_props=twine_prod_job_props,
            b_dist_wheel_job_props=b_dist_wheel_job_props,
            evaluate_git_tag_pep440_conformity_job_props=evaluate_git_tag_pep440_conformity_job_props,
            flake8_job_props=flake8_job_props,
            isort_job_props=isort_job_props,
            mypy_job_props=mypy_job_props,
            pytest_job_props=pytest_job_props,
            sphinx_props_job_props=sphinx_props_job_props,
            twine_dev_job_props=twine_dev_job_props,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="bDistWheelJob")
    def b_dist_wheel_job(self) -> PythonBuildBdistWheel:
        return typing.cast(PythonBuildBdistWheel, jsii.get(self, "bDistWheelJob"))

    @b_dist_wheel_job.setter
    def b_dist_wheel_job(self, value: PythonBuildBdistWheel) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8acb7d5e58b49ea448beb9689c5e4cc70e707315b29ee8db6566289228ed18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bDistWheelJob", value)

    @builtins.property
    @jsii.member(jsii_name="evaluateGitTagPep440ConformityJob")
    def evaluate_git_tag_pep440_conformity_job(
        self,
    ) -> "PythonTestEvaluateGitTagPep440Conformity":
        return typing.cast("PythonTestEvaluateGitTagPep440Conformity", jsii.get(self, "evaluateGitTagPep440ConformityJob"))

    @evaluate_git_tag_pep440_conformity_job.setter
    def evaluate_git_tag_pep440_conformity_job(
        self,
        value: "PythonTestEvaluateGitTagPep440Conformity",
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594ac4a987b8eb013a797d8dafe0bf19ec6fc88b9a6b7f9046e7c2bb54553cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateGitTagPep440ConformityJob", value)

    @builtins.property
    @jsii.member(jsii_name="flake8Job")
    def flake8_job(self) -> "PythonLintFlake8":
        return typing.cast("PythonLintFlake8", jsii.get(self, "flake8Job"))

    @flake8_job.setter
    def flake8_job(self, value: "PythonLintFlake8") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2beae900d62ec0358483fc28ebe7c6eb75d831ec289c54bc083ba2c154a356b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flake8Job", value)

    @builtins.property
    @jsii.member(jsii_name="isortJob")
    def isort_job(self) -> "PythonLintIsort":
        return typing.cast("PythonLintIsort", jsii.get(self, "isortJob"))

    @isort_job.setter
    def isort_job(self, value: "PythonLintIsort") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75720ebf5169fda73177ef67757d730673af4b04682928c555caaebf22362e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isortJob", value)

    @builtins.property
    @jsii.member(jsii_name="pytestJob")
    def pytest_job(self) -> "PythonTestPytest":
        return typing.cast("PythonTestPytest", jsii.get(self, "pytestJob"))

    @pytest_job.setter
    def pytest_job(self, value: "PythonTestPytest") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a479e4cc866f5507d72b227332d54f81aaf47a6ae9f66bccccfd545011ff1cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pytestJob", value)

    @builtins.property
    @jsii.member(jsii_name="twineProdJob")
    def twine_prod_job(self) -> PythonDeployTwineUpload:
        return typing.cast(PythonDeployTwineUpload, jsii.get(self, "twineProdJob"))

    @twine_prod_job.setter
    def twine_prod_job(self, value: PythonDeployTwineUpload) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191ec0344a76e3fcad4a620e80ab0f48cf3d54f917e5224bdecdf93d00d57917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineProdJob", value)

    @builtins.property
    @jsii.member(jsii_name="mypyJob")
    def mypy_job(self) -> typing.Optional["PythonLintMyPy"]:
        return typing.cast(typing.Optional["PythonLintMyPy"], jsii.get(self, "mypyJob"))

    @mypy_job.setter
    def mypy_job(self, value: typing.Optional["PythonLintMyPy"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1e8f645e9092419f7ad22582cc6d600c7ef44d51fd01259986729b7c78cceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mypyJob", value)

    @builtins.property
    @jsii.member(jsii_name="sphinxJob")
    def sphinx_job(self) -> typing.Optional[PagesSphinx]:
        return typing.cast(typing.Optional[PagesSphinx], jsii.get(self, "sphinxJob"))

    @sphinx_job.setter
    def sphinx_job(self, value: typing.Optional[PagesSphinx]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cb2f803c8be87976c40ae8fb25cd35f14c1d69f0b955b4bc9d0bc5b2413011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sphinxJob", value)

    @builtins.property
    @jsii.member(jsii_name="twineDevJob")
    def twine_dev_job(self) -> typing.Optional[PythonDeployTwineUpload]:
        return typing.cast(typing.Optional[PythonDeployTwineUpload], jsii.get(self, "twineDevJob"))

    @twine_dev_job.setter
    def twine_dev_job(self, value: typing.Optional[PythonDeployTwineUpload]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221a4cd39c2ae600b4b992e353a2f117aee684bfd2a6c757ff4dfbb98e11a848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twineDevJob", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonFullStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "twine_prod_job_props": "twineProdJobProps",
        "b_dist_wheel_job_props": "bDistWheelJobProps",
        "evaluate_git_tag_pep440_conformity_job_props": "evaluateGitTagPep440ConformityJobProps",
        "flake8_job_props": "flake8JobProps",
        "isort_job_props": "isortJobProps",
        "mypy_job_props": "mypyJobProps",
        "pytest_job_props": "pytestJobProps",
        "sphinx_props_job_props": "sphinxPropsJobProps",
        "twine_dev_job_props": "twineDevJobProps",
    },
)
class PythonFullStackProps:
    def __init__(
        self,
        *,
        twine_prod_job_props: typing.Union[PythonDeployTwineUploadProps, typing.Dict[builtins.str, typing.Any]],
        b_dist_wheel_job_props: typing.Optional[typing.Union[PythonBuildBdistWheelProps, typing.Dict[builtins.str, typing.Any]]] = None,
        evaluate_git_tag_pep440_conformity_job_props: typing.Optional[typing.Union["PythonTestEvaluateGitTagPep440ConformityProps", typing.Dict[builtins.str, typing.Any]]] = None,
        flake8_job_props: typing.Optional[typing.Union["PythonLintFlake8Props", typing.Dict[builtins.str, typing.Any]]] = None,
        isort_job_props: typing.Optional[typing.Union["PythonLintIsortProps", typing.Dict[builtins.str, typing.Any]]] = None,
        mypy_job_props: typing.Optional[typing.Union["PythonLintMyPyProps", typing.Dict[builtins.str, typing.Any]]] = None,
        pytest_job_props: typing.Optional[typing.Union["PythonTestPytestProps", typing.Dict[builtins.str, typing.Any]]] = None,
        sphinx_props_job_props: typing.Optional[typing.Union[PagesSphinxProps, typing.Dict[builtins.str, typing.Any]]] = None,
        twine_dev_job_props: typing.Optional[typing.Union[PythonDeployTwineUploadProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param twine_prod_job_props: 
        :param b_dist_wheel_job_props: 
        :param evaluate_git_tag_pep440_conformity_job_props: 
        :param flake8_job_props: 
        :param isort_job_props: 
        :param mypy_job_props: 
        :param pytest_job_props: 
        :param sphinx_props_job_props: 
        :param twine_dev_job_props: 
        '''
        if isinstance(twine_prod_job_props, dict):
            twine_prod_job_props = PythonDeployTwineUploadProps(**twine_prod_job_props)
        if isinstance(b_dist_wheel_job_props, dict):
            b_dist_wheel_job_props = PythonBuildBdistWheelProps(**b_dist_wheel_job_props)
        if isinstance(evaluate_git_tag_pep440_conformity_job_props, dict):
            evaluate_git_tag_pep440_conformity_job_props = PythonTestEvaluateGitTagPep440ConformityProps(**evaluate_git_tag_pep440_conformity_job_props)
        if isinstance(flake8_job_props, dict):
            flake8_job_props = PythonLintFlake8Props(**flake8_job_props)
        if isinstance(isort_job_props, dict):
            isort_job_props = PythonLintIsortProps(**isort_job_props)
        if isinstance(mypy_job_props, dict):
            mypy_job_props = PythonLintMyPyProps(**mypy_job_props)
        if isinstance(pytest_job_props, dict):
            pytest_job_props = PythonTestPytestProps(**pytest_job_props)
        if isinstance(sphinx_props_job_props, dict):
            sphinx_props_job_props = PagesSphinxProps(**sphinx_props_job_props)
        if isinstance(twine_dev_job_props, dict):
            twine_dev_job_props = PythonDeployTwineUploadProps(**twine_dev_job_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8008a9e354f94757430e51b6130b0d73774e2df953a85ab59db1946bb4a47c9)
            check_type(argname="argument twine_prod_job_props", value=twine_prod_job_props, expected_type=type_hints["twine_prod_job_props"])
            check_type(argname="argument b_dist_wheel_job_props", value=b_dist_wheel_job_props, expected_type=type_hints["b_dist_wheel_job_props"])
            check_type(argname="argument evaluate_git_tag_pep440_conformity_job_props", value=evaluate_git_tag_pep440_conformity_job_props, expected_type=type_hints["evaluate_git_tag_pep440_conformity_job_props"])
            check_type(argname="argument flake8_job_props", value=flake8_job_props, expected_type=type_hints["flake8_job_props"])
            check_type(argname="argument isort_job_props", value=isort_job_props, expected_type=type_hints["isort_job_props"])
            check_type(argname="argument mypy_job_props", value=mypy_job_props, expected_type=type_hints["mypy_job_props"])
            check_type(argname="argument pytest_job_props", value=pytest_job_props, expected_type=type_hints["pytest_job_props"])
            check_type(argname="argument sphinx_props_job_props", value=sphinx_props_job_props, expected_type=type_hints["sphinx_props_job_props"])
            check_type(argname="argument twine_dev_job_props", value=twine_dev_job_props, expected_type=type_hints["twine_dev_job_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "twine_prod_job_props": twine_prod_job_props,
        }
        if b_dist_wheel_job_props is not None:
            self._values["b_dist_wheel_job_props"] = b_dist_wheel_job_props
        if evaluate_git_tag_pep440_conformity_job_props is not None:
            self._values["evaluate_git_tag_pep440_conformity_job_props"] = evaluate_git_tag_pep440_conformity_job_props
        if flake8_job_props is not None:
            self._values["flake8_job_props"] = flake8_job_props
        if isort_job_props is not None:
            self._values["isort_job_props"] = isort_job_props
        if mypy_job_props is not None:
            self._values["mypy_job_props"] = mypy_job_props
        if pytest_job_props is not None:
            self._values["pytest_job_props"] = pytest_job_props
        if sphinx_props_job_props is not None:
            self._values["sphinx_props_job_props"] = sphinx_props_job_props
        if twine_dev_job_props is not None:
            self._values["twine_dev_job_props"] = twine_dev_job_props

    @builtins.property
    def twine_prod_job_props(self) -> PythonDeployTwineUploadProps:
        result = self._values.get("twine_prod_job_props")
        assert result is not None, "Required property 'twine_prod_job_props' is missing"
        return typing.cast(PythonDeployTwineUploadProps, result)

    @builtins.property
    def b_dist_wheel_job_props(self) -> typing.Optional[PythonBuildBdistWheelProps]:
        result = self._values.get("b_dist_wheel_job_props")
        return typing.cast(typing.Optional[PythonBuildBdistWheelProps], result)

    @builtins.property
    def evaluate_git_tag_pep440_conformity_job_props(
        self,
    ) -> typing.Optional["PythonTestEvaluateGitTagPep440ConformityProps"]:
        result = self._values.get("evaluate_git_tag_pep440_conformity_job_props")
        return typing.cast(typing.Optional["PythonTestEvaluateGitTagPep440ConformityProps"], result)

    @builtins.property
    def flake8_job_props(self) -> typing.Optional["PythonLintFlake8Props"]:
        result = self._values.get("flake8_job_props")
        return typing.cast(typing.Optional["PythonLintFlake8Props"], result)

    @builtins.property
    def isort_job_props(self) -> typing.Optional["PythonLintIsortProps"]:
        result = self._values.get("isort_job_props")
        return typing.cast(typing.Optional["PythonLintIsortProps"], result)

    @builtins.property
    def mypy_job_props(self) -> typing.Optional["PythonLintMyPyProps"]:
        result = self._values.get("mypy_job_props")
        return typing.cast(typing.Optional["PythonLintMyPyProps"], result)

    @builtins.property
    def pytest_job_props(self) -> typing.Optional["PythonTestPytestProps"]:
        result = self._values.get("pytest_job_props")
        return typing.cast(typing.Optional["PythonTestPytestProps"], result)

    @builtins.property
    def sphinx_props_job_props(self) -> typing.Optional[PagesSphinxProps]:
        result = self._values.get("sphinx_props_job_props")
        return typing.cast(typing.Optional[PagesSphinxProps], result)

    @builtins.property
    def twine_dev_job_props(self) -> typing.Optional[PythonDeployTwineUploadProps]:
        result = self._values.get("twine_dev_job_props")
        return typing.cast(typing.Optional[PythonDeployTwineUploadProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonFullStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPythonLintFlake8)
class PythonLintFlake8(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonLintFlake8",
):
    '''Runs:.

    Example::

       pip3 install --upgrade flake8
       flake8

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: flake8
    - stage: lint
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        props = PythonLintFlake8Props(job_name=job_name, job_stage=job_stage)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonLintFlake8Props",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "job_stage": "jobStage"},
)
class PythonLintFlake8Props:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98061508d00877b56ac304bd10159526ec5e85bb653f172b33b230c50cd39722)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

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
        return "PythonLintFlake8Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPythonLintIsort)
class PythonLintIsort(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonLintIsort",
):
    '''Runs:.

    Example::

       pip3 install --upgrade isort
       isort --check .

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: isort
    - stage: lint
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        props = PythonLintIsortProps(job_name=job_name, job_stage=job_stage)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonLintIsortProps",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "job_stage": "jobStage"},
)
class PythonLintIsortProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bbd1c47138ee0ac0f7a5a9c1347e66ff44ad38748c360003a1eff8b2c1fa39)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

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
        return "PythonLintIsortProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPythonLintMyPy)
class PythonLintMyPy(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonLintMyPy",
):
    '''Install mypy if not already installed. Execute mypy for ``packageDir``.

    This subclass of ``Job`` configures the following defaults for the superclass:

    - name: mypy
    - stage: lint

    :return: - The configured ``gcip.Job`` instance.
    '''

    def __init__(
        self,
        *,
        package_dir: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        my_py_options: typing.Optional[builtins.str] = None,
        my_py_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param package_dir: Package directory to type check.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param my_py_options: Adds arguments to mypy execution.
        :param my_py_version: If ``mypy`` is not already installed, this version will be installed. Installs latest version if ``undefined``.
        '''
        props = PythonLintMyPyProps(
            package_dir=package_dir,
            job_name=job_name,
            job_stage=job_stage,
            my_py_options=my_py_options,
            my_py_version=my_py_version,
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
    @jsii.member(jsii_name="packageDir")
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        return typing.cast(builtins.str, jsii.get(self, "packageDir"))

    @package_dir.setter
    def package_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0541eb0fd4f3dfb375a5ff719781360a8171189fd73434a364cc7df3cb2f79c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageDir", value)

    @builtins.property
    @jsii.member(jsii_name="myPyOptions")
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyOptions"))

    @my_py_options.setter
    def my_py_options(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c07d24edc0bad9c48f68e62522ac6a8bb00675f621c54625eb537213123a277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyOptions", value)

    @builtins.property
    @jsii.member(jsii_name="myPyVersion")
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "myPyVersion"))

    @my_py_version.setter
    def my_py_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d71623d24938276b1e15f2714b343ddc27ac76fb21f3ae34d234a140b541e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "myPyVersion", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonLintMyPyProps",
    jsii_struct_bases=[],
    name_mapping={
        "package_dir": "packageDir",
        "job_name": "jobName",
        "job_stage": "jobStage",
        "my_py_options": "myPyOptions",
        "my_py_version": "myPyVersion",
    },
)
class PythonLintMyPyProps:
    def __init__(
        self,
        *,
        package_dir: builtins.str,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        my_py_options: typing.Optional[builtins.str] = None,
        my_py_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param package_dir: Package directory to type check.
        :param job_name: The name of the job.
        :param job_stage: The stage of the job.
        :param my_py_options: Adds arguments to mypy execution.
        :param my_py_version: If ``mypy`` is not already installed, this version will be installed. Installs latest version if ``undefined``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a2bbe52c52e9930838eba5a2a54c4746d815ef73c4ff5b4cae684b58fb5bd9)
            check_type(argname="argument package_dir", value=package_dir, expected_type=type_hints["package_dir"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument my_py_options", value=my_py_options, expected_type=type_hints["my_py_options"])
            check_type(argname="argument my_py_version", value=my_py_version, expected_type=type_hints["my_py_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_dir": package_dir,
        }
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if my_py_options is not None:
            self._values["my_py_options"] = my_py_options
        if my_py_version is not None:
            self._values["my_py_version"] = my_py_version

    @builtins.property
    def package_dir(self) -> builtins.str:
        '''Package directory to type check.'''
        result = self._values.get("package_dir")
        assert result is not None, "Required property 'package_dir' is missing"
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

    @builtins.property
    def my_py_options(self) -> typing.Optional[builtins.str]:
        '''Adds arguments to mypy execution.'''
        result = self._values.get("my_py_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_py_version(self) -> typing.Optional[builtins.str]:
        '''If ``mypy`` is not already installed, this version will be installed.

        Installs latest version if ``undefined``.
        '''
        result = self._values.get("my_py_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonLintMyPyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PythonScripts(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonScripts",
):
    '''Represents a collection of utility functions for scripting tasks.'''

    @jsii.member(jsii_name="pipInstallRequirements")
    @builtins.classmethod
    def pip_install_requirements(
        cls,
        *,
        pipenv_version_specifier: typing.Optional[builtins.str] = None,
        requirements_file: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Generates a shell command to install project requirements using ``pipenv`` and ``pip`` based on the presence of a ``Pipfile.lock`` or ``requirements.txt``.

        :param pipenv_version_specifier: The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to an empty string, indicating installation of the latest version. Default: ""
        :param requirements_file: The location and name of the requirements file. Default: "requirements.txt"

        :return: A shell command string for installing project requirements.
        '''
        props = PipInstallRequirementsProps(
            pipenv_version_specifier=pipenv_version_specifier,
            requirements_file=requirements_file,
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "pipInstallRequirements", [props]))


@jsii.implements(IPythonTestEvaluateGitTagPep440Conformity)
class PythonTestEvaluateGitTagPep440Conformity(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonTestEvaluateGitTagPep440Conformity",
):
    '''Checks if the current pipelines ``$CI_COMMIT_TAG`` validates to a valid Python package version according to https://www.python.org/dev/peps/pep-0440.

    This job already contains a rule to only run when a ``$CI_COMMIT_TAG`` is
    present (``rules.only_tags()``).

    Runs ``pytest`` and installs project requirements before
    ``PythonScripts.pipInstallRequirements``

    - Requires a ``requirements.txt`` in your project folder containing
      at least ``pytest``

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: tag-pep440-conformity
    - stage: test
    - image: PredefinedImages.GCIP
    - rules: on_tagsg
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        '''
        props = PythonTestEvaluateGitTagPep440ConformityProps(
            job_name=job_name, job_stage=job_stage
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonTestEvaluateGitTagPep440ConformityProps",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "job_stage": "jobStage"},
)
class PythonTestEvaluateGitTagPep440ConformityProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7947cc4f53229eda557bd40303e49616890956d8073bae90f5369357dc42c86b)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage

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
        return "PythonTestEvaluateGitTagPep440ConformityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPythonTestPytest)
class PythonTestPytest(
    _Job_20682b42,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.python.PythonTestPytest",
):
    '''Runs ``pytest`` and installs project requirements before ``PythonScripts.pipInstallRequirements``.

    - Requires a ``Pipfile.lock`` or ``requirements.txt`` in your project folder
      containing at least ``pytest``

    This subclass of ``Job`` will configure following defaults for the superclass:

    - name: pytest
    - stage: test
    '''

    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pipenv_version_specifier: typing.Optional[builtins.str] = None,
        pytest_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param pipenv_version_specifier: The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to latest package version.
        :param pytest_command: This argument is only required if you have a custom command to call pytest.
        '''
        props = PythonTestPytestProps(
            job_name=job_name,
            job_stage=job_stage,
            pipenv_version_specifier=pipenv_version_specifier,
            pytest_command=pytest_command,
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
    @jsii.member(jsii_name="pipenvVersionSpecifier")
    def pipenv_version_specifier(self) -> builtins.str:
        '''The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to latest package version.'''
        return typing.cast(builtins.str, jsii.get(self, "pipenvVersionSpecifier"))

    @pipenv_version_specifier.setter
    def pipenv_version_specifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__226cae37a81ca25e87dcea78149b98689e164bed54b990066dafbba81111a5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipenvVersionSpecifier", value)

    @builtins.property
    @jsii.member(jsii_name="pytestCommand")
    def pytest_command(self) -> builtins.str:
        '''This argument is only required if you have a custom command to call pytest.'''
        return typing.cast(builtins.str, jsii.get(self, "pytestCommand"))

    @pytest_command.setter
    def pytest_command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2302c5b1a92b71eb7cc433187a083e860ef7bc095a983fcd81ff0787da417763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pytestCommand", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.python.PythonTestPytestProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_name": "jobName",
        "job_stage": "jobStage",
        "pipenv_version_specifier": "pipenvVersionSpecifier",
        "pytest_command": "pytestCommand",
    },
)
class PythonTestPytestProps:
    def __init__(
        self,
        *,
        job_name: typing.Optional[builtins.str] = None,
        job_stage: typing.Optional[builtins.str] = None,
        pipenv_version_specifier: typing.Optional[builtins.str] = None,
        pytest_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param job_name: The name of the Bootstrap job.
        :param job_stage: The stage of the Bootstrap job.
        :param pipenv_version_specifier: The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to latest package version.
        :param pytest_command: This argument is only required if you have a custom command to call pytest.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c30b182672351fe6435b400a314faa91f1a7042eb9ef7cce5fe6d6c896b63d)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_stage", value=job_stage, expected_type=type_hints["job_stage"])
            check_type(argname="argument pipenv_version_specifier", value=pipenv_version_specifier, expected_type=type_hints["pipenv_version_specifier"])
            check_type(argname="argument pytest_command", value=pytest_command, expected_type=type_hints["pytest_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_stage is not None:
            self._values["job_stage"] = job_stage
        if pipenv_version_specifier is not None:
            self._values["pipenv_version_specifier"] = pipenv_version_specifier
        if pytest_command is not None:
            self._values["pytest_command"] = pytest_command

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
    def pipenv_version_specifier(self) -> typing.Optional[builtins.str]:
        '''The version hint of pipenv to install if ``Pipfile.lock`` is found. For example '==2022.08.15'. Defaults to latest package version.'''
        result = self._values.get("pipenv_version_specifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pytest_command(self) -> typing.Optional[builtins.str]:
        '''This argument is only required if you have a custom command to call pytest.'''
        result = self._values.get("pytest_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonTestPytestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IPagesPdoc3",
    "IPagesSphinx",
    "IPythonBuildBdistWheel",
    "IPythonDeployTwineUpload",
    "IPythonFullStack",
    "IPythonLintFlake8",
    "IPythonLintIsort",
    "IPythonLintMyPy",
    "IPythonTestEvaluateGitTagPep440Conformity",
    "IPythonTestPytest",
    "PagesPdoc3",
    "PagesPdoc3Props",
    "PagesSphinx",
    "PagesSphinxProps",
    "PipInstallRequirementsProps",
    "PythonBuildBdistWheel",
    "PythonBuildBdistWheelProps",
    "PythonDeployTwineUpload",
    "PythonDeployTwineUploadProps",
    "PythonFullStack",
    "PythonFullStackProps",
    "PythonLintFlake8",
    "PythonLintFlake8Props",
    "PythonLintIsort",
    "PythonLintIsortProps",
    "PythonLintMyPy",
    "PythonLintMyPyProps",
    "PythonScripts",
    "PythonTestEvaluateGitTagPep440Conformity",
    "PythonTestEvaluateGitTagPep440ConformityProps",
    "PythonTestPytest",
    "PythonTestPytestProps",
]

publication.publish()

def _typecheckingstub__140d454e9594d840e53743eb2b20130db9bb7ec52f62f97bbe46e14b9f204a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8c65cef894cbe4a5cc2330b3f4cd77e69fc7ea7d99d31ac9db843f30bf42ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354586cef6fc67c1f9a319458092fb865de861b541ca2058a4b6a161ef851c48(
    value: typing.Optional[PipInstallRequirementsProps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9660a6af6f0331d5ef0889cb13f6b84c3b288609572c9b9a2155101f25277f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7400741906b0c3800b5a650a2bc50a84d537d16ed2deb183a26d6ea86779b55c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294991e35b11dd0a55e271a2d164d4c0f8ec6a83386fd51042dc0650ea48d84b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568861bbd1fe7d87d974cb539dc8d64587c42d630a1bed30a2346845d5da0f73(
    value: PythonBuildBdistWheel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf9ed1a47cec1b7ef35c54489f3d54ba6bf92e52a8de57510b769e9fbf18629(
    value: PythonTestEvaluateGitTagPep440Conformity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23465dc6f8fa6651d5a80d748cf1134c2d4d93bd7e8d7a25c5bf6f9a3aabc5e1(
    value: PythonLintFlake8,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bbff723efb147305eaa84407b2ddb9cb0968fe0b941f788a7f45dc32941da3(
    value: PythonLintIsort,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973a2ce3390bca53c20e2327ebcc03fc74f2eec2fb457d80227bca310a868247(
    value: PythonTestPytest,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085b971628c10b30ceed12ea1d639c048da63ba5e606d5233d7191e8fbddf797(
    value: PythonDeployTwineUpload,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c692346485d0e6ac60b5980eebdd8ceeabdabf81d594b089ba738b040d11029(
    value: typing.Optional[PythonLintMyPy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd60dad551f973eec4ba18b03eead5b07aceee826705f356cab33c000eb6599a(
    value: typing.Optional[PagesSphinx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c120af49a66b6d3e55e57d49aa1a97fffb5581661b87336df9701e82d7ca74(
    value: typing.Optional[PythonDeployTwineUpload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0292cf04a9fe7832e1972e0fb59b0afb40652a5aa4df5a8b31013bda0c15775e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f7dc13926bf2901d954705eb2b2080131744bd1c1a9a463e2bf9f300b786be(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cbe14da8069cbd2b9aa386715ffaa435bade1cd81e19ab0cf2cbd0628bd7ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e080d65e55a5fcd2b8fbb2f7646143710ebe547d295afc0517d92c4e3f925b3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0098dec7df0df3581a75e389645e9d96d409c81950b610da666da7a525675862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b6b36665ee5b05eca589deb7b94bd312d8af22e49daa6f7529cca7dc750378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56ae18de1241a2206a8b1a05e8029fe7706c1529d8a3e316d8024cbfaa7c747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90380030d730957ebee8c04fce8a4e8295ce646c15825b4e27ae670fa482475(
    *,
    module: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    output_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ce70a659a919456b0d69440802e137492954b2b045a49b622d4c0df19eb4db(
    value: typing.Optional[PipInstallRequirementsProps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b81e438f09bb67ab84286db25b1f9401359e060552f35868b18dc62e8feb7e(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    pip: typing.Optional[typing.Union[PipInstallRequirementsProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f23b66d8083ae889fbd949745fd77545b924a5aebcc1c180cd20b8e4f447ea(
    *,
    pipenv_version_specifier: typing.Optional[builtins.str] = None,
    requirements_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176b3c5202655c2120b1f4797286db6e2cf925b6ff78468974e3b96185c2a1bf(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    pip_requirements: typing.Optional[typing.Union[PipInstallRequirementsProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6504026af919021f131594420a0ecb8e9b7c1bbca0d584ac11b14a76489fcef0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404330b5ddcd370372addc52f78f0c934baa8fce06f1d597f9354cfc0c17c577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92058c1de881895984a14b99b9a3ac64d8e008e965bde3c19d2d83e2f2664ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dce1ff6466e0829306594500898f7fd88c82d1a07c636e777f4d6baa0e4e43(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    twine_password_env_var: typing.Optional[builtins.str] = None,
    twine_repository_url: typing.Optional[builtins.str] = None,
    twine_username_env_var: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8acb7d5e58b49ea448beb9689c5e4cc70e707315b29ee8db6566289228ed18(
    value: PythonBuildBdistWheel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594ac4a987b8eb013a797d8dafe0bf19ec6fc88b9a6b7f9046e7c2bb54553cae(
    value: PythonTestEvaluateGitTagPep440Conformity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2beae900d62ec0358483fc28ebe7c6eb75d831ec289c54bc083ba2c154a356b0(
    value: PythonLintFlake8,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75720ebf5169fda73177ef67757d730673af4b04682928c555caaebf22362e1b(
    value: PythonLintIsort,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a479e4cc866f5507d72b227332d54f81aaf47a6ae9f66bccccfd545011ff1cfd(
    value: PythonTestPytest,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191ec0344a76e3fcad4a620e80ab0f48cf3d54f917e5224bdecdf93d00d57917(
    value: PythonDeployTwineUpload,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1e8f645e9092419f7ad22582cc6d600c7ef44d51fd01259986729b7c78cceb(
    value: typing.Optional[PythonLintMyPy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cb2f803c8be87976c40ae8fb25cd35f14c1d69f0b955b4bc9d0bc5b2413011(
    value: typing.Optional[PagesSphinx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221a4cd39c2ae600b4b992e353a2f117aee684bfd2a6c757ff4dfbb98e11a848(
    value: typing.Optional[PythonDeployTwineUpload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8008a9e354f94757430e51b6130b0d73774e2df953a85ab59db1946bb4a47c9(
    *,
    twine_prod_job_props: typing.Union[PythonDeployTwineUploadProps, typing.Dict[builtins.str, typing.Any]],
    b_dist_wheel_job_props: typing.Optional[typing.Union[PythonBuildBdistWheelProps, typing.Dict[builtins.str, typing.Any]]] = None,
    evaluate_git_tag_pep440_conformity_job_props: typing.Optional[typing.Union[PythonTestEvaluateGitTagPep440ConformityProps, typing.Dict[builtins.str, typing.Any]]] = None,
    flake8_job_props: typing.Optional[typing.Union[PythonLintFlake8Props, typing.Dict[builtins.str, typing.Any]]] = None,
    isort_job_props: typing.Optional[typing.Union[PythonLintIsortProps, typing.Dict[builtins.str, typing.Any]]] = None,
    mypy_job_props: typing.Optional[typing.Union[PythonLintMyPyProps, typing.Dict[builtins.str, typing.Any]]] = None,
    pytest_job_props: typing.Optional[typing.Union[PythonTestPytestProps, typing.Dict[builtins.str, typing.Any]]] = None,
    sphinx_props_job_props: typing.Optional[typing.Union[PagesSphinxProps, typing.Dict[builtins.str, typing.Any]]] = None,
    twine_dev_job_props: typing.Optional[typing.Union[PythonDeployTwineUploadProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98061508d00877b56ac304bd10159526ec5e85bb653f172b33b230c50cd39722(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bbd1c47138ee0ac0f7a5a9c1347e66ff44ad38748c360003a1eff8b2c1fa39(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0541eb0fd4f3dfb375a5ff719781360a8171189fd73434a364cc7df3cb2f79c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c07d24edc0bad9c48f68e62522ac6a8bb00675f621c54625eb537213123a277(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d71623d24938276b1e15f2714b343ddc27ac76fb21f3ae34d234a140b541e2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a2bbe52c52e9930838eba5a2a54c4746d815ef73c4ff5b4cae684b58fb5bd9(
    *,
    package_dir: builtins.str,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    my_py_options: typing.Optional[builtins.str] = None,
    my_py_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7947cc4f53229eda557bd40303e49616890956d8073bae90f5369357dc42c86b(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226cae37a81ca25e87dcea78149b98689e164bed54b990066dafbba81111a5fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2302c5b1a92b71eb7cc433187a083e860ef7bc095a983fcd81ff0787da417763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c30b182672351fe6435b400a314faa91f1a7042eb9ef7cce5fe6d6c896b63d(
    *,
    job_name: typing.Optional[builtins.str] = None,
    job_stage: typing.Optional[builtins.str] = None,
    pipenv_version_specifier: typing.Optional[builtins.str] = None,
    pytest_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
