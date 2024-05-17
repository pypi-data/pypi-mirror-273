[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-deletable-bucket

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-deletable-bucket)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-deletable-bucket/)

> Bucket with content cleanup to allow bucket deletion when the stack will be destroyed

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-deletable-bucket
```

Python:

```bash
pip install cloudcomponents.cdk-deletable-bucket
```

## How to use

```python
import { DeletableBucket } from '@cloudcomponents/cdk-deletable-bucket';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class DeletableBucketStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new DeletableBucket(this, 'DeletableBucket', {
      bucketName: 'bucket2delete',
      forceDelete: true,
    });
  }
}
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-deletable-bucket/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-deletable-bucket/LICENSE)
