import re
import umap
import numpy as np
import hdbscan
import pandas as pd
import os
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector
from spacymoji import Emoji
from langchain.embeddings import HuggingFaceEmbeddings
from sklearn.feature_selection import chi2
from urlextract import URLExtract
import ast
import emoji
import requests
import json
from opsci_toolbox.helpers.common import write_json, write_pickle, load_pickle, create_dir, copy_file, write_jsonl
from textacy.preprocessing.replace import urls
from eldar import Query
import torch
from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer


####################################################################
# CLEANING
####################################################################

def filter_by_query(df, col_text, query, ignore_case=True, ignore_accent=True, match_word=False):
    eldar_query=Query(query, ignore_case = ignore_case, ignore_accent=ignore_accent, match_word=match_word)
    df[col_text] = df[df[col_text].apply(eldar_query)]
    df=df.reset_index(drop=True)
    return df

def TM_clean_text(df, col, col_clean):
    """
    Generic cleaning process for topic modeling
    """
    df[col_clean] = df[col].apply(lambda x : urls(x, repl= ''))
    df[col_clean] = df.apply(lambda row: " ".join(filter(lambda x: x[0] != "@", row[col_clean].split())), 1)
    df[col_clean] = df[col_clean].apply(remove_extra_spaces)
    # df = df.loc[(df[col_clean] != ""), :]
    return df

def extract_insta_shortcode(url):
    pattern =r'(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|tv|stories)\/([a-zA-Z0-9_-]+)\/?'

    shortcode = re.findall(pattern, url)
    return shortcode[0]

def remove_emojis(text):
    # Convert emojis to their textual representations
    text_no_emojis = emoji.demojize(text)
    
    # Remove emojis and their textual representations
    text_no_emojis = re.sub(r':[a-zA-Z_]+:', '', text_no_emojis)
    
    return text_no_emojis

def extract_urls_from_text(text):
    """Returns a list of URLs contained in text"""
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    return urls

def extract_hashtags(text, lower=True):
    ''' 
    Using a regular expression to find hashtags in the text
    '''
    hashtags = re.findall(r'\B#\w+', text)
    if lower : 
        hashtags= [h.lower() for h in hashtags]
    return hashtags

def extract_mentions(text, mention_char='@', lower=False):
    ''' 
    Using a regular expression to find mentions in the text
    '''
    pattern = r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))" + re.escape(mention_char) + r"([A-Za-z0-9_]{4,15})"

    mentions = re.findall(pattern, text)
    if lower: 
        mentions = [mention.lower() for mention in mentions]
    return mentions

def remove_extra_spaces(text):
    """
    Remove extra spaces
    """
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()

def remove_characters(text: str, start_indices: list, end_indices: list):
    """
    Remove words from a text using list of indices
    """
    if start_indices is None or len(start_indices) <1:
        return text
    if len(start_indices) != len(end_indices):
        print("ERROR - The number of start indices must be equal to the number of end indices.")
        return text

    result = ""
    current_start = 0

    for start, end in zip(start_indices, end_indices):
        if start < 0 or end > len(text) or start > end:
            print("ERROR - Invalid start or end indices")
            return text

        result += text[current_start:start]
        current_start = end + 1

    result += text[current_start:]

    return result


def load_stopwords_df(lang):
    """
    Load a CSV file without header containing stopwords. If the file doesn't exist, it creates an empty file.
    """
    lexicon_dir = os.path.join(os.getcwd(), "lexicons")
    file_path = os.path.join(lexicon_dir, f"stop_words_{lang.lower()}.csv")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        current_file_path = os.path.abspath(__file__)
        data_path = os.path.abspath(os.path.join(current_file_path, '..', '..', 'lexicons', f"stop_words_{lang.lower()}.csv"))
        if os.path.exists(data_path):
            create_dir(lexicon_dir)
            copy_file(data_path, lexicon_dir, f"stop_words_{lang.lower()}.csv")
            df = pd.read_csv(file_path)
        else:
            create_dir(lexicon_dir)
            df = pd.DataFrame(columns=['word'])
            df.to_csv(file_path, index=False)
            print("No stopwords list for this lang. New file created, use add_stopwords() to append words.")

    # df.rename(columns={0: 'word'}, inplace=True)
    df.sort_values(by="word", inplace=True)
    
    return df
    


def add_stopwords(lang:str, new_stopwords:list, lower:bool = True):
    """
    Add a list of stopwords to an existing file. It removes duplicates.
    """
    df = load_stopwords_df(lang)
    init_size = len(df.iloc[:, 0].unique())  # Selecting the first column

    if lower:
        new_stopwords_lowered = [x.lower() for x in new_stopwords]
        new_kw_list = list(set(list(df.iloc[:, 0].str.lower().unique()) + new_stopwords_lowered))  # Selecting the first column
    else:
        new_kw_list = list(set(list(df.iloc[:, 0].unique()) + new_stopwords))  # Selecting the first column

    new_df = pd.DataFrame({df.columns[0]: new_kw_list}).sort_values(by=df.columns[0])  # Selecting the first column

    added_kw = len(new_df.iloc[:, 0].unique()) - init_size  # Selecting the first column
    print(added_kw, "stop words added.")

    lexicon_dir = os.path.join(os.getcwd(), "lexicons")
    file_path = os.path.join(lexicon_dir, f"stop_words_{lang.lower()}.csv")
    new_df.to_csv(file_path, encoding="utf-8", index=False)


    return new_df

def remove_stopwords(lang:str, stopwords:list):
    """
    Remove stopwords from an existing file.
    """
    df = load_stopwords_df(lang)
    init_size = len(df.iloc[:, 0].unique())  # Selecting the first column
    df = df[~df.iloc[:, 0].isin(stopwords)].reset_index(drop=True)  # Selecting the first column
    removed_kw = init_size - len(df.iloc[:, 0].unique())  # Selecting the first column
    print(removed_kw, "stopwords removed")
    lexicon_dir = os.path.join(os.getcwd(), "lexicons")
    file_path = os.path.join(lexicon_dir, f"stop_words_{lang.lower()}.csv")
    df.to_csv(file_path,  encoding="utf-8", index=False)
    print("File saved -", file_path)
    return df
    

def keep_alphanum_char(text:str, replace:str = ''):
    """
    Replace all non-alphanumeric characters
    """
    return re.sub("[^a-zA-Z0-9]", replace, text)


