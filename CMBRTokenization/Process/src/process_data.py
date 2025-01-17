import numpy as np
from PIL import Image, ImageFilter
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import words
from collections import Counter
import logging
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download required NLTK resources
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

def load_and_process_image(image_path):
    logging.info(f"Loading image from {image_path}")
    img = Image.open(image_path)

    # Apply a smoothing filter to reduce noise
    img = img.filter(ImageFilter.SMOOTH)
    logging.info("Applied smoothing filter to the image")

    # Convert to grayscale
    img_array = np.array(img.convert('L'))
    logging.info("Image loaded and converted to grayscale")

    # Apply thresholding to reduce the number of unique values
    img_array = np.digitize(img_array, bins=np.linspace(0, 255, num=16))  # 16 levels of quantization
    logging.info("Applied thresholding to reduce duplication")

    # Normalize the grayscale values to the range 0-1
    normalized_data = (img_array - img_array.min()) / (img_array.max() - img_array.min())
    logging.info("Grayscale values normalized")

    return normalized_data

def get_word_frequencies():
    logging.info("Loading and tokenizing word list")
    word_list = words.words()
    tokens = word_tokenize(' '.join(word_list))
    
    word_frequencies = Counter(tokens)
    logging.info(f"Word frequencies calculated for {len(word_frequencies)} words")

    return word_frequencies, word_list

def create_frequency_adjusted_bins(word_frequencies, word_list):
    logging.info("Creating frequency-adjusted bins for tokenization")
    total_occurrences = sum(word_frequencies.values())
    new_thresholds = {}
    cumulative = 0

    for word, count in word_frequencies.most_common():
        cumulative += count
        new_thresholds[word] = cumulative / total_occurrences

    threshold_values = list(new_thresholds.values())
    tokens = list(new_thresholds.keys())

    logging.info(f"Frequency-adjusted bins created with {len(threshold_values)} thresholds")

    return threshold_values, tokens

def pre_process_tokens(tokens):
    logging.info("Pre-processing tokens to remove duplication")
    processed_tokens = []
    previous_token = None
    
    for token in tokens:
        if token != previous_token:
            processed_tokens.append(token)
        previous_token = token
    
    logging.info(f"Pre-processed tokens, reduced from {len(tokens)} to {len(processed_tokens)}")
    return processed_tokens

def should_start_new_sentence(previous_token, current_token, sentence):
    if previous_token == '.' or len(sentence) >= random.randint(5, 12):
        logging.info(f"Starting new sentence due to token '{current_token}'")
        return True
    if len(sentence) > 10 and current_token in ['and', 'but', 'or']:
        logging.info(f"Starting new sentence due to conjunction '{current_token}'")
        return True
    return False

def update_tokenized_output(tokenized_output, sentence, mask):
    flattened_tokens = sentence.split()
    count = np.sum(mask)
    
    if count > 0:
        segment_length = max(1, count // len(flattened_tokens))
        start_idx = 0
        for idx, token in enumerate(flattened_tokens):
            end_idx = start_idx + segment_length
            if idx == len(flattened_tokens) - 1:  # Make sure to cover all remaining indices
                end_idx = count
            tokenized_output[mask][start_idx:end_idx] = token
            start_idx = end_idx
            logging.debug(f"Token '{token}' assigned to indices {start_idx} to {end_idx}")

def frequency_adjusted_tokenizer(data, thresholds, tokens, max_repeats=4):
    logging.info("Starting tokenization with frequency-adjusted bins")
    tokenized_output = np.zeros(data.shape, dtype='<U10')
    previous_token = None
    repeat_count = 0
    sentence = []

    for i, threshold in enumerate(thresholds):
        mask = np.zeros_like(data, dtype=bool)
        if i == 0:
            mask = data <= threshold
        else:
            mask = (data > thresholds[i-1]) & (data <= threshold)
        
        current_token = tokens[i]

        if previous_token and should_start_new_sentence(previous_token, current_token, sentence):
            sentence_str = ' '.join(sentence) + '.'
            logging.info(f"Flushing sentence: '{sentence_str}'")
            update_tokenized_output(tokenized_output, sentence_str, mask)
            sentence = []

        if current_token == previous_token:
            repeat_count += 1
        else:
            repeat_count = 0

        if repeat_count < max_repeats:
            sentence.append(current_token)
            previous_token = current_token

        logging.debug(f"Token '{current_token}' assigned to {np.sum(mask)} data points")

    # Final sentence flush
    if sentence:
        sentence_str = ' '.join(sentence) + '.'
        logging.info(f"Flushing final sentence: '{sentence_str}'")
        update_tokenized_output(tokenized_output, sentence_str, mask)

    logging.info("Tokenization complete")

    return tokenized_output

def map_and_tag_text(tokenized_data, output_path):
    logging.info("Starting part-of-speech tagging")
    flattened_tokens = tokenized_data.flatten()
    tagged_tokens = pos_tag(flattened_tokens)

    logging.info(f"Saving tagged text to {output_path}")
    with open(output_path, 'w') as f:
        for token, tag in tagged_tokens:
            f.write(f'{token} ')  # Exclude the POS tags from the output
    
    logging.info("Part-of-speech tagging and saving complete")
    
    return tagged_tokens

if __name__ == '__main__':
    input_image_path = 'data/input_image.jpg'
    output_tagged_path = 'data/output_tags.txt'

    logging.info("Script started")

    # Process the image
    normalized_data = load_and_process_image(input_image_path)

    # Get word frequencies and word list
    word_frequencies, word_list = get_word_frequencies()

    # Create frequency-adjusted bins
    threshold_values, tokens = create_frequency_adjusted_bins(word_frequencies, word_list)

    # Tokenize the data using the frequency-adjusted bins, reducing repetition before tokenization
    tokenized_data = frequency_adjusted_tokenizer(normalized_data, threshold_values, tokens)

    # Map and tag the text
    map_and_tag_text(tokenized_data, output_tagged_path)

    logging.info("Script finished")
