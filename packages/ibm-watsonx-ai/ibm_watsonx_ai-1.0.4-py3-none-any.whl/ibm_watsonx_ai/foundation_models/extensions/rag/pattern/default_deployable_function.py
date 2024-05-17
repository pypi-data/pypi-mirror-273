#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------


def default_deployable_function(params=None):
    """
    Default function used in RAGPattern when no ``python_function`` is provided.

    Input schema:
    payload = {
        client.deployments.ScoringMetaNames.INPUT_DATA: [
            {'values': ['question 1', 'question 2']}
        ]
    }

    Output schema:
    result = {
        'predictions': [
            {
                'fields': ['answer', 'reference_documents'],
                'values': [
                    ['answer 1', [ {'page_content': 'page content 1',
                                    'metadata':     'metadata 1'} ]],
                    ['answer 2', [ {'page_content': 'page content 2',
                                    'metadata':     'metadata 2'} ]]
                ]
            }
        ]
    }
    """
    from ibm_watsonx_ai import APIClient
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.foundation_models.extensions.rag import VectorStore
    from ibm_watsonx_ai.metanames import RAGPatternParamsMetaNames

    client = APIClient(params["credentials"])
    client.set.default_space(params["space_id"])

    vector_store = VectorStore.from_dict(client=client, data=params["vector_store"])
    prompt = params["prompt"]
    model = ModelInference(api_client=client, **params["model"])
    rag_params = params["rag_params"]

    def score(payload):
        result = {
            "predictions": [{"fields": ["answer", "reference_documents"], "values": []}]
        }

        for question in payload[client.deployments.ScoringMetaNames.INPUT_DATA][0][
            "values"
        ]:
            num_retrieved_docs = rag_params.get(
                RAGPatternParamsMetaNames.NUM_RETRIEVED_DOCS
            )
            retrieved_docs = vector_store.search(query=question, k=num_retrieved_docs)
            reference_documents = [doc.page_content for doc in retrieved_docs]

            prompt_variables = {
                "question": question,
                "reference_documents": "\n".join(reference_documents),
            }
            prompt_input_text = prompt.format(**prompt_variables)

            answer = model.generate_text(prompt=prompt_input_text)

            result["predictions"][0]["values"].append(
                [
                    answer,
                    [
                        {"page_content": doc.page_content, "metadata": doc.metadata}
                        for doc in retrieved_docs
                    ],
                ]
            )

        return result

    return score
