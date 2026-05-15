from langchain_core.prompts import ChatPromptTemplate
from ai.prompts import PORTFOLIO_SUMMARY_PROMPT
from ai.llm_service import llm

prompt = ChatPromptTemplate.from_template(
    PORTFOLIO_SUMMARY_PROMPT
)

portfolio_chain = prompt | llm