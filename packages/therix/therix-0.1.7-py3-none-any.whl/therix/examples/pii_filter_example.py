from therix.core.data_sources import PDFDataSource
from therix.core.inference_models import GroqMixtral87bInferenceModel
from therix.core.embedding_models import BedrockTitanEmbedding
from therix.core.pii_filter_config import PIIFilterConfig
from therix.core.pipeline import Pipeline
import sys
from therix.core.trace import Trace



# TODO: Init therix with DB details, and license key


## Usage:
# python main.py ad11128d-d2ec-4f7c-8d87-15c1a5dfe1a9 "how does it help in reasoning?"

# if args has pipeline_id, then load the pipeline
## else create new pipeline
if len(sys.argv) > 1:
    pipeline = Pipeline.from_id(sys.argv[1])
    question = sys.argv[2]
    ans = pipeline.invoke(question)
    print(ans)
else:
    pipeline = Pipeline(name="My New Published Pipeline")
    (pipeline
    .add(PDFDataSource(config={'files': ['../../test-data/Essay-on-Lata-Mangeshkar-final.pdf']}))
    .add(BedrockTitanEmbedding(config={ "bedrock_aws_access_key_id":"",
                                            "bedrock_aws_secret_access_key" : "",
                                            "bedrock_aws_session_token" : "",
                                            "bedrock_region_name" : "us-east-1"
                                            }))
    .add(GroqMixtral87bInferenceModel(config={"groq_api_key": 'your groq api key'}))
    .add(PIIFilterConfig(config={
        'entities': ['PERSON','PHONE_NUMBER','EMAIL_ADDRESS']
    }))
    .add(Trace(config={
        'secret_key': 'sk-lf-e62aa7ce-c4c8-4c77-ad7d-9d76dfd96db1',
        'public_key': 'pk-lf-282ad728-c1d6-4247-b6cd-8022198591a9',
        'identifier': 'my own pipeline'
    }))
    .save())

    pipeline.publish()
    pipeline.preprocess_data()
    print(pipeline.id)
    ans = pipeline.invoke("Whom is the data about? And what are their personal details?")

    print(ans)