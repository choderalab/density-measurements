#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import xml
import re

# Read the data file.
filename = 'data/T1230.xml' # exported density file

# Find root of dataset XML.
import xml.etree.ElementTree as ET
xml_tree = ET.parse(filename)
xml_root = xml_tree.getroot()

# Create temperature array for protocol.
temperatures = np.array([i for i in range(20,61)] + [20])

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

# Create pandas dataframe
df = pd.DataFrame(samples, columns=['sampleid', 'resultid', 'temperature', 'density'])
# Sort the dataframe
df = df.sort(['sampleid', 'resultid'], ascending=True)

# Compute resultid to temperature mapping.
resultids = np.unique(df['resultid'])
resultid_to_temperature = dict()
for (resultid, temperature) in zip(resultids, temperatures):
    resultid_to_temperature[resultid] = temperature
df['temperature'] = [resultid_to_temperature[resultid] for resultid in df['resultid']]
print df

density_min = 1.02
density_max = 1.12

# Plot
from matplotlib.backends.backend_pdf import PdfPages
mpl.rcParams.update({'font.size': 4})
with PdfPages('densities.pdf') as pdf:
    sns.set(style="ticks")
    grid = sns.FacetGrid(df, col="sampleid", hue="sampleid", col_wrap=4, size=1.5)
    grid.map(plt.plot, "temperature", "density", marker="o", ms=3, ls='None').set_axis_labels("temperature (C)", "density (g/cm3)")
    grid.set(xticks=[20, 30, 40, 50, 60], xlim=(20, 60), ylim=(density_min, density_max))
    grid.fig.tight_layout(w_pad=1)
    #grid.set(xlabel='temperature (C)', ylabel='density (g/cm$^3$)')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

# Plot density array
# Extract 2D slice
ntemps = len(temperatures)
nsamples = 30
density_array = np.zeros([nsamples,ntemps], np.float64)
for sample_index in range(nsamples):
    print "sample %d / %d" % (sample_index, nsamples)
    for temp_index in range(ntemps):
        temperature = temperatures[temp_index]
        try:
            density_array[sample_index,temp_index] = np.array(df[df.sampleid==sample_index][df.temperature==temperature].density)[0]
        except:
            pass

with PdfPages('densities-oneplot.pdf') as pdf:
    sns.set(style="white")
    sns.set_context("notebook", font_scale=0.5)
    h = sns.heatmap(density_array, vmin=density_min, vmax=density_max, yticklabels=range(30,0,-1), xticklabels=temperatures)
    h.set_xlabel('temperature (C)')
    h.set_ylabel('sample index')

    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
