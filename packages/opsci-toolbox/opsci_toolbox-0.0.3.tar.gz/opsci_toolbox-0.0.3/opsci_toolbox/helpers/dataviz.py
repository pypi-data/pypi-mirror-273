from plotly.subplots import make_subplots
import plotly.graph_objects as go
import textwrap
import numpy as np
from scipy import interpolate
from scipy.spatial import ConvexHull
import random
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import chart_studio.tools as tls
import chart_studio.plotly as py
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import math
import pandas as pd
from opsci_toolbox.helpers.nlp import sample_most_engaging_posts, create_frequency_table
from matplotlib.colors import to_hex



def upload_chart_studio(username,api_key,fig, title):
    """
    Upload Plotly viz to chart studio
    """
    URL = ""
    EMBED = ""

    try:    
        tls.set_credentials_file(username=username, api_key=api_key)
        URL = py.plot(fig, filename = title, auto_open=True)
        EMBED = tls.get_embed(URL)
        print("* URL DE LA VIZ >> ",URL)
        print("\n*CODE EMBED A COLLER \n",EMBED)
        
    except Exception as e:
        pass
        print(e, "try to reduce the dataviz size by printing less data")

    return URL,EMBED


def scale_to_0_10(x):
    return ((x - x.min()) / (x.max() - x.min()) * 10).astype(int)

def normalize_data_size(df, col:str, coef = 20, constant = 5):
    """
    Function to normalize the sizes of dots 
    """
    df['normalized_'+col]=((df[col]-df[col].max())/(df[col]+df[col].max())+1) * coef + constant
    return df

def generate_color_palette(lst, transparency=1):
    """
    Function to generate a random color palette of RGBa codes
    """
    color_palette = {color: 'rgba({}, {}, {}, {})'.format(
                        random.randrange(0, 255),
                        random.randrange(0, 255),
                        random.randrange(0, 255),
                        transparency
                    ) for color in lst}
    return color_palette

def generate_color_palette_with_colormap(lst, colormap = "viridis"):
    num_colors = len(lst)
    # Generate some example data
    data = np.linspace(0, 1, num_colors)

    # Choose the colormap
    cmap = plt.get_cmap(colormap, num_colors)

    # Normalize the data
    norm = plt.Normalize(0, 1)

    # Interpolate colors
    colors = cmap(norm(data))

    # Convert colors to hexadecimal codes
    hex_colors = {item : to_hex(colors[i]) for i, item in enumerate(lst)}

    return hex_colors

def generate_hexadecimal_color_palette(lst, add_transparency=False, transparency=0.5):
    """
    Function to generate a random color palette with hexadecimal codes and transparency
    """
    if add_transparency:
        alpha_hex = int(transparency * 255)  # Convert transparency to integer (0-255 range)
        color_palette = {color: "#{:02x}{:02x}{:02x}{:02x}".format(
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255),
                            alpha_hex
                        ) for color in lst}
    else:
        color_palette = {color: "#{:02x}{:02x}{:02x}".format(
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255)
                        ) for color in lst}
    return color_palette

def generate_random_hexadecimal_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def wrap_text(txt, lenght=50):
    """
    Function to wrap text (for hover)
    """
    txt = '<br>'.join(textwrap.wrap(str(txt), width=lenght))
    return txt

def get_convex_hull_coord(points: np.array, interpolate_curve: bool = True) -> tuple:
    """
    Calculate the coordinates of the convex hull for a set of points.

    Args:
        points (np.array): Array of points, where each row is [x, y].
        interpolate_curve (bool): Whether to interpolate the convex hull.

    Returns:
        tuple: Tuple containing interpolated x and y coordinates of the convex hull.
    """
    # Calculate the convex hull of the points
    hull = ConvexHull(points)

    # Get the x and y coordinates of the convex hull vertices
    x_hull = np.append(points[hull.vertices, 0], points[hull.vertices, 0][0])
    y_hull = np.append(points[hull.vertices, 1], points[hull.vertices, 1][0])

    if interpolate_curve:
        # Calculate distances between consecutive points on the convex hull
        dist = np.sqrt(
            (x_hull[:-1] - x_hull[1:]) ** 2 + (y_hull[:-1] - y_hull[1:]) ** 2
        )

        # Calculate the cumulative distance along the convex hull
        dist_along = np.concatenate(([0], dist.cumsum()))

        # Use spline interpolation to generate interpolated points
        spline, u = interpolate.splprep([x_hull, y_hull], u=dist_along, s=0, per=1)
        interp_d = np.linspace(dist_along[0], dist_along[-1], 50)
        interp_x, interp_y = interpolate.splev(interp_d, spline)
    else:
        # If interpolation is not needed, use the original convex hull points
        interp_x = x_hull
        interp_y = y_hull

    return interp_x, interp_y
    
# def create_scatter_plot(df, col_x, col_y, col_category, color_palette, col_color, col_size, col_text, title="Scatter Plot", x_axis_label="X-axis", y_axis_label="Y-axis", width=1000, height=1000, xaxis_range=None, yaxis_range=None, 
#     size_value =4, opacity=0.8, maxdisplayed=0, plot_bgcolor=None, paper_bgcolor=None, color="indianred", line_width=0.5, line_color="white", colorscale='Viridis', showscale=True, template="plotly"):
#     """
#     Create a scatter plot : 
#     - df contains all data : X / Y values, category for colorization, sizes and text for hover.
#     - col_x : name of the column containing X values
#     - col_y : name of the column containing Y values
#     - col_category : name of the column for colorization
#     - color_palette : a dict mapping category with color value
#     - col_color : name of the column for color ==> to be used only for continuous scale
#     - col_size : name of the column for dot sizes
#     - col_text : name of the column containing text for legend on hover
#     - title : graph title
#     - x_axis_label : label for X
#     - y_axis_label : label for Y
#     - width / height : size of the graphe
#     - xaxis_range / y_axis_range : range values for axis. None for auto values.
#     - size_value =  minimun size (or constant) for dots 
#     - opacity : dots transparency
#     - maxdisplayed : maximum number of dots to display. 0 = infinite
#     - plot_bgcolor : background color for plot
#     - paper_bgcolor : background color for the area around the plot 
#     - color : color code for dots if col_category is None
#     - line_width : width of dots contours
#     - line_color : color of dots contours
#     """

#     if line_color is None :
#         line_color=color

#     fig = go.Figure()

#     #col_category is used to colorize dots
#     if col_category is not None:
#         for i, category in enumerate(df[col_category].unique()):
#             color = color_palette.get(category, 'rgb(0, 0, 0)')  # Default to black if category not found
            
#             #hovertemplate generation 
#             hovertemplate='<b>'+col_x+'</b>:'+df[df[col_category]==category][col_x].astype(str)+'<br><b>'+col_y+'</b>:'+df[df[col_category]==category][col_y].astype(str)+'<br><b>'+col_category+'</b>:'+str(category)
#             if col_size is None:
#                 size=size_value
#             else:
#                 size = df[df[col_category] == category][col_size]
#                 hovertemplate += '<br><b>'+col_size+'</b>:'+size.astype(str)

#             if col_text is not None:
#                 hovertemplate +='<br><b>'+col_text+'</b>:'+ df[df[col_category]==category][col_text].apply(wrap_text)

