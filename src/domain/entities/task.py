class Task:
    def __init__(self, name: str, steps: list[str], task_profile: list[str], agent,
    tools: list[str], async_execution: bool, context: str, config: str, output_json: str,output_pydantic: str, output_file: str, human_input: bool, converter_cls: str, callback: callable):
        self.name = name
        self.steps = steps
        self.description = task_profile
        self.expected_output = task_profile
        self.agent = agent
        self.tools = tools
        self.async_execution = async_execution
        self.context = context
        self.config = config
        self.output_json = output_json
        self.output_pydantic = output_pydantic
        self.output_file = output_file
        self.human_input = human_input
        self.converter_cls = converter_cls
        self.callback = callback

    def __repr__(self):
        return f"<Task name={self.name}, steps={len(self.steps)} steps, description={self.description}, expected_output={self.expected_output}, agent={self.agent}, tools={self.tools}, async_execution={self.async_execution}, context={self.context}, config={self.config}, output_json={self.output_json}, output_pydantic={self.output_pydantic}, output_file={self.output_file}, human_input={self.human_input}, converter_cls={self.converter_cls}, callback={self.callback}>"