---
slug: /components/pipeline-config/system-prompt
sidebar_position: 1
---

# System Prompt
System prompt is a way of adding custom prompt to your language models that override the existing prompt provided by Therix.


# Why Custom System-Prompt
A personalized system prompt allows you to direct your language model's behavior. This means you can tailor the model to suit your preferences, whether you need it to act like a teacher, a doctor, or anything else.

# Example of System-Prompt
Keep in mind to use the same placeholders for `{context}` and `{question}`

    ```Python
    sys_prompt =  
        """
        You are an AI chatbot who behaves as a doctor.
        Answer the question based only on the following context.
        Always prescribe according to the context provided
        Do not reply if you are not sure.
        Context: 
        {context}

        Question: {question}
        """
    ```

# Add System-Prompt to your pipeline
You can add system-prompt to your pipeline by doing a `.add` to your existing configurations.
```python
.add(SystemPromptConfig(config={"system_prompt" : sys_prompt}))
```

# Example
```python
pipeline = Pipeline(name="Summarizer Pipeline")
    (pipeline
    .add(SystemPromptConfig(config={"system_prompt" : sys_prompt}))
    .add(// Any other configuration you want to add)
    .save())

    pipeline.publish()
    answer = pipeline.invoke(text)
```

