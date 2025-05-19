import requests
import re
import string
from collections import Counter
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt


def download_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(rf"[{string.punctuation}”“’‘\"]", " ", text)  # розширене очищення
    words = text.split()
    stopwords = {"i", "“", "”", "’", "‘", "''", "--"}  # базові стоп-слова
    words = [word for word in words if word not in stopwords and word.isalpha()]
    return words



def map_function(chunk):
    return Counter(chunk)


def reduce_counters(counters):
    total = Counter()
    for counter in counters:
        total.update(counter)
    return total


def parallel_word_count(words, num_workers=None):
    if num_workers is None:
        num_workers = cpu_count()

    chunk_size = len(words) // num_workers
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

    with Pool(processes=num_workers) as pool:
        mapped = pool.map(map_function, chunks)
        reduced = reduce_counters(mapped)

    return reduced


def visualize_top_words(word_freq, top_n=10):
    most_common = word_freq.most_common(top_n)
    words, freqs = zip(*most_common)

    plt.figure(figsize=(10, 6))
    plt.barh(words[::-1], freqs[::-1], color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  
    print("Завантаження тексту...")
    text = download_text(url)
    words = clean_and_tokenize(text)

    print("Підрахунок частоти слів паралельно...")
    word_freq = parallel_word_count(words)

    print("Візуалізація...")
    visualize_top_words(word_freq, top_n=10)
