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


@jsii.data_type(
    jsii_type="@gcix/gcix.linux.LinuxInstallPackageProps",
    jsii_struct_bases=[],
    name_mapping={"packages": "packages", "sudo": "sudo"},
)
class LinuxInstallPackageProps:
    def __init__(
        self,
        *,
        packages: typing.Sequence[builtins.str],
        sudo: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param packages: A string listing all the packages to be installed, separated by spaces.
        :param sudo: Specifies whether the command(s) should be executed with sudo. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17faf0ce66d4b9e89af0a2ab53e0906338b3fedc80c356da28e121ee31b0529)
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument sudo", value=sudo, expected_type=type_hints["sudo"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "packages": packages,
        }
        if sudo is not None:
            self._values["sudo"] = sudo

    @builtins.property
    def packages(self) -> typing.List[builtins.str]:
        '''A string listing all the packages to be installed, separated by spaces.'''
        result = self._values.get("packages")
        assert result is not None, "Required property 'packages' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def sudo(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the command(s) should be executed with sudo.

        :default: false
        '''
        result = self._values.get("sudo")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxInstallPackageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxScripts(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.linux.LinuxScripts"):
    @jsii.member(jsii_name="installPackages")
    @builtins.classmethod
    def install_packages(
        cls,
        *,
        packages: typing.Sequence[builtins.str],
        sudo: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''Returns a shell command to check and install a Linux package using the available package manager.

        This function is useful for installing packages within a GitLab job when the system's package manager is uncertain.
        Currently supported package managers are: apk, apt-get, yum, dnf, and zypper.

        Keep in mind that this function supports installing only one package name. If different package managers have
        different names for the same package, this script might fail.

        Source: https://unix.stackexchange.com/a/571192/139685

        :param packages: A string listing all the packages to be installed, separated by spaces.
        :param sudo: Specifies whether the command(s) should be executed with sudo. Default: false

        :return: A shell command to install the specified package(s) using the available package manager.
        '''
        props = LinuxInstallPackageProps(packages=packages, sudo=sudo)

        return typing.cast(builtins.str, jsii.sinvoke(cls, "installPackages", [props]))


__all__ = [
    "LinuxInstallPackageProps",
    "LinuxScripts",
]

publication.publish()

def _typecheckingstub__d17faf0ce66d4b9e89af0a2ab53e0906338b3fedc80c356da28e121ee31b0529(
    *,
    packages: typing.Sequence[builtins.str],
    sudo: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
