from nltk.collocations import BigramCollocationFinder
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
from community import community_louvain
from collections import defaultdict
from opsci_toolbox.helpers.dataviz import generate_color_palette_with_colormap, generate_random_hexadecimal_color
from opsci_toolbox.helpers.common import scale_list
import pandas as pd
import math

def create_collocations(lst_text, word_freq, coloc_freq, stop_words):
    # Tokenize the documents into words using scikit-learn's CountVectorizer
    vectorizer = CountVectorizer(token_pattern=r'[^\s]+', stop_words=stop_words, min_df=word_freq)
    tokenized_documents = vectorizer.fit_transform(lst_text)
    feature_names = vectorizer.get_feature_names_out()
    word_count = tokenized_documents.sum(axis=0)
    df_nodes = pd.DataFrame(zip(list(feature_names), word_count.tolist()[0]), columns=["word","size"])

    # Convert the tokenized documents into lists of words
    tokenized_documents = tokenized_documents.toarray().tolist()
    tokenized_documents = [[feature_names[i] for i, count in enumerate(doc) if count > 0] for doc in tokenized_documents]

    # Create a BigramCollocationFinder from the tokenized documents
    finder = BigramCollocationFinder.from_documents(tokenized_documents)

    # Filter by frequency
    finder.apply_freq_filter(coloc_freq)
    
     # Calculate the total number of bigrams
    total_bigrams = sum(finder.ngram_fd.values())
    
    # Create the list of tuples with desired format and relative frequency
    edges = [(pair[0][0], pair[0][1], pair[1] / total_bigrams) for pair in finder.ngram_fd.items()]
    
    # Sort the tuples by relative frequency
    edges = sorted(edges, key=lambda t: (-t[2], t[0], t[1]))
    
    # List the distinct tokens
    unique_tokens = list(set(pair[0] for pair in edges) | set(pair[1] for pair in edges))
    df_nodes=df_nodes[df_nodes['word'].isin(unique_tokens)]
    
    return edges, df_nodes


def create_maximum_tree(edges, df_nodes):
    attributs=df_nodes.set_index('word')
    dictionnaire=attributs.to_dict('index')

    network=nx.Graph()
    network.add_weighted_edges_from(edges)
    nx.set_node_attributes(network, dictionnaire)
    
    tree = nx.maximum_spanning_tree(network)

    return network, tree

def words_partitions(network, resolution = 1.0):
    try:
        partition = community_louvain.best_partition(network, resolution=resolution)
        modularity = community_louvain.modularity(partition, network)
        nx.set_node_attributes(network, partition, "modularity")
        print("Partitioning and modularity calculation successful")
    except Exception as e:
        pass
        print(e, "Partitioning and modularity calculation failed")
        # Set a default value for partition and modularity
        partition = {node: 0 for node in network.nodes()}
        modularity = 0
        nx.set_node_attributes(network, partition, "modularity")

    
def compute_metrics(network):
    ### CALCUL DE LA CENTRALITE DE DEGRES
    try:
        degree_cent = nx.degree_centrality(network)
        nx.set_node_attributes(network, degree_cent, "degree_centrality")
        print("Calcul de la centralité de degrés effectué")
    except Exception as e:
        pass
        print(e, "Calcul de la centralité de degrés impossible")
        # Set a default value for degree centrality
        degree_cent = {node: 0 for node in network.nodes()}
        nx.set_node_attributes(network, degree_cent, "degree_centrality")

        
    ### CALCUL DE LA CENTRALITE DE VECTEUR PROPRE
    try:
        centrality = nx.eigenvector_centrality(network)
        nx.set_node_attributes(network, centrality, "eigenvector_centrality")
        print("Calcul de la centralité de vecteur propre effectué")
    except Exception as e:
        pass
        print(e, "Calcul de la centralité de vecteur propre impossible")
        # Set a default value for centrality
        centrality = {node: 0 for node in network.nodes()}
        nx.set_node_attributes(network, centrality, "eigenvector_centrality")
        
    try:
        betweenness_cent = nx.betweenness_centrality(network, k=None, normalized=True, weight='weight', endpoints=False, seed=None)
        nx.set_node_attributes(network, betweenness_cent, "betweenness_centrality")
        print("Calcul de l'intermédiarité effectué")
    except Exception as e:
        pass
        print(e, "Calcul de l'intermédiarité impossible")
        # Set a default value for betweenness centrality
        betweenness_cent = {node: 0 for node in network.nodes()}
        nx.set_node_attributes(network, betweenness_cent, "betweenness_centrality")

