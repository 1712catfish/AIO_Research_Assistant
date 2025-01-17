from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core import QueryBundle
from llama_index.core.response_synthesizers import Generation
from llama_index.core.schema import NodeWithScore, TextNode
code_qa_prompt = PromptTemplate(
    "You are a code assistant powered by a large language model. "
    "Your task is to help users solve programming problems, provide code examples, "
    "explain programming concepts, and debug code. "
    "Write python code to answer the question bellow\n"
    "---------------------\n"
    "{query_str}\n"
    "---------------------\n"
    "Answer: "
)


class CodeQueryEngine(CustomQueryEngine):
    llm: OpenAI
    qa_prompt: PromptTemplate
    synth: BaseSynthesizer
    def custom_query(self , query_str: str):
        query_bundle = QueryBundle(query_str)
        return self.synth.synthesize(query_bundle, [NodeWithScore(node=TextNode(text="temp"))])

def load_code_tool(llm):
    code_query_engine = CodeQueryEngine(
        llm = llm, 
        qa_prompt=code_qa_prompt, 
        synth=Generation(llm=llm, streaming=True, simple_template=code_qa_prompt))
    
    code_tool = QueryEngineTool.from_defaults(
        query_engine=code_query_engine,
        description="Useful for answering code-based questions"
    )
    
    return code_tool