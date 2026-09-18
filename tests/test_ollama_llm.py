from utils.ollama_llm import generate_ollama_answer


context = """
Supervised learning is a type of machine learning where a model
learns from labeled training data. Each training example contains
input features and a known target label. The model learns the
relationship between the inputs and outputs and uses it to make
predictions on new data.
"""


question = "What is supervised learning?"


answer = generate_ollama_answer(
    question,
    context
)


print("\nQUESTION")
print("=" * 60)
print(question)

print("\nANSWER")
print("=" * 60)
print(answer)
