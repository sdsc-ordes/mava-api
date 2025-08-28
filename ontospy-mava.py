import ontospy
from ontospy.gendocs.viz.viz_html_single import *

g = ontospy.Ontospy("mava-owl.ttl") # => load your ontology

v = HTMLVisualizer(g) # => instantiate the visualization object
v.build() # => render visualization. You can pass an 'output_path' parameter too
v.preview() # => open in browser
