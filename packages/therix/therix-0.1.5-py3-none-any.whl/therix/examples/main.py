from therix.core.data_sources import PDFDataSource
from therix.core.embedding_models import (
    BedrockTitanEmbedding,
    OpenAITextAdaEmbeddingModel,
)
from therix.core.inference_models import (
    OpenAIGPT4TurboPreviewInferenceModel,
)
from therix.core.inference_models import (
    OpenAIGPT4TurboPreviewInferenceModel,GroqLlama370b
)
from therix.core.embedding_models import (
    OpenAITextAdaEmbeddingModel,
)
from therix.core.inference_models import (
    OpenAIGPT4TurboPreviewInferenceModel,
)
from therix.core.pipeline import Pipeline
import sys

from therix.core.trace import Trace

# OPENAI_API_KEY = "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"

GROQ_API_KEY='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'

# TODO: Init therix with DB details, and license key


## Usage:
# python main.py ad11128d-d2ec-4f7c-8d87-15c1a5dfe1a9 "how does it help in reasoning?"

# if args has pipeline_id, then load the pipeline
## else create new pipeline
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
    (
        pipeline.add(PDFDataSource(config={"files": ["../../test-data/rat.pdf"]}))
        .add(BedrockTitanEmbedding(config={"bedrock_aws_access_key_id" : "ASIA5FTZANLGDHGX4LGX",
                                "bedrock_aws_secret_access_key" : "A1tixMuPKNUxIyigQHyx8OEaM9Ak6ZlnvyGoPzYn"        ,
                                "bedrock_aws_session_token" : "IQoJb3JpZ2luX2VjEMH//////////wEaCmFwLXNvdXRoLTEiRjBEAiBGXmRX50b9XDa1ESsU8x6xo4y0FbmplTqMwGx2uZiGwQIgC0lz7DnFKS+Shexoj5f+Cf+nMBGzun1PEfEs+15ZM/YqlQMIKhAAGgw5MDU0MTgxNDAzNjQiDCAALcsjagJnUqEWiiryAuG7vhozJlM2jCOtIJhWSCiSRf8+45X47gPVmvENV7BNw2lan6POioD8Yc5VKC9Vhr4APyBl24HjWEljBMi57Z/CK7+V5NHC+U6IujgeVW6OuxMJddseoS4153gKH489UwwN2Zq5X06IYpJpGnqVWoiQgWwf4FL5f/FTHMZNNaG4KllKjTjIbyCpFID4fsegJo2D7EFLbvGrlR3yKWaV1A7aZl9JTBQGK0dRuwTgx3qk1CS3FfXpf7kWtO2bHquf69nAupn56GAkobCAxTzKAqa8VOtLQuPFS7G+FmGZFVPcdIc2Sn7eKGZ5htC2QaT/1pMTDeCShBr/ygkthPZkVR/ncQ2i6E5mOxNqKpROUtNcBLHr29Ys4IztvgWAhaSRy2TK/+bbN3l8GAYa65QM72Ih7YzdEL8xsU7Efqqx0X2uJ631mxwX3byV/Gm7QKy7ANNxrCSrtfI8DI8v4CPfnMyOKHklE53wB3OVxA/bB/pIWawwjL/3sQY6pwEZifC3u90tMKG5lwyunVIuUeEv67T9VdLGh8WkqSZDUqlOeAfiYtsx96X4veg4S5FlIOmx0bwURbczEVVaN2FTsCI01NfM5pPRWEjKMp+nKeCFUlD31ELpjdBK5uhHIIkrPB1DI8sVUFhPl1t2l0fRimxRRzfUNt1RdPXmzOpesjO1pBrGYjvoFrYJa89U5J7bRBhFDJELemOKSJSLa05TvcqRSLesBQ==",
                                "bedrock_region_name" : "us-east-1"}))
        .add(GroqLlama370b(config={"groq_api_key": GROQ_API_KEY}))
        .add(
            Trace(
                config={
                    "secret_key": "sk-lf-e62aa7ce-c4c8-4c77-ad7d-9d76dfd96db1",
                    "public_key": "pk-lf-282ad728-c1d6-4247-b6cd-8022198591a9",
                    "identifier": "my own pipeline",
                }
            )
        )
        .save()
    )

    pipeline.publish()
    pipeline.preprocess_data()
    print(pipeline.id)
    ans = pipeline.invoke("Explain Ablation on retrieval in RAT")

    print(ans)
