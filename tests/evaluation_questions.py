# ==========================================
# PHASE 4 - ANSWER QUALITY EVALUATION
# ==========================================

EVALUATION_QUESTIONS = [

    # ======================================
    # ANSWERABLE QUESTIONS
    # ======================================

    {
        "question": "What programming and database skills does Aman have?",
        "type": "answerable",
        "expected_sections": ["TECHNICAL SKILLS"]
    },

    {
        "question": "Where does Aman currently work?",
        "type": "answerable",
        "expected_sections": ["PROFESSIONAL EXPERIENCE"]
    },

    {
        "question": "What is Aman's educational qualification?",
        "type": "answerable",
        "expected_sections": ["EDUCATION"]
    },

    {
        "question": "What projects has Aman worked on?",
        "type": "answerable",
        "expected_sections": ["PROJECTS"]
    },

    {
        "question": "What certifications does Aman have?",
        "type": "answerable",
        "expected_sections": ["CERTIFICATIONS"]
    },

    {
        "question": "What experience does Aman have with Power BI?",
        "type": "answerable",
        "expected_sections": [
            "TECHNICAL SKILLS",
            "PROFESSIONAL EXPERIENCE",
            "PROFESSIONAL SUMMARY"
        ]
    },

    {
        "question": "What tools does Aman use for data visualization?",
        "type": "answerable",
        "expected_sections": ["TECHNICAL SKILLS"]
    },

    {
        "question": "What SQL technologies does Aman know?",
        "type": "answerable",
        "expected_sections": ["TECHNICAL SKILLS"]
    },


    # ======================================
    # UNANSWERABLE / HALLUCINATION TESTS
    # ======================================

    {
        "question": "What is Aman's age?",
        "type": "unanswerable",
        "expected_sections": []
    },

    {
        "question": "What is Aman's salary?",
        "type": "unanswerable",
        "expected_sections": []
    },

    {
        "question": "What is Aman's favorite programming language?",
        "type": "unanswerable",
        "expected_sections": []
    },

    {
        "question": "Where was Aman born?",
        "type": "unanswerable",
        "expected_sections": []
    },

    {
        "question": "What is Aman's favorite company?",
        "type": "unanswerable",
        "expected_sections": []
    },

    {
        "question": "What is Aman's phone password?",
        "type": "unanswerable",
        "expected_sections": []
    }
]