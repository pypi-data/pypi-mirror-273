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


class Sops(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.security.Sops"):
    @jsii.member(jsii_name="exportDecryptedValues")
    @builtins.classmethod
    def export_decrypted_values(
        cls,
        path: builtins.str,
        install_sops: typing.Optional[builtins.bool] = None,
        download_url: typing.Optional[builtins.str] = None,
    ) -> typing.List[builtins.str]:
        '''Returns a helper string that can be embedded into jobs to allow exporting values that are decrypted using ``sops``, for example: 'export $(sops -d sops/encrypted_file.env)'.

        This function is useful if you want to use environment variables to authenticate, for instance, with a container registry.

        The script has been successfully tested with SOPS version 3.7 and is intentionally NOT COMPATIBLE with SOPS version 3.6.
        This is due to a bug in the latter version, which wraps the values to be exported in quotes.

        :param path: - Path to the ``sops``-encrypted file. The path must be relative to the project directory.
        :param install_sops: - Enable downloading ``sops`` from the provided ``download_url``.ue.
        :param download_url: - Download URL to acquire ``sops`` from. Defaults to the GitHub Mozilla SOPS releases.

        :default: https://github.com/getsops/sops/releases/download/v3.7.3/sops-v3.7.3.linux.amd64

        :return: An array of strings representing the export statement for the ``sops``-decrypted file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b7265595754e06a92b65adc0988d5af077f0a6c036850ec5316e4e24760426)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument install_sops", value=install_sops, expected_type=type_hints["install_sops"])
            check_type(argname="argument download_url", value=download_url, expected_type=type_hints["download_url"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "exportDecryptedValues", [path, install_sops, download_url]))


__all__ = [
    "Sops",
]

publication.publish()

def _typecheckingstub__82b7265595754e06a92b65adc0988d5af077f0a6c036850ec5316e4e24760426(
    path: builtins.str,
    install_sops: typing.Optional[builtins.bool] = None,
    download_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
