import pandas as pd
from tqdm import tqdm

def generate_index(df, col_author_id ='author_id', col_date='created_time'):
    """
    Generates an index based on user_id and date
    """
    res=[]
    for i, row in tqdm(df.iterrows(), total=df.shape[0], desc="generation des index"): 
        new_index=".".join([ str(i) for i in [ row[col_author_id], row[col_date].year, row[col_date].month, row[col_date].day]])
        res.append(new_index)
    df["index"]=res
    
    return df
                     
def avg_performance(df, 
                    col_date='created_time', 
                    col_author_id='author_id', 
                    col_engagement=['shares', 'comments', 'reactions', 'likes','top_comments', 'love', 'wow', 'haha', 
                                    'sad', 'angry','total_engagement', 'replies', 'percentage_replies'], 
                    rolling_period='7D'):
    
    """
    Function to compute average performance on a rolling period for a list of metrics
    """
                     
    # Nettoyage au cas où
    df[col_date] = pd.to_datetime(df[col_date]) 
    df = df.sort_values([col_author_id, col_date]) 

    # Le point central c'est la colone created_time, on la met en index.
    # Ensuite on groupe par author_id en gardant les colonnes de valeurs.
    # On applique la moyenne mean sur un rolling tous les 2 jours. Automatiquement il va prendre l'index, ici created_time comme pivot. 
    # On met tout à plat
    average = df.set_index(col_date).groupby(col_author_id)[col_engagement].rolling(rolling_period).mean(numeric_only=True).reset_index()
                     
    # Sur les résultats précédent, on simplifie pour récupérer une liste avec juste la liste jour / author_id
    average = average.set_index(col_date).groupby([col_author_id]).resample('1D').last(numeric_only=True).reset_index()

    # On génère nos supers index
    df=generate_index(df, col_author_id =col_author_id, col_date=col_date)    
    
    average = generate_index(average, col_author_id = col_author_id, col_date=col_date)

    # On fusionne 
    df = pd.merge(df, average[['index']+col_engagement], how='left', on=['index'], suffixes=('', '_avg'))
    
    return df

def kpi_reaction(df, cols):
    """
    Cette fonction prend un dataframe et une liste de colonnes en entrée.
    Pour chaque colonne, on va calculer le taux de sur-réaction.
    """
    for col in cols:
        df['tx_'+col]=(df[col]-df[col+'_avg'])/(df[col]+df[col+'_avg'])
    return df

def get_reactions_type(df, cols, col_dest):
    """
    Conditional function to return the reaction type based on a list of metrics 
    """
    all_val=[]
    
    for i,row in tqdm(df.iterrows(), total=df.shape[0], desc="qualification des posts"):
        
        str_val=''
        count=0
        for col in cols:
            if row[col]>0:
                str_val=str_val+' '+col.replace('tx_', 'sur-')
                count=count+1
        if count==0:
            str_val="sous reaction"
        if count==len(cols):
            str_val="sur reaction totale"
            
        all_val.append(str_val.strip())
            
    df[col_dest]=all_val       
    return df

def compute_surreaction(df, col_date, col_author_id, cols_sureaction_metrics, cols_typologie_sureaction, rolling_period_sureaction = '7D'):
    """
    Helpers to compute surreaction and return a dataframe with reaction rates and typology
    
    """
    # on désactive temporairement les messages d'alerte
    pd.options.mode.chained_assignment = None  # default='warn'
    # on calcule nos performances moyennes pour une liste de métriques
    df= avg_performance(
        df, 
        col_date=col_date, 
        col_author_id=col_author_id, 
        col_engagement= cols_sureaction_metrics, 
        rolling_period=rolling_period_sureaction
        ) 

    # on calcule les taux de sur-réaction pour notre liste de métriques
    df=kpi_reaction(df, cols_sureaction_metrics)
    cols_tx_engagement=['tx_'+c for c in cols_sureaction_metrics]
    df[cols_tx_engagement]=df[cols_tx_engagement].fillna(-1)

    # on supprime nos colonnes contenant la performance moyenne (on ne devrait plus en avoir besoin)
    cols_to_drop = [c for c in df.columns if c.lower()[-4:] == '_avg']
    df.drop(columns=cols_to_drop, inplace=True)

    # on catégorise les formes de réaction
    cols_typologie = ["tx_"+ col for col in cols_typologie_sureaction]
    df=get_reactions_type(df, cols_typologie, 'type_engagement')

    # on réactive les alertes
    pd.options.mode.chained_assignment = 'warn'  # default='warn'  
    return df