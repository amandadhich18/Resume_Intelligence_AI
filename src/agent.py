from src.retriever import retrieve_chunks
from src.dspy_module import ResumeDSPyModule


class ResumeAgent:
    """
    AI Agent for Resume Intelligence AI.

    The agent retrieves relevant resume information
    and uses DSPy to generate the final answer.
    """

    def __init__(self, chunks, embeddings, model):
        self.chunks = chunks
        self.embeddings = embeddings
        self.model = model

        # Initialize DSPy module
        self.dspy_module = ResumeDSPyModule()

    def answer_question(self, query, top_k=3):
        """
        Retrieve relevant resume information
        and generate an answer using DSPy.
        """

        # --------------------------------------
        # STEP 1: Retrieve relevant information
        # --------------------------------------

        retrieved_chunks = retrieve_chunks(
            query,
            self.chunks,
            self.embeddings,
            self.model,
            top_k=top_k
        )

        # --------------------------------------
        # STEP 2: Build resume context
        # --------------------------------------

        resume_context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        # --------------------------------------
        # STEP 3: Generate answer using DSPy
        # --------------------------------------

        answer = self.dspy_module(
            resume_context=resume_context,
            question=query
        )

        # --------------------------------------
        # STEP 4: Return result
        # --------------------------------------

        return {
            "answer": answer,
            "sources": retrieved_chunks
        }