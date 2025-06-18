# code from langgraph example: https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/ainsight_langgraph.ipynb
# Changes:
#   The connection address for ChatOpenAI has benn updated to an RNGD-based OpenAI-comptaible server.
#   The Tavily API call results are now stored, allowing execution without an API key.

import os
import json
import time
from typing import Dict, List, Any, TypedDict, Optional
from datetime import datetime
from pydantic import BaseModel
import subprocess
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph

# Initialize API clients
llm = ChatOpenAI(
    model="llama3.1-8b.bf16",
    temperature=0.1,
    base_url = "http://localhost:8000/v1/",
    openai_api_key = "EMPTY",
)

class Article(BaseModel):
    """
    Represents a single news article

    Attributes:
        title (str): Article headline
        url (str): Source URL
        content (str): Article content
    """
    title: str
    url: str
    content: str

class Summary(TypedDict):
    """
    Represents a processed article summary

    Attributes:
        title (str): Original article title
        summary (str): Generated summary
        url (str): Source URL for reference
    """
    title: str
    summary: str
    url: str

# This defines what information we can store and pass between nodes later
class GraphState(TypedDict):
    """
    Maintains workflow state between agents

    Attributes:
        articles (Optional[List[Article]]): Found articles
        summaries (Optional[List[Summary]]): Generated summaries
        report (Optional[str]): Final compiled report
    """
    articles: Optional[List[Article]]
    summaries: Optional[List[Summary]]
    report: Optional[str]

class NewsSearcher:
    """
    Agent responsible for finding relevant AI/ML news articles
    using the Tavily search API
    """
    
    def search(self) -> List[Article]:
        """
        Performs news search with configured parameters
        
        Returns:
            List[Article]: Collection of found articles
        """

        #response = tavily.search(
            #query="artificial intelligence and machine learning news", 
            #topic="news",
            #time_period="1w",
            #search_depth="advanced",
            #max_results=5
        #)

        response = json.load(open('response.json'))
        
        articles = []
        for result in response['results']:
            articles.append(Article(
                title=result['title'],
                url=result['url'],
                content=result['content']
            ))
        
        return articles

class Summarizer:
    """
    Agent that processes articles and generates accessible summaries
    using gpt-4o-mini
    """
    
    def __init__(self):
        self.system_prompt = """
        You are an AI expert who makes complex topics accessible 
        to general audiences. Summarize this article in 2-3 sentences, focusing on the key points 
        and explaining any technical terms simply.
        """
    
    def summarize(self, article: Article) -> str:
        """
        Generates an accessible summary of a single article
        
        Args:
            article (Article): Article to summarize
            
        Returns:
            str: Generated summary
        """
        response = llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Title: {article.title}\n\nContent: {article.content}")
        ])
        return response.content

class Publisher:
    """
    Agent that compiles summaries into a formatted report 
    and saves it to disk
    """
    
    def create_report(self, summaries: List[Dict]) -> str:
        """
        Creates and saves a formatted markdown report
        
        Args:
            summaries (List[Dict]): Collection of article summaries
            
        Returns:
            str: Generated report content
        """
        prompt = """
        Create a weekly AI/ML news report for the general public. 
        Format it with:
        1. A brief introduction
        2. The main news items with their summaries
        3. Links for further reading
        
        Make it engaging and accessible to non-technical readers.
        """
        
        # Format summaries for the LLM
        summaries_text = "\n\n".join([
            f"Title: {item['title']}\nSummary: {item['summary']}\nSource: {item['url']}"
            for item in summaries
        ])
        
        # Generate report
        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=summaries_text)
        ])
        
        # Add metadata and save
        current_date = '2025-03-14'
        markdown_content = f"""
        Generated on: {current_date}

        {response.content}
        """
        
        #filename = f"ai_news_report_{current_date}.md"
        #with open(filename, 'w') as f:
            #f.write(markdown_content)
        
        return response.content


def search_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node for article search
    
    Args:
        state (Dict[str, Any]): Current workflow state
        
    Returns:
        Dict[str, Any]: Updated state with found articles
    """
    searcher = NewsSearcher()
    state['articles'] = searcher.search() 
    return state

def summarize_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node for article summarization
    
    Args:
        state (Dict[str, Any]): Current workflow state
        
    Returns:
        Dict[str, Any]: Updated state with summaries
    """
    summarizer = Summarizer()
    state['summaries'] = []
    
    for article in state['articles']: # Uses articles from previous node
        summary = summarizer.summarize(article)
        state['summaries'].append({
            'title': article.title,
            'summary': summary,
            'url': article.url
        })
    return state

def publish_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node for report generation
    
    Args:
        state (Dict[str, Any]): Current workflow state
        
    Returns:
        Dict[str, Any]: Updated state with final report
    """
    publisher = Publisher()
    report_content = publisher.create_report(state['summaries'])
    state['report'] = report_content
    return state


def create_workflow() -> StateGraph:
    """
    Constructs and configures the workflow graph
    search -> summarize -> publish

    Returns:
        StateGraph: Compiled workflow ready for execution
    """

    # Create a workflow (graph) initialized with our state schema
    workflow = StateGraph(state_schema=GraphState)

    # Add processing nodes that we will flow between
    workflow.add_node("search", search_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("publish", publish_node)

    # Define the flow with edges
    workflow.add_edge("search", "summarize") # search results flow to summarizer
    workflow.add_edge("summarize", "publish") # summaries flow to publisher

    # Set where to start
    workflow.set_entry_point("search")

    return workflow.compile()

def start_furiosa_llm_servers():
    server = subprocess.Popen(
        [
            "furiosa-llm",
            "serve",
            "furiosa-ai/Llama-3.1-8B-Instruct",
            "--host",
            "localhost",
            "--port",
            "8000",
            "--devices",
            "npu:0",
        ]
    )
    return server

if __name__ == "__main__":

    server = start_furiosa_llm_servers()
    time.sleep(50)
    try:
        # Initialize and run workflow
        workflow = create_workflow()
        final_state = workflow.invoke({
            "articles": None,
            "summaries": None,
            "report": None
        })

        # Display results
        print("\n=== AI/ML Weekly News Report ===\n")
        print(final_state['report'])
    finally:
        server.terminate()  # Clean up server after execution
        server.wait()
