# Prompeteer

## **[pypi.org/prompeteer](https://pypi.org/project/prompeteer/)**

### Prompt evaluation and development environment

- Define a prompt template and run it with different variables from an input.csv file
- supports AzureOpenAi (GPT), AWS Bedrock (Anthropic Claude)
- write output to an output.csv file (or just the console)

## requirements

- Azure CLI. (```brew update && brew install azure-cli```)
- AWS CLI. (```brew update && brew install awscli```)

## installation

```shell
pip install prompeteer
```

## usage

### Azure OpenAI - GPT

1. Install Azure CLI and run `az login`
2. choose an AzureOpenAI Resource to work with and specify it in the ```AZURE_OPENAI_RESOURCE_NAME``` environment
   variable.

3. Create your prompt configuration YAML file:

```yaml 
# azure_openai_prompt.yaml
version: 1.0
name: my_prompt
provider: azure
schemaVersion: 1.0
variables:
  - name: topic
    required: true
  - name: year
    required: true
  - name: summary
    required: true
request:
  model: 'gpt-35-turbo' # corresponds to the AzureOpenAi deployment name
  temperature: 0.8
  topP: 1.0
  n: 1
  stream: false
  presencePenalty: 0.0
  frequencyPenalty: 0.0
  stop:
  user:
  messages:
    - role: system
      content: "You are a helpful assistant."
    - role: user
      content: "give a short summary about {topic} in the year {year} ahd here is a summary example"

```

### AWS Bedrock - Claude

1. Install the AWS CLI and login
2. authenticate using (verify that the correct profile is on at ~/.aws/credentials)


4. Create your prompt configuration YAML file:

```yaml
# aws_bedrock_prompt.yaml
version: 1.0
name: formal
provider: aws
schemaVersion: 1.0
variables:
   - name: topic
     required: true
   - name: year
     required: true
   - name: summary
     required: true
request:
   model: 'anthropic.claude-3-haiku-20240307-v1:0'
   temperature: 0.8
   topP: 1.0
   topK: 2
   maxTokens: 250
   messages:
      - role: user
        content: "summarize about {topic} in the year {year} use this example summary: {summary}. do it in a very formal way"
      - role: assistant
        content: "You are a helpful assistant."
```

```python
from prompeteer import prompeteer

prompeteer.run_prompt(prompt_config_file_path='azure_openai_prompt.yaml',
                      output_csv='./output.csv',
                      include_prompt=True,  # show request + response in the output
                      input_csv='./input.csv',
                      destination='file'  # write output to CSV file
                      )

prompeteer.run_prompt(prompt_config_file_path='aws_bedrock_prompt.yaml',
                      include_prompt=False,  # show only request in the output
                      input_csv='./input.csv',
                      row_numbers_to_process=[0, 1],  # use and run only rows 0 and 1 from the input.csv 
                      destination='console'  # write output to the console
                      )
```

### input.csv example: ("|" seperated)

"topic"|"year"|"summary"

"basketball"|2002|"A famous quote: ""Just do it"".

"soccer"|1999|"Championship game was exciting"

## development
```shell
python -m venv venv
```

```shell
source ./venv/bin/activate
```

### install locally and run tests

```shell
pip install -e .
```

```shell 
./test.sh
```

### build and publish to **[pypi.org](https://pypi.org/project/prompeteer/)**.

```shell 
./publish.sh
```