def substitute_punctuations_with_white_space(text):
    """
    Substitute punctuations with white spaces in the input string.

    Parameters:
        text (str): The input string.

    Returns:
        str: The modified string with punctuations replaced by white spaces.
    """
    text = re.sub(r"[%s]" % re.escape('!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~“…”’'), " ", text)
    return text

def translate_wt_libre(text, source, target, filename, dir_json, url = "http://127.0.0.1:5000/translate"):
    headers = {"Content-Type": "application/json"}
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text",
        "api_key": ""
    }

    file_path = os.path.join(dir_json , str(filename)+'.json')
    if not os.path.exists(file_path):
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        json_data = response.json()
        json_data['clean_text']=text
        write_json(json_data, dir_json , str(filename))
        return json_data
    
def translate_batch(batch_text, source, target, filename, dir_json, url = "http://127.0.0.1:5000/translate"):
    headers = {"Content-Type": "application/json"}
    payload = {
        "q": batch_text,
        "source": source,
        "target": target,
        "format": "text",
        "api_key": ""
    }

    file_path = os.path.join(dir_json , str(filename)+'.json')
    if not os.path.exists(file_path):
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        json_data = response.json()
        json_results=[]
        for i, value in enumerate(json_data.get("translatedText", [])):
            v = {"translated_text" : value, "clean_text" : batch_text[i]}
            json_results.append(v)
       
        write_jsonl(json_results, dir_json , str(filename))
        return json_results

def translate(text, source, target,  url = "http://127.0.0.1:5000/translate"):
    headers = {"Content-Type": "application/json"}
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text",
        "api_key": ""
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    json_data = response.json()
    translatedText = json_data.get("translatedText", "")
    return translatedText
    
def translate_row(df, col, source="auto", target = "en"):
    translations =[]
    for i, row in df.iterrows():
        txt_to_translate = row[col].replace(' | ', ', ')
        txt_translated = translate(txt_to_translate, source="auto", target = "en")
        translations.append(txt_translated)
    df["translation_"+col]=translations
    return df

###################################################################
# METRICS
###################################################################

