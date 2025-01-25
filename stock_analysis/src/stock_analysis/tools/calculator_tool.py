import ast
from crewai.tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Calculator tool"
    description: str = (
        "Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. The input to this tool should be a mathematical  expression, a couple examples are `200*7` or `5000/2*10."
    )

    def _run(self, operation: str) -> int:
        # Implementation goes here
        #return ast.literal_eval(operation)
        return eval(operation)