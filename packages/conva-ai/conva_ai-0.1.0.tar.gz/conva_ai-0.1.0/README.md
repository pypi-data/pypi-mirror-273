# Python Library for Conva AI

This is the python library for using Conva AI Co-pilots

## Examples

### 1. A simple example for generating response using Conva Co-pilot
```
import asyncio
from conva_ai import AsyncConvaAI
client = AsyncConvaAI(
    assistant_id="<YOUR_ASSISTANT_ID>", 
    assistant_version="<YOUR_ASSISTANT_VERSION>", 
    api_key="<YOUR_API_KEY>"
)
async def generate(client: AsyncConvaAI, query: str, stream: bool):
    response = client.invoke_capability(query, stream=stream)
    out = ""
    async for res in response:
        out = res.model_dump_json(indent=4)
    return out

final_response = asyncio.run(generate(client, "how are you", True))
print(final_response)
```

You can try out the co-pilot on [Google Colab](https://colab.research.google.com/drive/1WtbARTRQ9wCvztrAQuEhQUvwImhtPZXd#scrollTo=ZSVBQsOelgfv)

If you want to get the response as dictionary, then replace
```
out = res.model_dump_json(indent=4)
```

with
```
out = res.model_dump()
```

### 2. How to clear history

Conva AI client, by default keeps track of your conversation history and uses it as the context for responding intelligently

You can clear conversation history by executing the below code:

```
from conva_ai.client import AsyncConvaAI
client = AsyncConvaAI(
    assistant_id="<YOUR_ASSISTANT_ID>", 
    assistant_version="<YOUR_ASSISTANT_VERSION>", 
    api_key="<YOUR_API_KEY>"
)
client.clear_history()
```

In case you are buliding an application where you don't want to track conversation history, you can disable history tracking

```
client.use_history(False)
```

You can enable history by

```
client.use_history(True)
```

### 3. Debugging responses

Conva AI uses generative AI to give you the response to your query. In order for you to understand the reasoning behind the response. We also provide you with AI's reasoning

```
import asyncio
from conva_ai.client import AsyncConvaAI

client = AsyncConvaAI(
        assistant_id="<YOUR_ASSISTANT_ID>", 
        assistant_version="<YOUR_ASSISTANT_VERSION>", 
        api_key="<YOUR_API_KEY>"
    )

async def generate(client: AsyncConvaAI, query: str, stream: bool):
    response = client.invoke_capability(query, stream=stream)
    out=""
    async for res in response:
        out = res
    return out

final_response = asyncio.run(generate("how are you", True))
print(final_response.reason)
```

### How to use capability groups

Capability Groups are used to control the list of Capabilities that Co pilot will have access. 
You can make use of the capability group while using the `invoke_capability` method

```
async def generate(client: AsyncConvaAI, query: str, stream: bool):
    response = client.invoke_capability(query, stream=stream, capability_group="<CAPABILITY_GROUP_NAME>")
    out=""
    async for res in response:
        out = res
    return out
```