'''
# `data_launchdarkly_metric`

Refer to the Terraform Registry for docs: [`data_launchdarkly_metric`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric).
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


class DataLaunchdarklyMetric(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyMetric.DataLaunchdarklyMetric",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric launchdarkly_metric}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        event_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kind: typing.Optional[builtins.str] = None,
        maintainer_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
        selector: typing.Optional[builtins.str] = None,
        success_criteria: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
        urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyMetricUrls", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric launchdarkly_metric} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key: A unique key that will be used to reference the metric in your code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#key DataLaunchdarklyMetric#key}
        :param project_key: The LaunchDarkly project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#project_key DataLaunchdarklyMetric#project_key}
        :param description: A short description of what the metric will be used for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#description DataLaunchdarklyMetric#description}
        :param event_key: The event key for your metric (if custom metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#event_key DataLaunchdarklyMetric#event_key}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#id DataLaunchdarklyMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_active: Whether the metric is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#is_active DataLaunchdarklyMetric#is_active}
        :param is_numeric: Whether the metric is numeric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#is_numeric DataLaunchdarklyMetric#is_numeric}
        :param kind: The metric type -available choices are 'pageview', 'click', and 'custom'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#kind DataLaunchdarklyMetric#kind}
        :param maintainer_id: The LaunchDarkly ID of the user who will maintain the metric. If not set, the API will automatically apply the member associated with your Terraform API key or the most recently-set maintainer Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#maintainer_id DataLaunchdarklyMetric#maintainer_id}
        :param name: A human-readable name for your metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#name DataLaunchdarklyMetric#name}
        :param randomization_units: A set of one or more context kinds that this metric can measure events from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#randomization_units DataLaunchdarklyMetric#randomization_units}
        :param selector: The CSS selector for your metric (if click metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#selector DataLaunchdarklyMetric#selector}
        :param success_criteria: The success criteria for your metric (if numeric metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#success_criteria DataLaunchdarklyMetric#success_criteria}
        :param unit: The unit for your metric (if numeric metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#unit DataLaunchdarklyMetric#unit}
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#urls DataLaunchdarklyMetric#urls}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940870d658f81b181094dce03c0c5abcd0470099082422f7d39fee188ac01dd2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLaunchdarklyMetricConfig(
            key=key,
            project_key=project_key,
            description=description,
            event_key=event_key,
            id=id,
            is_active=is_active,
            is_numeric=is_numeric,
            kind=kind,
            maintainer_id=maintainer_id,
            name=name,
            randomization_units=randomization_units,
            selector=selector,
            success_criteria=success_criteria,
            unit=unit,
            urls=urls,
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
        '''Generates CDKTF code for importing a DataLaunchdarklyMetric resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLaunchdarklyMetric to import.
        :param import_from_id: The id of the existing DataLaunchdarklyMetric that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLaunchdarklyMetric to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b658093c5ff8c90baca64fe00d4ab21afde9de87023ffc429da18df2c113f5b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putUrls")
    def put_urls(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyMetricUrls", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61263f076154d7c62c447f6a969ff2ca48352fb17f4e328c789c41c5d20359a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrls", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEventKey")
    def reset_event_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventKey", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsActive")
    def reset_is_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsActive", []))

    @jsii.member(jsii_name="resetIsNumeric")
    def reset_is_numeric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsNumeric", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

    @jsii.member(jsii_name="resetMaintainerId")
    def reset_maintainer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainerId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRandomizationUnits")
    def reset_randomization_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRandomizationUnits", []))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @jsii.member(jsii_name="resetSuccessCriteria")
    def reset_success_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessCriteria", []))

    @jsii.member(jsii_name="resetUnit")
    def reset_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnit", []))

    @jsii.member(jsii_name="resetUrls")
    def reset_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrls", []))

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(self) -> "DataLaunchdarklyMetricUrlsList":
        return typing.cast("DataLaunchdarklyMetricUrlsList", jsii.get(self, "urls"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventKeyInput")
    def event_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isActiveInput")
    def is_active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isActiveInput"))

    @builtins.property
    @jsii.member(jsii_name="isNumericInput")
    def is_numeric_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isNumericInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainerIdInput")
    def maintainer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="randomizationUnitsInput")
    def randomization_units_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "randomizationUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="successCriteriaInput")
    def success_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="urlsInput")
    def urls_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyMetricUrls"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyMetricUrls"]]], jsii.get(self, "urlsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af427a083dfface80881669fd8530eeb96211e75203874b8091a5fed1dea2ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="eventKey")
    def event_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventKey"))

    @event_key.setter
    def event_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8190a2dff984f99f696691c6b58342f7a4958a091e1dd0048e78ba2bd4570375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventKey", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa51a7e41fc9e365a16a76a19a8ed6fac24f8ada5cd1e3901c2a92aa1466e200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isActive")
    def is_active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isActive"))

    @is_active.setter
    def is_active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86b00a416118b5be88a78967c67dd23c80caf14062f8b0a0a2b9a57606a94d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isActive", value)

    @builtins.property
    @jsii.member(jsii_name="isNumeric")
    def is_numeric(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isNumeric"))

    @is_numeric.setter
    def is_numeric(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aed97f44dc9a834d70ec621596b4899f524ba7d31e73500b1b8b4074b2c0afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isNumeric", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30dae8ea58a9b818574df64339c065802fc6a1064b4b3a359a5ec49b4063a448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a368119e142cc338941bbd7138cd335006052b23728b152d46289bc050f82431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="maintainerId")
    def maintainer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainerId"))

    @maintainer_id.setter
    def maintainer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8089986dffdd0da7b1f16fc43341cad59a0d32af62ac7ec7cc1d4e4a64335c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainerId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9470896a5b40b891cba6ec943c0ac4815633e421baa43e2c6082b1a9bbc14670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648f0e3bdd123fac226694060f2a7f96a139bd757e807540114e54850b0b55a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value)

    @builtins.property
    @jsii.member(jsii_name="randomizationUnits")
    def randomization_units(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "randomizationUnits"))

    @randomization_units.setter
    def randomization_units(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1881ff2fae1fee061cda847d181d545e8c1913b6af30e7d34cddbb716cf0786a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "randomizationUnits", value)

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888437ecd2a4d4cc2e8ef95a3dccbd5e1ed7dfd0d996475e5cf167f192962008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value)

    @builtins.property
    @jsii.member(jsii_name="successCriteria")
    def success_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successCriteria"))

    @success_criteria.setter
    def success_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28d2e3067faaaed83f99ebacc7ace4be7ffd745e192b90536c49ceee5006c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successCriteria", value)

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9985ac84583cc18974623fc572821382caafcfa5a5314b6cbca5f64a31e2afe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyMetric.DataLaunchdarklyMetricConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key": "key",
        "project_key": "projectKey",
        "description": "description",
        "event_key": "eventKey",
        "id": "id",
        "is_active": "isActive",
        "is_numeric": "isNumeric",
        "kind": "kind",
        "maintainer_id": "maintainerId",
        "name": "name",
        "randomization_units": "randomizationUnits",
        "selector": "selector",
        "success_criteria": "successCriteria",
        "unit": "unit",
        "urls": "urls",
    },
)
class DataLaunchdarklyMetricConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        event_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kind: typing.Optional[builtins.str] = None,
        maintainer_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
        selector: typing.Optional[builtins.str] = None,
        success_criteria: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
        urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyMetricUrls", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key: A unique key that will be used to reference the metric in your code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#key DataLaunchdarklyMetric#key}
        :param project_key: The LaunchDarkly project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#project_key DataLaunchdarklyMetric#project_key}
        :param description: A short description of what the metric will be used for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#description DataLaunchdarklyMetric#description}
        :param event_key: The event key for your metric (if custom metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#event_key DataLaunchdarklyMetric#event_key}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#id DataLaunchdarklyMetric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_active: Whether the metric is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#is_active DataLaunchdarklyMetric#is_active}
        :param is_numeric: Whether the metric is numeric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#is_numeric DataLaunchdarklyMetric#is_numeric}
        :param kind: The metric type -available choices are 'pageview', 'click', and 'custom'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#kind DataLaunchdarklyMetric#kind}
        :param maintainer_id: The LaunchDarkly ID of the user who will maintain the metric. If not set, the API will automatically apply the member associated with your Terraform API key or the most recently-set maintainer Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#maintainer_id DataLaunchdarklyMetric#maintainer_id}
        :param name: A human-readable name for your metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#name DataLaunchdarklyMetric#name}
        :param randomization_units: A set of one or more context kinds that this metric can measure events from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#randomization_units DataLaunchdarklyMetric#randomization_units}
        :param selector: The CSS selector for your metric (if click metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#selector DataLaunchdarklyMetric#selector}
        :param success_criteria: The success criteria for your metric (if numeric metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#success_criteria DataLaunchdarklyMetric#success_criteria}
        :param unit: The unit for your metric (if numeric metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#unit DataLaunchdarklyMetric#unit}
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#urls DataLaunchdarklyMetric#urls}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e7dd175594ceed19a99d810c24f0f6258ee9cd02779a36f8dc3326a139dca9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_key", value=event_key, expected_type=type_hints["event_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            check_type(argname="argument is_numeric", value=is_numeric, expected_type=type_hints["is_numeric"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument maintainer_id", value=maintainer_id, expected_type=type_hints["maintainer_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument randomization_units", value=randomization_units, expected_type=type_hints["randomization_units"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument success_criteria", value=success_criteria, expected_type=type_hints["success_criteria"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
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
        if description is not None:
            self._values["description"] = description
        if event_key is not None:
            self._values["event_key"] = event_key
        if id is not None:
            self._values["id"] = id
        if is_active is not None:
            self._values["is_active"] = is_active
        if is_numeric is not None:
            self._values["is_numeric"] = is_numeric
        if kind is not None:
            self._values["kind"] = kind
        if maintainer_id is not None:
            self._values["maintainer_id"] = maintainer_id
        if name is not None:
            self._values["name"] = name
        if randomization_units is not None:
            self._values["randomization_units"] = randomization_units
        if selector is not None:
            self._values["selector"] = selector
        if success_criteria is not None:
            self._values["success_criteria"] = success_criteria
        if unit is not None:
            self._values["unit"] = unit
        if urls is not None:
            self._values["urls"] = urls

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
    def key(self) -> builtins.str:
        '''A unique key that will be used to reference the metric in your code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#key DataLaunchdarklyMetric#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''The LaunchDarkly project key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#project_key DataLaunchdarklyMetric#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A short description of what the metric will be used for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#description DataLaunchdarklyMetric#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_key(self) -> typing.Optional[builtins.str]:
        '''The event key for your metric (if custom metric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#event_key DataLaunchdarklyMetric#event_key}
        '''
        result = self._values.get("event_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#id DataLaunchdarklyMetric#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the metric is active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#is_active DataLaunchdarklyMetric#is_active}
        '''
        result = self._values.get("is_active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_numeric(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the metric is numeric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#is_numeric DataLaunchdarklyMetric#is_numeric}
        '''
        result = self._values.get("is_numeric")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''The metric type -available choices are 'pageview', 'click', and 'custom'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#kind DataLaunchdarklyMetric#kind}
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintainer_id(self) -> typing.Optional[builtins.str]:
        '''The LaunchDarkly ID of the user who will maintain the metric.

        If not set, the API will automatically apply the member associated with your Terraform API key or the most recently-set maintainer

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#maintainer_id DataLaunchdarklyMetric#maintainer_id}
        '''
        result = self._values.get("maintainer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A human-readable name for your metric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#name DataLaunchdarklyMetric#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def randomization_units(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of one or more context kinds that this metric can measure events from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#randomization_units DataLaunchdarklyMetric#randomization_units}
        '''
        result = self._values.get("randomization_units")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def selector(self) -> typing.Optional[builtins.str]:
        '''The CSS selector for your metric (if click metric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#selector DataLaunchdarklyMetric#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_criteria(self) -> typing.Optional[builtins.str]:
        '''The success criteria for your metric (if numeric metric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#success_criteria DataLaunchdarklyMetric#success_criteria}
        '''
        result = self._values.get("success_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''The unit for your metric (if numeric metric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#unit DataLaunchdarklyMetric#unit}
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def urls(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyMetricUrls"]]]:
        '''urls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#urls DataLaunchdarklyMetric#urls}
        '''
        result = self._values.get("urls")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyMetricUrls"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyMetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyMetric.DataLaunchdarklyMetricUrls",
    jsii_struct_bases=[],
    name_mapping={
        "kind": "kind",
        "pattern": "pattern",
        "substring": "substring",
        "url": "url",
    },
)
class DataLaunchdarklyMetricUrls:
    def __init__(
        self,
        *,
        kind: builtins.str,
        pattern: typing.Optional[builtins.str] = None,
        substring: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: The url type - available choices are 'exact', 'canonical', 'substring' and 'regex'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#kind DataLaunchdarklyMetric#kind}
        :param pattern: The URL-matching regex. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#pattern DataLaunchdarklyMetric#pattern}
        :param substring: The URL substring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#substring DataLaunchdarklyMetric#substring}
        :param url: The exact or canonical URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#url DataLaunchdarklyMetric#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17be6f52ff7b594d336bd7722da74adc4c2ebbae3659610d20c305cddd8aa1e)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument substring", value=substring, expected_type=type_hints["substring"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
        }
        if pattern is not None:
            self._values["pattern"] = pattern
        if substring is not None:
            self._values["substring"] = substring
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def kind(self) -> builtins.str:
        '''The url type - available choices are 'exact', 'canonical', 'substring' and 'regex'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#kind DataLaunchdarklyMetric#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''The URL-matching regex.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#pattern DataLaunchdarklyMetric#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def substring(self) -> typing.Optional[builtins.str]:
        '''The URL substring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#substring DataLaunchdarklyMetric#substring}
        '''
        result = self._values.get("substring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The exact or canonical URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.18.3/docs/data-sources/metric#url DataLaunchdarklyMetric#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyMetricUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyMetricUrlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyMetric.DataLaunchdarklyMetricUrlsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7558e798b41e0af59f96dda5800ba2ad43cddfb11eace1d86474f213efd4fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataLaunchdarklyMetricUrlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a050990c264da4bb2752eadd38b2a6b52cf514bc9c5f8eb3cb91a0380f1e014)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyMetricUrlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d755a405a52c6380a3a6f930c46d6bd44bad00a8ae50a38beaf3c06948db9bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25347935fcbae3eb4a95860f01097cdeebf4ffb653ed280d2460bfa1a2beb364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060da9c7c2f8b00b603720ffdc55f0f08971229a9851123e2870f586f4ce198d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyMetricUrls]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyMetricUrls]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyMetricUrls]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc5e2d4e4e153c7b7670e3c73041c3627312103a30edad067613d59f6a4f3b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklyMetricUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyMetric.DataLaunchdarklyMetricUrlsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1deabdcf1e664b22424aa37e17a9f29c1e927a523829fde0f04e870ec04db87b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @jsii.member(jsii_name="resetSubstring")
    def reset_substring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstring", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="substringInput")
    def substring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "substringInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cda0550ece72b754024d95a115ea62739daa0b3bd974b6c5fe3bee05387b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1711bf218d352e521f163607b0062f6df858678e41bf2e060fe8821bcf020535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="substring")
    def substring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "substring"))

    @substring.setter
    def substring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6449c3d2970b62d2cb6a1a7702ca9d6784dfbe87076281bffd2ebff562f59f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substring", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc2bb059df45607b30dbddb72e915d0e735919a0cd96148dcef66dd4cc55167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyMetricUrls]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyMetricUrls]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyMetricUrls]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c068621f915b4dc6778aa80dd2719da54642007cbcf535ed52327c2db03a68c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataLaunchdarklyMetric",
    "DataLaunchdarklyMetricConfig",
    "DataLaunchdarklyMetricUrls",
    "DataLaunchdarklyMetricUrlsList",
    "DataLaunchdarklyMetricUrlsOutputReference",
]

publication.publish()

def _typecheckingstub__940870d658f81b181094dce03c0c5abcd0470099082422f7d39fee188ac01dd2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    event_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kind: typing.Optional[builtins.str] = None,
    maintainer_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    selector: typing.Optional[builtins.str] = None,
    success_criteria: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
    urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyMetricUrls, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__b658093c5ff8c90baca64fe00d4ab21afde9de87023ffc429da18df2c113f5b7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61263f076154d7c62c447f6a969ff2ca48352fb17f4e328c789c41c5d20359a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyMetricUrls, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af427a083dfface80881669fd8530eeb96211e75203874b8091a5fed1dea2ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8190a2dff984f99f696691c6b58342f7a4958a091e1dd0048e78ba2bd4570375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa51a7e41fc9e365a16a76a19a8ed6fac24f8ada5cd1e3901c2a92aa1466e200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86b00a416118b5be88a78967c67dd23c80caf14062f8b0a0a2b9a57606a94d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aed97f44dc9a834d70ec621596b4899f524ba7d31e73500b1b8b4074b2c0afc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30dae8ea58a9b818574df64339c065802fc6a1064b4b3a359a5ec49b4063a448(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a368119e142cc338941bbd7138cd335006052b23728b152d46289bc050f82431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8089986dffdd0da7b1f16fc43341cad59a0d32af62ac7ec7cc1d4e4a64335c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9470896a5b40b891cba6ec943c0ac4815633e421baa43e2c6082b1a9bbc14670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648f0e3bdd123fac226694060f2a7f96a139bd757e807540114e54850b0b55a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1881ff2fae1fee061cda847d181d545e8c1913b6af30e7d34cddbb716cf0786a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888437ecd2a4d4cc2e8ef95a3dccbd5e1ed7dfd0d996475e5cf167f192962008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28d2e3067faaaed83f99ebacc7ace4be7ffd745e192b90536c49ceee5006c8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9985ac84583cc18974623fc572821382caafcfa5a5314b6cbca5f64a31e2afe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e7dd175594ceed19a99d810c24f0f6258ee9cd02779a36f8dc3326a139dca9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    event_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kind: typing.Optional[builtins.str] = None,
    maintainer_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    selector: typing.Optional[builtins.str] = None,
    success_criteria: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
    urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyMetricUrls, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17be6f52ff7b594d336bd7722da74adc4c2ebbae3659610d20c305cddd8aa1e(
    *,
    kind: builtins.str,
    pattern: typing.Optional[builtins.str] = None,
    substring: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7558e798b41e0af59f96dda5800ba2ad43cddfb11eace1d86474f213efd4fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a050990c264da4bb2752eadd38b2a6b52cf514bc9c5f8eb3cb91a0380f1e014(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d755a405a52c6380a3a6f930c46d6bd44bad00a8ae50a38beaf3c06948db9bcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25347935fcbae3eb4a95860f01097cdeebf4ffb653ed280d2460bfa1a2beb364(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060da9c7c2f8b00b603720ffdc55f0f08971229a9851123e2870f586f4ce198d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc5e2d4e4e153c7b7670e3c73041c3627312103a30edad067613d59f6a4f3b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyMetricUrls]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1deabdcf1e664b22424aa37e17a9f29c1e927a523829fde0f04e870ec04db87b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cda0550ece72b754024d95a115ea62739daa0b3bd974b6c5fe3bee05387b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1711bf218d352e521f163607b0062f6df858678e41bf2e060fe8821bcf020535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6449c3d2970b62d2cb6a1a7702ca9d6784dfbe87076281bffd2ebff562f59f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc2bb059df45607b30dbddb72e915d0e735919a0cd96148dcef66dd4cc55167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c068621f915b4dc6778aa80dd2719da54642007cbcf535ed52327c2db03a68c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyMetricUrls]],
) -> None:
    """Type checking stubs"""
    pass
