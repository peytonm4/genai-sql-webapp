def parse_final_answer(output: str) -> str:
    """Select final query output for LLM"""
    return output.split("Final answer: ")[1]

def parse_final_answer_from_ai(output: str) -> str:
    """Select final query output for LLM"""
    return output.split(": ")[1]
