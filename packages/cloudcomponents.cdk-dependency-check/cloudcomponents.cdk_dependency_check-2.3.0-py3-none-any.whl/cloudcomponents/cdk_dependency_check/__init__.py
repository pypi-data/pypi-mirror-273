'''
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-dependency-check

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-dependency-check)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-dependency-check/)

> [OWASP dependency-check](https://owasp.org/www-project-dependency-check/) for codecommit repositories

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-dependency-check
```

Python:

```bash
pip install cloudcomponents.cdk-dependency-check
```

## How to use

```python
import { CodeCommitDependencyCheck } from '@cloudcomponents/cdk-dependency-check';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Repository } from 'aws-cdk-lib/aws-codecommit';
import { Schedule } from 'aws-cdk-lib/aws-events';
import { SnsTopic } from 'aws-cdk-lib/aws-events-targets';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { Topic } from 'aws-cdk-lib/aws-sns';
import { EmailSubscription } from 'aws-cdk-lib/aws-sns-subscriptions';
import { Construct } from 'constructs';

export class DependencyCheckStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    if (typeof process.env.REPOSITORY_NAME === 'undefined') {
      throw new Error('environment variable REPOSITORY_NAME undefined');
    }

    const repository = Repository.fromRepositoryName(this, 'Repository', process.env.REPOSITORY_NAME);

    const reportsBucket = new Bucket(this, 'Bucket');

    // The following example runs a task every day at 4am
    const check = new CodeCommitDependencyCheck(this, 'CodeCommitDependencyCheck', {
      repository,
      reportsBucket,
      preCheckCommand: 'npm i',
      schedule: Schedule.cron({
        minute: '0',
        hour: '4',
      }),
    });

    const checkTopic = new Topic(this, 'CheckTopic');

    if (process.env.DEVSECOPS_TEAM_EMAIL) {
      checkTopic.addSubscription(new EmailSubscription(process.env.DEVSECOPS_TEAM_EMAIL));
    }

    check.onCheckStarted('started', {
      target: new SnsTopic(checkTopic),
    });

    check.onCheckSucceeded('succeeded', {
      target: new SnsTopic(checkTopic),
    });

    check.onCheckFailed('failed', {
      target: new SnsTopic(checkTopic),
    });
  }
}
```

## Upload HTML Reports

```python
const reportsBucket = new Bucket(this, 'Bucket');

// The following example runs a task every day at 4am
const check = new CodeCommitDependencyCheck(this, 'CodeCommitDependencyCheck', {
  repository,
  reportsBucket,
  preCheckCommand: 'npm i',
  schedule: Schedule.cron({
    minute: '0',
    hour: '4',
  }),
});
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-dependency-check/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-dependency-check/LICENSE)
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
import aws_cdk.aws_codecommit as _aws_cdk_aws_codecommit_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class CodeCommitDependencyCheck(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-dependency-check.CodeCommitDependencyCheck",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
        schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        enable_experimental: typing.Optional[builtins.bool] = None,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        fail_on_cvss: typing.Optional[jsii.Number] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_check_command: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        reports_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
        suppressions: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param repository: The repository to be checked.
        :param schedule: Schedule for dependency check.
        :param compute_type: The type of compute to use for check the repositories. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param enable_experimental: Enable the experimental analyzers. If not set the analyzers marked as experimental will not be loaded or used. Default: false
        :param excludes: The path patterns to exclude from the scan.
        :param fail_on_cvss: If the score set between 0 and 10 the exit code from dependency-check will indicate if a vulnerability with a CVSS score equal to or higher was identified. Default: 0
        :param paths: The paths to scan. Basedir repositoryDir Default: the repositoryDir
        :param pre_check_command: Custom command to be executed before the dependency check. Default: ``echo "No preCheckCommand!"``
        :param project_name: The name of the project being scanned. - @default taken from {@link #repository#repositoryName}
        :param reports_bucket: Bucket for uploading html reports.
        :param suppressions: The file paths to the suppression XML files; used to suppress false positives.
        :param version: Version of the dependency check. Default: 5.3.2
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e8b10d31463ada9c354ae57b097b31f0725606b6eda7c2803c93df4ca9f22f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeCommitDependencyCheckProps(
            repository=repository,
            schedule=schedule,
            compute_type=compute_type,
            enable_experimental=enable_experimental,
            excludes=excludes,
            fail_on_cvss=fail_on_cvss,
            paths=paths,
            pre_check_command=pre_check_command,
            project_name=project_name,
            reports_bucket=reports_bucket,
            suppressions=suppressions,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="onCheckFailed")
    def on_check_failed(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''Defines an event rule which triggers when a check fails.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f0f7d85164f67fa4315cf0cbaff4bf5bd37b168be0650aa6fb4dfb1ffa7d82)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onCheckFailed", [id, options]))

    @jsii.member(jsii_name="onCheckStarted")
    def on_check_started(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''Defines an event rule which triggers when a check starts.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a346b73ee4b886833d4915f19e9a9c3ab067a3c22d983ce3224dbf6a4a5307)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onCheckStarted", [id, options]))

    @jsii.member(jsii_name="onCheckSucceeded")
    def on_check_succeeded(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''Defines an event rule which triggers when a check complets successfully.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b45ac81d3563478b33f6e47859d5d0d1b1879f9796ea61018dd2f61edd9a68)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onCheckSucceeded", [id, options]))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-dependency-check.CodeCommitDependencyCheckProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository": "repository",
        "schedule": "schedule",
        "compute_type": "computeType",
        "enable_experimental": "enableExperimental",
        "excludes": "excludes",
        "fail_on_cvss": "failOnCVSS",
        "paths": "paths",
        "pre_check_command": "preCheckCommand",
        "project_name": "projectName",
        "reports_bucket": "reportsBucket",
        "suppressions": "suppressions",
        "version": "version",
    },
)
class CodeCommitDependencyCheckProps:
    def __init__(
        self,
        *,
        repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
        schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        enable_experimental: typing.Optional[builtins.bool] = None,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        fail_on_cvss: typing.Optional[jsii.Number] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_check_command: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        reports_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
        suppressions: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The repository to be checked.
        :param schedule: Schedule for dependency check.
        :param compute_type: The type of compute to use for check the repositories. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param enable_experimental: Enable the experimental analyzers. If not set the analyzers marked as experimental will not be loaded or used. Default: false
        :param excludes: The path patterns to exclude from the scan.
        :param fail_on_cvss: If the score set between 0 and 10 the exit code from dependency-check will indicate if a vulnerability with a CVSS score equal to or higher was identified. Default: 0
        :param paths: The paths to scan. Basedir repositoryDir Default: the repositoryDir
        :param pre_check_command: Custom command to be executed before the dependency check. Default: ``echo "No preCheckCommand!"``
        :param project_name: The name of the project being scanned. - @default taken from {@link #repository#repositoryName}
        :param reports_bucket: Bucket for uploading html reports.
        :param suppressions: The file paths to the suppression XML files; used to suppress false positives.
        :param version: Version of the dependency check. Default: 5.3.2
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812bb3eca87a2e05cddf3142e0ad0afcd6243d343cd0f414edcb66f740215326)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument enable_experimental", value=enable_experimental, expected_type=type_hints["enable_experimental"])
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument fail_on_cvss", value=fail_on_cvss, expected_type=type_hints["fail_on_cvss"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument pre_check_command", value=pre_check_command, expected_type=type_hints["pre_check_command"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument reports_bucket", value=reports_bucket, expected_type=type_hints["reports_bucket"])
            check_type(argname="argument suppressions", value=suppressions, expected_type=type_hints["suppressions"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
            "schedule": schedule,
        }
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if enable_experimental is not None:
            self._values["enable_experimental"] = enable_experimental
        if excludes is not None:
            self._values["excludes"] = excludes
        if fail_on_cvss is not None:
            self._values["fail_on_cvss"] = fail_on_cvss
        if paths is not None:
            self._values["paths"] = paths
        if pre_check_command is not None:
            self._values["pre_check_command"] = pre_check_command
        if project_name is not None:
            self._values["project_name"] = project_name
        if reports_bucket is not None:
            self._values["reports_bucket"] = reports_bucket
        if suppressions is not None:
            self._values["suppressions"] = suppressions
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def repository(self) -> _aws_cdk_aws_codecommit_ceddda9d.IRepository:
        '''The repository to be checked.'''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_aws_cdk_aws_codecommit_ceddda9d.IRepository, result)

    @builtins.property
    def schedule(self) -> _aws_cdk_aws_events_ceddda9d.Schedule:
        '''Schedule for dependency check.'''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Schedule, result)

    @builtins.property
    def compute_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType]:
        '''The type of compute to use for check the repositories.

        See the {@link ComputeType} enum for the possible values.

        :default: taken from {@link #buildImage#defaultComputeType}
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType], result)

    @builtins.property
    def enable_experimental(self) -> typing.Optional[builtins.bool]:
        '''Enable the experimental analyzers.

        If not set the analyzers marked as experimental will not be loaded or used.

        :default: false
        '''
        result = self._values.get("enable_experimental")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The path patterns to exclude from the scan.'''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fail_on_cvss(self) -> typing.Optional[jsii.Number]:
        '''If the score set between 0 and 10 the exit code from dependency-check will indicate if a vulnerability with a CVSS score equal to or higher was identified.

        :default: 0
        '''
        result = self._values.get("fail_on_cvss")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The paths to scan.

        Basedir repositoryDir

        :default: the repositoryDir
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pre_check_command(self) -> typing.Optional[builtins.str]:
        '''Custom command to be executed before the dependency check.

        :default: ``echo "No preCheckCommand!"``
        '''
        result = self._values.get("pre_check_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''The name of the project being scanned.

        - @default taken from {@link #repository#repositoryName}
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reports_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket]:
        '''Bucket for uploading html reports.'''
        result = self._values.get("reports_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket], result)

    @builtins.property
    def suppressions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The file paths to the suppression XML files;

        used to suppress false positives.
        '''
        result = self._values.get("suppressions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the dependency check.

        :default: 5.3.2
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitDependencyCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CodeCommitDependencyCheck",
    "CodeCommitDependencyCheckProps",
]

publication.publish()

def _typecheckingstub__b7e8b10d31463ada9c354ae57b097b31f0725606b6eda7c2803c93df4ca9f22f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
    schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    enable_experimental: typing.Optional[builtins.bool] = None,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    fail_on_cvss: typing.Optional[jsii.Number] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_check_command: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    reports_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
    suppressions: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f0f7d85164f67fa4315cf0cbaff4bf5bd37b168be0650aa6fb4dfb1ffa7d82(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a346b73ee4b886833d4915f19e9a9c3ab067a3c22d983ce3224dbf6a4a5307(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b45ac81d3563478b33f6e47859d5d0d1b1879f9796ea61018dd2f61edd9a68(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812bb3eca87a2e05cddf3142e0ad0afcd6243d343cd0f414edcb66f740215326(
    *,
    repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
    schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    enable_experimental: typing.Optional[builtins.bool] = None,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    fail_on_cvss: typing.Optional[jsii.Number] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_check_command: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    reports_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.Bucket] = None,
    suppressions: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
