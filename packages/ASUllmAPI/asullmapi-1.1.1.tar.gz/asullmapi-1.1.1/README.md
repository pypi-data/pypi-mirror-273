# ASU LLM API
This package allows individuals at Arizona State University to access ASU GPT through API. You will need API access token, API endpoints in order to use this package.

## Install
Install via pip in a virtual environment or Conda.
```markdown
pip install ASUllmAPI
```

Note: Depending on your Python distribution, you may need to pip or conda
install `requests` and `tqdm` if it is not available in your local environment.
```markdown
pip install requests
pip install tqdm
```

## ASU GPT API endpoints
- LLM endpoint: `https://api-test-poc.aiml.asu.edu/queryV2`
- Model list endpoint: `https://api-test-poc.aiml.asu.edu/model?output=name%2Cprovider%2Cowner`

## API access token
Please contact Ayat Sweid <Ayat.Sweid@asu.edu> or Paul Alvarado <Paul.Alvarado.1@asu.edu> for API access token.

## Usage
- Use `query_model_info_api` module to pull list of available models from ASU GPT. See [Models](##Models) section below for details.

**Example code:**
```markdown
from ASUllmAPI import query_model_info_api, model_provider_mapper, model_list

model_info = query_model_info_api(access_token=access_token, url=model_list_url)
model_info
>>> [{"model": "gpt4", "owner": "openai", "provider": "openai"}, ...] 

model_provider_mapper(model_info)
>>> {"mistral-8x7b": "aws", "titang1express": "aws", ...}

model_list(model_info)
>>> ["gpt4", "gpt3_5", "claudeinstant", ...]
```

- Use `query_llm` module to query ASU GPT.

**Example code:**
```markdown
from ASUllmAPI import ModelConfig, query_llm, batch_query_llm

model = ModelConfig(name="gpt4", provider="openai", access_token=access_token, api_url=llm_api_url)

# run only one query to an LLM
query_llm(model=model, 
          query="Where is Phoenix Arizona?",
          # number of retries when API call is NOT successful
          num_retry=3,
          # number of seconds to sleep when API call successful
          success_sleep=0.0,
          # number of seconds to sleep when API call is NOT successful
          fail_sleep=1.0)
>>> "Phoenix is the capital city of the U.S. state of Arizona. It's located in the south-central part of the state, approximately halfway between Tucson to the southeast and Flagstaff to the north. With its coordinates being 33.4484° N, 112.0740° W, it lies within the Sonoran Desert surrounded by mountains on all sides."

queries = {1: 'Where is Phoenix Arizona?',
           2: 'Where is Flagstaff Arizona?',
           3: 'Where is Tucson Arizona?'}

# run multiple queries to an LLM

# the same arguments apply as `query_llm` in this function
batch_query_llm(model=model, 
                # a dictionary in the same format as `queries` above
                queries=queries, 
                # for multithreading, set above 1
                max_threads=4,
                num_retry=3, 
                # overrides `num_retry` to increment according to the question id
                # you supply in `queries`
                auto_increase_retry=False)

>>> {1: "Phoenix is the capital city of the U.S. state of Arizona. It's located in the south-central part of the state, approximately halfway between Tucson to the southeast and Flagstaff to the north. With its coordinates being 33.4484° N, 112.0740° W, it lies within the Sonoran Desert surrounded by mountains on all sides.",
     3: ...,
     2: ...}
```

Note: If you have a `project_id`, reference the following code snippet.
```markdown
from ASUllmAPI import ModelConfig, query_llm

model = ModelConfig(project_id=project_id, access_token=project_access_token, api_url=project_api_url)
query_llm(model=model, query="Where is Phoenix Arizona?")
>>> "Phoenix is the capital city of the U.S. state of Arizona. It's located in the south-central part of the state, approximately halfway between Tucson to the southeast and Flagstaff to the north. With its coordinates being 33.4484° N, 112.0740° W, it lies within the Sonoran Desert surrounded by mountains on all sides."
```

## Models

### Model Params
```markdown
"model_params": {
    "temperature": float,
    "max_tokens": int,
    "top_p": float,
    "top_k": int,
},
"enable_search": bool,
"search_params": {
    "collection": "asu",
    "top_k": int,
}
```
#### temperature
Randomness and Diversity parameter. Use a lower value to decrease randomness in the response.
#### top_p
Randomness and Diversity parameter. Use a lower value to ignore less probable options.
#### top_k
Randomness and Diversity parameter. The number of token choices the model uses to generate the next token.
#### max_tokens
The maximum number of tokens in the generated response.

## Provider: AES
Checkout [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html) for base model ids and versions.

### Titan Text Models

Model IDs:
- titang1lite
- titang1express

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html):

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 1       |
| Length                   | max_tokens  | max_tokens  | 0       | 8000    | 512     |


### Anthropic Claude models

Model IDs:
- claude2_1 
- claude2 
- claude1_3 
- claudeinstant

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html):

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.5     |
| Randomness and diversity | Top K       | top_k       | 0       | 500     | 250     |
| Length                   | max_tokens  | max_tokens  | 0       | 4096    | 200     |

### AI21 Labs Jurassic-2 models

Model IDs:
- j2ultra
- j2mid

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-jurassic2.html)

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.5     |
| Length                   | max_tokens  | max_tokens  | 0       | 8191    | 200     |

### Cohere Command Models

Model IDs:
- command
- commandlight

[Model documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-cohere-command.html)

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 5       | 0.9     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.75    |
| Randomness and diversity | Top K       | top_k       | 0       | 500     | 0       |
| Length                   | max_tokens  | max_tokens  | 1       | 4096    | 20      |

### Meta Llama2 Models

Model IDs:
- llama2-13b

[Model Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html)

| Category                 | Parameter   | Key         | Minimum | Maximum | Default |
|--------------------------|-------------|-------------|---------|---------|---------|
| Randomness and diversity | Temperature | temperature | 0       | 1       | 0.5     |
| Randomness and diversity | Top P       | top_p       | 0       | 1       | 0.9     |
| Length                   | max_tokens  | max_tokens  | 1       | 2048    | 512     |


## Provider: Azure

[Model Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)

| Model name | Model ID         | Max Request (tokens) |
|------------|------------------|----------------------|
| gpt3_5     | gpt-35-turbo     | 4096                 |
| gpt3_5-16k | gpt-35-turbo-16k | 16384                |
| gpt4       | gpt-4            | 8192                 |
| gpt4-32k   | gpt-4-32k        | 32768                |

## Provider: GCP

[Model Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models)

| Model name          | Model ID       | Max Input Tokens     | Max Output Tokens |
|---------------------|----------------|----------------------|-------------------|
| PaLM 2 for Chat     | chat-bison     | 8192                 | 1024              |
| PaLM 2 for Chat 32k | chat-bison-32k | 32768 (input+output) | 8192              |
