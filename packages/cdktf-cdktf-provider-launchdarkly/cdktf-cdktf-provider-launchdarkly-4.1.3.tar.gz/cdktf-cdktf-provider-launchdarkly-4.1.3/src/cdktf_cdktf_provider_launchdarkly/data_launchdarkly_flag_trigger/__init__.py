'''
# `data_launchdarkly_flag_trigger`

Refer to the Terraform Registry for docs: [`data_launchdarkly_flag_trigger`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataLaunchdarklyFlagTrigger(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFlagTrigger.DataLaunchdarklyFlagTrigger",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger launchdarkly_flag_trigger}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        env_key: builtins.str,
        flag_key: builtins.str,
        id: builtins.str,
        project_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instructions: typing.Optional[typing.Union["DataLaunchdarklyFlagTriggerInstructions", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_key: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger launchdarkly_flag_trigger} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_key: The LaunchDarkly environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#env_key DataLaunchdarklyFlagTrigger#env_key}
        :param flag_key: The key of the feature flag the trigger acts upon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#flag_key DataLaunchdarklyFlagTrigger#flag_key}
        :param id: The flag trigger resource ID. This can be found on your trigger URL - please see docs for more info Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#id DataLaunchdarklyFlagTrigger#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_key: The LaunchDarkly project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#project_key DataLaunchdarklyFlagTrigger#project_key}
        :param enabled: Whether the trigger is currently active or not. This property defaults to true upon creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#enabled DataLaunchdarklyFlagTrigger#enabled}
        :param instructions: instructions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#instructions DataLaunchdarklyFlagTrigger#instructions}
        :param integration_key: The unique identifier of the integration you intend to set your trigger up with. "generic-trigger" should be used for integrations not explicitly supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#integration_key DataLaunchdarklyFlagTrigger#integration_key}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18be6e072efbbe9c79f5893dc5d43ff8e83877a46b78b4e7f729e9fd34c49a01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLaunchdarklyFlagTriggerConfig(
            env_key=env_key,
            flag_key=flag_key,
            id=id,
            project_key=project_key,
            enabled=enabled,
            instructions=instructions,
            integration_key=integration_key,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataLaunchdarklyFlagTrigger resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLaunchdarklyFlagTrigger to import.
        :param import_from_id: The id of the existing DataLaunchdarklyFlagTrigger that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLaunchdarklyFlagTrigger to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cde40aaecd304dc8c96e04d9a05fb2d3e4c0b94e399cb2720bf628c7b0882e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInstructions")
    def put_instructions(self, *, kind: builtins.str) -> None:
        '''
        :param kind: The action to perform when triggering. Currently supported flag actions are "turnFlagOn" and "turnFlagOff". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#kind DataLaunchdarklyFlagTrigger#kind}
        '''
        value = DataLaunchdarklyFlagTriggerInstructions(kind=kind)

        return typing.cast(None, jsii.invoke(self, "putInstructions", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetInstructions")
    def reset_instructions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstructions", []))

    @jsii.member(jsii_name="resetIntegrationKey")
    def reset_integration_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationKey", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="instructions")
    def instructions(self) -> "DataLaunchdarklyFlagTriggerInstructionsOutputReference":
        return typing.cast("DataLaunchdarklyFlagTriggerInstructionsOutputReference", jsii.get(self, "instructions"))

    @builtins.property
    @jsii.member(jsii_name="maintainerId")
    def maintainer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainerId"))

    @builtins.property
    @jsii.member(jsii_name="triggerUrl")
    def trigger_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerUrl"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="envKeyInput")
    def env_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="flagKeyInput")
    def flag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instructionsInput")
    def instructions_input(
        self,
    ) -> typing.Optional["DataLaunchdarklyFlagTriggerInstructions"]:
        return typing.cast(typing.Optional["DataLaunchdarklyFlagTriggerInstructions"], jsii.get(self, "instructionsInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationKeyInput")
    def integration_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635be505f732de67f271454cefc0f7a2c2c32bf0748c050d3e8cde20bac8d380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="envKey")
    def env_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envKey"))

    @env_key.setter
    def env_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44fc29d0a03bf929753139ea61714c7d53f7993d2cce7b47389cf023b4c4cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envKey", value)

    @builtins.property
    @jsii.member(jsii_name="flagKey")
    def flag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flagKey"))

    @flag_key.setter
    def flag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb21adc39c1eab2cb2a03be6d7cf4e805881a8e10e22dff87d6b043f6daa3e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flagKey", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c96ba119ad96cc9913ed819d254d52c546e1709e9ee1b07f5aecc0ba09d6ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="integrationKey")
    def integration_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationKey"))

    @integration_key.setter
    def integration_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a9ed543d4e56668997905ea5d5cd20a13e69febfc64d6c1864b99320249d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationKey", value)

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575605ccc4817650f2d75025db5e4cb0c055416859afca16cd42824444481d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFlagTrigger.DataLaunchdarklyFlagTriggerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "env_key": "envKey",
        "flag_key": "flagKey",
        "id": "id",
        "project_key": "projectKey",
        "enabled": "enabled",
        "instructions": "instructions",
        "integration_key": "integrationKey",
    },
)
class DataLaunchdarklyFlagTriggerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        env_key: builtins.str,
        flag_key: builtins.str,
        id: builtins.str,
        project_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instructions: typing.Optional[typing.Union["DataLaunchdarklyFlagTriggerInstructions", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_key: The LaunchDarkly environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#env_key DataLaunchdarklyFlagTrigger#env_key}
        :param flag_key: The key of the feature flag the trigger acts upon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#flag_key DataLaunchdarklyFlagTrigger#flag_key}
        :param id: The flag trigger resource ID. This can be found on your trigger URL - please see docs for more info Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#id DataLaunchdarklyFlagTrigger#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_key: The LaunchDarkly project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#project_key DataLaunchdarklyFlagTrigger#project_key}
        :param enabled: Whether the trigger is currently active or not. This property defaults to true upon creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#enabled DataLaunchdarklyFlagTrigger#enabled}
        :param instructions: instructions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#instructions DataLaunchdarklyFlagTrigger#instructions}
        :param integration_key: The unique identifier of the integration you intend to set your trigger up with. "generic-trigger" should be used for integrations not explicitly supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#integration_key DataLaunchdarklyFlagTrigger#integration_key}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(instructions, dict):
            instructions = DataLaunchdarklyFlagTriggerInstructions(**instructions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5035f89f2d6f39b0055a9fa8c745d6fd8d07edb45d3058407584bfb25fc0ac54)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument env_key", value=env_key, expected_type=type_hints["env_key"])
            check_type(argname="argument flag_key", value=flag_key, expected_type=type_hints["flag_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument instructions", value=instructions, expected_type=type_hints["instructions"])
            check_type(argname="argument integration_key", value=integration_key, expected_type=type_hints["integration_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env_key": env_key,
            "flag_key": flag_key,
            "id": id,
            "project_key": project_key,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if enabled is not None:
            self._values["enabled"] = enabled
        if instructions is not None:
            self._values["instructions"] = instructions
        if integration_key is not None:
            self._values["integration_key"] = integration_key

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def env_key(self) -> builtins.str:
        '''The LaunchDarkly environment key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#env_key DataLaunchdarklyFlagTrigger#env_key}
        '''
        result = self._values.get("env_key")
        assert result is not None, "Required property 'env_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flag_key(self) -> builtins.str:
        '''The key of the feature flag the trigger acts upon.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#flag_key DataLaunchdarklyFlagTrigger#flag_key}
        '''
        result = self._values.get("flag_key")
        assert result is not None, "Required property 'flag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The flag trigger resource ID.

        This can be found on your trigger URL - please see docs for more info

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#id DataLaunchdarklyFlagTrigger#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''The LaunchDarkly project key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#project_key DataLaunchdarklyFlagTrigger#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the trigger is currently active or not. This property defaults to true upon creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#enabled DataLaunchdarklyFlagTrigger#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def instructions(
        self,
    ) -> typing.Optional["DataLaunchdarklyFlagTriggerInstructions"]:
        '''instructions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#instructions DataLaunchdarklyFlagTrigger#instructions}
        '''
        result = self._values.get("instructions")
        return typing.cast(typing.Optional["DataLaunchdarklyFlagTriggerInstructions"], result)

    @builtins.property
    def integration_key(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the integration you intend to set your trigger up with.

        "generic-trigger" should be used for integrations not explicitly supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#integration_key DataLaunchdarklyFlagTrigger#integration_key}
        '''
        result = self._values.get("integration_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFlagTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFlagTrigger.DataLaunchdarklyFlagTriggerInstructions",
    jsii_struct_bases=[],
    name_mapping={"kind": "kind"},
)
class DataLaunchdarklyFlagTriggerInstructions:
    def __init__(self, *, kind: builtins.str) -> None:
        '''
        :param kind: The action to perform when triggering. Currently supported flag actions are "turnFlagOn" and "turnFlagOff". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#kind DataLaunchdarklyFlagTrigger#kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427f08c549989595caa6db049131fa89e8c1d630b31e68b677cbd3f1109dce0d)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
        }

    @builtins.property
    def kind(self) -> builtins.str:
        '''The action to perform when triggering. Currently supported flag actions are "turnFlagOn" and "turnFlagOff".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/flag_trigger#kind DataLaunchdarklyFlagTrigger#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFlagTriggerInstructions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFlagTriggerInstructionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFlagTrigger.DataLaunchdarklyFlagTriggerInstructionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e88f640785b515f89c2e90b990d27f962d4ceb2e3b064b5f986f06cde6b0f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f6f42a75cbb3f9f9e361c7da4f9e2a5fa80dccf34012a2c72d5b6260d2ae5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFlagTriggerInstructions]:
        return typing.cast(typing.Optional[DataLaunchdarklyFlagTriggerInstructions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFlagTriggerInstructions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77162ff4c655842408c093560ba6e7a5b9fe39268e7613b9523297b5e37964a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataLaunchdarklyFlagTrigger",
    "DataLaunchdarklyFlagTriggerConfig",
    "DataLaunchdarklyFlagTriggerInstructions",
    "DataLaunchdarklyFlagTriggerInstructionsOutputReference",
]

publication.publish()

def _typecheckingstub__18be6e072efbbe9c79f5893dc5d43ff8e83877a46b78b4e7f729e9fd34c49a01(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    env_key: builtins.str,
    flag_key: builtins.str,
    id: builtins.str,
    project_key: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instructions: typing.Optional[typing.Union[DataLaunchdarklyFlagTriggerInstructions, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_key: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cde40aaecd304dc8c96e04d9a05fb2d3e4c0b94e399cb2720bf628c7b0882e7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635be505f732de67f271454cefc0f7a2c2c32bf0748c050d3e8cde20bac8d380(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44fc29d0a03bf929753139ea61714c7d53f7993d2cce7b47389cf023b4c4cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb21adc39c1eab2cb2a03be6d7cf4e805881a8e10e22dff87d6b043f6daa3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c96ba119ad96cc9913ed819d254d52c546e1709e9ee1b07f5aecc0ba09d6ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a9ed543d4e56668997905ea5d5cd20a13e69febfc64d6c1864b99320249d0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575605ccc4817650f2d75025db5e4cb0c055416859afca16cd42824444481d7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5035f89f2d6f39b0055a9fa8c745d6fd8d07edb45d3058407584bfb25fc0ac54(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_key: builtins.str,
    flag_key: builtins.str,
    id: builtins.str,
    project_key: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instructions: typing.Optional[typing.Union[DataLaunchdarklyFlagTriggerInstructions, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427f08c549989595caa6db049131fa89e8c1d630b31e68b677cbd3f1109dce0d(
    *,
    kind: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e88f640785b515f89c2e90b990d27f962d4ceb2e3b064b5f986f06cde6b0f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f6f42a75cbb3f9f9e361c7da4f9e2a5fa80dccf34012a2c72d5b6260d2ae5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77162ff4c655842408c093560ba6e7a5b9fe39268e7613b9523297b5e37964a9(
    value: typing.Optional[DataLaunchdarklyFlagTriggerInstructions],
) -> None:
    """Type checking stubs"""
    pass
