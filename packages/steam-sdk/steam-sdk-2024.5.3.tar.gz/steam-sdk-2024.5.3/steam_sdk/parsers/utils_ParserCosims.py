import os
from pathlib import Path
from typing import Union

from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.data.DataCoSim import NSTI
from steam_sdk.data.DataModelCosim import DataModelCosim, ParametersToModify
from steam_sdk.data.DataModelCosim import sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE
from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.utils.attribute_model import get_attribute_model, set_attribute_model
from steam_sdk.utils.sgetattr import rsetattr


def write_model_input_files(cosim_data: DataModelCosim,
                            model: Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE],
                            cosim_software: str,
                            data_settings: DataSettings,
                            extra_variables_to_change: ParametersToModify = ParametersToModify(),
                            nsti: NSTI = None,
                            verbose: bool = False):
    '''
    Make all required input files for the selected model. Save them to the COSIM subfolder. Delete temporary files.
    This method does not depend on the software tool
    :param cosim_data TODO
    :param model: Object defining the model information
    :param cosim_software: Name of the software (supported: COSIM, PyCosim)
    :param data_settings: DataSettings object containing all settings, previously read from user specific settings.SYSTEM.yaml file or from a STEAM analysis permanent settings
    :param nsti: NSTI parameters. N=Simulation number, S=Simulation set, T=Time window, I=Iteration
    :type nsti: NSTI
    :param extra_variables_to_change Additional parameters to change. These will be changed AFTER the parameter changes defined by model.variables_to_modify_pre_cosim, model.variables_to_modify_cosim, or model.variables_to_modify_post_cosim
    :param verbose: If True, display information while running
    :return:
    '''
    # Unpack input
    model_data_name = model.modelName
    case_model = model.modelCase
    software = model.type
    simulation_name = model.modelName
    # simulation_number = model.simulationNumber if hasattr(model, 'simulationNumber') else None  # PSPICE netlists don't have number
    # TODO variables_to_change, variables_values should be defined based on a new argmetn 1,2,3... defining whether it's pre-cosim, cosim, or post-cosim
    if nsti.t == 0:  # Before the first time window
        variables_to_change = model.variables_to_modify_pre_cosim.variables_to_change
        variables_values = model.variables_to_modify_pre_cosim.variables_values
    elif nsti.t > len(cosim_data.Settings.Time_Windows.t_0):  # Final simulation after the last time window
        variables_to_change = model.variables_to_modify_post_cosim.variables_to_change
        variables_values = model.variables_to_modify_post_cosim.variables_values
        # for variable in model.variables_to_modify_post_cosim.variables_to_change:
            # if  flag...
            #     variables_to_change = model.variables_to_modify_post_cosim.variables_to_change
            #     variables_values = model.variables_to_modify_post_cosim.variables_values
    else:  # Co-simulation
        variables_to_change = model.variables_to_modify_cosim.variables_to_change
        variables_values = model.variables_to_modify_cosim.variables_values
    # Add extra variables to change
    variables_to_change = variables_to_change + extra_variables_to_change.variables_to_change
    variables_values = variables_values + extra_variables_to_change.variables_values
    library_path = model.modelFolder  # TODO: maybe the following key should be deleted: cosim_data.Folders.path_model_folder
    cosim_name = cosim_data.GeneralParameters.cosim_name
    cosim_number = str(nsti.n)

    # Define folder paths
    if cosim_software == 'COSIM':
        local_cosim_folder = data_settings.local_COSIM_folder
        if software == 'FiQuS':
            raise ValueError(f'FiQuS does not support COSIM. Please use PyCoSim instead')
        elif software == 'LEDET':
            local_folder = os.path.join(local_cosim_folder, cosim_name, cosim_number, 'Input', model.name, 'LEDET')
        elif software == 'PSPICE':
            local_folder = os.path.join(local_cosim_folder, cosim_name, cosim_number, 'Input', model.name)
        if software == 'XYCE':
            local_folder = os.path.join(local_cosim_folder, cosim_name, cosim_number, 'Input', model.name)
    elif cosim_software == 'PyCoSim':
        local_cosim_folder = data_settings.local_PyCoSim_folder
        local_folder_prefix = os.path.join(local_cosim_folder, cosim_name, software)
        if software == 'FiQuS':
            local_folder = os.path.join(local_folder_prefix, model.modelName) # use model set in the input folder name
        elif software == 'LEDET':
            local_folder = os.path.join(local_folder_prefix, str(nsti.n))
        elif software in ['PSPICE', 'XYCE']:
            local_folder = os.path.join(local_folder_prefix, str(nsti.n))  #TODO double check
    else:
         raise Exception(f'Co-simulation software {cosim_software} not supported.')

    # Always assume the STEAM models folder structure, which contains subfolders "circuits", "conductors", "cosims", "magnets"
    file_model_data = os.path.join(library_path, f'{case_model}s', model_data_name, 'input', f'modelData_{model_data_name}.yaml')
    # Make BuilderModel object
    BM = BuilderModel(file_model_data=file_model_data, case_model=case_model, data_settings=data_settings, verbose=verbose)
    # Edit BuilderModel object with the variable changes set in the input file
    if not len(variables_to_change) == len(variables_values):
        raise Exception(f'Variables variables_to_change and variables_values must have the same length.')
    for v, (variable_to_change, value) in enumerate(zip(variables_to_change, variables_values)):
        if verbose:
            print(f'Modify variable {variable_to_change} to value {value}.')
        if 'Conductors[' in variable_to_change:  # Special case when the variable to change is the Conductors key
            if verbose:
                idx_conductor = int(variable_to_change.split('Conductors[')[1].split(']')[0])
                conductor_variable_to_change = variable_to_change.split('].')[1]
                print(f'Variable {variable_to_change} is treated as a Conductors key. Conductor index: #{idx_conductor}. Conductor variable to change: {conductor_variable_to_change}.')

                old_value = get_attribute_model(case_model, BM, conductor_variable_to_change, idx_conductor)
                print(f'Variable {conductor_variable_to_change} changed from {old_value} to {value}.')

                if case_model == 'conductor':
                    rsetattr(BM.conductor_data.Conductors[idx_conductor], conductor_variable_to_change, value)
                elif case_model == 'magnet':
                    rsetattr(BM.model_data.Conductors[idx_conductor], conductor_variable_to_change, value)
                else:
                    raise Exception(f'The selected case {case_model} is incompatible with the variable to change {variable_to_change}.')
        # TODO deal with the case where the entry to change contains "Netlist["
        else:  # Standard case when the variable to change is not the Conductors key
            if verbose:
                old_value = get_attribute_model(case_model, BM, variable_to_change)
                print(f'Variable {variable_to_change} changed from {old_value} to {value}.')
                set_attribute_model(case_model, BM, variable_to_change, value)
    # Write output of the BuilderModel object
    if 'FiQuS' == software:
        if BM.model_data.Options_FiQuS.run.type in ['start_from_yaml', 'solve_with_post_process_python']:
            variable_to_change = 'Options_FiQuS.run.solution'
            value = nsti.n_s_t_i
            set_attribute_model(case_model, BM, variable_to_change, value)
        BM.buildFiQuS(sim_name=model.modelName, sim_number=f'_{nsti.n_s_t_i}', output_path=local_folder,
                      flag_plot_all=False, verbose=False)  # flag_plot_all, verbose all hard-coded to False to avoid unwanted plots, and logging info
    elif 'LEDET' == software:
        sim_number = nsti.n if cosim_software == 'COSIM' else f'_{nsti.n_s_t_i}'
        # Write LEDET model
        local_model_folder = str(Path(Path(local_folder) / simulation_name / 'Input').resolve())
        field_maps_folder = Path(Path(local_folder) / '..' / 'Field maps' / simulation_name).resolve()  # The map2d files are written in a subfolder {simulation_name} inside a folder "Field maps" at the same level as the LEDET folder [this structure is hard-coded in STEAM-LEDET]
        BM.buildLEDET(sim_name=simulation_name, sim_number=sim_number,  # TODO edit nsti.n
                      output_path=local_model_folder, output_path_field_maps=field_maps_folder,
                      flag_json=False, flag_plot_all=False, verbose=False)  # flag_json, flag_plot_all, verbose all hard-coded to False to avoid unwanted files, plots, and logging info
    elif 'PSPICE' == software:
        # Write PSPICE model
        local_model_folder = str(Path(local_folder).resolve())
        BM.buildPSPICE(sim_name=simulation_name, sim_number='', output_path=local_model_folder, verbose=verbose)
    elif 'XYCE' == software:
        raise Exception(f'Writing of {software} models not yet supported within ParserCOSIM.')
    else:
        raise Exception(f'Writing of {software} models not yet supported within ParserCOSIM.')