#             fig.add_trace(
#                 go.Scatter(
#                     x=df[df[col_category]==category][col_x], 
#                     y=df[df[col_category]==category][col_y], 
#                     mode='markers', 
#                     marker=dict(color=color,                 #dots color
#                                 size=size,                   #dots size
#                                 opacity=opacity,             #dots opacity
#                                 line_color=line_color,       #line color around dot
#                                 line_width=line_width,       #line width around dot
#                                 sizemode='area',
#                                 sizemin = size_value,        #minimum size of dot
#                                 maxdisplayed=maxdisplayed,   #max number of dots to display (0 = infinite)
#                                 symbol = "circle"            #type of dot
#                                 ), 
#                     name=category,                           # trace name
#                     hovertemplate=hovertemplate+"<extra></extra>"
#                     )
#                 )
#     # if there is no category for color, we create a simpler plot
#     else:
#         hovertemplate='<b>'+col_x+'</b>:'+df[col_x].astype(str)+'<br><b>'+col_y+'</b>:'+df[col_y].astype(str)
#         if col_size is None:
#             size=size_value
#         else:
#             size = df[col_size]
#             hovertemplate += '<br><b>'+col_size+'</b>:'+size.astype(str)
#         if col_color is not None :
#             hovertemplate +='<br><b>'+col_color+'</b>:'+df[col_color].astype(str)
#             color = df[col_color]
#         else :
#             if color is None:
#                 color = generate_random_hexadecimal_color()
#         if col_text is not None:
#             hovertemplate +='<br><b>'+col_text+'</b>:'+ df[col_text].apply(wrap_text)

#         fig = go.Figure( go.Scatter(
#                     x=df[col_x], 
#                     y=df[col_y], 
#                     mode='markers', 
#                     marker=dict(color=color,                #dots color
#                                 size=size,                  #dots size
#                                 opacity=opacity,            #dots opacity
#                                 line_color=line_color,      #line color around dot
#                                 line_width=line_width,      #line width arount dot
#                                 sizemode='area',            # Scale marker sizes
#                                 sizemin = size_value,       #minimum size of dot
#                                 maxdisplayed=maxdisplayed,  #max number of dots to display (0 = infinite)
#                                 symbol = "circle",           #type of dot
#                                 colorscale=colorscale,
#                                 showscale=showscale
#                                 ), 
#                     name="",
#                     hovertemplate=hovertemplate+"<extra></extra>"
#                     ))

#     #we calculate X and Y axis ranges. 
#     if yaxis_range is None :
#         yaxis_range=[df[col_y].min()-0.1,df[col_y].max()+0.1]
#     if xaxis_range is None : 
#         xaxis_range = [df[col_x].min()-0.1,df[col_x].max()+0.1]

#     # Update layout
#     fig.update_layout(
#         title=title,                  #graph title
#         xaxis_title=x_axis_label,     #xaxis title
#         yaxis_title=y_axis_label,     #yaxis title
#         width=width,                  #plot size
#         height=height,                #plot size
#         xaxis_showline=False,         #intermediate lines
#         xaxis_showgrid=False,         #grid
#         xaxis_zeroline=False,         #zeroline
#         yaxis_showline=False,         #intermediate lines
#         yaxis_showgrid=False,         #grid
#         yaxis_zeroline=False,         #zeroline
#         yaxis_range = yaxis_range,    #yaxis range
#         xaxis_range = xaxis_range,    #xaxis range
#         template=template,
#         plot_bgcolor=plot_bgcolor,    #background color (plot)
#         paper_bgcolor=paper_bgcolor,   #background color (around plot)
#         font_family="Segoe UI Semibold",           # font

#     )

#     return fig

def create_scatter_plot(df, col_x, col_y, col_category, color_palette, col_color, col_size, col_text, col_legend = [], title="Scatter Plot", x_axis_label="X-axis", y_axis_label="Y-axis", width=1000, height=1000, xaxis_range=None, yaxis_range=None, 
    size_value =4, opacity=0.8, maxdisplayed=0, mode = "markers", textposition="bottom center", plot_bgcolor=None, paper_bgcolor=None, yaxis_showgrid = False, xaxis_showgrid = False, color="indianred", line_width=0.5, line_color="white", colorscale='Viridis', showscale=True, template="plotly"):
    """
    Create a scatter plot : 
    - df contains all data : X / Y values, category for colorization, sizes and text for hover.
    - col_x : name of the column containing X values
    - col_y : name of the column containing Y values
    - col_category : name of the column for colorization
    - color_palette : a dict mapping category with color value
    - col_color : name of the column for color ==> to be used only for continuous scale
    - col_size : name of the column for dot sizes
    - col_text : name of the column containing text for legend on hover
    - title : graph title
    - x_axis_label : label for X
    - y_axis_label : label for Y
    - width / height : size of the graphe
    - xaxis_range / y_axis_range : range values for axis. None for auto values.
    - size_value =  minimun size (or constant) for dots 
    - opacity : dots transparency
    - maxdisplayed : maximum number of dots to display. 0 = infinite
    - plot_bgcolor : background color for plot
    - paper_bgcolor : background color for the area around the plot 
    - color : color code for dots if col_category is None
    - line_width : width of dots contours
    - line_color : color of dots contours
    """

    if line_color is None :
        line_color=color

    fig = go.Figure()

    #col_category is used to colorize dots
    if col_category is not None:
        for i, category in enumerate(df[col_category].unique()):
            color = color_palette.get(category, 'rgb(0, 0, 0)')  # Default to black if category not found
            
            #hovertemplate generation 
            hovertemplate='<b>'+col_x+'</b>:'+df[df[col_category]==category][col_x].astype(str)+'<br><b>'+col_y+'</b>:'+df[df[col_category]==category][col_y].astype(str)+'<br><b>'+col_category+'</b>:'+str(category)
            if col_size is None:
                size=size_value
            else:
                size = df[df[col_category] == category][col_size]
                hovertemplate += '<br><b>'+col_size+'</b>:'+size.astype(str)

            if len(col_legend)>0:
                for c in col_legend:
                    hovertemplate +='<br><b>'+str(c)+'</b>:'+ df[df[col_category]==category][c].astype(str).apply(wrap_text)

            fig.add_trace(
                go.Scatter(
                    x=df[df[col_category]==category][col_x], 
                    y=df[df[col_category]==category][col_y], 
                    mode=mode, 
                    text = df[df[col_category]==category][col_text],
                    textposition=textposition,
                    marker=dict(color=color,                 #dots color
                                size=size,                   #dots size
                                opacity=opacity,             #dots opacity
                                line_color=line_color,       #line color around dot
                                line_width=line_width,       #line width around dot
                                sizemode='area',
                                sizemin = size_value,        #minimum size of dot
                                maxdisplayed=maxdisplayed,   #max number of dots to display (0 = infinite)
                                symbol = "circle"            #type of dot
                                ), 
                    name=category,                           # trace name
                    hovertemplate=hovertemplate+"<extra></extra>"
                    )
                )
    # if there is no category for color, we create a simpler plot
    else:
        hovertemplate='<b>'+col_x+'</b>:'+df[col_x].astype(str)+'<br><b>'+col_y+'</b>:'+df[col_y].astype(str)
        if col_size is None:
            size=size_value
        else:
            size = df[col_size]
            hovertemplate += '<br><b>'+col_size+'</b>:'+size.astype(str)
        if col_color is not None :
            hovertemplate +='<br><b>'+col_color+'</b>:'+df[col_color].astype(str)
            color = df[col_color]
        else :
            if color is None:
                color = generate_random_hexadecimal_color()
        if len(col_legend)>0:
            for c in col_legend:
                hovertemplate +='<br><b>'+str(c)+'</b>:'+ df[c].astype(str).apply(wrap_text)

        fig = go.Figure( go.Scatter(
                    x=df[col_x], 
                    y=df[col_y], 
                    mode=mode, 
                    text = df[col_text],
                    textposition=textposition,
                    marker=dict(color=color,                #dots color
                                size=size,                  #dots size
                                opacity=opacity,            #dots opacity
                                line_color=line_color,      #line color around dot
                                line_width=line_width,      #line width arount dot
                                sizemode='area',            # Scale marker sizes
                                sizemin = size_value,       #minimum size of dot
                                maxdisplayed=maxdisplayed,  #max number of dots to display (0 = infinite)
                                symbol = "circle",           #type of dot
                                colorscale=colorscale,
                                showscale=showscale
                                ), 
                    name="",
                    hovertemplate=hovertemplate+"<extra></extra>"
                    ))

    #we calculate X and Y axis ranges. 
    if yaxis_range is None :
        yaxis_range=[df[col_y].min()- 0.1,df[col_y].max() +  0.1]
    if yaxis_range == "auto":
        yaxis_range=None
    
    if xaxis_range is None : 
        xaxis_range = [df[col_x].min()- 0.1,df[col_x].max()+ 0.1]
    if xaxis_range =="auto":
        xaxis_range=None

    # Update layout
    fig.update_layout(
        title=title,                  #graph title
        xaxis_title=x_axis_label,     #xaxis title
        yaxis_title=y_axis_label,     #yaxis title
        width=width,                  #plot size
        height=height,                #plot size
        xaxis_showgrid=xaxis_showgrid,         #grid
        yaxis_showgrid=yaxis_showgrid,         #grid
        yaxis_range = yaxis_range,    #yaxis range
        xaxis_range = xaxis_range,    #xaxis range
        template=template,
        plot_bgcolor=plot_bgcolor,    #background color (plot)
        paper_bgcolor=paper_bgcolor,   #background color (around plot)
        font_family="Segoe UI Semibold",           # font

    )
    return fig

