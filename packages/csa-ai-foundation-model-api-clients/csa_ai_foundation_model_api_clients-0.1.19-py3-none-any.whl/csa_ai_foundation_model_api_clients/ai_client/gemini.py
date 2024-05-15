#!/usr/bin/env python3

import google.generativeai as genai
from google.generativeai import types
import datetime

def generate_response(model_name, api_key, system_prompt, user_prompt, **kwargs):
    TIME_START = datetime.datetime.now()

    genai.configure(api_key=api_key)

    gemini_model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt
        )

    temperature = kwargs.get('temperature', 1)
    max_tokens = kwargs.get('max_tokens', 4096)

    config = types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=max_tokens,
        temperature=temperature
    )

    response = gemini_model.generate_content(user_prompt, generation_config=config)

    TIME_FINISHED = datetime.datetime.now()
    duration = TIME_FINISHED - TIME_START
    TIME_TO_RUN = duration.total_seconds()

    try:
        response_message = response.text
        status = "success"
    except AttributeError:
        response_message = None
        status = "error"

    # https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/get-token-count
    # response = model.count_tokens(prompt)
    # print(f"Prompt Token Count: {response.total_tokens}")

    api_response = {
        "status": "success",
        "model_name": model_name,
        "temperature": temperature,
        "ai_query_time": TIME_START.isoformat(),
        "ai_response_time": TIME_FINISHED.isoformat(),
        "ai_runtime": TIME_TO_RUN,
        "tokens_input": None,
        "tokens_output": None,
        "tokens_total": None,
        "ai_response_http_status_code": None,
        "ai_response_stop_reason": None,
        "ai_response_data": response_message
    }

    return api_response
