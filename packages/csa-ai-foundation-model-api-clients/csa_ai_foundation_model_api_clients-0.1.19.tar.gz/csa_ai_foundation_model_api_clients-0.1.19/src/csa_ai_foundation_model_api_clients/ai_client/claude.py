#!/usr/bin/env python3

import anthropic
import datetime

def generate_response(model_name, api_key, system_prompt, user_prompt, **kwargs):
    TIME_START = datetime.datetime.now()

    client = anthropic.Anthropic(api_key=api_key)

    temperature = kwargs.get('temperature', 1)
    max_tokens = kwargs.get('max_tokens', 4096)

    completion = client.messages.create(
        model=model_name,        
        temperature=temperature,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ],
    )

    TIME_FINISHED = datetime.datetime.now()
    duration = TIME_FINISHED - TIME_START
    TIME_TO_RUN = duration.total_seconds()

# https://docs.anthropic.com/en/api/messages

    try:
        tokens_input = completion.usage.input_tokens
        tokens_output = completion.usage.output_tokens
        total_tokens = completion.usage.input_tokens + completion.usage.output_tokens
    except AttributeError:
        tokens_input = tokens_output = total_tokens = None

# TODO: update this to test completion.stop_reason "end_turn"
    try:
        response_message = completion.content[0].text
        status = "success"
    except AttributeError:
        response_message = None
        status = "error"

    api_response = {
        "status": status,
        "model_name": model_name,
        "temperature": temperature,
        "ai_query_time": TIME_START.isoformat(),
        "ai_response_time": TIME_FINISHED.isoformat(),
        "ai_runtime": TIME_TO_RUN,
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "tokens_total": total_tokens,
        "ai_response_http_status_code": None,
        "ai_response_stop_reason": completion.stop_reason,
        "ai_response_data": response_message
    }

    return api_response