def add_annotations(fig, df, col_x, col_y, col_txt, width=1000, label_size_ratio=100, bordercolor = "#C7C7C7", arrowcolor = "SlateGray", bgcolor ="#FFFFFF", font_color = "SlateGray"):
    df[col_txt]=df[col_txt].fillna("").astype(str)
    for i, row in df.iterrows():
        fig.add_annotation(x=row[col_x], 
                           y=row[col_y], 
                           text='<b>'+wrap_text(row[col_txt])+'</b>', 
                           showarrow=True, 
                           arrowhead=1, 
                           font=dict(
                               family="Helvetica, Sans-serif",
                               size=width / label_size_ratio,
                               color=font_color
                               ),
                            bordercolor=bordercolor, 
                            borderwidth=width / 1000, 
                            borderpad=width / 500, 
                            bgcolor=bgcolor, 
                            opacity=1, 
                            arrowcolor=arrowcolor
                        )

    return fig

def scatter3D(df, col_x, col_y, col_z, col_category, color_palette, col_size, col_text, title="3D Scatter Plot", x_axis_label="X-axis", y_axis_label="Y-axis", z_axis_label="Z-axis", width=1000, height=1000, xaxis_range=None, yaxis_range=None, 
              zaxis_range=None, size_value =4, opacity=0.8, plot_bgcolor=None, paper_bgcolor=None, color="indianred", line_width=0.5, line_color="white", template = "plotly"):
    """
    Create a 3D scatter plot : 
    - df contains all data : X / Y values, category for colorization, sizes and text for hover.
    - col_x : name of the column containing X values
    - col_y : name of the column containing Y values
    - col_z : name of the column containing Z values
    - col_category : name of the column for colorization
    - color_palette : a dict mapping category with color value
    - col_size : name of the column for dot sizes
    - col_text : name of the column containing text for legend on hover
    - title : graph title
    - x_axis_label / y_axis_label / z_axis_label : label for X, Y, Z axis
    - width / height : size of the graphe
    - xaxis_range / y_axis_range / z_axis_range : range values for axis. None for auto values.
    - size_value =  minimun size (or constant) for dots 
    - opacity : dots transparency
    - plot_bgcolor : background color for plot
    - paper_bgcolor : background color for the area around the plot 
    - color : color code for dots if col_category is None
    - line_width : width of dots contours
    - line_color : color of dots contours
    """
    fig=go.Figure()
    if col_category is not None:
        for i, category in enumerate(df[col_category].unique()):
            color = color_palette.get(category, 'rgb(0, 0, 0)')  # Default to black if category not found

            #hovertemplate generation 
            hovertemplate='<b>X</b>:'+df[df[col_category]==category][col_x].astype(str)+'<br><b>Y</b>:'+df[df[col_category]==category][col_y].astype(str)+'<br><b>Z</b>:'+df[df[col_category]==category][col_z].astype(str)+'<br><b>'+col_category+'</b>:'+str(category)
            if col_size is None:
                size=size_value
            else:
                size = df[df[col_category] == category][col_size]
                hovertemplate += '<br><b>'+col_size+'</b>:'+size.astype(str)

            if col_text is not None:
                hovertemplate +='<br><b>'+col_text+'</b>:'+ df[df[col_category]==category][col_text].apply(wrap_text)

            fig.add_trace(
                go.Scatter3d(
                    x=df[df[col_category]==category][col_x], 
                    y=df[df[col_category]==category][col_y], 
                    z=df[df[col_category]==category][col_z], 
                    mode='markers', 
                    marker=dict(color=color,                 #dots color
                                size=size,                   #dots size
                                opacity=opacity,             #dots opacity
                                line_color=line_color,          #line color around dot
                                line_width=line_width,              #line width around dot
                                sizemin = size_value,        #minimum size of dot
                                symbol = "circle"            #type of dot
                                ), 
                    name=category,                           # trace name
                    hovertemplate=hovertemplate+"<extra></extra>"
                    )
                )
    else:
        #hovertemplate creation
        hovertemplate='<b>X</b>:'+df[col_x].astype(str)+'<br><b>Y</b>:'+df[col_y].astype(str)+'<br><b>Z</b>:'+df[col_z].astype(str)
        if col_size is None:
            size=size_value
        else:
            size = df[col_size]
            hovertemplate += '<br><b>'+col_size+'</b>:'+size.astype(str)
        if col_text is not None:
            hovertemplate +='<br><b>'+col_text+'</b>:'+ df[col_text].apply(wrap_text)

        fig = go.Figure( go.Scatter3d(
                    x=df[col_x], 
                    y=df[col_y],
                    z=df[col_z], 
                    mode='markers', 
                    marker=dict(color=color,                #dots color
                                size=size,                  #dots size
                                opacity=opacity,            #dots opacity
                                line_color=line_color,         #line color around dot
                                line_width=line_width,             #line width arount dot
                                sizemin = size_value,       #minimum size of dot
                                symbol = "circle"           #type of dot
                                ), 
                    name="",
                    hovertemplate=hovertemplate+"<extra></extra>"
                    ))


    #we calculate X and Y axis ranges. 
    if yaxis_range is None :
        yaxis_range=[df[col_y].min()-0.1,df[col_y].max()+0.1]
    if xaxis_range is None : 
        xaxis_range = [df[col_x].min()-0.1,df[col_x].max()+0.1]
    if zaxis_range is None : 
        zaxis_range = [df[col_z].min()-0.1,df[col_z].max()+0.1]
    fig.update_layout(
        
        font_family="Segoe UI Semibold",           # font
        title=title,                  #graph title
        xaxis_title=x_axis_label,     #xaxis title
        yaxis_title=y_axis_label,     #yaxis title
        zaxis_title=z_axis_label,     #zaxis title
        width=width,                  #plot size
        height=height,                #plot size
        xaxis_showline=False,         #intermediate lines
        xaxis_showgrid=False,         #grid
        xaxis_zeroline=False,         #zeroline
        yaxis_showline=False,         #intermediate lines
        yaxis_showgrid=False,         #grid
        yaxis_zeroline=False,         #zeroline
        zaxis_showline=False,         #intermediate lines
        zaxis_showgrid=False,         #grid
        zaxis_zeroline=False,         #zeroline
        scene_yaxis_range = yaxis_range,    #yaxis range
        scene_xaxis_range = xaxis_range,    #xaxis range
        scene_zaxis_range = zaxis_range,    #zaxis range
        scene_camera = dict(               #camera orientation at start
            up=dict(x=1, y=0, z=2),        
            center=dict(x=0, y=0, z=0),
            eye=dict(x=2, y=1.25, z=0.5)
        ),
        template=template,
        plot_bgcolor=plot_bgcolor,    #background color (plot)
        paper_bgcolor=paper_bgcolor,   #background color (around plot)
        margin=dict(
                    t=width / 15,
                    b=width / 25,
                    r=width / 25,
                    l=width / 25,
                ),
        legend=dict(   
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="right",
            x=1,
            itemsizing= 'constant'
        )
    )

    return fig
    

