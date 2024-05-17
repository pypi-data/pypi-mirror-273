#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import os
import pytest

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.tests.utils import get_wml_credentials
from ibm_watsonx_ai.foundation_models.extensions.rag import VectorStore
from langchain_ibm import WatsonxLLM, WatsonxEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.outputs import LLMResult
from langchain_core.prompts import PromptTemplate
from langchain.chains import (
    LLMChain,
    SimpleSequentialChain,
    SequentialChain,
    TransformChain,
    ConversationChain,
    LLMMathChain,
)
from langchain.chains.router import MultiPromptChain
from langchain.memory import ConversationBufferMemory
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.docstore.document import Document
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from ibm_watsonx_ai.foundation_models.utils.enums import (
    ModelTypes,
    DecodingMethods,
    EmbeddingTypes,
)

wml_credentials = get_wml_credentials()
project_id = wml_credentials.__dict__.get('project_id')
space_id = wml_credentials.__dict__.get('space_id')
client = APIClient(wml_credentials, project_id=project_id, space_id=space_id)
model_types_list = [model.value for model in ModelTypes]
available_models = [
    model_spec["model_id"]
    for model_spec in client.foundation_models.get_model_specs().get("resources", [])
    if model_spec["model_id"] in model_types_list
]

embedding_model_types_list = [model.value for model in EmbeddingTypes]
available_embedding_models = [
    model_spec["model_id"]
    for model_spec in client.foundation_models.get_embeddings_model_specs().get("resources", [])
    if model_spec["model_id"] in embedding_model_types_list
]

DOCUMENTS = ["What is a generative ai?", "What is a loan and how does it works?"]


