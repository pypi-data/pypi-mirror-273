from cuml import UMAP
from cuml.cluster.hdbscan import HDBSCAN, all_points_membership_vectors, approximate_predict, membership_vector
import numpy as np 
from tqdm import tqdm
import os
from opsci_toolbox.helpers.common import load_pickle, create_dir, write_pickle

def reduce_with_cuml_UMAP(embeddings, n_neighbors = 5, n_components = 3, min_dist = 0.0, metric = "cosine", spread = 1.0):
    reducer = UMAP(n_neighbors=n_neighbors, 
                   n_components=n_components, 
                   min_dist=min_dist, 
                   metric=metric,
                   spread =  spread).fit(embeddings)
    
    reduced_embeddings = reducer.transform(embeddings)
    return reducer, reduced_embeddings

def transform_with_cuml_UMAP(reducer, new_embeddings):
    """
    Transform new data points using a UMAP object
    """
    reduced_embeddings = reducer.transform(new_embeddings)
    return reduced_embeddings


def hdbscan_cuml_clustering(embeddings, min_cluster_size=5, min_samples=None, max_cluster_size = 0,  metric='euclidean', alpha=1.0, p=2, cluster_selection_epsilon=0.0, cluster_selection_method='eom', 
                       approx_min_span_tree=True, gen_min_span_tree = False, gen_condensed_tree = False, gen_single_linkage_tree_ = False, prediction_data=True):
    
    """
    Parameters:
    embeddings : array-like or sparse matrix, shape (n_samples, n_features)
        The input data to be clustered.
    min_cluster_size : int, optional
        The minimum number of samples in a group for that group to be considered a cluster; groupings smaller than this size will be left as noise.
    min_samples : int or None, optional
        The number of samples in a neighborhood for a point to be considered as a core point. This includes the point itself. If ‘None’, it defaults to the min_cluster_size.
    max_cluster_size : int, optional (default=0)
        A limit to the size of clusters returned by the eom algorithm. Has no effect when using leaf clustering (where clusters are usually small regardless) and can also be overridden in rare cases by a high value for cluster_selection_epsilon. 
        Note that this should not be used if we want to predict the cluster labels for new points in future (e.g. using approximate_predict), as the approximate_predict function is not aware of this argument.    
    metric : str or callable, optional
        The metric to use for distance computation. Default is 'euclidean'.
    alpha : float, optional
         distance scaling parameter as used in robust single linkage.
    p : int, optional
        The Minkowski p-norm distance metric parameter. Default is None.
    cluster_selection_epsilon : float, optional
        A distance threshold. Clusters below this value will be merged. Note that this should not be used if we want to predict the cluster labels for new points in future (e.g. using approximate_predict), as the approximate_predict function is not aware of this argument.
    cluster_selection_method : {'eom', 'leaf'}, optional
        The method used to select clusters from the condensed tree. The standard approach for HDBSCAN* is to use an Excess of Mass algorithm to find the most persistent clusters. Alternatively you can instead select the clusters at the leaves of the tree – this provides the most fine grained and homogeneous clusters. Options are:
    approx_min_span_tree : bool, optional
        Whether to compute an approximation of the minimum spanning tree. Default is True.
    gen_min_span_tree : bool, optional
        Whether to populate the minimum_spanning_tree_ member for utilizing plotting tools. This requires the hdbscan CPU Python package to be installed
    gen_condensed_tree : bool, optional
        Whether to populate the condensed_tree_ member for utilizing plotting tools. 
    gen_single_linkage_tree_ :  bool
        Whether to populate the single_linkage_tree_ member for utilizing plotting tools.
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
    clusterer = HDBSCAN(min_cluster_size=min_cluster_size, 
                                min_samples=min_samples, 
                                max_cluster_size = max_cluster_size,  
                                metric=metric, 
                                alpha=alpha, 
                                p=p, 
                                cluster_selection_epsilon=cluster_selection_epsilon, 
                                cluster_selection_method=cluster_selection_method, 
                                approx_min_span_tree=approx_min_span_tree,
                                gen_min_span_tree = gen_min_span_tree, 
                                gen_condensed_tree = gen_condensed_tree, 
                                gen_single_linkage_tree_ = gen_single_linkage_tree_, 
                                prediction_data=prediction_data)

    clusterer.fit_predict(embeddings)
    
    return clusterer, clusterer.labels_, clusterer.probabilities_

def transform_with_cuml_HDBSCAN(clusterer, new_embeddings):
    """
    Transform new data points using a HDBSCAN object
    """
    new_data_topic, new_data_proba = approximate_predict(clusterer, new_embeddings)
    return new_data_topic, new_data_proba


def cuml_soft_clustering(clusterer):
    """
    HDBSCAN SOFT CLUSTERING
    """
    soft_clusters = all_points_membership_vectors(clusterer)
    soft_clusters_val = [str(np.argmax(x)) for x in soft_clusters] 
    soft_clusters_proba = [np.max(x) for x in soft_clusters] 
    return soft_clusters_val, soft_clusters_proba


def soft_cuml_clustering_new_data(clusterer, embeddings):
    """
    PREDICT NEW DATA POINTS HDBSCAN SOFT CLUSTERING
    """
    soft_clusters =membership_vector(clusterer, embeddings)
    soft_clusters_val = [str(np.argmax(x)) for x in soft_clusters] 
    soft_clusters_proba = [np.max(x) for x in soft_clusters] 
    return soft_clusters_val, soft_clusters_proba

def process_UMAP(embedded_chunks_paths, path_reduced_embeddings_id, reducer, reencode =  False):

    new_file_paths=[]
    for file_path in tqdm(embedded_chunks_paths, total=len(embedded_chunks_paths), desc="UMAP transform from files"):
        
        filename = os.path.splitext(os.path.basename(file_path))[0][:-9]
        new_filename = filename+"_reduce_embeddings.pickle"
        new_file_path = os.path.join(path_reduced_embeddings_id, new_filename)
    
        if not os.path.exists(new_file_path) or reencode:
            df = load_pickle(file_path)
            create_dir(path_reduced_embeddings_id)
            # embeddings = df["embeddings"].to_list()
            embeddings = np.vstack(df['embeddings'].values)
            reduced_embeddings = transform_with_cuml_UMAP(reducer, embeddings)
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
            # reduced_embeddings = df["reduced_embeddings"].to_list()
            reduced_embeddings = np.vstack(df['reduced_embeddings'].values)
            topics, probas = transform_with_cuml_HDBSCAN(clusterer, reduced_embeddings)
            df["topic"]=topics.astype(int).astype(str)
            df["proba"]=probas
            if run_soft_clustering:
                soft_clusters, soft_proba = soft_cuml_clustering_new_data(clusterer, np.array(reduced_embeddings))
                df["soft_topic"]=soft_clusters
                df["soft_proba"]=soft_proba

            write_pickle(df, path_predictions_dataset_id, filename+ "_predictions")
            new_file_paths.append(new_file_path)
        else:
            print("CLUSTERING ALREADY EXISTS", file_path)
            new_file_paths.append(new_file_path)
    return new_file_paths
