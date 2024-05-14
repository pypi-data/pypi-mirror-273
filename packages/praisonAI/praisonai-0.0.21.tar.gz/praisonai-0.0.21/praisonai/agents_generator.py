# praisonai/agents_generator.py

import sys
from .version import __version__
import yaml, os
from rich import print
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
load_dotenv()
import autogen
import gradio as gr
import argparse
from .auto import AutoGenerator
from crewai_tools import (
    CodeDocsSearchTool, CSVSearchTool, DirectorySearchTool, DOCXSearchTool, DirectoryReadTool,
    FileReadTool, TXTSearchTool, JSONSearchTool, MDXSearchTool, PDFSearchTool, RagTool,
    ScrapeElementFromWebsiteTool, ScrapeWebsiteTool, WebsiteSearchTool, XMLSearchTool, YoutubeChannelSearchTool,
    YoutubeVideoSearchTool
)
from .inbuilt_tools import *
import inspect
from pathlib import Path
import importlib
import importlib.util
from praisonai_tools import BaseTool

class AgentsGenerator:
    def __init__(self, agent_file, framework, config_list):
        self.agent_file = agent_file
        self.framework = framework
        self.config_list = config_list
        
    def is_function_or_decorated(self, obj):
        return inspect.isfunction(obj) or hasattr(obj, '__call__')

    def load_tools_from_module(self, module_path):
        spec = importlib.util.spec_from_file_location("tools_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return {name: obj for name, obj in inspect.getmembers(module, self.is_function_or_decorated)}
    
    def load_tools_from_module_class(self, module_path):
        spec = importlib.util.spec_from_file_location("tools_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return {name: obj() for name, obj in inspect.getmembers(module, lambda x: inspect.isclass(x) and (x.__module__.startswith('langchain_community.tools') or issubclass(x, BaseTool)) and x is not BaseTool)}

    def load_tools_from_package(self, package_path):
        tools_dict = {}
        for module_file in os.listdir(package_path):
            if module_file.endswith('.py') and not module_file.startswith('__'):
                module_name = f"{package_path.name}.{module_file[:-3]}"  # Remove .py for import
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module, self.is_function_or_decorated):
                    tools_dict[name] = obj
        return tools_dict

    def generate_crew_and_kickoff(self):
        if self.agent_file == '/app/api:app' or self.agent_file == 'api:app':
            self.agent_file = 'agents.yaml'
        try:
            with open(self.agent_file, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"File not found: {self.agent_file}")
            return

        topic = config['topic']
        tools_dict = {
            'CodeDocsSearchTool': CodeDocsSearchTool(),
            'CSVSearchTool': CSVSearchTool(),
            'DirectorySearchTool': DirectorySearchTool(),
            'DOCXSearchTool': DOCXSearchTool(),
            'DirectoryReadTool': DirectoryReadTool(),
            'FileReadTool': FileReadTool(),
            # 'GithubSearchTool': GithubSearchTool(),
            # 'SeperDevTool': SeperDevTool(),
            'TXTSearchTool': TXTSearchTool(),
            'JSONSearchTool': JSONSearchTool(),
            'MDXSearchTool': MDXSearchTool(),
            'PDFSearchTool': PDFSearchTool(),
            # 'PGSearchTool': PGSearchTool(),
            'RagTool': RagTool(),
            'ScrapeElementFromWebsiteTool': ScrapeElementFromWebsiteTool(),
            'ScrapeWebsiteTool': ScrapeWebsiteTool(),
            'WebsiteSearchTool': WebsiteSearchTool(),
            'XMLSearchTool': XMLSearchTool(),
            'YoutubeChannelSearchTool': YoutubeChannelSearchTool(),
            'YoutubeVideoSearchTool': YoutubeVideoSearchTool(),
        }
        root_directory = os.getcwd()
        tools_py_path = os.path.join(root_directory, 'tools.py')
        tools_dir_path = Path(root_directory) / 'tools'
        
        if os.path.isfile(tools_py_path):
            tools_dict.update(self.load_tools_from_module_class(tools_py_path))
            # print("tools.py exists in the root directory. Loading tools.py and skipping tools folder.")
        elif tools_dir_path.is_dir():
            tools_dict.update(self.load_tools_from_module_class(tools_dir_path))
            # print("tools folder exists in the root directory")
        
        framework = self.framework or config.get('framework')

        agents = {}
        tasks = []
        if framework == "autogen":
            # Load the LLM configuration dynamically
            # print(self.config_list)
            llm_config = {"config_list": self.config_list}
            
            # Assuming the user proxy agent is set up as per your requirements
            user_proxy = autogen.UserProxyAgent(
                name="User",
                human_input_mode="NEVER",
                is_termination_msg=lambda x: (x.get("content") or "").rstrip().rstrip(".").lower().endswith("terminate") or "TERMINATE" in (x.get("content") or ""),
                code_execution_config={
                    "work_dir": "coding",
                    "use_docker": False,
                },
                # additional setup for the user proxy agent
            )
            
            for role, details in config['roles'].items():
                agent_name = details['role'].format(topic=topic).replace("{topic}", topic)
                agent_goal = details['goal'].format(topic=topic)
                # Creating an AssistantAgent for each role dynamically
                agents[role] = autogen.AssistantAgent(
                    name=agent_name,
                    llm_config=llm_config,
                    system_message=details['backstory'].format(topic=topic)+". Must Reply \"TERMINATE\" in the end when everything is done.",
                )
                for tool in details.get('tools', []):
                    if tool in tools_dict:
                        try:
                            tool_class = globals()[f'autogen_{type(tools_dict[tool]).__name__}']
                            print(f"Found {tool_class.__name__} for {tool}")
                        except KeyError:
                            print(f"Warning: autogen_{type(tools_dict[tool]).__name__} function not found. Skipping this tool.")
                            continue
                        tool_class(agents[role], user_proxy)

                # Preparing tasks for initiate_chats
                for task_name, task_details in details.get('tasks', {}).items():
                    description_filled = task_details['description'].format(topic=topic)
                    expected_output_filled = task_details['expected_output'].format(topic=topic)
                    
                    chat_task = {
                        "recipient": agents[role],
                        "message": description_filled,
                        "summary_method": "last_msg", 
                        # Additional fields like carryover can be added based on dependencies
                    }
                    tasks.append(chat_task)

            response = user_proxy.initiate_chats(tasks)
            result = "### Output ###\n"+response[-1].summary if hasattr(response[-1], 'summary') else ""
        else:
            for role, details in config['roles'].items():
                role_filled = details['role'].format(topic=topic)
                goal_filled = details['goal'].format(topic=topic)
                backstory_filled = details['backstory'].format(topic=topic)
                
                # Adding tools to the agent if exists
                agent_tools = [tools_dict[tool] for tool in details.get('tools', []) if tool in tools_dict]
                agent = Agent(role=role_filled, goal=goal_filled, backstory=backstory_filled, tools=agent_tools, allow_delegation=False)
                agents[role] = agent

                for task_name, task_details in details.get('tasks', {}).items():
                    description_filled = task_details['description'].format(topic=topic)
                    expected_output_filled = task_details['expected_output'].format(topic=topic)

                    task = Task(description=description_filled, expected_output=expected_output_filled, agent=agent)
                    tasks.append(task)
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=2
            )

            response = crew.kickoff()
            result = f"### Task Output ###\n{response}"
        return result