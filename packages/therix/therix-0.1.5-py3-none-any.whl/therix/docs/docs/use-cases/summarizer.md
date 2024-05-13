---
slug: /use-cases/summarizer
sidebar_position: 2
---

# Summarizer

The Summarizer tool in Therix condenses lengthy texts into concise summaries. It analyzes documents, extracts key information, and generates coherent summaries, enabling users to grasp core content efficiently.

The Summarizer uses two main methods: "Extractive" and "Abstractive" summarization. They work differently but both help make summaries, depending on what you need.

## Summarizer - Abtractive

Abstractive Summarization in Therix is a smart way to make short summaries from long texts. Unlike Extractive Summarization that just rearranges the text, Abstractive Summarization really understands the text. It figures out the main ideas and context, then writes original summaries that capture those ideas in a new way.

This method lets you be creative in summarizing and isn't limited by how the original text is structured. Abstractive Summarization is great for simplifying complex information, making it easier to understand for making decisions and sharing knowledge in different areas.

**Sample Output:**
```python
{'answer': '\nBeets are a root vegetable rich in fiber, folate, manganese, and antioxidants, and can improve athletic performance and reduce blood pressure. More research is needed to fully understand their health benefits.', 'session_id': UUID('b9548328-6982-40e9-9cea-06208090f25f')}
```

## Summarizer - Extractive

In the Extractive Summarizer of Therix, the aim is to make a brief summary of a text in a JSON format. It picks out important sentences or phrases from the text and puts them in a structured way in JSON.

Users can also give a custom model to customize how the information is organized in the JSON. This gives more control over how the summary looks.
If you don't specify a custom model, the system itself decides how to organize the summary in JSON, making sure it's clear and concise.

Whether using the default JSON setup or a custom model, the result is a neat and informative summary in JSON. This helps in understanding big chunks of text quickly and making decisions based on them in different fields.

Custom model is made by extending from the SummarizerOutputModel of therix.
```python
from therix.core.summarizer_output_model import SummarizerOutputModel

class TopicModel(SummarizerOutputModel):
    mainTopic: str
    subTopic1: str
    subTopic2: str
```

**Sample Output:**
```python
{'answer': {"mainTopic": "Superfoods", "subTopic1": "Health Benefits", "subTopic2": "10 Superfoods"} , 'session_id': UUID('3f2d3cef-8091-4e0d-accd-71b6387938c7')}
```

## How you can integrate summarizer in your code:

- Import Necessary Modules: Begin by importing the required modules for configuring the Summarizer.

```python
from therix.summarizer import SummarizerConfig, SummarizerTypeMaster
from therix.core.summarizer_output_model import SummarizerOutputModel  # Import SummarizerOutputModel if needed
```

- Instantiate SummarizerConfig:

Create an instance of the SummarizerConfig class by specifying the type of summarizer and, optionally, the Pydantic model for structuring the JSON output.

- **For Extractive Summarizer with custom Pydantic model**
```python
summarizer_config = SummarizerConfig(SummarizerTypeMaster.EXTRACTIVE, TopicModel)
```

- **For Abstractive Summarizer**
```python
summarizer_config = SummarizerConfig(SummarizerTypeMaster.ABSTRACTIVE)
```

- Add Summarizer Configuration to Pipeline: Use the .add() method to add the SummarizerConfig to your Therix pipeline.

```python
pipeline.add(summarizer_config)
```

## Example

```python
pipeline = Pipeline(name="Summarizer Pipeline")
    (pipeline
    .add(SummarizerConfig(SummarizerTypeMaster.EXTRACTIVE,TopicModel))
    .add(// Any other configuration you want to add)
    .save())

    pipeline.publish()
    answer = pipeline.invoke(text)
```

By following these steps and adjusting the parameters as needed, you can seamlessly integrate the Summarizer into your Therix pipeline. Whether you require Extractive or Abstractive summarization, with or without a custom model, Therix provides the flexibility and functionality to meet your summarization needs effectively.