def cosine_similarity(a, b):
    """
    calculate cosine similarity between two vectors
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
                           
def approximate_tokens(text):
    """
    Approximate the number of tokens
    """
    return len(text.split(' '))

def approximate_unique_tokens(text):
    """
    Approximate the number of distinct tokens
    """
    return len(list(set(text.split(' '))))

def count_word_occurrences(text, word):
    """
    Count word occurences
    """
    # Convert both text and word to lowercase for case-insensitive matching    
    word_lower = word.lower()

    # Use count() to find the number of occurrences
    occurrences = text.count(word_lower)
    
    return occurrences


def chi2_per_category(lst_text, lst_categorie, col_cat, n_words = 10, p_value_limit=0.95, min_freq=3):
    """
    Parameters:
        lst_text : list
            List of texts for which Chi2 will be calculated.
        lst_categorie : list
            List of categories corresponding to each text.
        col_cat : str
            Name of the column for categories in the resulting DataFrame.
        n_words : int, optional
            Number of top words to display per category. Default is 10.
        p_value_limit : float, optional
            Threshold for p-values to filter significant words. Default is 0.95.
        min_freq : int, optional
            Minimum frequency threshold for word occurrences per class. Default is 3.

    Returns:
        DataFrame
            DataFrame containing the top words with their corresponding Chi2 scores, p-values, and word counts per class.

    Description:
        This function calculates Chi-squared (Chi2) statistics per category based on the provided texts and corresponding categories. 
        It identifies significant words that are most associated with each category, filtering out those with p-values greater than 
        the specified limit and those with word counts below the minimum frequency threshold.
    """
    count_vectorizer = CountVectorizer(token_pattern=r'[^\s]+')
    X_train_count = count_vectorizer.fit_transform(lst_text)
    X_names_count = count_vectorizer.get_feature_names_out()

    df_chi=pd.DataFrame()
    for cat in np.unique(lst_categorie):
        chi2_scores, p_values = chi2(X_train_count, lst_categorie == str(cat))
        word_count = X_train_count[lst_categorie == str(cat)].sum(axis=0) 
        df_chi_tmp = pd.DataFrame({col_cat: cat, "relevant_words_chi2": X_names_count, "chi2":chi2_scores, "p_values": 1 - p_values, "word_count_per_class":word_count.tolist()[0]}).sort_values(by="chi2", ascending=False).head(n_words)
        df_chi_tmp = df_chi_tmp[df_chi_tmp["p_values"]>p_value_limit]
        df_chi_tmp = df_chi_tmp[df_chi_tmp["word_count_per_class"]>min_freq]
        df_chi=pd.concat([df_chi, df_chi_tmp])

    df_chi.reset_index(drop=True)
    return df_chi

def word_frequency_per_categorie(df, col_text, col_cat, ngram_range=(1, 1), stop_words=[], n_words = 20, min_freq=3):
    count_vectorizer = CountVectorizer(token_pattern=r'[^\s]+', ngram_range=ngram_range, stop_words=stop_words)
    X_train_count = count_vectorizer.fit_transform(df[col_text].to_list())
    X_names_count = count_vectorizer.get_feature_names_out()

    df_count = pd.DataFrame()
    for cat in np.unique(df[col_cat].tolist()):
        word_count = X_train_count[df[col_cat] == str(cat)].sum(axis=0)
        df_count_tmp = pd.DataFrame({col_cat: [cat]*len(X_names_count), "word": X_names_count, "freq": word_count.tolist()[0]}).sort_values(by="freq", ascending=False)
        if n_words:
            df_count_tmp=df_count_tmp.head(n_words)
        if min_freq:
            df_count_tmp=df_count_tmp[df_count_tmp["freq"]>min_freq]
        df_count = pd.concat([df_count, df_count_tmp])
    return df_count


def top_items_per_category(df, col_lst ="hashtags", col_cat = "soft_topic", col_id = "tweet_id", n_items= 10):
    """
    Take a dataframe with a column containing lists of tokens (ex hashtags) and count their occurences grouped by a category.
    For instance : count the most used hashtags per topic, metric will be a volume of tweets
    """
    df_count = (df[[col_cat, col_id, col_lst]].explode(col_lst)
            .groupby([col_cat, col_lst], group_keys=False)
            .agg({col_id:'nunique'})
            .reset_index()
            .groupby(col_cat, group_keys=False)
            .apply(lambda x: x.nlargest(n_items, col_id))
            .reset_index(drop=True)
            .groupby(col_cat, group_keys=False)
            .apply(lambda x: list(zip(x[col_lst], x[col_id])))
            .reset_index(name="top_"+col_lst)
            )
    return df_count

def topic_representation(df_processed_data, col_topic, col_id, col_engagement, col_user_id, metrics):

    #on s'assure que les colonnes de métriques soient bien complètes et en float
    # df_processed_data[metrics]=df_processed_data[metrics].fillna(0).astype(float) 

    #on crée un dictionnaire contenant les agrégations
    metrics_dict = dict()
    metrics_dict['verbatims']=(col_id,'nunique')
    metrics_dict['engagements']=(col_engagement,'sum')
    if col_user_id:
        metrics_dict["users"]=(col_user_id,"nunique")

    metrics_dict.update(metrics)

    print(metrics_dict)

    metrics_dict['avg_word_count']=("tokens_count", lambda x: round(x.mean(),2))
    metrics_dict['verbatims_with_emoji']=("emojis_count", lambda x: (x > 0).sum() )
    metrics_dict['emojis_occurences']=("emojis_count", "sum")
    metrics_dict['unique_emojis']=("unique_emojis", lambda x: len(set(emoji for sublist in x for emoji in sublist)))
    metrics_dict['unique_hashtags']=("hashtags", lambda x: len(set(hashtag for sublist in x for hashtag in sublist)))
    metrics_dict['verbatims_with_hashtags']=("hashtags_count", lambda x: (x > 0).sum() )
    metrics_dict['hashtags_occurences']=("hashtags_count", "sum")
    metrics_dict['unique_mentions']=("mentions", lambda x: len(set(mention for sublist in x for mention in sublist)))
    metrics_dict['verbatims_with_mentions']=("mentions_count", lambda x: (x > 0).sum() )
    metrics_dict['mentions_occurences']=("mentions_count", "sum")
    metrics_dict['topic_x']=("x", "mean")
    metrics_dict['topic_y']=("y", "mean")


    # on produit la représentation des topics finale
    df_distrib_all = (df_processed_data.groupby(col_topic)
                      .agg(**metrics_dict)
                      .sort_values(by="verbatims", ascending=False)
                      .assign(engagement_per_verbatims = lambda x : x["engagements"] / x["verbatims"])
                      .assign(verbatims_per_user = lambda x : x["verbatims"] / x["users"] if col_user_id else 0)
                      .assign(engagement_per_user = lambda x : x["engagements"] / x["users"] if col_user_id else 0)
                      .assign(percentage_verbatims = lambda x : x["verbatims"] / x["verbatims"].sum())
                      .assign(percentage_engagement = lambda x : x["engagements"] / x["engagements"].sum())
                      .assign(percentage_users = lambda x : x["users"] / x["users"].sum() if col_user_id else 0)
                      .assign(percentage_verbatims_with_emoji = lambda x : x["verbatims_with_emoji"] / x["verbatims"])
                      .assign(percentage_verbatims_with_hashtags = lambda x : x["verbatims_with_hashtags"] / x["verbatims"])  
                      .assign(percentage_verbatims_with_mentions = lambda x : x["verbatims_with_mentions"] / x["verbatims"])
                      .reset_index())

    df_distrib_all[col_topic]=df_distrib_all[col_topic].astype(str)
    return df_distrib_all

def generic_representation(df_processed_data, col_gb, col_id, col_engagement, col_user_id = None, metrics={}):
    #on crée un dictionnaire contenant les agrégations
    metrics_dict = dict()
    metrics_dict['verbatims']=(col_id,'nunique')
    metrics_dict['engagements']=(col_engagement,'sum')
    if col_user_id:
        metrics_dict["users"]=(col_user_id,"nunique")
        
    metrics_dict.update(metrics)

    # on produit la représentation 
    df_distrib_all = (df_processed_data.groupby(col_gb)
                      .agg(**metrics_dict)
                      .sort_values(by="verbatims", ascending=False)
                      .assign(verbatims_per_user = lambda x : x["verbatims"] / x["users"] if col_user_id else 0)
                      .assign(engagement_per_verbatims = lambda x : x["engagements"] / x["verbatims"])
                      .assign(engagement_per_user = lambda x : x["engagements"] / x["users"] if col_user_id else 0)
                      .assign(percentage_verbatims = lambda x : x["verbatims"] / x["verbatims"].sum())
                      .assign(percentage_engagement = lambda x : x["engagements"] / x["engagements"].sum())
                      .assign(percentage_users = lambda x : x["users"] / x["users"].sum() if col_user_id else 0)
                      .reset_index())

    return df_distrib_all

def create_frequency_table(df, col):
    df_frequency=(df.sort_values(col, ascending=False)
                  .reset_index(drop=True)
                  .reset_index()
                  .assign(rank=lambda x: x['index'] + 1)
                  .drop(columns=['index'])
                  .assign(rank_dense=lambda x: x[col].rank(method='dense', ascending=False).astype(int))
                  .assign(rank_dense_asc=lambda x: x[col].rank(method='dense', ascending=True).astype(int))
                 )
    return df_frequency

###################################################################
# SAMPLING
###################################################################

def calculate_sample(len_df, n_rows):
    """
    Percentage conversion to number of rows
    """
    if 0 < n_rows <= 1 :
        top_rows = int(n_rows * len_df)
        return top_rows
    elif n_rows > 1 or n_rows == 0:
        top_rows = n_rows
        return top_rows
    else :
        print("ERREUR - paramètre du sampling incorrect")
    
def sampling_by_engagement(df, col_engagement, top_rows=0.3, sample_size=0.5):
    """
    Create a sample dataset by keeping a part of the top publications:
    - sample_size : final size of the sample. Ex : 1000 rows from an original dataset of 100000 rows
    - top_rows : number of "most engaging" rows to keep 
    Values could be either an integer or a float between 0 and 1 (= sample a percentage)
    """
    
    sample_rows = calculate_sample(len(df), sample_size)  
    top_rows = calculate_sample(sample_rows, top_rows)

    print(sample_rows, top_rows)
    print("TOP ROWS:", top_rows, "- SAMPLE SIZE:", sample_rows)

    if sample_rows < len(df):
        if sample_rows < top_rows:
            raise ValueError("sample_size must be higher than top_rows")    

        df = df.sort_values(by=col_engagement, ascending = False) #sort dataset by metric
        df_head = df.head(top_rows) # keep the most engaging rows
        df_tail = df[top_rows:].sample(sample_rows-top_rows, random_state = 42) #sample the tail
        df_sample = pd.concat([df_head, df_tail]).sample(frac=1, random_state=42).reset_index(drop=True) #create a new df and shuffle rows
        return df_sample
    else:
        return df
    
def sample_most_engaging_posts(df, col_topic, col_engagement, sample_size= 0.1, min_size=10):
    """
    "Stratified sample" of the most engaging content per topic. Returns a minimun number of items per group.
    """
    df = (df.groupby(col_topic, group_keys=False)
          .apply(lambda x: x.sort_values(by=col_engagement, ascending=False)
                 .head(max(min_size, int(len(x)*sample_size)))
                 )
        )
    return df

###################################################################
# SPACY
###################################################################

def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)  # We use the seed 42

def TM_nlp_process(nlp, df, col_text, col_lemma, pos_to_keep, stopwords, batch_size=100, n_process=1, stats=True, join_list = False):
    """ 
    Spacy implementation for topic modeling
    
    """
    all_lemmas=[]
    tokens_counts=[]
    tokens_kept=[]
    all_emojis=[]
    all_unique_emojis=[]
    emojis_counts=[]
    unique_emojis_count=[]

    text=list(df[col_text].astype('unicode').values)

    for doc in tqdm(nlp.pipe(text, batch_size=batch_size, n_process=n_process), total= len(text), desc = "NLP Process"):

        emojis=[str(token) for token in doc if token._.is_emoji]
        unique_emojis=list(set(emojis))
        all_emojis.append(emojis)
        all_unique_emojis.append(unique_emojis)

        if len(pos_to_keep)>0 and len(stopwords)>0:
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.text.lower() not in stopwords and tok.pos_ in pos_to_keep] 
        elif len(pos_to_keep)>0 and len(stopwords) < 1:
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.pos_ in pos_to_keep] 
        elif len(pos_to_keep) < 1 and len(stopwords) > 0:
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.text.lower() not in stopwords] 
        else :
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space)] 
            
        all_lemmas.append(lemmas_list)

        if stats:
            tokens_counts.append(len(doc))
            emojis_counts.append(len(emojis))
            unique_emojis_count.append(len(unique_emojis))
            tokens_kept.append(len(lemmas_list))
            
    if join_list:
        df[col_lemma]=[' '.join(map(str, l)) for l in all_lemmas]    
    else:
        df[col_lemma]=all_lemmas
    if stats:
        df["tokens_count"]=tokens_counts
        df["emojis_count"]=emojis_counts
        df["unique_emojis_count"]=unique_emojis_count
        df["lemmas_count"]=tokens_kept

    df["emojis"]=all_emojis
    df["unique_emojis"]=all_unique_emojis
    
    return df


def load_spacy_model(model,  disable_components=["transformer", "morphologizer", "trainable_lemmatizer", "textcat_multilabel", "textcat", "entity_ruler", "entity_linker"], lang_detect=False, emoji=False):
    """
    Parameters:
    model : str
        Name of the spaCy model to load.
    disable_components : list, optional
        List of spaCy components to disable. Default is ["transformer", "morphologizer", "trainable_lemmatizer", "textcat_multilabel", "textcat", "entity_ruler", "entity_linker"].
    lang_detect : bool, optional
        Flag indicating whether language detection should be enabled. Default is False.
    emoji : bool, optional
        Flag indicating whether to include the emoji component in the spaCy pipeline. Default is False.

    Returns:
        nlp : spacy.language.Language
            Loaded spaCy language processing pipeline.

    Description:
        This function loads a spaCy model with optional configurations such as disabling specific components, enabling emoji parsing, 
        and enabling language detection. It first loads the spaCy model specified by the 'model' parameter and then applies 
        additional configurations based on the provided flags.

        If 'disable_components' is provided, the specified spaCy components will be disabled. If 'lang_detect' is set to True, 
        language detection will be enabled using the 'get_lang_detector' function. If 'emoji' is set to True, the emoji component 
        will be included in the spaCy pipeline.

    """
    if torch.cuda.is_available():
        
        spacy.prefer_gpu()

    if len(disable_components)>0:
        nlp = spacy.load(model, disable=disable_components)
    else:
        nlp = spacy.load(model)

    if emoji:
        nlp.add_pipe("emoji", first=True)
    
    if lang_detect:
        Language.factory("language_detector", func=get_lang_detector)
        nlp.add_pipe('language_detector', last=True)

    return nlp

def get_labels(nlp, pipe_step="ner", explanations=False):
    """ Return labels associated to a pipeline step and explanations
    Available names: ['tok2vec', 'tagger', 'parser', 'senter', 'attribute_ruler', 'lemmatizer', 'ner']
     
    """
    pipe_details=nlp.get_pipe(pipe_step)
    labels=list(pipe_details.labels)
    df=pd.DataFrame({'label':labels})
    if explanations:
        descriptions=[spacy.explain(label) for label in labels]
        df['explanation']=descriptions

    return df


def spacy_langdetect(nlp, df, col_text, batch_size=100, n_process=1):
    """
    Detect language and returns a score
    """
    text=list(df[col_text].astype('unicode').values)

    languages=[]
    for doc in tqdm(nlp.pipe(text, batch_size=batch_size, n_process=n_process), total= len(text), desc = "Language detection"):
        lang=doc._.language.get("language")
        score =doc._.language.get("score")
        languages.append((lang, score))

    df[['detected_language','score']]=languages

    return df

def extract_noun_chunks(nlp, df, col_text, batch_size=100, n_process=1, stats=False):
    """
    Spacy implementation to extract noun chunks
    """
    all_chunks = []
    all_unique_chunks =[]
    chunks_count=[]
    unique_chunks_count=[]
    text=list(df[col_text].astype('unicode').values)

    for doc in tqdm(nlp.pipe(text, batch_size=batch_size, n_process=n_process), total= len(text), desc = "Noun Chunks extraction"):
        chunks=[chunk.text for chunk in doc.noun_chunks]
        unique_chunks=list(set(chunks))
        all_chunks.append(chunks)
        all_unique_chunks.append(unique_chunks)
        
        if stats:
            chunks_count.append(len(chunks))
            unique_chunks_count.append(len(unique_chunks))

    df['noun_chunks']=all_chunks
    df['unique_noun_chunks']=all_chunks
    if stats:
        df['noun_chunks_count']=chunks_count
        df['unique_noun_chunks_count']=unique_chunks_count
    return df

def extract_emojis(nlp, df, col_text, batch_size=100, n_process=1, stats=True):
    """ 
    Spacy implementation to extract emojis
    
    """
    all_emojis=[]
    all_unique_emojis=[]
    emojis_counts=[]
    unique_emojis_count=[]

    text=list(df[col_text].astype('unicode').values)

    for doc in tqdm(nlp.pipe(text, batch_size=batch_size, n_process=n_process), total= len(text), desc = "Emojis detection"):
        emojis=[str(token) for token in doc if token._.is_emoji]
        unique_emojis=list(set(emojis))
            
        all_emojis.append(emojis)
        all_unique_emojis.append(unique_emojis)

        if stats:
            emojis_counts.append(len(emojis))
            unique_emojis_count.append(len(unique_emojis))
        
    df["emojis"]=all_emojis
    df["unique_emojis"]=all_unique_emojis
    if stats:
        df["emojis_count"]=emojis_counts
        df["unique_emojis_count"]=unique_emojis_count
    
    return df

def split_n_sentences(nlp, df, col_text, n_sentences=1, batch_size=100, n_process=1, stats=False):
    """
    Split a text into chunks of n sentences
    """

    text=list(df[col_text].astype('unicode').values)
    
    count_sentences=[]
    count_batches=[]
    results=[]
    for doc in tqdm(nlp.pipe(text, batch_size=batch_size, n_process=n_process), total= len(text), desc = "Sentence splitting"):
        # Split the text into sentences
        sentences = [sent.text for sent in doc.sents]
        if stats:
            count_sentences.append(len(sentences))
        if n_sentences>1:
            # Split the sentences into batches of size n
            batches = [sentences[i:i + n_sentences] for i in range(0, len(sentences), n_sentences)]
            concatenate_batches=[" ".join(sublist) for sublist in batches]
            results.append(concatenate_batches)
            if stats:
                count_batches.append(len(concatenate_batches))
            
        else:
            results.append(sentences)

    df['sentences'] = results
    if stats:
        df['sentences_count']=count_sentences
        df['batch_sentences_count']=count_batches
    return df


def spacy_NER(nlp, df, col_text, entities_to_keep=['PERSON','ORG'], explode= True):
    """
    Spacy implementation of NER. 
    To define entities type to keep, call get_labels(nlp, pipe_step="ner", explanations=False)
    explode = False means it return 1 list of entities per document
    explode = True means it returns 1 entity per row
    """
    # Create columns to store the NER information
    df['NER_type'] = None
    df['NER_text'] = None
    df['NER_start_char'] = None
    df['NER_end_char'] = None

    # Function to process each row in the DataFrame
    def process_row(row):
        doc = nlp(row[col_text])
        entities_data = []

        if len(entities_to_keep)>0:
            for ent in doc.ents:
                if ent.label_ in entities_to_keep:
                    entities_data.append([ent.label_, ent.text, ent.start_char, ent.end_char])
        else:
            for ent in doc.ents:
                entities_data.append([ent.label_, ent.text, ent.start_char, ent.end_char])

        if entities_data:
            entity_label, entity_text, start_char, end_char = zip(*entities_data)
            row['NER_type'] = entity_label
            row['NER_text'] = entity_text
            row['NER_start_char'] = start_char
            row['NER_end_char'] = end_char

        return row

    # Apply the processing function to each row
    df = df.apply(process_row, axis=1)

    if explode:
        df= df.explode(['NER_type', 'NER_text','NER_start_char','NER_end_char'])

    return df


def tokenize(nlp, df, col_text, col_tokens, pos_to_keep, stopwords, batch_size=100, n_process=1, stats=True):
    """ 
    Spacy implementation to tokenize text
    
    """
    all_tokens=[]
    tokens_counts=[]
    tokens_kept=[]

    text=list(df[col_text].astype('unicode').values)

    for doc in tqdm(nlp.pipe(text, batch_size=batch_size, n_process=n_process), total= len(text), desc = "Tokenization"):
        if len(pos_to_keep)>0 and len(stopwords)>0:
            token_list = [str(tok.text).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.text.lower() not in stopwords and tok.pos_ in pos_to_keep] 
        elif len(pos_to_keep)>0 and len(stopwords) < 1:
            token_list = [str(tok.text).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.pos_ in pos_to_keep] 
        elif len(pos_to_keep) < 1 and len(stopwords) > 0:
            token_list = [str(tok.text).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.text.lower() not in stopwords] 
        else :
            token_list = [str(tok.text).lower() for tok in doc if not (tok.is_punct or tok.is_space)] 
            
        all_tokens.append(token_list)

        if stats:
            tokens_counts.append(len(doc))
            tokens_kept.append(len(token_list))
        
    df[col_tokens]=all_tokens
    if stats:
        df["tokens_count"]=tokens_counts
        df["kept_tokens_count"]=tokens_kept
    
    return df


def lemmatize(nlp, df, col_text, col_lemma, pos_to_keep, stopwords, batch_size=100, n_process=1, stats=True, join_list = False):
    """ 
    Spacy implementation to lemmatize text
    
    """
    all_lemmas=[]
    tokens_counts=[]
    tokens_kept=[]

    text=list(df[col_text].astype('unicode').values)

    for doc in tqdm(nlp.pipe(text, batch_size=batch_size, n_process=n_process), total= len(text), desc = "Lemmatization"):

        if len(pos_to_keep)>0 and len(stopwords)>0:
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.text.lower() not in stopwords and tok.pos_ in pos_to_keep] 
        elif len(pos_to_keep)>0 and len(stopwords) < 1:
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.pos_ in pos_to_keep] 
        elif len(pos_to_keep) < 1 and len(stopwords) > 0:
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space) and tok.text.lower() not in stopwords] 
        else :
            lemmas_list = [str(tok.lemma_).lower() for tok in doc if not (tok.is_punct or tok.is_space)] 
            
        all_lemmas.append(lemmas_list)

        if stats:
            tokens_counts.append(len(doc))
            tokens_kept.append(len(lemmas_list))
        
    if join_list:
        df[col_lemma]=[' '.join(map(str, l)) for l in all_lemmas]    
    else:
        df[col_lemma]=all_lemmas
    if stats:
        df["tokens_count"]=tokens_counts
        df["lemmas_count"]=tokens_kept
    
    return df



####################################################################
# VECTORISATION
####################################################################

def count_vectorize(lst_text):
    """
    Parameters:
        lst_text : list
            List of texts to be vectorized.

    Returns:
        count_vectorizer : sklearn.feature_extraction.text.CountVectorizer
            CountVectorizer object used for vectorization.
        features : scipy.sparse.csr.csr_matrix
            Sparse matrix of token counts.
        features_names : list
            List of feature names.
        vocabulary : dict
            Vocabulary dictionary mapping terms to feature indices.

    Description:
        This function vectorizes a list of texts using the CountVectorizer from scikit-learn. It tokenizes the texts based on 
        the provided token pattern, which defaults to considering any non-whitespace sequence as a token. The function returns 
        the CountVectorizer object itself, the sparse matrix of token counts, the list of feature names, and the vocabulary 
        dictionary mapping terms to feature indices.   
    """
    count_vectorizer = CountVectorizer(token_pattern=r'[^\s]+')
    features = count_vectorizer.fit_transform(lst_text)
    features_names = count_vectorizer.get_feature_names_out()
    vocabulary=count_vectorizer.vocabulary_
    
    return count_vectorizer, features, features_names, vocabulary 

def tfidf_vectorize(lst_text, analyzer='word', max_df=1.0, max_features=None, 
                    min_df=1, use_idf=True, ngram_range=(1,1), stop_words=None):
    """
    Parameters:
        lst_text : list
            List of texts to be vectorized.
        analyzer : str, {'word', 'char', 'char_wb'}, optional
            Whether to use word or character n-grams. Default is 'word'.
        max_df : float, optional
            Ignore terms that have a document frequency higher than the given threshold. Default is 1.0.
        max_features : int or None, optional
            Maximum number of features to be extracted. Default is None.
        min_df : float, optional
            Ignore terms that have a document frequency lower than the given threshold. Default is 1.
        use_idf : bool, optional
            Enable inverse-document-frequency reweighting. Default is True.
        ngram_range : tuple, optional
            The lower and upper boundary of the range of n-values for different n-grams to be extracted. Default is (1, 1).
        stop_words : str or list, optional
            Specifies the stopwords to be removed. Default is None.

    Returns:
        tfidf_vectorizer : sklearn.feature_extraction.text.TfidfVectorizer
            TfidfVectorizer object used for vectorization.
        features : scipy.sparse.csr.csr_matrix
            Sparse matrix of TF-IDF features.
        features_names : list
            List of feature names.
        vocabulary : dict
            Vocabulary dictionary mapping terms to feature indices.

    Description:
        This function vectorizes a list of texts using the TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer 
        from scikit-learn. It applies various parameters to customize the vectorization process, such as input format, 
        encoding, analyzer, document frequency thresholds, n-gram range, stopwords, and token pattern for tokenization. 
        The function returns the TfidfVectorizer object itself, the sparse matrix of TF-IDF features, the list of feature 
        names, and the vocabulary dictionary mapping terms to feature indices.
    """
    tfidf_vectorizer = TfidfVectorizer(input="content", 
                                       analyzer=analyzer, 
                                       max_df=max_df,
                                       max_features=max_features, 
                                       min_df=min_df, 
                                       use_idf=use_idf, 
                                       ngram_range=ngram_range, 
                                       stop_words=stop_words,
                                      token_pattern=r'[^\s]+')
    
    features = tfidf_vectorizer.fit_transform(lst_text)
    features_names = tfidf_vectorizer.get_feature_names_out()
    vocabulary=tfidf_vectorizer.vocabulary_
    
    return tfidf_vectorizer, features, features_names, vocabulary

def SF_vectorize(lst_text, model_name):
    """
    Vectorize text using Sentence Transformers
    """
    model = SentenceTransformer(model_name)
    features = model.encode(lst_text)
    return features

def load_HF_embeddings(model_name, encode_kwargs={'batch_size':32}, model_kwargs={'device': 'cuda:0'}):
    """
    create a HugginFace encoder
    """
    try:
        HF_encoder = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs = encode_kwargs, model_kwargs=model_kwargs)
        return HF_encoder
    except Exception as e:
        pass
        print(e)


def HF_vectorize(HF_encoder, lst_txt):
    """
    Vectorize using a Huggingface encoder
    """
    embeddings = HF_encoder.embed_documents(lst_txt)

    return embeddings

def encode_chunked_files(chunk_files_paths, HF_encoder, cols, col_text, path_embedded_chunks, reencode = False):
    """
    Encode text from files and save the results in another pickle file.
    
    Parameters:
        chunk_files_paths (list): List of file paths containing documents.
        HF_encoder (Encoder): Encoder object for text vectorization.
        cols (list): Columns to keep in the resulting DataFrame.
        col_text (str): Column containing text data in the DataFrame.
        path_embedded_chunks (str): Path to save the embedded chunks.
        reencode (bool): Whether to re-encode files even if they already exist.
    
    Returns:
        list: List of paths for newly created files.
    """
    new_file_paths=[]
    for file in tqdm(chunk_files_paths, total=len(chunk_files_paths), desc="Encoding text from files"):
        new_filename = os.path.splitext(os.path.basename(file))[0]+"_embedded"
        new_file_path = os.path.join(path_embedded_chunks, new_filename+".pickle")
        # on vérifie si on a déjà effectué l'encodage, si reencode == True, on effectue quand même la procédure
        if not os.path.exists(new_file_path) or reencode:
            current_df = load_pickle(file)

            text_list = current_df[col_text].to_list()

            # text vectorization
            embeddings = HF_encoder.embed_documents(text_list)

            # on crée un dataframe avec les embeddings
            current_df = current_df[cols]
            current_df['embeddings'] = embeddings

            # on sauvegarde
            new_file_path = write_pickle(current_df, path_embedded_chunks, new_filename)
            new_file_paths.append(new_file_path)
        else :
            new_file_paths.append(new_file_path)

    return new_file_paths


####################################################################
# SCALING FEATURES
####################################################################

def scaling_features(features, method="standard"):
    """
    Scale features if metho
    """
    try:
        if method=="standard":
            scaled_feat = StandardScaler(with_mean=False).fit_transform(features)

        else:
            scaled_feat = MinMaxScaler().fit_transform(features)
            
    except Exception as e:
        pass
        scaled_feat=features
        print(e, "features NOT SCALED")
            
    return scaled_feat
            
    

####################################################################
# REDUCTION DIMENSION
####################################################################

def lsa_reduction(features, n_components=50):
    """
    Reduce dimensions using TruncatedSVD
    """
    lsa = TruncatedSVD(n_components=n_components, random_state=0)
    embeddings = lsa.fit_transform(features)
    return embeddings

def reduce_with_UMAP(embeddings, n_neighbors = 5, n_components = 3, min_dist = 0.0, metric = "cosine"):
    """
    Reduce dimensions using UMAP
    - n_neighbors : number of neighbors
    - n_components : number of components
    - min_dist : minimum grouping distance 
    - metric : distance metric, usually "cosine" "hellinger" is another potential choice
    """
    #on réduit le nombe de dimensions
    reducer = umap.UMAP(n_neighbors=n_neighbors, 
                    n_components=n_components, 
                    min_dist=min_dist,
                    metric=metric).fit(embeddings)

    #on récupère les vecteurs réduits
    sample_reduced_embeddings = reducer.transform(embeddings)

    return reducer, sample_reduced_embeddings
    

def transform_with_UMAP(reducer, new_embeddings):
    """
    Transform new data points using a UMAP object
    """
    reduced_embeddings = reducer.transform(new_embeddings)
    return reduced_embeddings


def TSNE_reduction(features, n_components=2, perplexity=5, angle=0.5, n_iter=2000, distance_metric= 'cosine'):
    """
    Reduce dimensions using TSNE
    """
    embeddings = TSNE(n_components=n_components, 
                      perplexity=perplexity, 
                      angle=angle, 
                      n_iter=n_iter, 
                      metric=distance_metric, 
                      square_distances=True, 
                      init='random', 
                      learning_rate='auto',
                      random_state=42).fit_transform(features)
    return embeddings


def process_UMAP(embedded_chunks_paths, path_reduced_embeddings_id, reducer, reencode =  False):

    new_file_paths=[]
    for file_path in tqdm(embedded_chunks_paths, total=len(embedded_chunks_paths), desc="UMAP transform from files"):
        
        filename = os.path.splitext(os.path.basename(file_path))[0][:-9]
        new_filename = filename+"_reduce_embeddings.pickle"
        new_file_path = os.path.join(path_reduced_embeddings_id, new_filename)
    
        if not os.path.exists(new_file_path) or reencode:
            df = load_pickle(file_path)
            create_dir(path_reduced_embeddings_id)
            embeddings = df["embeddings"].to_list()
            reduced_embeddings = transform_with_UMAP(reducer, embeddings)
            reduced_embeddings_transformed=[list(e) for e in reduced_embeddings]
            df['reduced_embeddings'] = reduced_embeddings_transformed
            df.drop(columns=["embeddings"], inplace=True)
            print(path_reduced_embeddings_id, filename+"_reduce_embeddings")
            write_pickle(df, path_reduced_embeddings_id, filename+"_reduce_embeddings")
            new_file_paths.append(new_file_path)
        else:
            print("REDUCED EMBEDDINGS ALREADY EXISTS", file_path)
            new_file_paths.append(new_file_path)
    return new_file_paths

    
def process_HDBSCAN(clusterer, reduced_embeddings_paths, path_predictions_dataset_id, run_soft_clustering= False, reencode = False):
    new_file_paths=[]
    for file_path in tqdm(reduced_embeddings_paths, total=len(reduced_embeddings_paths), desc="HDBSCAN transform from files"):
        
        filename = os.path.splitext(os.path.basename(file_path))[0][:-18]
        new_filename = filename+ "_predictions.pickle"
        new_file_path = os.path.join(path_predictions_dataset_id, new_filename)
        if not os.path.exists(new_file_path) or reencode:
            df = load_pickle(file_path)
            reduced_embeddings = df["reduced_embeddings"].to_list()
            topics, probas = transform_with_HDBSCAN(clusterer, reduced_embeddings)
            df["topic"]=topics.astype(int).astype(str)
            df["proba"]=probas
            if run_soft_clustering:
                soft_clusters, soft_proba = soft_clustering_new_data(clusterer, np.array(reduced_embeddings))
                df["soft_topic"]=soft_clusters
                df["soft_proba"]=soft_proba

            write_pickle(df, path_predictions_dataset_id, filename+ "_predictions")
            new_file_paths.append(new_file_path)
        else:
            print("CLUSTERING ALREADY EXISTS", file_path)
            new_file_paths.append(new_file_path)
    return new_file_paths

    
    
####################################################################
# CLUSTERING
####################################################################

def agglomerative_clustering(embeddings, n_clusters=15, metric="euclidean", linkage="average", distance_threshold=None):
    """
    # on précise soit le nombre de clusters que l'on souhaite obtenir, soit le seuil de distance entre cluster.
    # un seul paramètre peut être défini, laisser l'autre à None
    n_clusters=15
    distance_threshold=None

    # métrique de distance : "euclidean", "l1", "l2", "manhattan", "cosine", or "precomputed"
    metric="euclidean"

    #méthode de calcul pour les branches
    # ward : minimizes the variance of the clusters being merged.
    # average : uses the average of the distances of each observation of the two sets.
    # complete or maximum : uses the maximum distances between all observations of the two sets.
    # single : uses the minimum of the distances between all observations of the two sets.
    linkage="average"

    """
    
    clusterer = AgglomerativeClustering(n_clusters=n_clusters, 
                                     metric=metric, 
                                     linkage=linkage, 
                                     distance_threshold=distance_threshold,
                                     compute_distances=True).fit(embeddings)
    return clusterer, clusterer.labels_
    
    
    
def hdbscan_clustering(embeddings, algorithm='best', alpha=1.0, cluster_selection_epsilon=0.0, approx_min_span_tree=True,
                       gen_min_span_tree=True, leaf_size=40, metric='euclidean', min_cluster_size=5, min_samples=None,
                       p=None, cluster_selection_method='eom', prediction_data = True):
    
    """
    Parameters:
    embeddings : array-like or sparse matrix, shape (n_samples, n_features)
        The input data to be clustered.
    algorithm : {'best', 'generic', 'prims_kdtree', 'boruvka_kdtree', 'boruvka_balltree', 'prims_balltree'}, optional
        The algorithm to use for computation. Default is 'best'.
    alpha : float, optional
        Scaling factor determining the individual weight of the (unnormalized) density estimate. Default is 1.0.
    cluster_selection_epsilon : float, optional
        The epsilon value to specify a minimum cluster size. Default is 0.0.
    approx_min_span_tree : bool, optional
        Whether to compute an approximation of the minimum spanning tree. Default is True.
    gen_min_span_tree : bool, optional
        Whether to compute the minimum spanning tree. Default is True.
    leaf_size : int, optional
        Leaf size for the underlying KD-tree or Ball Tree. Default is 40.
    metric : str or callable, optional
        The metric to use for distance computation. Default is 'euclidean'.
    min_cluster_size : int, optional
        The minimum size of clusters; single linkage splits that produce smaller clusters than this will be considered points "falling out" of a cluster rather than a cluster splitting into two new clusters. Default is 5.
    min_samples : int or None, optional
        The number of samples in a neighborhood for a point to be considered a core point. If None, the value is set to min_cluster_size. Default is None.
    p : int, optional
        The Minkowski p-norm distance metric parameter. Default is None.
    cluster_selection_method : {'eom', 'leaf', 'leaf_similar', 'eom_similar', 'tree', 'beagle'}, optional
        The method used to select clusters from the condensed tree. Default is 'eom'.
    prediction_data : bool, optional
        Whether the data is prediction data or not. Default is True.

