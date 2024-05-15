#!/usr/bin/env python3

import openai
import datetime

def generate_response(model_name, api_key, system_prompt, user_prompt, **kwargs):
    TIME_START = datetime.datetime.now().isoformat()

    openai.api_key = api_key

    temperature = kwargs.get('temperature', 1)
    max_tokens = kwargs.get('max_tokens', 4096)

    completion = openai.chat.completions.create(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    TIME_FINISHED = datetime.datetime.now().isoformat()

    time_start = datetime.datetime.fromisoformat(TIME_START)
    time_complete = datetime.datetime.fromisoformat(TIME_FINISHED)

    duration = time_complete - time_start
    TIME_TO_RUN = duration.total_seconds()

    try:
        tokens_input = completion.usage.prompt_tokens
        tokens_output = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens
    except AttributeError:
        tokens_input = tokens_output = total_tokens = None
    
    serialized_completion = {
        "id": getattr(completion, 'id', None),
        "model": getattr(completion, 'model', None),
        "created": getattr(completion, 'created', None),
        "system_fingerprint": getattr(completion, 'system_fingerprint', None),
        "choices": [
            {
                "finish_reason": choice.finish_reason,
                "index": choice.index,
                "message": {
                    "content": getattr(choice.message, 'content', None),
                    "role": getattr(choice.message, 'role', None)
                }
            } for choice in getattr(completion, 'choices', [])
        ] if hasattr(completion, 'choices') else [],
        "usage": {
            "prompt_tokens": tokens_input,
            "completion_tokens": tokens_output,
            "total_tokens": total_tokens
        }
    }
    
    try:
        response_message = completion.choices[0].message.content
        status = "success"
    except AttributeError:
        response_message = None
        status = "error"

    api_response = {
        "status": "success",
        "model_name": model_name,
        "temperature": temperature,
        "ai_query_time": TIME_START,
        "ai_response_time": TIME_FINISHED,
        "ai_runtime": TIME_TO_RUN,
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "tokens_total": total_tokens,
        "ai_response_http_status_code": None,
        "ai_response_stop_reason": None,
        "ai_response_data": response_message
    }

    return api_response
