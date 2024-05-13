from typing import Optional

import func_agent
from hamilton import driver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.utilities import PythonREPL

from burr import core
from burr.core import Action, ApplicationBuilder, State
from burr.core.action import action
from burr.lifecycle import PostRunStepHook
from burr.tracking import client as burr_tclient

# Initialize some things needed for tools.
# see func_agent.py for the code for this pipeline
tool_dag = driver.Builder().with_modules(func_agent).build()
# Will run code provided by the LLM.
repl = PythonREPL()


def python_repl(code: str) -> dict:
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user.

    :param code: string. The python code to execute.
    :return: the output
    """
    try:
        result = repl.run(code)
    except BaseException as e:
        return {"error": repr(e), "status": "error"}
    return {"status": "success", "code": f"```python\n{code}\n```", "Stdout": result}


@action(reads=["query", "messages"], writes=["messages", "next_hop"])
def chart_generator(state: State) -> tuple[dict, State]:
    """
    Generates a chart based on the provided query and updates the state.

    :param state: The current state of the application.
    :return: A tuple containing the result of the tool execution and the updated state.
    """
    query = state["query"]
    # see func_agent.py for the code for this pipeline
    result = tool_dag.execute(
        ["executed_tool_calls", "parsed_tool_calls", "llm_function_message"],
        inputs={
            "tools": [python_repl],
            "system_message": "Any charts you display will be visible by the user.",
            "user_query": query,
            "messages": state["messages"],
        },
    )
    # _code = result["parsed_tool_calls"][0]["function_args"]["code"]
    new_messages = [result["llm_function_message"]]
    for tool_name, tool_result in result["executed_tool_calls"]:
        new_messages.append(tool_result)
    if len(new_messages) == 1:
        if new_messages[0]["content"] and "FINAL ANSWER" in new_messages[0]["content"]:
            next_hop = "complete"
        else:
            next_hop = "continue"
    else:
        # assess tool results
        next_hop = "self"
    state = state.update(next_hop=next_hop)
    for message in new_messages:
        state = state.append(messages=message)
    return result, state


tavily_tool = TavilySearchResults(max_results=5)


@action(reads=["query", "messages"], writes=["messages", "next_hop"])
def researcher(state: State) -> tuple[dict, State]:
    """
    Performs research based on the provided query and updates the state.

    :param state: The current state of the application.
    :return: A tuple containing the result of the tool execution and the updated state.
    """
    query = state["query"]
    # see func_agent.py for the code for this pipeline
    result = tool_dag.execute(
        ["executed_tool_calls", "parsed_tool_calls", "llm_function_message"],
        inputs={
            "tools": [tavily_tool],
            "system_message": "You should provide accurate data for the chart generator to use.",
            "user_query": query,
            "messages": state["messages"],
        },
    )
    new_messages = [result["llm_function_message"]]
    for tool_name, tool_result in result["executed_tool_calls"]:
        new_messages.append(tool_result)
    if len(new_messages) == 1:
        if "FINAL ANSWER" in new_messages[0]["content"]:
            next_hop = "complete"
        else:
            next_hop = "continue"
    else:
        # assess tool results
        next_hop = "self"
    state = state.update(next_hop=next_hop)
    for message in new_messages:
        state = state.append(messages=message)
    return result, state


@action(reads=[], writes=[])
def terminal_step(state: State) -> tuple[dict, State]:
    """One can express a terminal action like this."""
    return {}, state


class PrintStepHook(PostRunStepHook):
    """Example of a post run step hook that prints the state and action."""

    def post_run_step(self, *, state: "State", action: "Action", **future_kwargs):
        print("action=====\n", action)
        print("state======\n", state)


def default_state_and_entry_point() -> tuple[dict, str]:
    """Default state and entry point for the application."""
    return {
        "messages": [],
        "query": "Fetch the UK's GDP over the past 5 years,"
        " then draw a line graph of it."
        " Once you code it up, finish.",
        "next_hop": "",
    }, "researcher"


def application(app_instance_id: Optional[str] = None):
    project_name = "demo_hamilton-multi-agent"
    # TODO -- use the new persistence API
    if app_instance_id:
        state, entry_point = burr_tclient.LocalTrackingClient.load_state(
            project_name,
            app_instance_id,
        )
    else:
        state, entry_point = default_state_and_entry_point()
    app = (
        ApplicationBuilder()
        .with_state(**state)
        .with_actions(
            researcher=researcher,
            chart_generator=chart_generator,
            terminal=terminal_step,
        )
        .with_transitions(
            ("researcher", "researcher", core.expr("next_hop == 'self'")),
            ("researcher", "chart_generator", core.expr("next_hop == 'continue'")),
            ("chart_generator", "chart_generator", core.expr("next_hop == 'self'")),
            ("chart_generator", "researcher", core.expr("next_hop == 'continue'")),
            (
                "researcher",
                "terminal",
                core.expr("next_hop == 'complete'"),
            ),
            (
                "chart_generator",
                "terminal",
                core.expr("next_hop == 'complete'"),
            ),
        )
        .with_entrypoint(entry_point)
        .with_hooks(PrintStepHook())
        .with_tracker(project=project_name)
        .build()
    )
    return app


if __name__ == "__main__":
    """
    The entry point of the application.

    If an app_id is provided, the application will restart from the last
    sequence in that state.
    E.g. fine the ID in the UI and then put it in here "app_4d1618d2-79d1-4d89-8e3f-70c216c71e63"
    """
    app = application(app_instance_id=None)
    app.visualize(output_file_path="statemachine", include_conditions=True, view=True, format="png")
    app.run(halt_after=["terminal"])

    # some test code
    # tavily_tool = TavilySearchResults(max_results=5)
    # result = tool_dag.execute(
    #     ["executed_tool_calls"],
    #     inputs={
    #         "tools": [tavily_tool],
    #         "system_message": "You should provide accurate data for the chart generator to use.",
    #         "user_query": "Fetch the UK's GDP over the past 5 years,"
    #         " then draw a line graph of it."
    #         " Once you have written code for the graph, finish.",
    #     },
    # )
    # import pprint
    #
    # pprint.pprint(result)
    #
    # result = tool_dag.execute(
    #     ["executed_tool_calls"],
    #     inputs={
    #         "tools": [python_repl],
    #         "system_message": "Any charts you display will be visible by the user.",
    #         "user_query": "Draw a simple line graph of y = x",
    #     },
    # )
    # import pprint
    #
    # pprint.pprint(result)