def prepare_nodes(T, layout_positions, colormap, min_node_size = 8, max_node_size = 40):

    # on génère une palette de couleur à partir de colormap
    modularity_palette = generate_color_palette_with_colormap(set(nx.get_node_attributes(T,"modularity").values()), colormap=colormap)
    dc_palette = generate_color_palette_with_colormap(set(nx.get_node_attributes(T,"degree_centrality").values()), colormap=colormap)
    ec_palette = generate_color_palette_with_colormap(set(nx.get_node_attributes(T,"eigenvector_centrality").values()), colormap=colormap)
    bc_palette = generate_color_palette_with_colormap(set(nx.get_node_attributes(T,"betweenness_centrality").values()), colormap=colormap)

    # on scale nos métriques
    sizes = []
    degree_centralities = []
    eigenvector_centralities = []
    betweenness_centralities = []
    for n in T.nodes(data=True):
        sizes.append(n[1].get('size',0))
        degree_centralities.append(n[1].get('degree_centrality',0))
        eigenvector_centralities.append(n[1].get('eigenvector_centrality',0))
        betweenness_centralities.append(n[1].get('betweenness_centrality',0))

    scaled_sizes = scale_list(sizes, min_node_size, max_node_size)
    scaled_dc = scale_list(degree_centralities, min_node_size, max_node_size)
    scaled_ec = scale_list(eigenvector_centralities, min_node_size, max_node_size)
    scaled_bc = scale_list(betweenness_centralities, min_node_size, max_node_size)
    # sizes = [n[1]['size'] for n in T.nodes(data=True)]
    
    # on ajoute les attributs à nos nodes
    node_attributes = {n[0]: {'scaled_size': math.ceil(scaled_sizes[i]), 
                              'modularity_color': modularity_palette.get(n[1]["modularity"], generate_random_hexadecimal_color()),
                              'scaled_degree_centrality' : scaled_dc[i],
                              'degree_centrality_color': dc_palette.get(n[1]["degree_centrality"], generate_random_hexadecimal_color()),
                              'scaled_eigenvector_centrality' : scaled_ec[i],
                              'eigenvector_centrality_color': ec_palette.get(n[1]["eigenvector_centrality"], generate_random_hexadecimal_color()),
                              'scaled_betweenness_centrality' : scaled_bc[i],
                             'betweenness_centrality_color': bc_palette.get(n[1]["betweenness_centrality"], generate_random_hexadecimal_color()),
                              } for i, n in enumerate(T.nodes(data=True))}

    nx.set_node_attributes(T, node_attributes)

    for n, p in layout_positions.items():
        T.nodes[n]['pos'] = p

def prepare_edges(T, min_edge_size=1, max_edge_size=5):
    w = [e[2]['weight'] for e in T.edges(data=True)]
    scaled_w = scale_list(w, min_edge_size, max_edge_size)
    edges_attributes_dict = {(e[0], e[1]): {'scaled_weight': scaled_w[i]} for i, e in enumerate(T.edges(data=True))}
    nx.set_edge_attributes(T, edges_attributes_dict)
    

def layout_graphviz(network, layout ="fdp", args=""):
    layout_positions = nx.nx_agraph.graphviz_layout(network, prog=layout, args=args)
    return layout_positions

def layout_spring(network, k = 0.08, scale = 2, iterations = 200, weight="weight"):
    layout_positions = nx.spring_layout(network, k=k,  scale=scale, iterations=iterations, weight=weight)
    return layout_positions