class TestLangchain:
    """
    This tests covers:
    - response using WatsonxLLM wrapper from `langchain_ibm` package,
    - response using LLMChain,
    - response using SequentialChain,
    - response using SimpleSequentialChain,
    - response using TransformChain,
    - response using ConversationChain,
    - response using `to_langchain()` wrapper
    """

    @pytest.mark.parametrize("model_type", available_models)
    def test_01_watsonxllm_invoke(self, model_type, project_id, api_client) -> None:
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        response = llm.invoke("What color sunflower is?\n")
        assert isinstance(response, str)
        assert len(response) > 0

    @pytest.mark.parametrize("model_type", available_models)
    def test_02_watsonxllm_generate(self, model_type, project_id, api_client) -> None:
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        response = llm.generate(["What color sunflower is?\n"])
        response_text = response.generations[0][0].text
        assert isinstance(response, LLMResult)
        assert len(response_text) > 0

    @pytest.mark.parametrize("model_type", available_models)
    def test_03_watsonxllm_generate_with_multiple_prompts(
        self, model_type, project_id, api_client
    ) -> None:
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        response = llm.generate(
            ["What color sunflower is?\n", "What color turtle is?\n"]
        )
        response_text = response.generations[0][0].text
        assert isinstance(response, LLMResult)
        assert len(response_text) > 0

    @pytest.mark.parametrize("model_type", available_models)
    def test_04_watsonxllm_generate_stream(
        self, model_type, project_id, api_client
    ) -> None:
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        response = llm.generate(["What color sunflower is?\n"], stream=True)
        response_text = response.generations[0][0].text
        assert isinstance(response, LLMResult)
        assert len(response_text) > 0

    @pytest.mark.parametrize("model_type", available_models)
    def test_05_watsonxllm_stream(self, model_type, project_id, api_client) -> None:
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        response = llm.invoke("What color sunflower is?\n")

        stream_response = llm.stream("What color sunflower is?\n")

        linked_text_stream = ""
        for chunk in stream_response:
            assert isinstance(
                chunk, str
            ), f"chunk expect type '{str}', actual '{type(chunk)}'"
            linked_text_stream += chunk

        assert (
            response == linked_text_stream
        ), "Linked text stream are not the same as generated text"

    @pytest.mark.parametrize("model_type", available_models)
    def test_10_llm_chain(self, model_type, project_id, api_client):
        prompt_template = "What is a good name for a company that makes {product} ?\n"
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        llm_chain = LLMChain(
            llm=llm, prompt=PromptTemplate.from_template(prompt_template)
        )
        product = "car"
        print("\n" + prompt_template.replace("{product}", product))
        review = llm_chain(product)
        print(f"Respond by use 'llm_chain(product)': {review['text']}")
        assert product == review["product"]
        assert review["text"]
        review_run = llm_chain.run(product)
        print(f"Respond by use 'llm_chain.run(product)': {review_run}")
        assert review["text"] == review_run
        review_predict = llm_chain.predict(product=product)
        print(f"Respond by use 'llm_chain.predict(product)': {review_predict}")
        assert review["text"] == review_predict

    @pytest.mark.parametrize("model_type", available_models)
    def test_11_llm_chain_model_with_params(self, model_type, project_id, api_client):
        params = {
            GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
            GenParams.MAX_NEW_TOKENS: 50,
            GenParams.STOP_SEQUENCES: ["\n\n"],
        }
        prompt_template = "What color is the {flower}?\n"
        model = ModelInference(
            model_id=model_type,
            api_client=api_client,
            params=params,
            project_id=project_id,
        )
        llm = WatsonxLLM(watsonx_model=model)
        llm_chain = LLMChain(
            llm=llm, prompt=PromptTemplate.from_template(prompt_template)
        )
        flower = "sunflower"
        print("\n" + prompt_template.replace("{flower}", flower))
        review = llm_chain(flower)
        print(f"Respond by use 'llm_chain(flower)': {review['text']}")
        assert flower == review["flower"]
        assert review["text"]
        review_run = llm_chain.run(flower)
        print(f"Respond by use 'llm_chain.run(flower)': {review['text']}")
        assert review["text"] == review_run
        review_predict = llm_chain.predict(flower=flower)
        print(f"Respond by use 'llm_chain.predict(flower)': {review['text']}")
        assert review["text"] == review_predict

    @pytest.mark.parametrize("model_type", available_models)
    def test_12_sequential_chain(self, model_type, project_id, api_client):
        template_1 = """You are a playwright. 
        Given the title of play and the era it is set in, it is your job to write a synopsis for that title.

        Title: {title}
        Era: {era}
        Playwright: This is a synopsis for the above play:\n"""
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        prompt_template_1 = PromptTemplate(
            input_variables=["title", "era"], template=template_1
        )
        synopsis_chain = LLMChain(
            llm=llm, prompt=prompt_template_1, output_key="synopsis"
        )

        template_2 = """You are a play critic from the New York Times. 
        Given the synopsis of play, it is your job to write a review for that play.

        Play Synopsis:
        {synopsis}
        Review from a New York Times play critic of the above play:\n"""
        prompt_template_2 = PromptTemplate(
            input_variables=["synopsis"], template=template_2
        )
        review_chain = LLMChain(llm=llm, prompt=prompt_template_2, output_key="review")

        overall_chain = SequentialChain(
            chains=[synopsis_chain, review_chain],
            input_variables=["era", "title"],
            output_variables=["synopsis", "review"],
            verbose=True,
        )
        title = "Tragedy at sunset on the beach"
        era = "Victorian England"
        review = overall_chain({"title": title, "era": era})
        print(review)
        assert len(review) == 4, "We should have 4 elements"
        assert review["title"] == title
        assert review["era"] == era
        assert review["synopsis"]
        assert review["review"]

    @pytest.mark.parametrize("model_type", available_models)
    def test_13_simple_sequential_chain(self, model_type, project_id, api_client):
        params = {
            GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
            GenParams.MAX_NEW_TOKENS: 100,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.TEMPERATURE: 0,
            GenParams.TOP_K: 50,
            GenParams.TOP_P: 1,
        }
        pt_1 = PromptTemplate(
            input_variables=["topic"],
            template="Generate a random question about {topic}: Question: ",
        )
        pt_2 = PromptTemplate(
            input_variables=["question"],
            template="Answer the following question: {question}",
        )
        model_1 = ModelInference(
            model_id=model_type,
            api_client=api_client,
            project_id=project_id,
            params=params,
        )
        llm_1 = WatsonxLLM(watsonx_model=model_1)
        model_2 = ModelInference(
            model_id=model_type,
            api_client=api_client,
            project_id=project_id,
            params=params,
        )
        llm_2 = WatsonxLLM(watsonx_model=model_2)
        prompt_to_flan = LLMChain(llm=llm_1, prompt=pt_1)
        flan_to_t5 = LLMChain(llm=llm_2, prompt=pt_2)

        qa = SimpleSequentialChain(chains=[prompt_to_flan, flan_to_t5], verbose=True)
        assert len(qa.chains) == 2
        assert pt_1.template == qa.chains[0].prompt.template
        assert pt_2.template == qa.chains[1].prompt.template
        review = qa.run("cat")
        assert review

    @pytest.mark.parametrize("model_type", available_models)
    def test_14_transformation_chain(self, model_type, project_id, api_client):
        with open(
            os.path.join(
                os.path.dirname(__file__), "../artifacts/state_of_the_union.txt"
            )
        ) as f:
            state_of_the_union = f.read()

        def transform_func(inputs: dict) -> dict:
            text = inputs["text"]
            shortened_text = "\n\n".join(text.split("\n\n")[:10])
            return {"output_text": shortened_text}

        transform_chain = TransformChain(
            input_variables=["text"],
            output_variables=["output_text"],
            transform=transform_func,
        )
        transform_review = transform_chain(state_of_the_union)
        print(f"\n Transform_review: {transform_review['output_text']}")
        assert transform_review["output_text"] in state_of_the_union

        template = """Summarize this text:

        {output_text}

        Summary:\n"""
        prompt = PromptTemplate(input_variables=["output_text"], template=template)
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        sequential_chain = SimpleSequentialChain(chains=[transform_chain, llm_chain])
        review = sequential_chain.run(state_of_the_union)
        print(f"\nReview: {review}")
        assert review

    @pytest.mark.skip(reason="This scenario not supported yet")
    def test_15_router_chain(self, project_id, api_client):
        physics_template = """You are a very smart physics professor. \
        You are great at answering questions about physics in a concise and easy to understand manner. \
        When you don't know the answer to a question you admit that you don't know.

        Here is a question:
        {input}"""

        math_template = """You are a very good mathematician. You are great at answering math questions. \
        You are so good because you are able to break down hard problems into their component parts, \
        answer the component parts, and then put them together to answer the broader question.

        Here is a question:
        {input}"""
        prompt_infos = [
            {
                "name": "physics",
                "description": "Good for answering questions about physics",
                "prompt_template": physics_template,
            },
            {
                "name": "math",
                "description": "Good for answering math questions",
                "prompt_template": math_template,
            },
        ]
        params = {
            GenParams.MAX_NEW_TOKENS: 50,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.REPETITION_PENALTY: 2,
        }
        model = ModelInference(
            model_id="eleutherai/gpt-neox-20b",
            api_client=api_client,
            project_id=project_id,
            params=params,
        )
        llm = WatsonxLLM(watsonx_model=model)
        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
            chain = LLMChain(llm=llm, prompt=prompt)
            destination_chains[name] = chain
        default_chain = ConversationChain(llm=llm, output_key="text")

        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )
        router_chain = LLMRouterChain.from_llm(llm, router_prompt)

        chain = MultiPromptChain(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=default_chain,
            verbose=True,
        )
        print(chain.run("What is black body radiation?"))

    @pytest.mark.parametrize("model_type", available_models)
    def test_16_conversation_buffer_memory_chain(
        self, model_type, project_id, api_client
    ):
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())
        qa_1 = "Answer briefly. What are the first 3 colors of a rainbow?\n"
        print(f"\n{qa_1}")
        response_1 = conversation(qa_1)
        print(response_1["response"])
        assert qa_1 == response_1["input"]
        assert response_1["response"]
        assert not response_1["history"]

        qa_2 = "And the first 4?"
        print(qa_2)
        response_2 = conversation(qa_2)
        print(response_2["response"])
        assert qa_2 == response_2["input"]
        assert response_2["response"]
        history = response_2["history"].split("\n", 2)
        assert qa_1 in history[0] + "\n"
        assert response_1["response"] in history[2]

    @pytest.mark.parametrize(
        "model_type",
        [
            model
            for model in available_models
            if model
            not in ["google/flan-t5-xxl", "google/flan-ul2", "ibm/granite-13b-chat-v1"]
        ],
    )
    def test_17_math_chain(self, model_type, project_id, api_client):
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm = WatsonxLLM(watsonx_model=model)
        llm_math = LLMMathChain.from_llm(llm, verbose=True)
        qa = "What is 2 raised to the 3 power?"
        response = llm_math(qa)
        assert qa == response["question"]
        assert response["answer"]

    @pytest.mark.parametrize("model_type", available_models)
    def test_18_to_langchain_wrapper(self, model_type, project_id, api_client):
        prompt_template = "What color is the {flower}?\n"
        model = ModelInference(
            model_id=model_type, api_client=api_client, project_id=project_id
        )
        llm_chain = LLMChain(
            llm=model.to_langchain(),
            prompt=PromptTemplate.from_template(prompt_template),
        )
        flower = "sunflower"
        print("\n" + prompt_template.replace("{flower}", flower))
        review = llm_chain(flower)
        print(f"Respond by use 'llm_chain(flower)': {review['text']}")
        assert flower == review["flower"]
        assert review["text"]
        review_run = llm_chain.run(flower)
        print(f"Respond by use 'llm_chain.run(flower)': {review['text']}")
        assert review["text"] == review_run
        review_predict = llm_chain.predict(flower=flower)
        print(f"Respond by use 'llm_chain.predict(flower)': {review['text']}")
        assert review["text"] == review_predict

    @pytest.mark.parametrize("model_type", available_models)
    def test_19_to_langchain_wrapper_with_param(
        self, model_type, project_id, api_client
    ):
        prompt_template = "What color is the {flower}?\n"
        params = {
            GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
            GenParams.MAX_NEW_TOKENS: 100,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.TEMPERATURE: 0,
            GenParams.TOP_K: 50,
            GenParams.TOP_P: 1,
        }
        model = ModelInference(
            model_id=model_type,
            api_client=api_client,
            project_id=project_id,
            params=params,
        )
        llm_chain = LLMChain(
            llm=model.to_langchain(),
            prompt=PromptTemplate.from_template(prompt_template),
        )
        flower = "sunflower"
        print("\n" + prompt_template.replace("{flower}", flower))
        review = llm_chain(flower)
        print(f"Respond by use 'llm_chain(flower)': {review['text']}")
        assert (
            flower == review["flower"]
        ), "Response under input key are not the same, but should be"
        assert review["text"], "Response under 'text' key should not be empty"
        review_run = llm_chain.run(flower)
        print(f"Respond by use 'llm_chain.run(flower)': {review['text']}")
        assert review_run, "Response should not be empty"
        review_predict = llm_chain.predict(flower=flower)
        print(f"Respond by use 'llm_chain.predict(flower)': {review['text']}")
        assert review_predict, "Response should not be empty"

    @pytest.mark.parametrize("model_type", available_embedding_models)
    def test_30_generate_embed_documents(self, model_type, project_id):
        watsonx_embedding = WatsonxEmbeddings(
            apikey=wml_credentials.api_key,
            model_id=model_type,
            url=wml_credentials.url,
            project_id=project_id,
        )
        generate_embedding = watsonx_embedding.embed_documents(texts=DOCUMENTS)
        assert len(generate_embedding) == len(
            DOCUMENTS
        ), "Amount of generated embeddings not equal amount of inputs"
        assert all(
            isinstance(el, float) for el in generate_embedding[0]
        ), "All elements in first list are not float"

    @pytest.mark.parametrize("model_type", available_embedding_models)
    def test_31_generate_embed_query(self, model_type, project_id, api_client) -> None:
        watsonx_embedding = WatsonxEmbeddings(
            model_id=model_type, watsonx_client=api_client, project_id=project_id
        )
        generate_embedding = watsonx_embedding.embed_query(text=DOCUMENTS[0])
        assert isinstance(generate_embedding, list) and isinstance(
            generate_embedding[0], float
        ), "Wrong type of response, should be list[float]"

    @pytest.mark.parametrize("model_type", available_embedding_models)
    def test_32_generate_embed_documents_with_param(
        self, model_type, project_id, api_client
    ) -> None:
        embed_params = {
            EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
        }
        watsonx_embedding = WatsonxEmbeddings(
            model_id=model_type,
            watsonx_client=api_client,
            project_id=project_id,
            params=embed_params,
        )
        generate_embedding = watsonx_embedding.embed_documents(texts=DOCUMENTS)
        assert len(generate_embedding) == len(
            DOCUMENTS
        ), "Amount of generated embeddings not equal amount of inputs"
        assert all(
            isinstance(el, float) for el in generate_embedding[0]
        ), "All elements in first list are not float"

    @pytest.mark.parametrize("model_type", available_embedding_models)
    def test_40_generate_embed_chroma_integration(
        self, project_id, api_client, model_type
    ) -> None:
        watsonx_embedding = WatsonxEmbeddings(
            model_id=model_type,
            watsonx_client=api_client,
            project_id=project_id,
        )
        vectorstore = Chroma.from_texts(
            texts=[
                "harrison worked at kensho",
                "I have blue eye's",
                "My name is Mateusz",
                "I got 5 at math in school",
                "My best friend is Lukas",
            ],
            collection_name=f"rag-chroma-40-{len(model_type)}",
            embedding=watsonx_embedding,
        )
        retriever = vectorstore.as_retriever()
        docs = retriever.get_relevant_documents(
            query="What is my best grade in school?"
        )

        assert docs, "Chroma retriever is empty, but not should be"
        assert isinstance(
            docs, list
        ), "Wrong type of get_relevant_documents, should be list"
        assert getattr(
            docs[0], "page_content", None
        ), "Relevant document do not contains page_content attribute, but should contains"

    @pytest.mark.parametrize("model_type", available_embedding_models)
    def test_41_chroma_similarity_search(
        self, project_id, api_client, model_type
    ) -> None:
        watsonx_embedding = WatsonxEmbeddings(
            model_id=model_type,
            watsonx_client=api_client,
            project_id=project_id,
        )
        docs = [
            Document(page_content="This is a demo document"),
            Document(page_content="This is another demo document"),
        ]
        vectorstore = Chroma.from_documents(
            documents=docs,
            collection_name=f"rag-chroma-41-{len(model_type)}",
            embedding=watsonx_embedding,
        )

        assert (
            len(vectorstore.similarity_search("demo document", k=999)) == 2
        ), "Similar search are not equal amount of docs"
        assert len(vectorstore.get()["documents"]) == len(
            docs
        ), "Documents got from vectorstore are not equal amount of docs"

    @pytest.mark.parametrize("model_type", available_embedding_models)
    def test_42_watsonx_vectorstore_search(
        self, project_id, api_client, model_type
    ) -> None:
        vectorstore_input = [
            "harrison worked at kensho",
            "I have blue eye's",
            "My name is Mateusz",
            "I got 5 at math in school",
            "My best friend is Lukas",
        ]
        watsonx_embedding = WatsonxEmbeddings(
            model_id=model_type,
            watsonx_client=api_client,
            project_id=project_id,
        )
        vectorstore = Chroma.from_texts(
            texts=vectorstore_input,
            collection_name=f"rag-chroma-42-{len(model_type)}",
            embedding=watsonx_embedding,
        )
        watsonx_vectorstore = VectorStore(
            client=api_client,
            embeddings=watsonx_embedding,
            langchain_vector_store=vectorstore,
        )

        vectorstore_search = watsonx_vectorstore.search(query="math", k=1)
        assert (
            len(vectorstore_search) == 1
        ), f"Vectorstore search should contains 1 element, but contains {len(vectorstore_search)}"

        vectorstore_search = watsonx_vectorstore.search(query="Mateusz", k=5)
        assert (
            vectorstore_search[0].page_content == vectorstore_input[2]
        ), "Wrong output element of vectorstore search"
