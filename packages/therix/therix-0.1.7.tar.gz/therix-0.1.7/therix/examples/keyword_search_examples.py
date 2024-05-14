from therix.core.data_sources import PDFDataSource
from typing import List
from therix.core.embedding_models import AzureOpenAIEmbedding3LargeEmbeddingModel
from therix.core.inference_models import AzureOpenAIGPT4InferenceModel
from therix.core.output_parser import OutputParserWrapper
from therix.core.pipeline import Pipeline
import sys
from therix.core.trace import Trace
from pydantic import BaseModel, Field

if len(sys.argv) > 1:
    pipeline = Pipeline.from_id(sys.argv[1])
    question = sys.argv[2]
    session_id = None

    if len(sys.argv) < 4:
        pass
    else:
        session_id = sys.argv[3]

    ans = pipeline.invoke(question, session_id)
    print(ans)
else:
    pipeline = Pipeline(name="My New Published Pipeline")
    (pipeline
    .add(PDFDataSource(config={'files': ['./test-data/file.pdf' , './test-data/rat.pdf']}))
    .add(AzureOpenAIEmbedding3LargeEmbeddingModel(config={"azure_deployment" : "", "azure_api_key" : "" , "azure_endpoint" : "" , "openai_api_version" :  ""}))
    .add(AzureOpenAIGPT4InferenceModel(config={"azure_api_key" : "" , "openai_api_version" :  "", "azure_endpoint" : "" , "azure_deployment" : "" }))
    .add(Trace(config={
                    'secret_key': 'sk-lf-e62aa7ce-c4c8-4c77-ad7d-9d76dfd96db1',
                    'public_key': 'pk-lf-282ad728-c1d6-4247-b6cd-8022198591a9',
                    'identifier': 'my own pipeline'
         }))
        .save()
        )

    pipeline.publish()
    embedding_created_response = pipeline.preprocess_data()
    print(pipeline.id)
    # ans = pipeline.invoke("What are some use cases of RAT?")
    class TestDetails(BaseModel):
        name: str = Field(description="Name of the Test")
        description: str = Field(description="Short description of the Test")

    class OutputParserJSON(BaseModel):
        tests: List[TestDetails] = Field(description="Test")


    keyword_search_dict = {
        "config_id" : embedding_created_response.get("config_id"),
        "prompt" : "Analyze the provided report content for all the documents provided and include only the sentences that matches {keywords} that is being provided separately and also add the keywords whose records are not found and add description as not found. Response should be a list of JSON  format.{format_instructions} Example: {{tests: [{{name: 'name of test', description: 'short description of Test'}}]}}",
        "keywords" : ["FINE-TUNED MODELS" , "abc" , "RAT"],
        "output_parser" : OutputParserWrapper.parse_output(pydantic_object=OutputParserJSON)
    }
    
    ans = pipeline.invoke(keyword_search_params=keyword_search_dict)
    # ans = pipeline.invoke(question="What are some usecases of RAT", type="RAG")

    print(ans)