def fig_bar_trend(df, col_x, bar_measure, trend_measure, x_name="X", bar_name ="metric1", trend_name = "metric2", marker_color='lightpink', line_color='indianred', title_text="Couverture & Résonance", width=1500, height=700, xaxis_tickangle=0, opacity=0.8, plot_bgcolor=None, paper_bgcolor=None, template = "plotly"):
    """
    Display a graph that combine bar and trend chart to compare 2 metrics :
    - x = x axis data
    - bar_measure = data represented as bar diagram
    - trend_measure = data represented as trend line
    - x_name / bar_name / trend_name : axis labels
    - marker_color = color code for bars
    - line_color = color code for trend line
    - title_text = graph title
    - width / height = size of plot
    - xaxis_tickangle =  angle for x ticks
    - opacity = opacity of bars
    """

    # nk = np.empty(shape=(len(x), 3, 1), dtype="object")
    # nk[:, 0] = np.array(x.apply(lambda txt: '<br>'.join(textwrap.wrap(str(txt), width=50)))).reshape(-1, 1)
    # nk[:, 1] = np.array(bar_measure).reshape(-1, 1)
    # nk[:, 2] = np.array(trend_measure).reshape(-1, 1)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df[col_x].apply(wrap_text), 
            y=df[trend_measure], 
            name=trend_name,
            mode='lines', 
            line_color=line_color, 
            line_width=4,
            textfont=dict(size=8),
            # customdata=nk,
            hovertemplate=("<br>"+x_name+" :"+df[col_x].astype(str)+"<br>"+bar_name+" - "+df[bar_measure].astype(str)+"<br>"+trend_name+" : "+df[trend_measure].astype(str)+"<extra></extra>"),
        ),
        secondary_y=True,
    )
    # Add traces
    fig.add_trace(
        go.Bar(
            x=df[col_x].apply(wrap_text), 
            y = df[bar_measure], 
            name=bar_name, 
            marker_color=marker_color, 
            opacity=opacity,
            # customdata=nk,
            hovertemplate=("<br>"+x_name+" :"+df[col_x].astype(str)+"<br>"+bar_name+" - "+df[bar_measure].astype(str)+"<br>"+trend_name+" : "+df[trend_measure].astype(str)+"<extra></extra>"),
        ),
        secondary_y=False,

    )
    first_axis_range=[-0.5,df[bar_measure].max()*1.01]
    secondary_axis_range=[-0.5,df[trend_measure].max()*1.01]

    # Add figure title
    fig.update_layout(
        
        title_text=title_text, 
        showlegend=True,
        width = width,
        height= height,
        xaxis_tickangle=xaxis_tickangle,
        xaxis_showline=False,
        xaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_showgrid=False,
        font_family="Segoe UI Semibold",
        template=template,
        plot_bgcolor=plot_bgcolor,    #background color (plot)
        paper_bgcolor=paper_bgcolor,   #background color (around plot)
        margin=dict(
                    t=width / 15,
                    b=width / 20,
                    r=width / 20,
                    l=width / 20,
                ),
    )

    # # Set x-axis title
    fig.update_xaxes(title_text=x_name)

    # Set y-axes titles
    fig.update_yaxes(title_text=bar_name, range = first_axis_range, secondary_y=False)
    fig.update_yaxes(title_text=trend_name, range = secondary_axis_range, secondary_y=True)  
    
    return fig


# def fig_bar_trend(x, bar_measure, trend_measure, x_name="X", bar_name ="metric1", trend_name = "metric2", marker_color='lightpink', line_color='indianred', title_text="Couverture & Résonance", width=1500, height=700, xaxis_tickangle=0, opacity=0.8, plot_bgcolor=None, paper_bgcolor=None, template = "plotly"):
#     """
#     Display a graph that combine bar and trend chart to compare 2 metrics :
#     - x = x axis data
#     - bar_measure = data represented as bar diagram
#     - trend_measure = data represented as trend line
#     - x_name / bar_name / trend_name : axis labels
#     - marker_color = color code for bars
#     - line_color = color code for trend line
#     - title_text = graph title
#     - width / height = size of plot
#     - xaxis_tickangle =  angle for x ticks
#     - opacity = opacity of bars
#     """

#     nk = np.empty(shape=(len(x), 3, 1), dtype="object")
#     nk[:, 0] = np.array(x.apply(lambda txt: '<br>'.join(textwrap.wrap(str(txt), width=50)))).reshape(-1, 1)
#     nk[:, 1] = np.array(bar_measure).reshape(-1, 1)
#     nk[:, 2] = np.array(trend_measure).reshape(-1, 1)

#     fig = make_subplots(specs=[[{"secondary_y": True}]])

#     fig.add_trace(
#         go.Scatter(
#             x=x, 
#             y=trend_measure, 
#             name=trend_name,
#             mode='lines', 
#             line_color=line_color, 
#             line_width=4,
#             textfont=dict(size=8),
#             customdata=nk,
#             hovertemplate=("<br>"+x_name+" :%{customdata[0]}<br>"+bar_name+" - %{customdata[1]}<br>"+trend_name+":%{customdata[2]}"+"<extra></extra>"),
#         ),
#         secondary_y=True,
#     )
#     # Add traces
#     fig.add_trace(
#         go.Bar(
#             x=x, 
#             y = bar_measure, 
#             name=bar_name, 
#             marker_color=marker_color, 
#             opacity=opacity,
#             hovertemplate=("<br>"+x_name+" :%{customdata[0]}<br>"+bar_name+" - %{customdata[1]}<br>"+trend_name+":%{customdata[2]}"+"<extra></extra>"),
#         ),
#         secondary_y=False,

#     )
#     first_axis_range=[-0.5,bar_measure.max()*1.01]
#     secondary_axis_range=[-0.5,trend_measure.max()*1.01]

#     # Add figure title
#     fig.update_layout(
        
#         title_text=title_text, 
#         showlegend=True,
#         width = width,
#         height= height,
#         xaxis_tickangle=xaxis_tickangle,
#         xaxis_showline=False,
#         xaxis_showgrid=False,
#         yaxis_showline=False,
#         yaxis_showgrid=False,
#         font_family="Segoe UI Semibold",
#         template=template,
#         plot_bgcolor=plot_bgcolor,    #background color (plot)
#         paper_bgcolor=paper_bgcolor,   #background color (around plot)
#         margin=dict(
#                     t=width / 15,
#                     b=width / 20,
#                     r=width / 20,
#                     l=width / 20,
#                 ),
#     )

#     # # Set x-axis title
#     fig.update_xaxes(title_text=x_name)

#     # Set y-axes titles
#     fig.update_yaxes(title_text=bar_name, range = first_axis_range, secondary_y=False)
#     fig.update_yaxes(title_text=trend_name, range = secondary_axis_range, secondary_y=True)  
    
#     return fig


