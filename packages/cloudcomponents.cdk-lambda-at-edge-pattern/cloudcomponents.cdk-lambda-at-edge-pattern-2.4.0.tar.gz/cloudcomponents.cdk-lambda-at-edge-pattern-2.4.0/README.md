[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-lambda-at-edge-pattern

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-lambda-at-edge-pattern)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-lambda-at-edge-pattern/)

> CDK Constructs for Lambda@Edge pattern: HttpHeaders

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-lambda-at-edge-pattern
```

Python:

```bash
pip install cloudcomponents.cdk-lambda-at-edge-pattern
```

## How to use

```python
import { StaticWebsite } from '@cloudcomponents/cdk-static-website';
import { OriginMutation } from '@cloudcomponents/cdk-lambda-at-edge-pattern';
import { RemovalPolicy, Stack, StackProps, aws_route53 } from 'aws-cdk-lib';

import { Construct } from 'constructs';

export class StaticWebsiteStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    const hostedZone = aws_route53.HostedZone.fromLookup(this, 'HostedZone', {
      domainName: 'cloudcomponents.org',
    });

    // Create a lambda at edge
    const originMutation = new OriginMutation(stack, 'OriginMutation');

    new StaticWebsite(this, 'StaticWebsite', {
      hostedZone,
      domainNames: ['cloudcomponents.org', 'www.cloudcomponents.org'],
      edgeLambdas: [originMutation],
      removalPolicy: RemovalPolicy.DESTROY,
    });
  }
}
```

### Cloudfront Distribution

```python
new cloudfront.Distribution(this, 'myDist', {
  defaultBehavior: {
    origin: new origins.S3Origin(myBucket),
    edgeLambdas: [httpHeaders],
  },
});
```

### HttpHeaders

```python
const httpHeaders = new HttpHeaders(this, 'HttpHeaders', {
  httpHeaders: {
    'Content-Security-Policy':
      "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; object-src 'none'; connect-src 'self'",
    'Strict-Transport-Security':
      'max-age=31536000; includeSubdomains; preload',
    'Referrer-Policy': 'same-origin',
    'X-XSS-Protection': '1; mode=block',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Cache-Control': 'no-cache',
  },
});
```

### OriginMutation

https://chrisschuld.com/2020/05/gatsby-hosting-on-cloudfront/

```python
const originMutation = new OriginMutation(stack, 'OriginMutation');
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-lambda-at-edge-pattern/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-lambda-at-edge-pattern/LICENSE)
