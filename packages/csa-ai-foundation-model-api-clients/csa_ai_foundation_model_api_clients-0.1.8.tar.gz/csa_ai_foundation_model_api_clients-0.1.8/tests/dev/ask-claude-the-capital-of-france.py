#!/usr/bin/env python3

# This is a local test for dev

from csa_ai_foundation_model_api_clients import FoundationModelAPIClient

def main():
    model = 'claude'
    system_prompt = "You are a helpful assistant who answers in rhyme."
    user_prompt = "What is the capital of "
    user_data = "France?"
    output_file = 'claude-response.json'

    FoundationModelAPIClient(
        model=model,
        system_prompt=system_prompt,
        system_prompt_type="text",
        user_prompt=user_prompt,
        user_prompt_type="text",
        user_data=user_data,
        user_data_type="text",
        temperature=0.7,
        max_tokens=100,
        output_file=output_file
    )

if __name__ == '__main__':
    main()
