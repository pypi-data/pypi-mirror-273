'''
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-secret-key

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-secret-key)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-secret-key/)

> Provide secret keys to lambdas

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-secret-key
```

Python:

```bash
pip install cloudcomponents.cdk-secret-key
```

## How to use

```python
import { SecretKey } from '@cloudcomponents/cdk-secret-key';

const secretKey = SecretKey.fromPlainText(process.env.SECRET_KEY as string);
const secretKeyString = secretKey.serialize(),
```

See [cloudcomponents/lambda-utils-nodejs](https://github.com/cloudcomponents/lambda-utils-nodejs) for the counterpart in lambda functions

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-secret-key/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-secret-key/LICENSE)
'''
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d


@jsii.enum(jsii_type="@cloudcomponents/cdk-secret-key.KeyType")
class KeyType(enum.Enum):
    SECRETS_MANAGER = "SECRETS_MANAGER"
    SSM_PARAMETER = "SSM_PARAMETER"
    PLAIN_TEXT = "PLAIN_TEXT"


class SecretKey(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cloudcomponents/cdk-secret-key.SecretKey",
):
    def __init__(self, secret_key_type: KeyType) -> None:
        '''
        :param secret_key_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aace37e201f8230f945f68ebb28137a30afe16d65d757c54a1980f7cc8dd833)
            check_type(argname="argument secret_key_type", value=secret_key_type, expected_type=type_hints["secret_key_type"])
        jsii.create(self.__class__, self, [secret_key_type])

    @jsii.member(jsii_name="fromPlainText")
    @builtins.classmethod
    def from_plain_text(cls, value: builtins.str) -> "SecretKey":
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43565191b35a50bfdeee54582a58b38e2ceaa31c5ddb8f04d34bc5fbc2cdd46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("SecretKey", jsii.sinvoke(cls, "fromPlainText", [value]))

    @jsii.member(jsii_name="fromSecretsManager")
    @builtins.classmethod
    def from_secrets_manager(
        cls,
        secret_key_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        field_name: typing.Optional[builtins.str] = None,
    ) -> "SecretKey":
        '''
        :param secret_key_secret: -
        :param field_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d63e539e56ca5128a9c359c4c650d7515b174678a164b0157d56f60ffab0c05)
            check_type(argname="argument secret_key_secret", value=secret_key_secret, expected_type=type_hints["secret_key_secret"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
        return typing.cast("SecretKey", jsii.sinvoke(cls, "fromSecretsManager", [secret_key_secret, field_name]))

    @jsii.member(jsii_name="fromSSMParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        secret_key_parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
    ) -> "SecretKey":
        '''
        :param secret_key_parameter: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1f0d09335484f4a84bc4c0c59d8a1cf52755e32aa8ceb0c51b69032e6bcde8)
            check_type(argname="argument secret_key_parameter", value=secret_key_parameter, expected_type=type_hints["secret_key_parameter"])
        return typing.cast("SecretKey", jsii.sinvoke(cls, "fromSSMParameter", [secret_key_parameter]))

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="serialize")
    @abc.abstractmethod
    def serialize(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="secretKeyType")
    def secret_key_type(self) -> KeyType:
        return typing.cast(KeyType, jsii.get(self, "secretKeyType"))


class _SecretKeyProxy(SecretKey):
    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d95d745387c79b7ddf51c1b7226bb2bf65e4d4cecbed05dc2236e16038f42cb)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "serialize", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SecretKey).__jsii_proxy_class__ = lambda : _SecretKeyProxy


class SecretKeyStore(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cloudcomponents/cdk-secret-key.SecretKeyStore",
):
    def __init__(self, secret_key_type: KeyType) -> None:
        '''
        :param secret_key_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9736d0c7e90d9a4365c2dc9433ae728fd43061ee3375c2acbe9c9744afcce2d6)
            check_type(argname="argument secret_key_type", value=secret_key_type, expected_type=type_hints["secret_key_type"])
        jsii.create(self.__class__, self, [secret_key_type])

    @jsii.member(jsii_name="fromSecretsManager")
    @builtins.classmethod
    def from_secrets_manager(
        cls,
        secret_key_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> "SecretKeyStore":
        '''
        :param secret_key_secret: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b3282b1d88bdd33235228e8acd63999512db58c753eebc599a4dc3937b6a48)
            check_type(argname="argument secret_key_secret", value=secret_key_secret, expected_type=type_hints["secret_key_secret"])
        return typing.cast("SecretKeyStore", jsii.sinvoke(cls, "fromSecretsManager", [secret_key_secret]))

    @jsii.member(jsii_name="fromSSMParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        secret_key_parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
    ) -> "SecretKeyStore":
        '''
        :param secret_key_parameter: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18437762a69c18cbe2ea14d25c98a67fe53095efd86a606539203b432ba80b26)
            check_type(argname="argument secret_key_parameter", value=secret_key_parameter, expected_type=type_hints["secret_key_parameter"])
        return typing.cast("SecretKeyStore", jsii.sinvoke(cls, "fromSSMParameter", [secret_key_parameter]))

    @jsii.member(jsii_name="grantWrite")
    @abc.abstractmethod
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="serialize")
    @abc.abstractmethod
    def serialize(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="secretKeyType")
    def secret_key_type(self) -> KeyType:
        return typing.cast(KeyType, jsii.get(self, "secretKeyType"))


class _SecretKeyStoreProxy(SecretKeyStore):
    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7053d97d3eab0684232d0fe359fe64243f3a60371bc22bd6a73c1dc963fd0b0f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "serialize", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SecretKeyStore).__jsii_proxy_class__ = lambda : _SecretKeyStoreProxy


__all__ = [
    "KeyType",
    "SecretKey",
    "SecretKeyStore",
]

publication.publish()

def _typecheckingstub__1aace37e201f8230f945f68ebb28137a30afe16d65d757c54a1980f7cc8dd833(
    secret_key_type: KeyType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43565191b35a50bfdeee54582a58b38e2ceaa31c5ddb8f04d34bc5fbc2cdd46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d63e539e56ca5128a9c359c4c650d7515b174678a164b0157d56f60ffab0c05(
    secret_key_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1f0d09335484f4a84bc4c0c59d8a1cf52755e32aa8ceb0c51b69032e6bcde8(
    secret_key_parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d95d745387c79b7ddf51c1b7226bb2bf65e4d4cecbed05dc2236e16038f42cb(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9736d0c7e90d9a4365c2dc9433ae728fd43061ee3375c2acbe9c9744afcce2d6(
    secret_key_type: KeyType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b3282b1d88bdd33235228e8acd63999512db58c753eebc599a4dc3937b6a48(
    secret_key_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18437762a69c18cbe2ea14d25c98a67fe53095efd86a606539203b432ba80b26(
    secret_key_parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7053d97d3eab0684232d0fe359fe64243f3a60371bc22bd6a73c1dc963fd0b0f(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass
