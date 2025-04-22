import pandas as pd
import re
import string
from nltk.corpus import stopwords

# Download necessary NLTK resources (run this once)
import nltk
try:
    stopwords.words('italian')
except LookupError:
    nltk.download('stopwords')

def clean_italian_description(text):
    """
    Cleans a single Italian description string by removing noise, handling contractions,
    punctuation, and Italian stopwords.

    Args:
        text (str): The input Italian description string.

    Returns:
        str: The cleaned Italian description string.
    """
    if isinstance(text, float):  # Handle potential NaN values
        text = str(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove parentheses and their content
    text = re.sub(r'\([^)]*\)', '', text)
    
    # Handle missing spaces around apostrophes and contractions
    text = re.sub(r"(\b[dl]')([a-z])", r"\1 \2", text)  # Add space after "d'" or "l'"
    
    # Handle missing spaces between words caused by punctuation removal
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between lowercase and uppercase letters
    
    # Replace abbreviations and common issues dynamically
    text = re.sub(r'\bges\b', 'gesu', text)  # Replace "ges" with "gesu"
    
    # Replace punctuation with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('italian'))
    text_tokens = text.split()
    filtered_tokens = [word for word in text_tokens if word not in stop_words]
    
    # Join tokens back into a single string
    cleaned_text = " ".join(filtered_tokens).strip()
    
    return cleaned_text

def load_and_clean_italian_descriptions_from_csv(file_paths):
    """
    Loads Italian text data from multiple CSV files, performs cleaning on the 'titolo' and
    'descrizione' columns, and saves the DataFrame with cleaned columns replacing the originals.

    Args:
        file_paths (list of str): A list containing the paths to the CSV files.
    """
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            # Print the first 5 rows of the DataFrame
            print(f"\nFirst 5 rows of the DataFrame from {file_path}:")
            print(df.head())

            # Ensure the required columns exist
            if 'titolo' not in df.columns or 'descrizione' not in df.columns:
                print(f"Warning: 'titolo' or 'descrizione' column not found in {file_path}. Skipping this file.")
                continue

            # Clean the 'titolo' and 'descrizione' columns
            df['titolo'] = df['titolo'].apply(clean_italian_description)
            df['descrizione'] = df['descrizione'].apply(clean_italian_description)

            # Save the DataFrame with cleaned columns replacing the originals
            output_file = file_path.replace('.csv', '_cleaned.csv')
            df.to_csv(output_file, index=False)
            print(f"Cleaned data saved to: {output_file}")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

if __name__ == "__main__":
    # Updated file paths
    file_paths = [
        '../../CH_IT/CSV/A/architettura.csv',
        '../../CH_IT/CSV/Ar/archeologia.csv',
        '../../CH_IT/CSV/dea/demoetnoantropologici.csv',
        '../../CH_IT/CSV/vaw/opere_arte_visiva.csv'
    ]
    load_and_clean_italian_descriptions_from_csv(file_paths)