Returns:
    clusterer : hdbscan.hdbscan_.HDBSCAN
        HDBSCAN clusterer object.
    labels : array, shape (n_samples,)
        Cluster labels for each point. Noisy samples are given the label -1.
    probabilities : array, shape (n_samples,)
        The probability of each sample being an outlier.

Description:
    This function performs clustering using the HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) algorithm. 
    It clusters the input data based on the specified parameters and returns the clusterer object, cluster labels for each point, and the 
    probability of each sample being an outlier.
    """
    clusterer = hdbscan.HDBSCAN(algorithm=algorithm, 
                                alpha=alpha, 
                                cluster_selection_epsilon=cluster_selection_epsilon, 
                                approx_min_span_tree=approx_min_span_tree,
                                gen_min_span_tree=gen_min_span_tree,
                                leaf_size=leaf_size,
                                metric=metric,
                                min_cluster_size=min_cluster_size, 
                                min_samples=min_samples,
                                p=p,
                                cluster_selection_method=cluster_selection_method,
                                prediction_data = prediction_data)

    clusterer.fit(embeddings)
    
    return clusterer, clusterer.labels_, clusterer.probabilities_

def transform_with_HDBSCAN(clusterer, new_embeddings):
    """
    Transform new data points using a HDBSCAN object
    """
    new_data_topic, new_data_proba = hdbscan.approximate_predict(clusterer, new_embeddings)
    return new_data_topic, new_data_proba


def soft_clustering(clusterer):
    """
    HDBSCAN SOFT CLUSTERING
    """
    soft_clusters = hdbscan.all_points_membership_vectors(clusterer)
    soft_clusters_val = [str(np.argmax(x)) for x in soft_clusters] 
    soft_clusters_proba = [np.max(x) for x in soft_clusters] 
    return soft_clusters_val, soft_clusters_proba


def soft_clustering_new_data(clusterer, embeddings):
    """
    PREDICT NEW DATA POINTS HDBSCAN SOFT CLUSTERING
    """
    soft_clusters = hdbscan.prediction.membership_vector(clusterer, embeddings)
    soft_clusters_val = [str(np.argmax(x)) for x in soft_clusters] 
    soft_clusters_proba = [np.max(x) for x in soft_clusters] 
    return soft_clusters_val, soft_clusters_proba

def get_most_relevant_documents(cluster_id, condensed_tree):
          
    assert cluster_id > -1, "The topic's label should be greater than -1!"
        
    raw_tree = condensed_tree._raw_tree
    
    # Just the cluster elements of the tree, excluding singleton points
    cluster_tree = raw_tree[raw_tree['child_size'] > 1]
    
    # Get the leaf cluster nodes under the cluster we are considering
    leaves = hdbscan.plots._recurse_leaf_dfs(cluster_tree, cluster_id)
    
    # Now collect up the last remaining points of each leaf cluster (the heart of the leaf)
    result = np.array([])
    
    for leaf in leaves:
        max_lambda = raw_tree['lambda_val'][raw_tree['parent'] == leaf].max()
        points = raw_tree['child'][(raw_tree['parent'] == leaf) & (raw_tree['lambda_val'] == max_lambda)]
        result = np.hstack((result, points))
        
    return result.astype(int)

def get_exemplars(clusterer, df, col_topic, cols_to_keep, top_messages):
    """
    List the most relevant documents for each cluster
    """
    tree = clusterer.condensed_tree_
    clusters = tree._select_clusters()
    df_exemplars=pd.DataFrame()
    for idx in df[col_topic].unique():
        if int(idx) > -1:
            c_exemplars = get_most_relevant_documents(clusters[int(idx)], tree)
            df_exemplars_tmp = df.iloc[c_exemplars[:top_messages]]
            df_exemplars = pd.concat([df_exemplars, df_exemplars_tmp])
            df_exemplars = df_exemplars[cols_to_keep].reset_index(drop=True)
    return df_exemplars

def df_transform_column_as_list(column):
    """Transform a column with unknown data format to a list of values"""
    if isinstance(column.iloc[0], str):
        # Check if it's a list formatted as string, and convert to list
        try:
            values = ast.literal_eval(column.iloc[0])
        except ValueError:
            # If it's a single URL as string, make it a list
            values = [column.iloc[0]]
    elif isinstance(column.iloc[0], int):
        # Check if it's a list formatted as int, and convert to list
        values = [column.iloc[0]]
    elif isinstance(column.iloc[0], float):
        # Check if it's a list formatted as float, and convert to list
        values = [column.iloc[0]]
    elif isinstance(column.iloc[0], bool):
        # Check if it's a list formatted as bool, and convert to list
        values = [column.iloc[0]]
    elif isinstance(column.iloc[0], list):
        # If it's already a list, use it as is
        values = column.iloc[0]
    else:
        raise ValueError("Unsupported format")

    return values

def check_gpu():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    return device
  
def HF_load_model(model_checkpoint):
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
    if torch.cuda.is_available():
        model.cuda()
    return model, tokenizer

def HF_sentiment_classifier(tokenizer, model, text, col_text, filename, dir_json):
    """ Calculate sentiment of a text. `return_type` can be 'label', 'score' or 'proba' """
    file_path= os.path.join(dir_json , str(filename)+'.json')
    if not os.path.exists(file_path):
        with torch.no_grad():
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(model.device)
            proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()[0]
            label = model.config.id2label[proba.argmax()]
            results = {"label":label, "score" : proba.max(), col_text : text}
            write_json(results, dir_json , str(filename))
    return results

