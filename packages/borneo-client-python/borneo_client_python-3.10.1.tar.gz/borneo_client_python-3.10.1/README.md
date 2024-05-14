# borneo-client-python

Borneo Client Python SDK

## Installing

To install the this package, simply add or install using your favorite package manager:

- `pip install borneo-python-client`

### Usage

To send a request using `@borneodata/borneo-client` and an example command:

```python
# import { BorneoClient, DescribeCatalogResourceCommand } from '@borneodata/borneo-client';
# import { BorneoAuthProvider } from '@borneodata/borneo-client-auth-provider';

# async function getData() {
#   const authProvider = await BorneoAuthProvider.fromConfigFile(`./Borneo-Service-Account-Token.json`);
#   const client = new BorneoClient({
#     endpoint: authProvider.getApiEndpoint(),
#     apiKey: authProvider.getApiKey()
#   });
#   const input = {
#     resourceId: '1bea4d02-8ce7-11ee-942f-3c7d0a1cd55d'
#   };
#   const cmd = new DescribeCatalogResourceCommand(input)
#   const data = await client.send(cmd)
  
#   // The data is returned here and can be further processed.
#   console.log(data)
#   return data
# }

# getData()
```

### Config
```
const config = {
  clientId: 'STRING_VALUE', /* required */
  region: 'STRING_VALUE', /* required */
  token: 'STRING_VALUE', /* required */
  apiEndpoint: 'STRING_VALUE', /* required */
  secret: 'STRING_VALUE'
}
```

## API Documentation

More API documentation is here at `https://<my-stack>/docs/api`

## License

This SDK is distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)
