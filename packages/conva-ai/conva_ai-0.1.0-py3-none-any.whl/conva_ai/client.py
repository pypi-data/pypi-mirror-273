import uuid
import json
import requests
import sseclient
from conva_ai.base import BaseClient
from conva_ai.response import ConvaAIResponse
from typing import AsyncGenerator


class AsyncConvaAI(BaseClient):

    async def stream_response(self, response):
        client = sseclient.SSEClient(response)  # type: ignore
        for event in client.events():
            event_data = event.data
            event_response = json.loads(event_data)
            rt = event_response.get("response_type", "assistant")
            if rt != "status":
                is_final = event_response.get("is_final", False)
                yield ConvaAIResponse(**event_response)
                if is_final:
                    action_response = ConvaAIResponse(**event_response)
                    self.history = action_response.conversation_history
                    yield action_response

    def _send_text2action_request(
        self, query, app_context, *, stream, capability_name="", capability_group="", disable_cache=False
    ):
        request_id = uuid.uuid4().hex
        response = requests.post(
            f"{self.host}/v1/assistants/{self.assistant_id}/text2action",
            json={
                "type": "text2action",
                "request_id": request_id,
                "assistant_id": self.assistant_id,
                "assistant_version": self.assistant_version,
                "device_id": str(uuid.getnode()),
                "input_query": query,
                "domain_name": self.domain,
                "app_context": app_context,
                "conversation_history": "{}" if not self.keep_conversation_history else self.history,
                "capability_name": capability_name if capability_name else "",
                "capability_group": capability_group if capability_group else "",
                "disable_cache": disable_cache,
                "stream": stream,
            },
            headers={"Authorization": self.api_key, "Content-Type": "application/json"},
            stream=stream,
        )
        return response

    async def invoke_capability(
        self,
        query: str,
        capability_name: str,
        disable_cache: bool = False,
    ) -> ConvaAIResponse:
        app_context: dict = {}
        response = self._send_text2action_request(
            query, app_context, capability_name=capability_name, disable_cache=disable_cache, stream=False
        )
        action_response = ConvaAIResponse(**json.loads(response.json()))
        self.history = action_response.conversation_history
        return action_response

    async def invoke_capability_stream(
        self,
        query: str,
        capability_name: str,
        disable_cache: bool = False,
    ) -> AsyncGenerator[ConvaAIResponse, None]:
        app_context: dict = {}
        response = self._send_text2action_request(
            query, app_context, capability_name=capability_name, disable_cache=disable_cache, stream=True
        )
        return self.stream_response(response)

    async def invoke_capability_group(
        self,
        query: str,
        capability_group: str = "",
        disable_cache: bool = False,
    ) -> ConvaAIResponse:
        app_context: dict = {}
        response = self._send_text2action_request(
            query, app_context, capability_group=capability_group, disable_cache=disable_cache, stream=False
        )
        action_response = ConvaAIResponse(**json.loads(response.json()))
        self.history = action_response.conversation_history
        return action_response

    async def invoke_capability_group_stream(
        self,
        query: str,
        capability_group: str = "",
        disable_cache: bool = False,
    ) -> AsyncGenerator[ConvaAIResponse, None]:
        app_context: dict = {}
        response = self._send_text2action_request(
            query, app_context, capability_group=capability_group, disable_cache=disable_cache, stream=True
        )
        return self.stream_response(response)
