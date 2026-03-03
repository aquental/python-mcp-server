import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer

def get_sentences_and_categories():
    """Return the sentences and their corresponding categories."""
    sentences = [
        # Topic: NLP
        "RAG stands for Retrieval-Augmented Generation.",
        "Retrieval is a crucial aspect of modern NLP systems.",
        "Generating text with correct facts is challenging.",
        "Large language models can generate coherent text.",
        "GPT models have billions of parameters.",
        "Natural Language Processing enables computers to understand human language.",
        "Word embeddings capture semantic relationships between words.",
        "Transformer architectures revolutionized NLP research.",
        
        # Topic: Machine Learning
        "Machine learning benefits from large datasets.",
        "Supervised learning requires labeled data.",
        "Reinforcement learning is inspired by behavioral psychology.",
        "Neural networks can learn complex functions.",
        "Overfitting is a common problem in ML.",
        "Unsupervised learning uncovers hidden patterns in data.",
        "Feature engineering is critical for model performance.",
        "Cross-validation helps in assessing model generalization.",
        
        # Topic: Food
        "Bananas are commonly used in smoothies.",
        "Oranges are rich in vitamin C.",
        "Pizza is a popular Italian dish.",
        "Cooking pasta requires boiling water.",
        "Chocolate can be sweet or bitter.",
        "Fresh salads are a healthy and refreshing meal.",
        "Sushi combines rice, fish, and seaweed in a delicate balance.",
        "Spices can transform simple ingredients into gourmet dishes.",
        
        # Topic: Weather
        "It often rains in the Amazon rainforest.",
        "Summers can be very hot in the desert.",
        "Hurricanes form over warm ocean waters.",
        "Snowstorms can disrupt transportation.",
        "A sunny day can lift people's mood.",
        "Foggy mornings are common in coastal regions.",
        "Winter brings frosty nights and chilly winds.",
        "Thunderstorms can produce lightning and heavy rain."
        
        # new category (prompt evaluation):
        "Prompt evaluation measures how well instructions guide LLM outputs.",
        "Clear and specific prompts improve evaluation scores significantly.",
        "Chain-of-thought prompting enhances reasoning during evaluation.",
        "Relevance and factual accuracy are core metrics in prompt evaluation.",
        "Few-shot examples boost performance in prompt evaluation tests.",
        "Automated evaluators use BLEU and ROUGE for objective scoring.",
        "Iterative refinement is essential for strong prompt evaluation.",
        "Bias detection is a critical step in modern prompt evaluation."
    ]
    
    categories = (["NLP"] * 8 + ["ML"] * 8 + ["Food"] * 8 + ["Weather"] * 8 + ["Prompt"] * 8)
    # TODO: Update categories list with your new category
    return sentences, categories

def get_color_and_shape_maps():
    """Return color and marker maps for each category."""
    color_map = {
        "NLP": "red",
        "ML": "blue",
        "Food": "green",
        "Weather": "purple",
        #new category color here
        "Prompt": "gray"
    }
    shape_map = {
        "NLP": "o",
        "ML": "s",
        "Food": "^",
        "Weather": "X",
        #new category shape here
        "Prompt": "."
    }
    return color_map, shape_map

def compute_tsne_embeddings(sentences, model_name="sentence-transformers/all-MiniLM-L6-v2",
                              perplexity=10, max_iter=3000, random_state=42):
    """Compute and return t-SNE reduced embeddings for the given sentences."""
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences)
    tsne = TSNE(n_components=2, random_state=random_state,
                perplexity=perplexity, max_iter=max_iter)
    return tsne.fit_transform(embeddings)

def plot_embeddings(reduced_embeddings, sentences, categories, color_map, shape_map):
    """Plot the 2D embeddings with labels and a legend."""
    plt.figure(figsize=(10, 8))
    for i, (sentence, category) in enumerate(zip(sentences, categories)):
        x, y = reduced_embeddings[i]
        plt.scatter(x, y, color=color_map[category], marker=shape_map[category])
        plt.text(x - 2.5, y - 1.0, sentence[:20] + "...", fontsize=9)
    
    for cat, color in color_map.items():
        plt.scatter([], [], color=color, label=cat, marker=shape_map[cat])
    plt.legend(loc="best")

    plt.title("t-SNE Visualization of Sentence Embeddings", fontsize=14)
    plt.xlabel("t-SNE Dimension 1", fontsize=12)
    plt.ylabel("t-SNE Dimension 2", fontsize=12)
    plt.tight_layout()
    plt.savefig('static/images/plot.png')

if __name__ == "__main__":
    sentences, categories = get_sentences_and_categories()
    color_map, shape_map = get_color_and_shape_maps()
    reduced_embeddings = compute_tsne_embeddings(sentences)
    plot_embeddings(reduced_embeddings, sentences, categories, color_map, shape_map)
e3