def density_map(df_posts, 
              df_dots, 
              df_topics,
              col_topic, 
              col_engagement, 
              col_text,
              col_text_dots,
              colorscale = "Portland", 
              marker_color = "#ff7f0e",
              arrow_color = "#ff7f0e",
              width=1000, 
              height=1000, 
              show_text=True, 
              show_topics=True,
              show_halo=False,
              show_histogram =True,
              label_size_ratio=100, 
              n_words = 3,
              title_text = "Clustering",
              max_dots_displayed=0,
              max_topics_displayed=20,
              opacity=0.3,
              plot_bgcolor=None, 
              paper_bgcolor=None, 
              template = "plotly"):
    """
    Display a 2Dhistogram with contours :
    - df_posts : dataframe containing all data points to plot (corresponding to contours)
    - df_dots : dataframe containing a sample of points to plot as dots
    - df_topics : dataframe containing topics representations
    - col_topic : column name corresponding to category
    - col_engagement : column name corresponding to a metric
    - col_text : column name corresponding to a text separated by | 
    - colorscale : possible values are https://plotly.com/python/builtin-colorscales/
    - marker_color : dots color value
    - arrow_color : arrow pointing to topic centroid color value
    - width / height = size of plot
    - show_text : show dots
    - show_topic : show topics labels
    - show_halo : show circles around topics
    - show_histogram : show 2Dhistogram with contours
    - label_size_ratio : influence the size of the topics labels, higher value means smaller topics labels
    - n_words : number of words to display (words should be separated by | in col_text)
    - title_text = graph title
    - max_dots_displayed : number of dots to display,
    - max_topics_displayed : number of topics to display
    - opacity : opacity of dots
    """  

    # df_topics = df_distrib_sample.copy()
    df_topics= df_topics.dropna(subset=col_text)
    df_topics['text_bunka']= df_topics[col_text].apply(lambda x : "|".join(x.split('|')[:n_words]))
    

    if (max_topics_displayed>0) and (max_topics_displayed < len(df_topics[col_topic].unique())):
        df_topics= df_topics.sample(max_topics_displayed)

    #on  crée l'histogramme principal
    if show_histogram:
        fig_density = go.Figure(
                go.Histogram2dContour(
                    x=df_posts['x'],
                    y=df_posts['y'],
                    colorscale=colorscale,
                    showscale=False,
                    hoverinfo="none"
                )
            )
    else : 
        fig_density = go.Figure()

    #paramètre des contours
    fig_density.update_traces(
        contours_coloring="fill", contours_showlabels=False
    )

    #paramètres cosmetiques
    fig_density.update_layout(
                font_size=25,
                width=width,
                height=height,
                margin=dict(
                    t=width / 15,
                    b=width / 25,
                    r=width / 25,
                    l=width / 25,
                ),
                title=dict(text=title_text, font=dict(size=width / 40)),
                xaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False),
                yaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=False),
            )

    # création de la légende de chaque points
    nk = np.empty(shape=(len(df_dots), 3, 1), dtype="object")
    nk[:, 0] = np.array(df_dots[col_topic]).reshape(-1, 1)
    nk[:, 1] = np.array(df_dots[col_text_dots].apply(lambda txt: '<br>'.join(textwrap.wrap(txt, width=50)))).reshape(-1, 1)
    nk[:, 2] = np.array(df_dots[col_engagement]).reshape(-1, 1)

    # ajout des points
    if show_text:
        fig_density.add_trace(
            go.Scatter(
                x=df_dots['x'],
                y=df_dots['y'],
                mode="markers",
                marker=dict(opacity=opacity, 
                            color=marker_color, 
                            maxdisplayed=max_dots_displayed
                            ),
                customdata=nk,
                hovertemplate=("<br>%{customdata[1]}<br>Engagements: %{customdata[2]}"+"<extra></extra>"),
                name="",
                
            )
        )

    if show_topics:
        # Afficher les topics
        for i, row in df_topics.iterrows():
            fig_density.add_annotation(
                x=row['topic_x'],
                y=row['topic_y'],
                # text="|".join(row['top_keywords'].split('|')[:n_words]),
                text=str(row['text_bunka']),
                showarrow=True,
                arrowhead=1,
                font=dict(
                    family="Segoe UI Semibold",
                    size=width / label_size_ratio,
                    color="blue",
                ),
                bordercolor="#c7c7c7",
                borderwidth=width / 1000,
                borderpad=width / 500,
                bgcolor="white",
                opacity=1,
                arrowcolor=arrow_color,
            )
    if show_halo:
        for i, row in df_posts.groupby(col_topic):
            x_hull, y_hull = get_convex_hull_coord(np.array(row[['x','y']]))
                
            # Create a Scatter plot with the convex hull coordinates
            trace = go.Scatter(
                x=x_hull,
                y=y_hull,
                mode="lines",
                name="Convex Hull",
                line=dict(color="grey", dash="dot"),
                hoverinfo="none",
            )
            fig_density.add_trace(trace)

    fig_density.update_layout(showlegend=False, 
                              width=width, 
                              height=height, 
                              template=template,
                              plot_bgcolor=plot_bgcolor,    #background color (plot)
                              paper_bgcolor=paper_bgcolor,   #background color (around plot)
                            )


    return fig_density



def topic_heatmap(df, col_x = "topic_x", col_y = "topic_y", col_topic = "soft_topic", color_continuous_scale='GnBu', title ="Similarity between topics"):
    """
    
    """

    distance_matrix = cosine_similarity(np.array(df[[col_x,col_y]]))

    fig = px.imshow(distance_matrix,
                        labels=dict(color="Similarity Score"),
                        x=df[col_topic].astype(int).sort_values().astype(str),
                        y=df[col_topic].astype(int).sort_values().astype(str),
                        color_continuous_scale=color_continuous_scale
                        )

    fig.update_layout(
        title={
            'text': title,
            'y': .95,
            'x': 0.55,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=22,
                color="Black")
        },
        width=1000,
        height=1000,
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
    )
    fig.update_layout(showlegend=True)
    fig.update_layout(legend_title_text='Trend')
    return fig

def generate_wordcloud(df, col_word, col_metric, width=3000, height=1500, dpi=300, background_color='white', font_path = "font/SEGUIEMJ.TTF", colormap="Viridis", show=False):
    
    top_n_words={row[col_word]:row[col_metric] for i,row in df.iterrows()}
    
    # Generate a wordcloud of the top n words
    wordcloud = WordCloud(width=width, height=height, background_color=background_color, font_path = font_path, colormap = colormap, prefer_horizontal=1).generate_from_frequencies(top_n_words)
    if show : 
        plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    return wordcloud



def create_radar(df, col_topic, col_metrics, title="Radar", opacity=0.6, width = 1000, height= 1000, template = "ggplot2" , plot_bgcolor=None, paper_bgcolor=None):

    df = df[[col_topic] + col_metrics]
    col_metrics.append(col_metrics[0])

    fig = go.Figure()
    for topic in list(df[col_topic].unique()) :

        data = df[df[col_topic]==topic].drop(columns=[col_topic]).values.tolist()[0]
        data.append(data[0])
        fig.add_trace(
            go.Scatterpolar(
                r=data,
                theta=col_metrics,
                fill="toself",
                fillcolor=None,
                name=topic,
                opacity=opacity            
                )
            )

    fig.update_layout(
        polar=dict(
                    angularaxis_showgrid=False,   # remove the axis
                    radialaxis=dict(
                    gridwidth=0,
                    gridcolor=None,
                    tickmode='array',  # Set tick mode to 'array'
                    tickvals=[0, 2, 4, 6, 8, 10],  # Specify tick values
                    showticklabels=True,  # Show tick labels
                    visible=True,
                    range=[0, 10],
                ),
                gridshape='linear',
                # bgcolor="white",
                ),
        showlegend=True,
        font_family="Segoe UI Semibold",
        font_color="SlateGrey",
        title=title,             
        width=width,                  #plot size
        height=height,                #plot size
        plot_bgcolor=plot_bgcolor,    #background color (plot)
        paper_bgcolor=paper_bgcolor,   #background color (around plot)
        template=template,
        margin=dict(l=100, r=100, t=100, b=100)
    )


    return fig

