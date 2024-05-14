from typing import Any, Dict


class Document(object):
    def __init__(self, page_content: str, metadata: Dict[str, Any]):
        self.page_content = page_content
        self.metadata = metadata
    
    def __repr__(self):
        return f"Document(page_content={repr(self.page_content)}, metadata={repr(self.metadata)})"


class QAResult(object):
    def __init__(self, summary: str, answers: Dict[str, Document]):
        self.summary = summary
        self.answers = answers
    
    def __repr__(self):
        info = ["QAResult(", f"    summary = {repr(self.summary)},", "    answers = {"]
        for ans, doc in self.answers.items():
            info.append(f"        {repr(ans)}: {doc},")
        info.append("    }")
        info.append(")")
        return "\n".join(info)