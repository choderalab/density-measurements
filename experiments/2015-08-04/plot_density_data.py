#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import xml
import re

# Read the data file.
filename = 'data/T1230.xml' # exported density file

# Find root of dataset XML.
import xml.etree.ElementTree as ET
xml_tree = ET.parse(filename)
xml_root = xml_tree.getroot()

# Process samples
samples = list()

for xml_sample in xml_root.iter('Sample'):
    # Get sample ID.
    xml_sampleid = xml_sample.find('SampleId')
    #print sampleid_xml.tag, sampleid_xml.attrib
    sampleid_text = xml_sampleid.attrib['SampleId1'] # Sample_XXX, where XXX is integer
    sampleid = int(re.match('^Sample_(\d+)$', sampleid_text).groups()[0]) # integer sample index
    print "Sample: %d" % sampleid

    # Get data.
    densities = list()
    for xml_result in xml_sample.findall('ResultResult'):
        if (xml_result.attrib['Title'] == 'Density') and (xml_result.attrib['Unit'][0:4]=='g/cm'):
            # Get result index.
            resultid_text = xml_result.attrib['Name'] # CalculateOnInstrumentX, where X is integer
            resultid = int(re.match('^CalculateOnInstrument(\d+)$', resultid_text).groups()[0]) # integer result index
            # Get density.
            density = float(xml_result.attrib['Value']) # g/cm3
            densities.append(density)
            # Add to pandas dataframe.
            samples.append({ 'sampleid' : sampleid, 'resultid' : resultid, 'density' : density })

# Show dataframe.
df = pd.DataFrame(samples)
print df

# Plot
from matplotlib.backends.backend_pdf import PdfPages
with PdfPages('densities.pdf') as pdf:
    sns.set(style="ticks")
    grid = sns.FacetGrid(df, col="sampleid", hue="sampleid", col_wrap=4, size=1.5)
    grid.map(plt.plot, "resultid", "density", marker="o", ms=3, ls='None')
    grid.set(xticks=[], ylim=(1.02, 1.12))
    grid.fig.tight_layout(w_pad=1)
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

