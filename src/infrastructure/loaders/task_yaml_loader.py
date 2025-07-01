from crewai import Task

class TaskLoader:
    @staticmethod
    def load_tasks(task_dict: dict, agent=None, context=None, output_file=None) -> Task:
        task_kwargs = {
            "description": task_dict["description"],
            "expected_output": task_dict.get("expected_output", ""),
            "agent": agent,
            "tools": task_dict.get("tools", []),
            "async_execution": task_dict.get("async_execution", False),
            "context": context,
            "config": task_dict.get("config"),
            "output_json": task_dict.get("output_json"),
            "output_pydantic": task_dict.get("output_pydantic"),
            "human_input": task_dict.get("human_input", False),
            "converter_cls": task_dict.get("converter_cls"),
            "callback": task_dict.get("callback"),
        }
        if output_file is not None:
            task_kwargs["output_file"] = output_file

        return Task(**task_kwargs)