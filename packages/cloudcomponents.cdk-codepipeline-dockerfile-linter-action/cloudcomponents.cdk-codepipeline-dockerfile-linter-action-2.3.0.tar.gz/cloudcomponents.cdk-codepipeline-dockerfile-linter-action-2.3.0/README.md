[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-codepipeline-dockerfile-linter-action

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-codepipeline-dockerfile-linter-action)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-codepipeline-dockerfile-linter-action/)

> CodePipeline action to lint dockerfiles with [hadolint](https://github.com/hadolint/hadolint)

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-codepipeline-dockerfile-linter-action
```

Python:

```bash
pip install cloudcomponents.cdk-codepipeline-dockerfile-linter-action
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

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-dockerfile-linter-action/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-dockerfile-linter-action/LICENSE)
