from okahu_apptrace.utils import task_wrapper, atask_wrapper, llm_wrapper, allm_wrapper

class WrapperMethod:
    def __init__(
            self,
            package: str,
            object: str,
            method: str,
            span_name: str = None,
            wrapper = task_wrapper
            ):
        self.package = package
        self.object = object
        self.method = method
        self.span_name = span_name
        self.wrapper = wrapper
        

LANGCHAIN_METHODS = [
    {
        "package": "langchain.prompts.base",
        "object": "BasePromptTemplate",
        "method": "invoke",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.prompts.base",
        "object": "BasePromptTemplate",
        "method": "ainvoke",
        "wrapper": atask_wrapper,
    },
    {
        "package": "langchain.chat_models.base",
        "object": "BaseChatModel",
        "method": "invoke",
        "wrapper": llm_wrapper,
    },
    {
        "package": "langchain.chat_models.base",
        "object": "BaseChatModel",
        "method": "ainvoke",
        "wrapper": allm_wrapper,
    },
    {
        "package": "langchain_core.language_models.llms",
        "object": "LLM",
        "method": "_generate",
        "wrapper": llm_wrapper,
    },
    {
        "package": "langchain_core.language_models.llms",
        "object": "LLM",
        "method": "_agenerate",
        "wrapper": llm_wrapper,
    },
    {
        "package": "langchain_core.retrievers",
        "object": "BaseRetriever",
        "method": "get_relevant_documents",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain_core.retrievers",
        "object": "BaseRetriever",
        "method": "aget_relevant_documents",
        "wrapper": atask_wrapper,
    },
    {
        "package": "langchain.schema",
        "object": "BaseOutputParser",
        "method": "invoke",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.schema",
        "object": "BaseOutputParser",
        "method": "ainvoke",
        "wrapper": atask_wrapper,
    },
    {
        "package": "langchain.schema.runnable",
        "object": "RunnableSequence",
        "method": "invoke",
        "span_name": "langchain.workflow",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.schema.runnable",
        "object": "RunnableSequence",
        "method": "ainvoke",
        "span_name": "langchain.workflow",
        "wrapper": atask_wrapper,
    },
    {
        "package": "langchain.schema.runnable",
        "object": "RunnableParallel",
        "method": "invoke",
        "span_name": "langchain.workflow",
        "wrapper": task_wrapper,
    },
    {
        "package": "langchain.schema.runnable",
        "object": "RunnableParallel",
        "method": "ainvoke",
        "span_name": "langchain.workflow",
        "wrapper": atask_wrapper,
    },
    
]

LLAMAINDEX_METHODS = [
    {
        "package": "llama_index.core.indices.base_retriever",
        "object": "BaseRetriever",
        "method": "retrieve",
        "span_name": "llamaindex.retrieve",
        "wrapper": task_wrapper
    },
    {
        "package": "llama_index.core.indices.base_retriever",
        "object": "BaseRetriever",
        "method": "aretrieve",
        "span_name": "llamaindex.retrieve",
        "wrapper": atask_wrapper
    },
    {
        "package": "llama_index.core.base.base_query_engine",
        "object": "BaseQueryEngine",
        "method": "query",
        "span_name": "llamaindex.query",
        "wrapper": task_wrapper,
    },
    {
        "package": "llama_index.core.base.base_query_engine",
        "object": "BaseQueryEngine",
        "method": "aquery",
        "span_name": "llamaindex.query",
        "wrapper": atask_wrapper,
    },
    {
        "package": "llama_index.core.llms.custom",
        "object": "CustomLLM",
        "method": "chat",
        "span_name": "llamaindex.llmchat",
        "wrapper": task_wrapper,
    },
    {
        "package": "llama_index.core.llms.custom",
        "object": "CustomLLM",
        "method": "achat",
        "span_name": "llamaindex.llmchat",
        "wrapper": atask_wrapper,
    }
]

METHODS_LIST = LANGCHAIN_METHODS + LLAMAINDEX_METHODS

