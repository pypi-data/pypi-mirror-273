#!/usr/bin/env python3

import os
import argparse
import json
from csa_ai_foundation_model_api_clients.ai_client import claude, chatgpt, gemini

class FoundationModelAPIClient:
    def __init__(self, *, model, api_key=None, system_prompt, system_prompt_type, user_prompt, user_prompt_type, user_data=None, user_data_type, output_file=None, temperature=None, max_tokens=None):
        #
        # Increment this when updating the model
        #
        self.csa_ai_foundation_model_api_clients_version = "0.1.10"
        self.model = model
        self.api_key = api_key or self.get_model_api_key()
        self.model_name = self.get_model_mapping()
        self.system_prompt = system_prompt
        self.system_prompt_type = system_prompt_type
        self.user_prompt = user_prompt
        self.user_prompt_type = user_prompt_type
        self.user_data = user_data
        self.user_data_type = user_data_type
        self.output_file = output_file
        self.temperature = temperature
        self.max_tokens = max_tokens

        #
        # Get the file contents and build the prompts with user data if specified
        #
        if self.system_prompt_type == 'file':
            with open(self.system_prompt, 'r', encoding='utf-8') as file:
                self.system_prompt_data = file.read().strip()
        elif system_prompt_type == 'text':
            self.system_prompt_data = self.system_prompt
        else:
            raise ValueError("Unsupported system prompt type")
        
        if self.user_prompt_type == 'file':
            with open(self.user_prompt, 'r', encoding='utf-8') as file:
                self.user_prompt_data = file.read().strip()
        elif user_prompt_type == 'text':
            self.user_prompt_data = self.user_prompt
        else:
            raise ValueError("Unsupported user prompt type")

        if self.user_data is not None:
            if self.user_data_type == 'file':
                with open(self.user_data, 'r', encoding='utf-8') as file:
                    self.user_data_data = file.read().strip()
                    self.user_prompt_final_data = f"{self.user_prompt_data}\n{self.user_data_data}"
            elif user_data_type == 'text':
                self.user_data_data = self.user_data

            self.user_prompt_final_data = f"{self.user_prompt_data}\n{self.user_data_data}"

        else:   
            self.user_prompt_final_data = self.user_prompt_data

        self.api_response = self.generate_response()

        self.system_prompt_absolute_path = os.path.abspath(system_prompt)
        self.user_prompt_absolute_path = os.path.abspath(user_prompt)
        self.user_data_absolute_path = os.path.abspath(user_data)
        self.output_file_absolute_path = os.path.abspath(output_file)

        output_data = {
            "dataType": "csa-ai-foundation-model-api-clients-JSON-output",
            "dataVersion": "0.2",
            "csa-ai-foundation-model-api-clients-version": self.csa_ai_foundation_model_api_clients_version,
            "arguments": {
                "model": self.model_name,
                "system_prompt": self.system_prompt,
                "user_prompt": self.user_prompt,
                "user_data_file": self.user_data,
                "system_prompt_absolute": self.system_prompt_absolute_path,
                "user_prompt_absolute": self.user_prompt_absolute_path,
                "user_data_file_absolute": self.user_data_absolute_path,
                # TODO: add optional _data for each file
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "output_file": self.output_file,
                "output_file_absolute": self.output_file_absolute_path
            },
            "api_response": self.api_response
        }

        if self.output_file is not None:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                json.dump(output_data, file, sort_keys=True, indent=2)
        else:
            print(json.dumps(output_data, sort_keys=True, indent=2))


    def get_model_mapping(self):
        model_mapping = {
            # curl https://api.openai.com/v1/models   -H "Authorization: Bearer $OPENAI_CHATGPT_API_KEY"
            'chatgpt': 'gpt-4o',
            'gpt': 'gpt-4o',
            'gpt-4o': 'gpt-4o',
            'gpt-4': 'gpt-4',
            # TODO: find API call for claude models
            'claude': 'claude-3-opus-20240229',
            'claude-haiku': 'claude-3-haiku-20240307',
            'claude-sonnet': 'claude-3-sonnet-20240229',
            'claude-opus': 'claude-3-opus-20240229',
            # TODO: find API call for gemini models
            'gemini': 'gemini-1.5-pro-latest'
        }
        return model_mapping.get(self.model, self.model)

    def get_model_api_key(self):
        model_api_key = {
            'chatgpt': 'OPENAI_CHATGPT_API_KEY',
            'gpt': 'OPENAI_CHATGPT_API_KEY',
            'claude': 'ANTHROPIC_CLAUDE_API_KEY',
            'claude-haiku': 'ANTHROPIC_CLAUDE_API_KEY',
            'claude-sonnet': 'ANTHROPIC_CLAUDE_API_KEY',
            'claude-opus': 'ANTHROPIC_CLAUDE_API_KEY',
            'gemini': 'GOOGLE_GEMINI_API_KEY'
        }
        api_key_env = model_api_key.get(self.model, model_api_key)
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ValueError("API KEY environment variable not set.")
        return api_key

    def generate_response(self):
        if self.model.startswith('claude'):
            api_response = claude.generate_response(self.model_name, self.api_key, self.system_prompt_data, self.user_prompt_final_data)
        elif self.model.startswith('chatgpt') or self.model.startswith('gpt'):
            api_response = chatgpt.generate_response(self.model_name, self.api_key, self.system_prompt_data, self.user_prompt_final_data)
        elif self.model.startswith('gemini'):
            api_response = gemini.generate_response(self.model_name, self.api_key, self.system_prompt_data, self.user_prompt_final_data)
        else:
            raise ValueError(f"Unsupported model: {self.model}")
        return api_response

def main():#
    parser = argparse.ArgumentParser(description='AI Model Client')
    parser.add_argument('--model', type=str, required=True, help='Model name')
    parser.add_argument('--system-prompt', type=str, required=True, help='Path to the file containing the system prompt')
    parser.add_argument('--user-prompt', type=str, required=True, help='Path to the file containing the user content')
    parser.add_argument('--user-data', type=str, default=None, help='Path to additional user data to append to the user prompt')
    parser.add_argument('--output-file', type=str, default=None, help='Output file path to write the response and metadata')
    parser.add_argument('--temperature', type=float, default=1, help='Temperature setting for model (default: 1)')
    parser.add_argument('--max-tokens', type=int, default=4096, help='Maximum number of tokens (default: 4096)')

    args = parser.parse_args()

    #
    # Change it so we call it in a single go, if no output-file is provided, we print the response
    #
    FoundationModelAPIClient(
        model=args.model,
        system_prompt=args.system_prompt,
        system_prompt_type='file',
        user_prompt=args.user_prompt,
        user_prompt_type='file',
        user_data=args.user_data,
        user_data_type='file',
        output_file=args.output_file,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )
    #
    # TODO: longer term break this function up a bit?
    #

if __name__ == '__main__':
    main()