def bar_subplots(df, col_x, col_y, col_cat, color_palette, n_cols=4, n_top_words = 20, horizontal_spacing = 0.2, vertical_spacing = 0.08, textposition=None, color = None, title =  "Top words per topic", template = "plotly", bargap = 0.4,  width = 500, height = 35, plot_bgcolor=None, paper_bgcolor=None, showlegend = True):
    
    categories = df[col_cat].unique()

    # user define a number of columns, we compute the number of rows requires
    n_rows =  math.ceil(len(categories) / n_cols)

    # fine tune parameter according to the text position provided
    if textposition == 'inside':
        horizontal_spacing = (horizontal_spacing / n_cols)/2
    else:
        horizontal_spacing = (horizontal_spacing / n_cols)
        
    # create subplots
    fig = make_subplots(
        rows = n_rows,                           # number of rows
        cols = n_cols,                           # number of columns
        subplot_titles = list(categories),       # title for each subplot
        vertical_spacing = vertical_spacing / n_rows,     # space between subplots
        horizontal_spacing = horizontal_spacing  # space between subplots
        )

    # create bar traces for each subplot
    row_id = 0
    col_id = 0
    for i, category in enumerate(categories):
        
        # define bar color or create a random color
        if color_palette:
            color = color_palette.get(category, generate_random_hexadecimal_color())
        else : 
            if color is None:
                color = generate_random_hexadecimal_color()

        # define row and column position
        col_id +=1 
        if i % n_cols == 0:
            row_id += 1
        if col_id > n_cols:
            col_id = 1

        # select data
        current_df = df[df[col_cat]==category].sort_values(by=col_x, ascending = True)
        hovertemplate='<b>'+current_df[current_df[col_cat]==category][col_y].astype(str)+"</b><br>"+current_df[current_df[col_cat]==category][col_x].astype(str)

        if textposition == 'inside':
            showticklabels = False
            text=current_df[col_y].head(n_top_words)
        else:
            showticklabels = True
            textposition="auto"
            text=None

        fig.add_trace(
            go.Bar(
                x=current_df[col_x].tail(n_top_words), 
                y=current_df[col_y].tail(n_top_words),
                orientation='h',                                # horizontal bars
                name=category,                                  # trace name for legend
                text=text,                                      # text to display
                textposition=textposition,                      # text position
                textangle=0,                                    # text angle
                marker_color = color,                           # bar color
                hovertemplate=hovertemplate+"<extra></extra>"   # hover info
                ),
            row=row_id, 
            col=col_id
            )

    fig.update_layout(
        height = n_rows * n_top_words * height,    # height depending on the number of rows and words to display
        width = n_cols * width,                    # width depending on the number of cols
        bargap = bargap,                           # space between bars
        uniformtext_minsize=7,                     # Adjust the minimum size of text to avoid overlap
        margin=dict(l=75, r=75, t=75, b=50),       # margins around the plot
        showlegend=showlegend,                     # legend display
        font_family="Segoe UI Semibold",           # font
        template=template,                         # template, possible values : plotly, plotly_white, plotly_dark, ggplot2, seaborn, simple_white, none
        plot_bgcolor=plot_bgcolor,                 # background color (plot)
        paper_bgcolor=paper_bgcolor,               # background color (around plot)
        title_text=title                           # viz title
        )

    fig.update_yaxes(
        showticklabels = showticklabels,          # show text near the bars
        showline=False,                           #intermediate lines
        showgrid=False,                           #grid
        zeroline=False,
        )
    fig.update_xaxes(
        showline=False,         #intermediate lines
        showgrid=False,         #grid
        zeroline=False,
        )
    return fig

def pie_subplots(df, col_x, col_y, col_cat, col_color, n_cols=4, horizontal_spacing = 0.2, vertical_spacing = 0.08, title =  "Top words per topic", template = "plotly",  width = 500, height = 150, plot_bgcolor=None, paper_bgcolor=None, showlegend = True):
    
    categories = df[col_cat].unique()

    # user define a number of columns, we compute the number of rows requires
    n_rows =  math.ceil(len(categories) / n_cols)
        
    specs = [[{'type':'domain'}] * n_cols] * n_rows
    # create subplots
    fig = make_subplots(
        rows=n_rows,
        cols=n_cols,
        subplot_titles=list(categories),
        horizontal_spacing=horizontal_spacing / n_cols,
        vertical_spacing=vertical_spacing / n_rows,
        specs=specs
    )

    # create pie chart subplots
    for i, category in enumerate(categories):
        col_id = i % n_cols + 1
        row_id = i // n_cols + 1 

        current_df = df[df[col_cat] == category]
        hovertemplate = '<b>' + current_df[current_df[col_cat] == category][col_y].astype(str) + "</b><br>" + current_df[current_df[col_cat] == category][col_x].astype(str)

        fig.add_trace(
            go.Pie(
            labels=current_df[col_x],
            values=current_df[col_y],
            name=category,
            hole=.4,
            hovertemplate=hovertemplate+"<extra></extra>",
            marker=dict(colors=list(current_df[col_color])),
            sort=False 
            ),
        row=row_id,
        col=col_id,
        )

    # Update layout and axes
    fig.update_layout(
        height=n_rows * height,
        width=n_cols * width,
        uniformtext_minsize=7,
        margin=dict(l=75, r=75, t=75, b=50),
        showlegend=showlegend,
        font_family="Segoe UI Semibold",
        template=template,
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=paper_bgcolor,
        title_text=title
    )
    fig.update_yaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )
    fig.update_xaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )

    return fig


def horizontal_stacked_bars(df, col_x, col_y, col_percentage, col_cat, col_color, title_text = "Sentiment per topic", width=1200, height=1200, xaxis_tickangle=0, horizontal_spacing = 0, vertical_spacing = 0.08, plot_bgcolor=None, paper_bgcolor=None, template = "plotly"):

    categories = df[col_cat].unique()

    n_cols=2
    fig = make_subplots(
        rows = 1,                           # number of rows
        cols = 2,                           # number of columns
        # subplot_titles = list(categories),       # title for each subplot
        vertical_spacing = vertical_spacing,     # space between subplots
        horizontal_spacing = horizontal_spacing / n_cols # space between subplots
        )
    
    for cat in categories:
        current_df = df[df[col_cat] == cat]
        hovertemplate="Catégorie "+current_df[col_y].astype(str)+"<br><b>"+str(cat)+"</b><br>"+current_df[col_x].astype(str)+" "+str(col_x)+"<br>"+current_df[col_percentage].map("{:.1%}".format).astype(str)

        fig.add_trace(
            go.Bar(
                
                x=current_df[col_x], 
                y=current_df[col_y],
                orientation='h',
                # text = current_df[col_x],
                # textposition="inside",
                name=cat, 
                marker=dict(color=current_df[col_color]),
                hovertemplate=hovertemplate+'<extra></extra>',
                textfont_size=14
                ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                
                x=current_df[col_percentage], 
                y=current_df[col_y],
                orientation='h',
                text = current_df[col_percentage].map("{:.1%}".format),
                textposition="inside",
                textangle=0,
                name="",
                marker=dict(color=current_df[col_color]),
                hovertemplate=hovertemplate+'<extra></extra>',
                 showlegend = False
                ),
            row=1,
            col=2,
        )

    fig.update_layout(
            barmode='stack',
            title_text=title_text, 
            showlegend=True,
            width = width,
            height= height,
            xaxis_tickangle=xaxis_tickangle,
            xaxis_showline=False,
            xaxis_showgrid=False,
            yaxis_showline=False,
            yaxis_showgrid=False,
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            font_family="Segoe UI Semibold",
            template=template,
            plot_bgcolor=plot_bgcolor,    #background color (plot)
            paper_bgcolor=paper_bgcolor,   #background color (around plot)

        )
    fig.update_xaxes(title_text=col_x)
    fig.update_yaxes(title_text=col_y, row=1,col=1)
    fig.update_xaxes(title_text=col_x, range=[0,1], tickformat=".0%", row=1,col=2)
    fig.update_yaxes(showticklabels = False, row=1,col=2)
    
    return fig

