# NetworkX with Bokeh example
import networkx as nx
import pandas as pd

from bokeh.io import output_notebook, output_file, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx

from bokeh.core.validation import silence
from bokeh.core.validation.warnings import EMPTY_LAYOUT

# https://docs.bokeh.org/en/latest/docs/reference/palettes.html
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8, Turbo256, Bokeh, inferno
from bokeh.transform import linear_cmap
from networkx.algorithms import community

def generateGraph(outputDir,dfGraphData,programScope):

    try:
        programName = programScope['program']
        # Load program data
        fileName = programName + '-graph.html'
        graphOutputPath = outputDir + fileName

        sourceColumn = 'domain'
        targetColumn = 'baseurl'
        programColumn = 'program'
    
        G2 = nx.from_pandas_edgelist(df=dfGraphData, source=sourceColumn, target=targetColumn, edge_attr=None)

        # Load communities
        communities = nx.algorithms.community.greedy_modularity_communities(G2)

        # Create empty dictionaries
        modularity_class = {}
        modularity_color = {}
        #Loop through each community in the network
        for community_number, community in enumerate(communities):
        #For each member of the community, add their community number and a distinct color
            for name in community: 
                modularity_class[name] = community_number
                modularity_color[name] = inferno(128)[community_number]
              
        # Add modularity class and color as attributes from the network above
        nx.set_node_attributes(G2, modularity_class, 'modularity_class')
        nx.set_node_attributes(G2, modularity_color, 'modularity_color')

        # Adapted from https://melaniewalsh.github.io/Intro-Cultural-Analytics/Network-Analysis/Making-Network-Viz-with-Bokeh.html

        #Establish which categories will appear when hovering over each node
        HOVER_TOOLTIPS = [("baseurl", "@index")]

        #Create a plot — set dimensions, toolbar, and title
        plot = figure(tooltips = HOVER_TOOLTIPS,
            tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=programName)

        #Create a network graph object with spring layout
        network_graph = from_networkx(G2, nx.spring_layout, scale=10, center=(0, 0))

        color_by_this_attribute = 'modularity_color'
        #Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
        #color_palette = inferno(24)#Turbo256#(30)#Turbo256#Blues8
        color_palette = Turbo256

        #Set node sizes and colors according to node degree (color as category from attribute)
        network_graph.node_renderer.glyph = Circle(size=10, fill_color=color_by_this_attribute)
        #Set node size and color
        #network_graph.node_renderer.glyph = Circle(size=degree, fill_color='skyblue')

        #Set edge opacity and width
        network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

        #Add network graph to the plot
        plot.renderers.append(network_graph)
        plot.sizing_mode = 'scale_both'
        #output_file = fileName
        output_file = fileName
        save(plot, filename=graphOutputPath)
        return "Graph successfully generated."
        
    except:
        return "Graph creation failed."