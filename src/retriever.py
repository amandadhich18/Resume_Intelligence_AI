import numpy as np
import re


def _keyword_score(query, chunk):
    """
    Section-aware keyword scoring.

    Gives an additional score when the user's question
    strongly indicates a particular resume section.
    """

    query_lower = query.lower().strip()
    section = chunk["section"].upper()

    score = 0.0

    # ------------------------------------------
    # PROFESSIONAL EXPERIENCE
    # ------------------------------------------

    if section == "PROFESSIONAL EXPERIENCE":

        experience_phrases = [
            "currently work",
            "currently working",
            "where does",
            "where do",
            "work at",
            "works at",
            "working at",
            "current company",
            "current employer",
            "employer",
            "job",
            "employment",
            "professional experience",
            "work experience"
        ]

        if any(
            phrase in query_lower
            for phrase in experience_phrases
        ):
            score += 1.0

        # Individual keywords
        experience_keywords = [
            "work",
            "working",
            "experience",
            "company",
            "employer",
            "job",
            "role",
            "position"
        ]

        for keyword in experience_keywords:
            if keyword in query_lower:
                score += 0.10

    # ------------------------------------------
    # PROJECTS
    # ------------------------------------------

    elif section == "PROJECTS":

        project_phrases = [
            "what projects",
            "which projects",
            "projects has",
            "projects did",
            "worked on",
            "built",
            "developed projects"
        ]

        if any(
            phrase in query_lower
            for phrase in project_phrases
        ):
            score += 1.0

        project_keywords = [
            "project",
            "projects",
            "dashboard",
            "built",
            "developed"
        ]

        for keyword in project_keywords:
            if keyword in query_lower:
                score += 0.10

    # ------------------------------------------
    # TECHNICAL SKILLS
    # ------------------------------------------

    elif section == "TECHNICAL SKILLS":

        skill_phrases = [
            "technical skills",
            "programming skills",
            "programming",
            "database skills",
            "database",
            "sql technologies",
            "technologies",
            "tools",
            "data visualization",
            "visualization tools"
        ]

        if any(
            phrase in query_lower
            for phrase in skill_phrases
        ):
            score += 1.0

        skill_keywords = [
            "skill",
            "skills",
            "programming",
            "database",
            "sql",
            "python",
            "tools",
            "technology",
            "technologies",
            "visualization"
        ]

        for keyword in skill_keywords:
            if keyword in query_lower:
                score += 0.10

    # ------------------------------------------
    # EDUCATION
    # ------------------------------------------

    elif section == "EDUCATION":

        education_phrases = [
            "educational qualification",
            "educational background",
            "education",
            "degree",
            "qualification",
            "academic background",
            "graduation",
            "college",
            "university"
        ]

        if any(
            phrase in query_lower
            for phrase in education_phrases
        ):
            score += 1.0

        education_keywords = [
            "education",
            "degree",
            "qualification",
            "college",
            "university",
            "graduation"
        ]

        for keyword in education_keywords:
            if keyword in query_lower:
                score += 0.10

    # ------------------------------------------
    # CERTIFICATIONS
    # ------------------------------------------

    elif section == "CERTIFICATIONS":

        certification_phrases = [
            "certification",
            "certifications",
            "certificate",
            "certificates"
        ]

        if any(
            phrase in query_lower
            for phrase in certification_phrases
        ):
            score += 1.0

    # ------------------------------------------
    # PROFESSIONAL SUMMARY
    # ------------------------------------------

    elif section == "PROFESSIONAL SUMMARY":

        summary_phrases = [
            "professional background",
            "professional summary",
            "career background",
            "career summary",
            "profile",
            "background"
        ]

        if any(
            phrase in query_lower
            for phrase in summary_phrases
        ):
            score += 0.8

    return score


def retrieve_chunks(
    query,
    chunks,
    embeddings,
    model,
    top_k=3
):
    """
    Retrieve the most relevant resume chunks.

    Ranking combines:
    1. Semantic similarity
    2. Section-aware keyword scoring
    """

    # ------------------------------------------
    # 1. Query embedding
    # ------------------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    # ------------------------------------------
    # 2. Semantic similarity
    # ------------------------------------------

    semantic_scores = np.dot(
        embeddings,
        query_embedding
    )

    # ------------------------------------------
    # 3. Hybrid scoring
    # ------------------------------------------

    final_scores = []

    for index, chunk in enumerate(chunks):

        semantic_score = float(
            semantic_scores[index]
        )

        keyword_score = _keyword_score(
            query,
            chunk
        )

        # Semantic similarity remains important,
        # but section matching gets a strong boost.
        final_score = (
            semantic_score
            + keyword_score
        )

        final_scores.append(final_score)

    final_scores = np.array(final_scores)

    # ------------------------------------------
    # 4. Rank chunks
    # ------------------------------------------

    top_indexes = np.argsort(
        final_scores
    )[::-1][:top_k]

    # ------------------------------------------
    # 5. Return chunks
    # ------------------------------------------

    retrieved_chunks = []

    for index in top_indexes:

        chunk = chunks[index].copy()

        chunk["score"] = float(
            final_scores[index]
        )

        chunk["semantic_score"] = float(
            semantic_scores[index]
        )

        chunk["keyword_score"] = float(
            final_scores[index]
            - semantic_scores[index]
        )

        retrieved_chunks.append(chunk)

    return retrieved_chunks