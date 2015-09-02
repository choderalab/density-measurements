import yaml
import numpy as np


def make_mixture_parameters(param_dict):
    """
    This uses an input dictionary with two molecular weights and
    number of data points to create evenly spaced mole fractions
    
    Arguments
    ---------
    param_dict : dict
        Dictionary of parameters. Usually from a yaml file
    
    Returns
    ------
    mass_list : n_compounds x n_mixtures numpy array
        Contains the masses to dispense for each compound
    """
    compound1 = param_dict['compound1_name']
    compound2 = param_dict['compound2_name']
    compound1_mw = param_dict[compound1]['mw']
    compound2_mw = param_dict[compound2]['mw']
    n_fractions = param_dict['n_fractions']
    compound1_frac_range = np.linspace(0,1,n_fractions)
    total_mass = param_dict['total_mass'] #grams
    output_mass = {}
    output_mass[compound1] = np.zeros(n_fractions)
    output_mass[compound2] = np.zeros(n_fractions) 
    compound_mw_array = np.array([compound1_mw, compound2_mw])
    for i, frac in enumerate(compound1_frac_range):
        fractions = np.linalg.solve([compound_mw_array,[1.0-frac, -1.0*frac]],[10, 0])
        output_mass[compound1][i] = fractions[0]*compound1_mw
        output_mass[compound2][i] = fractions[1]*compound2_mw
    return output_mass

def _calculate_mole_fraction(mol1, mol2):
    """convenience function to calculate mole fractions"""
    return mol1/(mol1+mol2)

def verify_output_parameters(parm_dict, output_mass):
    """
    This method checks that the output produces less than 14g,
    and prints the fraction of each compound
    """
    #hardcoded 30 fractions
    compound1 = parm_dict['compound1_name']
    compound2 = parm_dict['compound2_name']
    for i in range(30):
        mole_fraction_1 = _calculate_mole_fraction(output_mass[compound1][i], output_mass[compound2][i])
        mole_fraction_2 = 1.0 - mole_fraction_1
        print("%s:%f %s:%f total mass:%f" %(compound1, mole_fraction_1, compound2, mole_fraction_2, output_mass[compound1][i]+output_mass[compound2][i]))
    return

def _test_make_mixture():
    param_dict = {}
    param_dict['compound1_name'] = 'DMSO'
    param_dict['DMSO']={'mw' : 75.0}
    param_dict['compound2_name'] = 'H2O'
    param_dict['H2O'] = {'mw':18.0}
    output = make_mixture_parameters(param_dict)
    verify_output_parameters(param_dict, output)
    return

if __name__=="__main__":
    import sys
    fname = sys.argv[1]
    yaml_file = open(fname,'r')
    param_dict = yaml.load(yaml_file)
    yaml_file.close()
    output_masses = make_mixture_parameters(param_dict)
    compound1 = param_dict['compound1_name']
    compound2 = param_dict['compound2_name']
    if param_dict['output_filename']:
        output_file = open(param_dict['output_filename'],'w')
    else:
	output_file = open('density_measurement_masses.txt','w')
    output_file.write("%s,%s\n" % (compound1, compound2))
    for i in range(param_dict['n_fractions']):
        output_file.write("%f,%f\n" % (output_masses[compound1][i], output_masses[compound2][i]))
    output_file.close()
