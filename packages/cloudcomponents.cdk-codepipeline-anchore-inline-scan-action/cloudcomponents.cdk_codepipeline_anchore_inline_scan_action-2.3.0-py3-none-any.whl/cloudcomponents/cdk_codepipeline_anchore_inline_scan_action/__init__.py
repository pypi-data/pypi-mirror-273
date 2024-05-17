'''
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-codepipeline-anchore-inline-scan-action

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-codepipeline-anchore-inline-scan-action)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-codepipeline-anchore-inline-scan-action/)

> CodePipeline action to integrate [Anchore Engine](https://docs.anchore.com/current/) into your pipeline

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-codepipeline-anchore-inline-scan-action
```

Python:

```bash
pip install cloudcomponents.cdk-codepipeline-anchore-inline-scan-action
```

## How to use

```python
import { CodePipelineAnchoreInlineScanAction } from '@cloudcomponents/cdk-codepipeline-anchore-inline-scan-action';
import { CodePipelineDockerfileLinterAction } from '@cloudcomponents/cdk-codepipeline-dockerfile-linter-action';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Repository } from 'aws-cdk-lib/aws-codecommit';
import { Pipeline, Artifact } from 'aws-cdk-lib/aws-codepipeline';
import { CodeCommitSourceAction } from 'aws-cdk-lib/aws-codepipeline-actions';
import { Construct } from 'constructs';

export class ContainerAuditStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const repository = new Repository(this, 'Repository', {
      repositoryName: 'container-audit-repository',
    });

    const sourceArtifact = new Artifact();

    const sourceAction = new CodeCommitSourceAction({
      actionName: 'CodeCommit',
      repository,
      output: sourceArtifact,
      branch: 'master',
    });

    const linterAction = new CodePipelineDockerfileLinterAction({
      actionName: 'Linter',
      input: sourceArtifact,
    });

    const vulnScanAction = new CodePipelineAnchoreInlineScanAction({
      actionName: 'VulnScan',
      input: sourceArtifact,
    });

    new Pipeline(this, 'Pipeline', {
      pipelineName: 'container-audit-pipeline',
      stages: [
        {
          stageName: 'Source',
          actions: [sourceAction],
        },
        {
          stageName: 'Audit',
          actions: [linterAction, vulnScanAction],
        },
      ],
    });
  }
}
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-anchore-inline-scan-action/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-anchore-inline-scan-action/LICENSE)
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

import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_ceddda9d
import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_ceddda9d
import aws_cdk.aws_codepipeline_actions as _aws_cdk_aws_codepipeline_actions_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class CodePipelineAnchoreInlineScanAction(
    _aws_cdk_aws_codepipeline_actions_ceddda9d.Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-codepipeline-anchore-inline-scan-action.CodePipelineAnchoreInlineScanAction",
):
    def __init__(
        self,
        *,
        input: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        custom_anchore_image: typing.Optional[builtins.str] = None,
        ecr_login: typing.Optional[builtins.bool] = None,
        policy_bundle_path: typing.Optional[builtins.str] = None,
        project_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        timeout: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input: The source to use as input for this action.
        :param compute_type: The type of compute to use for backup the repositories. See the {@link ComputeType} enum for the possible values. Default: taken from {@link LinuxBuildImage.STANDARD_4_0#defaultComputeType}
        :param custom_anchore_image: This will override the image name from Dockerhub.
        :param ecr_login: Default: false
        :param policy_bundle_path: Path to local Anchore policy bundle. Default: ./policy_bundle.json
        :param project_role: -
        :param timeout: Specify timeout for image scanning in seconds. Default: 300
        :param version: Version of anchore ci-tools. Default: v0.8.2
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your ``IAction.bind`` method in the ``ActionBindOptions.role`` property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        '''
        props = CodePipelineAnchoreInlineScanActionProps(
            input=input,
            compute_type=compute_type,
            custom_anchore_image=custom_anchore_image,
            ecr_login=ecr_login,
            policy_bundle_path=policy_bundle_path,
            project_role=project_role,
            timeout=timeout,
            version=version,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _constructs_77d1e7e8.Construct,
        _stage: _aws_cdk_aws_codepipeline_ceddda9d.IStage,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> _aws_cdk_aws_codepipeline_ceddda9d.ActionConfig:
        '''This is a renamed version of the ``IAction.bind`` method.

        :param scope: -
        :param _stage: -
        :param bucket: 
        :param role: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0db02596e6cb6df774b36704a91bfe9ea19de334818f35e653d772649c7737b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument _stage", value=_stage, expected_type=type_hints["_stage"])
        options = _aws_cdk_aws_codepipeline_ceddda9d.ActionBindOptions(
            bucket=bucket, role=role
        )

        return typing.cast(_aws_cdk_aws_codepipeline_ceddda9d.ActionConfig, jsii.invoke(self, "bound", [scope, _stage, options]))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-codepipeline-anchore-inline-scan-action.CodePipelineAnchoreInlineScanActionProps",
    jsii_struct_bases=[_aws_cdk_aws_codepipeline_ceddda9d.CommonAwsActionProps],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "input": "input",
        "compute_type": "computeType",
        "custom_anchore_image": "customAnchoreImage",
        "ecr_login": "ecrLogin",
        "policy_bundle_path": "policyBundlePath",
        "project_role": "projectRole",
        "timeout": "timeout",
        "version": "version",
    },
)
class CodePipelineAnchoreInlineScanActionProps(
    _aws_cdk_aws_codepipeline_ceddda9d.CommonAwsActionProps,
):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        input: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        custom_anchore_image: typing.Optional[builtins.str] = None,
        ecr_login: typing.Optional[builtins.bool] = None,
        policy_bundle_path: typing.Optional[builtins.str] = None,
        project_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        timeout: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your ``IAction.bind`` method in the ``ActionBindOptions.role`` property. Default: a new Role will be generated
        :param input: The source to use as input for this action.
        :param compute_type: The type of compute to use for backup the repositories. See the {@link ComputeType} enum for the possible values. Default: taken from {@link LinuxBuildImage.STANDARD_4_0#defaultComputeType}
        :param custom_anchore_image: This will override the image name from Dockerhub.
        :param ecr_login: Default: false
        :param policy_bundle_path: Path to local Anchore policy bundle. Default: ./policy_bundle.json
        :param project_role: -
        :param timeout: Specify timeout for image scanning in seconds. Default: 300
        :param version: Version of anchore ci-tools. Default: v0.8.2
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad265ed580bc387a27b9ef61a320dac22cc7168e28fa23566b922743de25de4)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
            check_type(argname="argument variables_namespace", value=variables_namespace, expected_type=type_hints["variables_namespace"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument custom_anchore_image", value=custom_anchore_image, expected_type=type_hints["custom_anchore_image"])
            check_type(argname="argument ecr_login", value=ecr_login, expected_type=type_hints["ecr_login"])
            check_type(argname="argument policy_bundle_path", value=policy_bundle_path, expected_type=type_hints["policy_bundle_path"])
            check_type(argname="argument project_role", value=project_role, expected_type=type_hints["project_role"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_name": action_name,
            "input": input,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if custom_anchore_image is not None:
            self._values["custom_anchore_image"] = custom_anchore_image
        if ecr_login is not None:
            self._values["ecr_login"] = ecr_login
        if policy_bundle_path is not None:
            self._values["policy_bundle_path"] = policy_bundle_path
        if project_role is not None:
            self._values["project_role"] = project_role
        if timeout is not None:
            self._values["timeout"] = timeout
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def action_name(self) -> builtins.str:
        '''The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your ``IAction.bind``
        method in the ``ActionBindOptions.role`` property.

        :default: a new Role will be generated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def input(self) -> _aws_cdk_aws_codepipeline_ceddda9d.Artifact:
        '''The source to use as input for this action.'''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_aws_cdk_aws_codepipeline_ceddda9d.Artifact, result)

    @builtins.property
    def compute_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType]:
        '''The type of compute to use for backup the repositories.

        See the {@link ComputeType} enum for the possible values.

        :default: taken from {@link LinuxBuildImage.STANDARD_4_0#defaultComputeType}
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType], result)

    @builtins.property
    def custom_anchore_image(self) -> typing.Optional[builtins.str]:
        '''This will override the image name from Dockerhub.'''
        result = self._values.get("custom_anchore_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecr_login(self) -> typing.Optional[builtins.bool]:
        '''
        :default: false
        '''
        result = self._values.get("ecr_login")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def policy_bundle_path(self) -> typing.Optional[builtins.str]:
        '''Path to local Anchore policy bundle.

        :default: ./policy_bundle.json
        '''
        result = self._values.get("policy_bundle_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        result = self._values.get("project_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Specify timeout for image scanning in seconds.

        :default: 300
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of anchore ci-tools.

        :default: v0.8.2
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineAnchoreInlineScanActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CodePipelineAnchoreInlineScanAction",
    "CodePipelineAnchoreInlineScanActionProps",
]

publication.publish()

def _typecheckingstub__b0db02596e6cb6df774b36704a91bfe9ea19de334818f35e653d772649c7737b(
    scope: _constructs_77d1e7e8.Construct,
    _stage: _aws_cdk_aws_codepipeline_ceddda9d.IStage,
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad265ed580bc387a27b9ef61a320dac22cc7168e28fa23566b922743de25de4(
    *,
    action_name: builtins.str,
    run_order: typing.Optional[jsii.Number] = None,
    variables_namespace: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    input: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    custom_anchore_image: typing.Optional[builtins.str] = None,
    ecr_login: typing.Optional[builtins.bool] = None,
    policy_bundle_path: typing.Optional[builtins.str] = None,
    project_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    timeout: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
