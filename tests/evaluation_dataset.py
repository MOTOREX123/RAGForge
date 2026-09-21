# EVALUATION_DATASET = [
#     {
#         "question": "What is overfitting in machine learning?",
#         "expected_sources": [
#             "Introduction to Machine Learning with Python.pdf"
#         ],
#         "expected_pages": [42],
#     },
#     {
#         "question": "What is a convolutional neural network?",
#         "expected_sources": [
#             "DeepLearning.pdf"
#         ],
#         "expected_pages": [34, 95, 124],
#     },
#     {
#         "question": "What is underfitting in machine learning?",
#         "expected_sources": [
#             "Introduction to Machine Learning with Python.pdf"
#         ],
#         "expected_pages": [42, 62],
#     },
#     {
#     "question": "What is a random forest?",
#     "expected_sources": [
#         "Introduction to Machine Learning with Python.pdf"
#     ],
#     "expected_pages": [98, 99, 101],
#     },
#     {
#         "question": "What is a convolutional layer?",
#         "expected_sources": [
#             "DeepLearning.pdf"
#         ],
#         "expected_pages": [95, 114, 124],
#     },
# ]
from pathlib import Path

content = """
RAGForge retrieval evaluation dataset.

Balanced benchmark:
- 7 questions: AI & ML DIGITAL NOTES.pdf
- 7 questions: DeepLearning.pdf
- 7 questions: Introduction to Machine Learning with Python.pdf
- 7 questions: IntroductiontoAgenticAI.pdf

Expected pages are grounded in the page metadata stored in vectorstore/chunks.json.
For broad concepts, multiple relevant pages are included.
"""

evaluation_dataset = [
    # ============================================================
    # AI & ML DIGITAL NOTES.pdf — 7 questions
    # ============================================================

    {
        "question": "What is an agent in artificial intelligence?",
        "expected_sources": [
            "AI & ML DIGITAL NOTES.pdf"
        ],
        "expected_pages": [10, 11],
    },
    {
        "question": "What makes an AI agent rational?",
        "expected_sources": [
            "AI & ML DIGITAL NOTES.pdf"
        ],
        "expected_pages": [12, 13],
    },
    {
        "question": "What does PEAS stand for in an agent's task environment?",
        "expected_sources": [
            "AI & ML DIGITAL NOTES.pdf"
        ],
        "expected_pages": [13],
    },
    {
        "question": "How does breadth-first search explore a search tree?",
        "expected_sources": [
            "AI & ML DIGITAL NOTES.pdf"
        ],
        "expected_pages": [25, 26, 28],
    },
    {
        "question": "What is depth-first search and what is one of its limitations?",
        "expected_sources": [
            "AI & ML DIGITAL NOTES.pdf"
        ],
        "expected_pages": [29, 32],
    },
    {
        "question": "What is the hill-climbing algorithm?",
        "expected_sources": [
            "AI & ML DIGITAL NOTES.pdf"
        ],
        "expected_pages": [35, 36],
    },
    {
        "question": "How does simulated annealing improve on hill climbing?",
        "expected_sources": [
            "AI & ML DIGITAL NOTES.pdf"
        ],
        "expected_pages": [37, 38],
    },

    # ============================================================
    # DeepLearning.pdf — 7 questions
    # ============================================================

    {
        "question": "What is a convolutional neural network and what is it useful for?",
        "expected_sources": [
            "DeepLearning.pdf"
        ],
        "expected_pages": [34, 95],
    },
    {
        "question": "What type of data pattern is a recurrent neural network designed to handle?",
        "expected_sources": [
            "DeepLearning.pdf"
        ],
        "expected_pages": [34],
    },
    {
        "question": "What is the purpose of an activation function in a neural network?",
        "expected_sources": [
            "DeepLearning.pdf"
        ],
        "expected_pages": [29, 32],
    },
    {
        "question": "What is backpropagation used for in neural network training?",
        "expected_sources": [
            "DeepLearning.pdf"
        ],
        "expected_pages": [39],
    },
    {
        "question": "What is dropout as a deep learning technique?",
        "expected_sources": [
            "DeepLearning.pdf"
        ],
        "expected_pages": [62, 63, 64],
    },
    {
        "question": "What types of layers can be used when building neural networks with Keras?",
        "expected_sources": [
            "DeepLearning.pdf"
        ],
        "expected_pages": [80],
    },
    {
        "question": "What are some applications of deep learning?",
        "expected_sources": [
            "DeepLearning.pdf"
        ],
        "expected_pages": [59, 60, 67, 68],
    },

    # ============================================================
    # Introduction to Machine Learning with Python.pdf — 7
    # ============================================================

    {
        "question": "What is overfitting in machine learning?",
        "expected_sources": [
            "Introduction to Machine Learning with Python.pdf"
        ],
        "expected_pages": [42],
    },
    {
        "question": "What is underfitting in machine learning?",
        "expected_sources": [
            "Introduction to Machine Learning with Python.pdf"
        ],
        "expected_pages": [42, 62],
    },
    {
        "question": "How is a random forest constructed?",
        "expected_sources": [
            "Introduction to Machine Learning with Python.pdf"
        ],
        "expected_pages": [98, 99],
    },
    {
        "question": "What are linear models used for in machine learning?",
        "expected_sources": [
            "Introduction to Machine Learning with Python.pdf"
        ],
        "expected_pages": [59, 60, 61],
    },
    {
        "question": "What is logistic regression?",
        "expected_sources": [
            "Introduction to Machine Learning with Python.pdf"
        ],
        "expected_pages": [70, 71, 75, 77, 78],
    },
    {
        "question": "What is the basic idea behind Naive Bayes classifiers?",
        "expected_sources": [
            "Introduction to Machine Learning with Python.pdf"
        ],
        "expected_pages": [82, 83, 84],
    },
    {
        "question": "What is cross-validation used for when evaluating machine learning models?",
        "expected_sources": [
            "Introduction to Machine Learning with Python.pdf"
        ],
        "expected_pages": [266, 267, 268, 269],
    },

    # ============================================================
    # IntroductiontoAgenticAI.pdf — 7 questions
    # ============================================================

    {
        "question": "What is Agentic AI?",
        "expected_sources": [
            "IntroductiontoAgenticAI.pdf"
        ],
        "expected_pages": [1, 2],
    },
    {
        "question": "What does autonomy mean in Agentic AI?",
        "expected_sources": [
            "IntroductiontoAgenticAI.pdf"
        ],
        "expected_pages": [2],
    },
    {
        "question": "How does goal-orientation work in Agentic AI?",
        "expected_sources": [
            "IntroductiontoAgenticAI.pdf"
        ],
        "expected_pages": [3],
    },
    {
        "question": "What is the OODA loop described in Agentic AI?",
        "expected_sources": [
            "IntroductiontoAgenticAI.pdf"
        ],
        "expected_pages": [3],
    },
    {
        "question": "What are the main architectural components of Agentic AI?",
        "expected_sources": [
            "IntroductiontoAgenticAI.pdf"
        ],
        "expected_pages": [4, 5],
    },
    {
        "question": "How do memory, planning, execution, and tool integration work together in an Agentic AI architecture?",
        "expected_sources": [
            "IntroductiontoAgenticAI.pdf"
        ],
        "expected_pages": [4, 5],
    },
    {
        "question": "What are the Tool-Using Agent, Multi-Agent Collaboration, and Reflection design patterns?",
        "expected_sources": [
            "IntroductiontoAgenticAI.pdf"
        ],
        "expected_pages": [6, 7],
    },
]

