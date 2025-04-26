
### Sentence Transformer API

This repository contains an Azure Function with an HTTP trigger serving a sentence transformer API for MiniLM-L6-v2 embeddings. 
This is built to be used by the Weaviate vector database & can be used as an end point for the text2vec-transformers. 

The AMD64 docker image for the transformer (semitechnologies/transformers-inference:sentence-transformers-all-MiniLM-L6-v2) was taking
upto 9GB hence I decided to run this as an Azure function which would be cheaper than running a container app based on a consumption plan.

The function contains 2 end points 

-   GET : a health check    _(eg : http://localhost:5000/.well-known/ready)_
-   POST : catch all end point for any route other than the health check. This will return embeddings _(eg: http://localhost:5000/v1/vectorizer)_
  
    This takes JSON input inthe following 2 formats

    ```json
    {
       "texts" : "Any text to be converted to embeddings"
    }
    ```

     ```json
    {
       "texts" : ["text for embeddings1","text for embeddings2"]
    }
    ```

#### Usage
once deployed to an azure function use the function url as the value for transforrmer inference api 

```yaml
  environment:
      DEFAULT_VECTORIZER_MODULE: "text2vec-transformers"
      ENABLE_MODULES: "text2vec-transformers"
      TRANSFORMERS_INFERENCE_API: "https://my-function-url"
```

