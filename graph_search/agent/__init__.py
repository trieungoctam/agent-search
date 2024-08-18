import os
from datetime import datetime

from actions import ActionExecutor, BingBrowser

import agent.models as llm_factory
from agent.search_agent import (MindSearchAgent,MindSearchProtocol)
from agent.search_prompt import (
    FINAL_RESPONSE_EN, GRAPH_PROMPT_EN,
    fewshot_example_en,
    graph_fewshot_example_en,
    searcher_context_template_en,
    searcher_input_template_en,
    searcher_system_prompt_en)

LLM = {}


def init_agent(lang='cn', model_format='internlm_server',search_engine='DuckDuckGoSearch'):
    llm = LLM.get(model_format, None)
    if llm is None:
        llm_cfg = getattr(llm_factory, model_format)
        if llm_cfg is None:
            raise NotImplementedError
        llm_cfg = llm_cfg.copy()
        llm = llm_cfg.pop('type')(**llm_cfg)
        LLM[model_format] = llm

    interpreter_prompt = GRAPH_PROMPT_EN
    plugin_prompt = searcher_system_prompt_en
    if not model_format.lower().startswith('internlm'):
        interpreter_prompt += graph_fewshot_example_en
        plugin_prompt += fewshot_example_en

    agent = MindSearchAgent(
        llm=llm,
        protocol=MindSearchProtocol(meta_prompt=datetime.now().strftime(
            'The current date is %Y-%m-%d.'),
                                    interpreter_prompt=interpreter_prompt,
                                    response_prompt=FINAL_RESPONSE_EN),
        searcher_cfg=dict(
            llm=llm,
            plugin_executor=ActionExecutor(
                BingBrowser(searcher_type=search_engine,
                            topk=6,
                            api_key=os.environ.get('BING_API_KEY',
                                                   'YOUR BING API'))),
            protocol=MindSearchProtocol(
                meta_prompt=datetime.now().strftime(
                    'The current date is %Y-%m-%d.'),
                plugin_prompt=plugin_prompt,
            ),
            template=dict(input=searcher_input_template_en,
                          context=searcher_context_template_en)),
        max_turn=10)
    return agent