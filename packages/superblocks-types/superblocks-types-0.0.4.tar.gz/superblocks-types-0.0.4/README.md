# types

[![default](https://github.com/superblocksteam/types/actions/workflows/default.yaml/badge.svg)](https://github.com/superblocksteam/types/actions/workflows/default.yaml)

## About

This is the **NEW HOME** for Superblocks types as we migrate to Protobuf! Unsure if you're type should live here? If you answer **yes** to any of the following, it should live here! Still not sure? Ask Frank!

1. Will your type be used across services?
2. Are you using gRPC?
3. Part of our public APIs?

## Usage

**Node.js**

```json
{
    "dependencies": {
        "@superblocksteam/types": "*",
        "@superblocksteam/types": "file:../path/to/gen/ts"
    }
}
```

```ts
import * as Types from '@superblocksteam/types';
import { Kafkav1, Api } from '@superblocksteam/types';
```

**Golang**

```sh
$ go get -u github.com/superblocksteam/types/gen/go
```

```go
// Modified go.mod when developing locally.
replace (
    github.com/superblocksteam/types/gen/go => ../path/to/gen/go
)
```

```go
package main

import apiv1 "github.com/superblocksteam/types/gen/go/api/v1"

func main() {
    api := new(apiv1.Api)
    // your code
}
```

**Python**

```py
# Coming Soon!!
```

## Development

```sh
# dependencies
$ make deps-local

# generate code
$ make proto[-(js|py|go)]

# format code
$ make fmt
```

## Publishing

This is done automatically by the CI and will bump the packages versions on your behalf. Just make sure to generate the code changes before merging your proto changes.

## Rules

- This repo is **not** for utility function **unless** it is a method on the type. In these cases, it **must** be pure!

## Troubleshooting

**Q:** The `make proto` target is failing:

```sh
{"path":"proto/superblocks/api/v1/api.proto","start_line":5,"start_column":8,"end_line":5,"end_column":8,"type":"COMPILE","message":"superblocks/plugins/javascript/v1/plugin.proto: does not exist"}
make: *** [proto] Error 100
```

**Q:** The `make proto` target is failing with the following error:

```sh
pattern ./...: directory prefix . does not contain main module or its selected dependencies
make: *** [protoc-gen-superblocks] Error 1
```

We've seen this issue on `make` 3.81, make sure to upgrade/install the latest `make`.

**Q:** The `make proto-go` target is failing with the following error:

```sh
Failure: plugin superblocks: could not find protoc plugin for name superblocks - please make sure protoc-gen-superblocks is instaleld and present on your $PATH
```

Try exporting the following env variables:
```
export GOPRIVATE=github.com/superblocksteam
export PATH="$(go env GOPATH)/bin:$PATH"
```

Then build target `make protoc-gen-superblocks`

**Q:** I can't import my type in TypeScript

You have to make sure that the types are exported in the npm package you are using. See gen/ts/index.ts and other index.ts files that export types in the gen/ts folder
