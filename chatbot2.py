import boto3, json
import os

os.environ["AWS_PROFILE"] = "sidrik-iam"

bedrock_runtime=boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

prompt="Who is captain of indian Cricket team?"

kwargs={
  "modelId": "ai21.j2-ultra-v1",
  "contentType": "application/json",
  "accept": "*/*",
  "body": "{\"prompt\":\"" + prompt + "\",\"maxTokens\":200,\"temperature\":0.7,\"topP\":1,\"stopSequences\":[],\"countPenalty\":{\"scale\":0},\"presencePenalty\":{\"scale\":0},\"frequencyPenalty\":{\"scale\":0}}"
}
# print(kwargs)
respone = bedrock_runtime.invoke_model(**kwargs)
print(respone)

respone_body=json.loads(respone.get('body').read())
# print(respone_body)

completion=respone_body.get('completions')[0].get('data').get('text')
# print(completion)