def bar_trend_per_day(df, col_date, col_metric1, col_metric2,  xaxis_title = "Date", y1_axis_title = "Verbatims", y2_axis_title = "Engagements", title_text = "Trend - couverture & résonance", width = 1500, height = 700, marker_color = "indianred", line_color = "#273746", plot_bgcolor=None, paper_bgcolor=None, template = "plotly"):

    # Plotly Stacked Bar Chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    hovertemplate='<b>Date :</b>'+ df[col_date].astype(str) + '<br><b>'+y1_axis_title+'</b>:'+ df[col_metric1].astype(str)+ '<br><b>'+y2_axis_title+'</b>:'+ df[col_metric2].astype(int).astype(str)

    fig.add_trace(
            go.Bar(
                name=y1_axis_title, 
                x=df[col_date], 
                y=df[col_metric1], 
                marker_color=marker_color, 
                opacity=0.8,
                hovertemplate=hovertemplate+"<extra></extra>"
                ),
            secondary_y=False,
        )       
        
    fig.add_trace(
            go.Scatter(
                x=df[col_date], 
                y=df[col_metric2], 
                name=y2_axis_title,
                mode='lines', 
                line_color=line_color, 
                line_width=2,
                hovertemplate=hovertemplate+"<extra></extra>"            
                ),
            secondary_y=True,
        )

    first_axis_range=[-0.5,df[col_metric1].max()*1.01]
    secondary_axis_range=[-0.5,df[col_metric2].max()*1.01]
    # Change the layout if necessary
    fig.update_layout(
        barmode='stack',
        xaxis_title=xaxis_title, 
        width = width,
        height = height,
        title_text=title_text, 
        showlegend=True,
        xaxis_tickangle=0,
        xaxis_showline=False,
        xaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_showgrid=False,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        font_family="Segoe UI Semibold",
        template=template,
        plot_bgcolor=plot_bgcolor,    #background color (plot)
        paper_bgcolor=paper_bgcolor,   #background color (around plot)
        )

                    
    fig.update_yaxes(title_text=y1_axis_title, range=first_axis_range, secondary_y=False)
    fig.update_yaxes(title_text=y2_axis_title, range = secondary_axis_range, secondary_y=True) 
    fig.update_yaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )
    fig.update_xaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    ) 

    return fig

def bar_trend_per_day_per_cat(df, col_date, col_cat, col_metric1, col_metric2, col_color, xaxis_title = "Date", y1_axis_title = "Verbatims", y2_axis_title = "Engagements", title_text = "Trend - couverture & résonance", vertical_spacing = 0.1, width = 1500, height = 700, marker_color = "indianred", line_color = "#273746", plot_bgcolor=None, paper_bgcolor=None, template = "plotly"):

    fig = make_subplots(
        rows = 2,                           # number of rows
        cols = 1,                           # number of columns
        vertical_spacing = vertical_spacing,     # space between subplots
    )

    categories = df[col_cat].unique()
    for cat in categories:
        current_df = df[df[col_cat] == cat]
    
        hovertemplate='<b>Categorie : </b>'+str(cat)+'<br><b>Date : </b>'+ current_df[col_date].astype(str) + '<br><b>'+y1_axis_title+'</b> : '+ current_df[col_metric1].astype(str)+' ('+current_df["per_"+col_metric1].map("{:.1%}".format).astype(str)+')' +'<br><b>'+y2_axis_title+'</b> : '+ current_df[col_metric2].astype(int).astype(str)+' ('+current_df["per_"+col_metric2].map("{:.1%}".format).astype(str)+')'

        fig.add_trace(
            go.Bar(
                x=current_df[col_date], 
                y=current_df[col_metric1],
                orientation='v',
                name=cat, 
                marker=dict(color=current_df[col_color]),
                hovertemplate=hovertemplate+'<extra></extra>',
                textfont_size=14,
                legendgroup=cat
                ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                
                x=current_df[col_date], 
                y=current_df[col_metric2],
                orientation='v',
                name="",
                marker=dict(color=current_df[col_color]),
                hovertemplate=hovertemplate+'<extra></extra>',
                showlegend = False,
                legendgroup=cat
                ),
            row=2,
            col=1,
        )

    fig.update_layout(
            barmode='stack',
            title_text=title_text, 
            showlegend=True,
            width = width,
            height= height,
            xaxis_tickangle=0,
            xaxis_showline=False,
            xaxis_showgrid=False,
            yaxis_showline=False,
            yaxis_showgrid=False,
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            font_family="Segoe UI Semibold",
            template=template,
            plot_bgcolor=plot_bgcolor,    #background color (plot)
            paper_bgcolor=paper_bgcolor,   #background color (around plot)
            legend_tracegroupgap=0

        )
    fig.update_xaxes(showticklabels = False, row=1,col=1)
    fig.update_xaxes(title_text=xaxis_title, row=2,col=1)
    fig.update_yaxes(title_text=y1_axis_title, row=1,col=1)
    fig.update_yaxes(title_text=y2_axis_title, row=2,col=1)
    fig.update_yaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )
    fig.update_xaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )

    return fig

def pie(df, col_x, col_y, col_color, title =  "Sentiment", template = "plotly",  width = 1000, height = 1000, plot_bgcolor=None, paper_bgcolor=None, showlegend = True):
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df[col_x],
        values=df[col_y],
        name="",
        hole=.4,
        hovertemplate='<b>'+ df[col_x].astype(str) +"</b><br>"+ str(col_y) + " : "+df[col_y].astype(str) + "<extra></extra>",
        marker=dict(colors=list(df[col_color])),
        textfont_size = 18,
        sort=False 
        ),
    )

    # Update layout and axes
    fig.update_layout(
        height=height,
        width=width,
        uniformtext_minsize=7,
        margin=dict(l=75, r=75, t=75, b=50),
        showlegend=showlegend,
        font_family="Segoe UI Semibold",
        template=template,
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=paper_bgcolor,
        title_text=title
    )
    fig.update_yaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )
    fig.update_xaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )
    return fig

def bar(df, x, y, color="indianred", xaxis_title="x", yaxis_title="y", width=1200, height = 700, title_text="", plot_bgcolor=None, paper_bgcolor=None, template = "plotly", showlegend=True):

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
                x=df[x], 
                y=df[y],
                orientation='v',
                name=yaxis_title, 
                marker=dict(color=color),
                hovertemplate = str(x) +" : "+df[x].astype(str)+"<br>"+str(y)+" : "+df[y].astype(str)+'<extra></extra>'
        )

    )
    fig.update_traces(marker_color=color)
    fig.update_layout(
        title=title_text, 
        xaxis_title=xaxis_title, 
        yaxis_title=yaxis_title,
        title_text=title_text, 
        showlegend=showlegend,
        width = width,
        height= height,
        xaxis_tickangle=0,
        xaxis_showline=False,
        xaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_showgrid=False,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        font_family="Segoe UI Semibold",
        template=template,
        plot_bgcolor=plot_bgcolor,    #background color (plot)
        paper_bgcolor=paper_bgcolor,   #background color (around plot)
        )
    return fig


def add_horizontal_line(fig, y, line_color = "gray", line_width = 1.5, line_dash = "dash", annotation_text = "Longueur moyenne des textes", annotation_position = "top right"):
    fig.add_hline(
        y=y, 
        line_width=line_width, 
        line_dash=line_dash, 
        line_color=line_color,
        annotation_text=annotation_text, 
        annotation_position=annotation_position
        )
    return fig

def add_vertical_line(fig, x, line_color = "gray", line_width = 1.5, line_dash = "dash", annotation_text = "Longueur moyenne des textes", annotation_position = "top right"):
    fig.add_vline(
        x=x, 
        line_width=line_width, 
        line_dash=line_dash, 
        line_color=line_color,
        annotation_text=annotation_text, 
        annotation_position=annotation_position
        )
    return fig

def network_graph(T, col_size="scaled_size", col_color="modularity_color",  title_text = "Analyse de similitudes", sample_nodes = 0.15, show_edges=True, show_halo=False, textposition=None, line_color = "#B7B7B7", line_dash="dot", edge_mode = "lines+markers", node_mode="markers+text", opacity=0.2, width=1600, height=1200, plot_bgcolor=None, paper_bgcolor=None, template="plotly"):
    
    
    # on construit un dataframe des noeuds à partir des données du graphe pour plus de simplicité
    df_nodes=pd.DataFrame()
    for node in T.nodes(data=True):
        df_nodes_tmp=pd.json_normalize(node[1])
        df_nodes_tmp['node']=node[0]
        df_nodes=pd.concat([df_nodes, df_nodes_tmp])
    df_nodes[['x','y']]=df_nodes['pos'].apply(pd.Series)
    df_nodes = df_nodes.sort_values(by=col_size, ascending=False).reset_index(drop=True)

    # on conserve les labels pour seulement un échantillon de noeuds
    df_sample = sample_most_engaging_posts(df_nodes, "modularity", col_size, sample_size= sample_nodes, min_size=3)

    for index, row in df_nodes.iterrows():
        if row['node'] in df_sample['node'].values:
            df_nodes.at[index, 'node_label'] = row['node']
        else:
            df_nodes.at[index, 'node_label'] = ''
    
    fig = go.Figure()
    # on crée nos liens
    if show_edges:
        for edge in T.edges(data=True):
            x0, y0 = T.nodes[edge[0]]['pos']
            x1, y1 = T.nodes[edge[1]]['pos']

            fig.add_trace(
                go.Scatter(
                    x = tuple([x0, x1, None]),
                    y = tuple([y0, y1, None]),
                    line_width = edge[2]['scaled_weight'],
                    line_color = line_color,
                    mode=edge_mode,
                    line_dash=line_dash,
                    name="",
                    hoverinfo='skip',
                )
            )

    # on affiche éventuellement les halo
    if show_halo:
        for i, row in df_nodes.groupby("modularity"):
            try:
                x_hull, y_hull = get_convex_hull_coord(np.array(row[['x','y']]))
                hull_color = row[col_color].iloc[0]
                # Create a Scatter plot with the convex hull coordinates
                fig.add_trace( 
                    go.Scatter(
                        x=x_hull,
                        y=y_hull,
                        mode="lines",
                        fill="toself",
                        fillcolor=hull_color,
                        opacity=0.1,
                        name="Convex Hull",
                        line=dict(color="grey", dash="dot"),
                        hoverinfo="none",
                    )
                )
            except:
                pass

    # on affiche nos noeuds
    for i, row in df_nodes.iterrows():
        fig.add_trace(
            go.Scatter(
                x = [row['x']],
                y = [row['y']],
                mode=node_mode,
                marker_opacity=opacity,
                marker_size=row[col_size],
                marker_color= row[col_color],
                marker_sizemode='area',
                marker_sizemin = 8,
                textposition=textposition,
                text = row['node_label'],
                textfont_size=row[col_size],
                textfont_color=row[col_color],
                hovertemplate='<b>'+str(row['node'])+'</b><br>Modularity :'+str(row["modularity"])+'</b><br>Frequency :'+str(row["size"])+'</b><br>Eigenvector Centrality : '+str(round(row["eigenvector_centrality"],3))+'</b><br>Degree Centrality : '+str(round(row["degree_centrality"],3))+'</b><br>Betweenness Centrality : '+str(round(row["betweenness_centrality"],3))+"<extra></extra>"
            )
        )

    fig.update_layout(
            width=width,
            height=height,
            showlegend=False,
            hovermode='closest',
            title=title_text,
            titlefont_size=18,
            font_family="Segoe UI Semibold",
            # font_size = 12,
            # uniformtext_minsize=8,
            template=template,
            plot_bgcolor=plot_bgcolor,
            paper_bgcolor = paper_bgcolor,
            
            xaxis=dict(
                showgrid=False, 
                showline=False,                           #intermediate lines
                zeroline=False,
                showticklabels=False, 
                mirror=False
                ),
            yaxis=dict(
                showgrid=False, 
                showline=False,                           #intermediate lines
                zeroline=False,
                showticklabels=False, 
                mirror=False
                ))
    
    return fig

def richesse_lexicale(df, title= "Richesse lexicale", width=1200, height=1000, template="plotly"):
    df = create_frequency_table(df, "freq")
    fig_richesse = go.Figure()
    fig_richesse.add_trace(
            go.Scatter(
                x=df['rank'],
                y=df['freq'], 
                # marker_color=generate_random_hexadecimal_color(),
                mode='markers', 
                name="",
                hovertemplate = 'rank : '+df["rank"].astype(str)+'<br>'+'<b>word : '+df["word"].astype(str)+'</b><br>'+'count : '+df["freq"].astype(str)+'<br>')
            ) 
    fig_richesse.update_layout(title=title, 
                            xaxis_title="Rank", 
                            width=width, 
                            height=height,
                            template=template)    
    fig_richesse.update_xaxes(tickformat=".0f", title_text="Rank", type="log")
    fig_richesse.update_yaxes(tickformat=".0f", title_text="Freq", type="log")
    return fig_richesse

def richesse_lexicale_per_topic(df, col_topic, title= "Richesse lexicale par topic", width=1200, height=1000, template="plotly"):
    fig_richesse = go.Figure()
    for topic in list(df[col_topic].unique()):
        df_tmp = create_frequency_table(df[df[col_topic]==topic], "freq")
        fig_richesse.add_trace(
                go.Scatter(
                    x=df_tmp['rank'],
                    y=df_tmp['freq'], 
                    # marker_color=generate_random_hexadecimal_color(),
                    mode='markers', 
                    name=topic,
                    hovertemplate = col_topic+ ' : '+ str(topic)+'<br> rank : '+df_tmp["rank"].astype(str)+'<br>'+'<b>word : '+df_tmp["word"].astype(str)+'</b><br>'+'count : '+df_tmp["freq"].astype(str)+'<br>')
                ) 
        fig_richesse.update_layout(title=title, 
                                xaxis_title="Rank", 
                                width=width, 
                                height=height,
                                template=template)    
        fig_richesse.update_xaxes(tickformat=".0f", title_text="Rank", type="log")
        fig_richesse.update_yaxes(tickformat=".0f", title_text="Freq", type="log")
    return fig_richesse

def subplots_bar_per_day_per_cat(df, col_date, col_cat, metrics, col_color, y_axis_titles, xaxis_title = "Date",title_text = "Trend - couverture & résonance", vertical_spacing = 0.1, width = 1500, height = 700, marker_color = "indianred", line_color = "#273746", plot_bgcolor=None, paper_bgcolor=None, template = "plotly"):

    fig = make_subplots(
        rows = len(metrics),                           # number of rows
        cols = 1,                           # number of columns
        vertical_spacing = vertical_spacing,     # space between subplots
    )

    categories = df[col_cat].unique()
    for cat in categories:
        current_df = df[df[col_cat] == cat]
    
        hovertemplate='<b>Categorie : </b>'+str(cat)+'<br><b>Date : </b>'+ current_df[col_date].astype(str)

        for i, metric in enumerate(metrics):
            hovertemplate +=  '<br><b>'+ metric + " : "+current_df[metric].astype(str) 
            if i==0:
                showlegend = True
            else:
                showlegend = False

            fig.add_trace(
                go.Bar(
                    x=current_df[col_date], 
                    y=current_df[metric],
                    orientation='v',
                    name=cat, 
                    marker=dict(color=current_df[col_color]),
                    hovertemplate=hovertemplate+'<extra></extra>',
                    textfont_size=14,
                    showlegend = showlegend,
                    legendgroup=cat
                    ),
                row = i+1,
                col=1,
            )

    fig.update_layout(
            barmode='stack',
            title_text=title_text, 
            showlegend=True,
            width = width,
            height= height * len(metrics),
            xaxis_tickangle=0,
            xaxis_showline=False,
            xaxis_showgrid=False,
            yaxis_showline=False,
            yaxis_showgrid=False,
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            font_family="Segoe UI Semibold",
            template=template,
            plot_bgcolor=plot_bgcolor,    #background color (plot)
            paper_bgcolor=paper_bgcolor,   #background color (around plot)
            legend_tracegroupgap=0

        )

    for i, title in enumerate(y_axis_titles):
        fig.update_xaxes(title_text=xaxis_title, row=i+1,col=1)

        fig.update_yaxes(title_text=title, row=i+1,col=1)

    fig.update_yaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )
    fig.update_xaxes(
        showline=False,
        showgrid=False,
        zeroline=False
    )

    return fig

    
def add_shape(fig, shape_type = "rect", x0= -1, y0= -1, x1 = 0, y1=0, fillcolor= 'Silver', opacity = 0.1, line_width = 0, line_color = 'white', dash = None, layer = "below"):
    fig.add_shape(
            # Shape for the area between (-1, 0)
            {
                'type': shape_type,
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
                'fillcolor': fillcolor,
                'opacity': opacity,
                "layer": layer,
                'line': {
                    'width': line_width, 
                    "color": line_color,
                    "dash" : dash,
                    },
                
            }
        )
    return fig