import os
import shutil
from pathlib import Path
from typing import Union, List

import numpy as np
from scipy.interpolate import interp1d

from steam_sdk.data.DataCoSim import NSTI
from steam_sdk.data.DataFiQuS import DataFiQuS
from steam_sdk.data.DataModelCircuit import DataModelCircuit
from steam_sdk.data.DataModelConductor import DataModelConductor
from steam_sdk.data.DataModelCosim import sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE, sim_Generic, FileToCopy, VariableToCopy, ParametersToModify
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from steam_sdk.data.DataPyCoSim import DataPyCoSim
from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.drivers.DriverFiQuS import DriverFiQuS
from steam_sdk.drivers.DriverLEDET import DriverLEDET
from steam_sdk.drivers.DriverPSPICE import DriverPSPICE
from steam_sdk.drivers.DriverXYCE import DriverXYCE
from steam_sdk.parsers.ParserFile import get_signals_from_file
from steam_sdk.parsers.ParserYAML import yaml_to_data
from steam_sdk.parsers.utils_ParserCosims import write_model_input_files
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.rgetattr import rgetattr


class CosimPyCoSim:
    """
        Class to run a co-operative simulation
    """

    def __init__(self,
                 file_model_data: str,
                 sim_number: int,
                 data_settings: DataSettings = None,
                 verbose: bool = False
                 ):
        """
            Builder object to generate models from STEAM simulation tools specified by user

            file_model_data: path to folder with input data (DataPyCoSim yaml input file)
            sim_number: number of the simulation
            :param data_settings: DataSettings object containing all settings, previously read from user specific settings.SYSTEM.yaml file or from a STEAM analysis permanent settings
            verbose: to display internal processes (output of status & error messages) for troubleshooting

            Notes:
            The PyCoSim folder structure will be as follows:
            - local_PyCoSim is the main folder
              - COSIM_NAME
                - SOFTWARE_FOLDER
                  - SIMULATION_NAME
                    - {COSIM_NUMBER}_{SIMULATION_NUMBER}_{TIME_WINDOW_NUMBER}_{ITERATION_NUMBER}

            Example 1:
            - C:\local_PyCoSim
              - RQX
                - LEDET
                  - MQXA
                    - Field Maps
                    - 55_1_1_1\LEDET\Input
                  - MQXA
                    - 55_2_1_1
                  - MQXB
                    - 55_1_1_1
                  - MQXB
                    - 55_2_1_1

            Example 1:
            - C:\local_PyCoSim
              - RQX
                - FiQuS
                  - MQXA
                    - G1
                      - M1
                        - 55_1_1_1
                - LEDET
                  - MQXB
                    - Field Maps
                    - 55
                     - 1_1_1\LEDET\Input
                - PSPICE
                  - RQX_cosim
                    - 55_1_1_1

            D:\library_mesh

        """
        # Load data from input file
        self.cosim_data: DataPyCoSim = yaml_to_data(file_model_data, DataPyCoSim)
        self.local_PyCoSim_folder = Path(data_settings.local_PyCoSim_folder).resolve()
        self.sim_number = sim_number
        self.data_settings = data_settings
        self.verbose = verbose
        self.summary = {}  # This will be populated with a summary of simulation results (mainly used ofr DAKOTA)

        # Initialize the dictionary that will be used to pass variable values from an output file to a model data object
        self._reset_variables_to_pass()

        # Initialize the dictionary that will be used to check convergence at each time window
        self.dict_convergence_variables = {key: {} for key in self.cosim_data.Simulations}  # Assign empty list to all models

        if verbose:
            print(f'PyCoSim initialized with input file {file_model_data}.')
            print(f'Local PyCoSim folder is {self.local_PyCoSim_folder}')

    def run(self):
        """
        This runs co-sim
        """
        # Read initial
        # A1 Make the folder structure
        # A2 Make the input files for the pre-run simulation
        # A3 Run the pre-run input files
        # B Start a while loop with some convergence criteria
        #   B0 If present, check output to see if convergence is met
        #   B1 Make new folders
        #   B2 Make new input files using output of previous simulation
        #   B3 Run the new input files
        # C1 Make the folder structure for the final run
        # C2 Make the input files for the final-run simulation
        # C3 Run the final-run input files

        if self.verbose: print(f'Co-simulation {self.cosim_data.GeneralParameters.cosim_name} {self.sim_number} started.')
        self.nsti = NSTI(self.sim_number, 0, 0, 0)

        # Pre-cosim
        for model_set, model in enumerate(self.cosim_data.Simulations.values()):
            self.nsti.update(self.sim_number, model_set, 0, 0)  # Initial time window and iteration  # cosim_nsti --> N=Simulation number. S=Simulation set. T=Time window. I=Iteration.
            # TODO Pass input/output
            # if flag_run_precosim...
            if model.flag_run_pre_cosim:
                if self.verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Pre-cosim simulation.')

                write_model_input_files(cosim_data=self.cosim_data, model=model,
                                        cosim_software='PyCoSim', data_settings=self.data_settings,
                                        extra_variables_to_change=self.variables_to_pass[model.name]['variables_to_modify_pre_cosim'],
                                        nsti=self.nsti, verbose=self.verbose)
                self._run_sim(model=model)
                # TODO add some basic check that the simulation run without errors
                self._copy_files(model=model)
                self._copy_variables(model=model, verbose=self.verbose)

        # Co-simulation
        # Loop through time windows
        for tw, time_wind in enumerate(self.cosim_data.Settings.Time_Windows):
            # Reset convergence variables
            flag_converge, list_flag_converge, current_iteration = False, [], 0
            # Reset the dictionary that is used to pass variable values from an output file to a model data object TODO how to pass info from one time window to the next?
            self._reset_variables_to_pass()
            # Loop until convergence is found
            while flag_converge == False:
                for model_set, model in enumerate(self.cosim_data.Simulations.values()):
                    self.nsti.update(self.sim_number, model_set, tw + 1, current_iteration)
                    # Make model
                    if model.flag_run_cosim:
                        if self.verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Time window {self.nsti.t}. Iteration {self.nsti.i}.')
                        write_model_input_files(cosim_data=self.cosim_data, model=model,
                                                cosim_software='PyCoSim', data_settings=self.data_settings,
                                                extra_variables_to_change=self.variables_to_pass[model.name]['variables_to_modify_cosim'],
                                                nsti=self.nsti, verbose=self.verbose)
                        self._run_sim(model=model)
                        # TODO add some basic check that the simulation run without errors
                        self._copy_files(model=model)
                        self._copy_variables(model=model, verbose=self.verbose)

                        # Check convergence
                        list_flag_converge.append(self._check_convergence(model=model))

                flag_converge = all(list_flag_converge)
                if not flag_converge:
                    current_iteration = current_iteration + 1

        # Post-cosim
        # TODO how to pass info from the last time window to the post-cosim?
        for model_set, model in enumerate(self.cosim_data.Simulations.values()):
            self.nsti.update(self.sim_number, model_set, len(self.cosim_data.Settings.Time_Windows.t_0) + 1, 0)
            if model.flag_run_post_cosim:
                if self.verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Post-cosim simulation.')
                # Make model
                write_model_input_files(cosim_data=self.cosim_data, model=model,
                                        cosim_software='PyCoSim', data_settings=self.data_settings,
                                        extra_variables_to_change=self.variables_to_pass[model.name]['variables_to_modify_post_cosim'],
                                        nsti=self.nsti, verbose=self.verbose)
                # Run model
                self._run_sim(model=model)
                # TODO add some basic check that the simulation run without errors
                self._copy_files(model=model)
                self._copy_variables(model=model, verbose=self.verbose)

        if self.verbose: print(f'Co-simulation {self.cosim_data.GeneralParameters.cosim_name} {self.sim_number} finished.')


    def _run_sim(self, model: Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        """
        Run selected simulation.
        The function applies a different logic for each simulation software.
        """

        # Define local folder
        local_folder = self.__find_local_target_folder(model=model)

        # Run simulation
        if model.type == 'FiQuS':
            dFiQuS = DriverFiQuS(path_folder_FiQuS_input=local_folder, path_folder_FiQuS_output=local_folder,
                                 FiQuS_path=self.data_settings.FiQuS_path, GetDP_path=self.data_settings.GetDP_path, verbose=self.verbose)
            self.summary[model.name] = dFiQuS.run_FiQuS(sim_file_name=f'{model.modelName}_{self.nsti.n_s_t_i}_FiQuS')
        elif model.type == 'LEDET':
            dLEDET = DriverLEDET(path_exe=self.data_settings.LEDET_path, path_folder_LEDET=os.path.dirname(local_folder), verbose=self.verbose)  # Note: os.path.dirname() needed because DriverLEDET will add nameMagnet to the simulation path already
            sim_result = dLEDET.run_LEDET(nameMagnet=model.modelName, simsToRun=self.nsti.n_s_t_i, simFileType='.yaml')  # simFileType is hard-coded
            # if sim_result == 0:
            #     raise Exception(f'Error when running LEDET! Executable: {self.data_settings.LEDET_path}. LEDET local folder {local_folder}. ')
        elif model.type == 'PSPICE':
            dPSPICE = DriverPSPICE(path_exe=self.data_settings.PSPICE_path, path_folder_PSPICE=local_folder, verbose=self.verbose)
            dPSPICE.run_PSPICE(nameCircuit=model.modelName, suffix='')
        elif model.type == 'XYCE':
            dXYCE = DriverXYCE(path_exe=self.data_settings.XYCE_path, path_folder_XYCE=local_folder, verbose=self.verbose)
            dXYCE.run_XYCE(nameCircuit=model.modelName, suffix='')
        else:
            raise Exception(f'Software {model.type} not supported for automated running.')


    def _copy_files(self, model: Union[sim_Generic, sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        '''
        This function copies files across from the output of one model to another.
        :param model:
        :param verbose: If True, display additional logging info
        :return:
        '''

        # Get list of files to copy, which depends on the current co-simulation state
        if self.nsti.t == 0:
            files_to_copy: List[FileToCopy] = model.files_to_copy_after.pre_cosim
        elif self.nsti.t > len(self.cosim_data.Settings.Time_Windows.t_0):
            files_to_copy: List[FileToCopy] = model.files_to_copy_after.post_cosim
        else:
            files_to_copy: List[FileToCopy] = model.files_to_copy_after.cosim

        if len(files_to_copy) > 0:
            # Define local folder
            local_folder = self.__find_local_source_folder(model=model)

            # Copy files
            for file_to_copy in files_to_copy:
                # Check whether to add an NSTI suffix between the base name and the extension of the old file name. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number
                old_file_name_relative_path = self._add_nsti_to_file_name(file_to_copy.old_file_name_relative_path, nsti=self.nsti) if file_to_copy.flag_add_nsti_to_old_file_name else file_to_copy.old_file_name_relative_path
                target_set = list(self.cosim_data.Simulations.keys()).index(file_to_copy.target_model)
                target_time_window = self.nsti.t
                target_iteration = self.nsti.i if target_set >= self.nsti.s else self.nsti.i + 1  # Go to next iteration if the set of the target model has not been run in this time window yet
                new_nsti = NSTI(self.sim_number, target_set, target_time_window, target_iteration)
                new_file_name_relative_path = self._add_nsti_to_file_name(file_to_copy.new_file_name_relative_path, nsti=new_nsti) if file_to_copy.flag_add_nsti_to_new_file_name else file_to_copy.new_file_name_relative_path

                original_file = Path(Path(local_folder), old_file_name_relative_path).resolve()
                target_local_folder = self.__find_local_target_folder(model=self.cosim_data.Simulations[file_to_copy.target_model])
                if not new_file_name_relative_path:
                    new_file_name_relative_path = old_file_name_relative_path
                target_file = Path(Path(target_local_folder), new_file_name_relative_path).resolve()
                make_folder_if_not_existing(os.path.dirname(target_file), verbose=self.verbose)
                if self.verbose: print(f'Copy file {original_file} to file {target_file}.')
                shutil.copyfile(original_file, target_file)

    def _copy_variables(self, model: Union[sim_Generic, sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE], verbose: bool = None):
        '''
        This function copies variables across from the output files of one model to the BuilderModel object of another.
        :param model:
        :param verbose: If True, display additional logging info
        :return:
        '''
        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Get list of variables to copy, which depends on the current co-simulation state
        if self.nsti.t == 0:
            vars_to_copy: List[VariableToCopy] = model.variables_to_copy_after.pre_cosim
            dict_key = 'variables_to_modify_pre_cosim'
        elif self.nsti.t > len(self.cosim_data.Settings.Time_Windows.t_0):
            vars_to_copy: List[VariableToCopy] = model.variables_to_copy_after.post_cosim
            dict_key = 'variables_to_modify_post_cosim'
        else:
            vars_to_copy: List[VariableToCopy] = model.variables_to_copy_after.cosim
            dict_key = 'variables_to_modify_cosim'

        if len(vars_to_copy) > 0:
            # Define local folder
            local_folder = self.__find_local_source_folder(model=model)

            # Copy files
            for var_to_copy in vars_to_copy:
                # Check whether to add an NSTI suffix between the base name and the extension of the old file name. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number
                file_name_relative_path = self._add_nsti_to_file_name(var_to_copy.file_name_relative_path, nsti=self.nsti) if var_to_copy.flag_add_nsti_to_file_name else var_to_copy.file_name_relative_path

                # Define dict_variable_types, which determines the expected shape of the variable (used by the function get_signals_from_file() )
                if self.cosim_data.Simulations[model.name].modelCase == 'magnet':
                    empty_data_model = DataModelMagnet()
                elif self.cosim_data.Simulations[model.name].modelCase == 'conductor':
                    empty_data_model = DataModelConductor()
                elif self.cosim_data.Simulations[model.name].modelCase == 'circuit':
                    empty_data_model = DataModelCircuit()
                empty_attr = rgetattr(empty_data_model, var_to_copy.model_var_name)
                if isinstance(empty_attr, list) and len(empty_attr) == 1:
                    dict_variable_types = {var_to_copy.model_var_name: '2D'}
                elif isinstance(empty_attr, list):
                    dict_variable_types = {var_to_copy.model_var_name: '1D'}
                else:
                    dict_variable_types = {var_to_copy.model_var_name: '2D'}

                # Get variable value from the source file. Supported formats: .csd, .csv, .mat
                original_file = Path(Path(local_folder), file_name_relative_path).resolve()
                var_value = get_signals_from_file(full_name_file=original_file, list_signals=var_to_copy.var_name,
                                                  dict_variable_types=dict_variable_types)  # Note: get_signals_from_file() returns a dict
                # If the get_signals_from_file() function returned a dictionary, select the appropriate key
                if isinstance(var_value, dict):
                    var_value = var_value[var_to_copy.var_name]
                # If a numpy array, make it a list
                if isinstance(var_value, np.ndarray):
                    var_value = var_value.tolist()

                # Assign variable values to the self variable that is used to pass their values to future model generation within the co-simulation
                self.variables_to_pass[var_to_copy.target_model][dict_key].variables_to_change.append(var_to_copy.model_var_name)
                self.variables_to_pass[var_to_copy.target_model][dict_key].variables_values.append(var_value)

    def __find_local_source_folder(self, model: Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        '''
        Function to find the path to the local folder, which has a different logic for each simulation tool
        :param model: Current simulation model
        :return: Path to the local folder of the current simulation model
        '''
        local_folder_prefix = os.path.join(self.local_PyCoSim_folder,
                                           self.cosim_data.GeneralParameters.cosim_name,
                                           model.type)
        if model.type == 'FiQuS':
            fiqus_input_file_path = os.path.join(local_folder_prefix, model.modelName, f'{model.modelName}_{self.nsti.n_s_t_i}_FiQuS.yaml')
            fiqus_data: DataFiQuS = yaml_to_data(fiqus_input_file_path, DataFiQuS)
            if fiqus_data.run.type in ['geometry_only']:
                return os.path.join(local_folder_prefix, model.modelName, f'Geometry_{fiqus_data.run.geometry}')
            elif fiqus_data.run.type in ['start_from_yaml', 'solve_with_post_process_python']:
                return os.path.join(local_folder_prefix, model.modelName, f'Geometry_{fiqus_data.run.geometry}', f'Mesh_{fiqus_data.run.mesh}', f'Solution_{fiqus_data.run.solution}')
        elif model.type == 'LEDET':
            return os.path.join(local_folder_prefix, str(self.nsti.n), model.modelName)
        elif model.type == 'PSPICE':
            pass
        elif model.type == 'XYCE':
            pass
        else:
            raise Exception(f'Software {model.type} not supported for automated running.')


    def __find_local_target_folder(self, model: Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]):
        '''
        Function to find the path to the local folder, which has a different logic for each simulation tool
        :param model: Current simulation model
        :return: Path to the local folder of the current simulation model
        '''

        # Define local folder
        local_folder_prefix = os.path.join(self.local_PyCoSim_folder,
                                           self.cosim_data.GeneralParameters.cosim_name,
                                           model.type)
        if model.type == 'FiQuS':
            local_folder = os.path.join(local_folder_prefix, model.modelName)
        elif model.type == 'LEDET':
            local_folder = os.path.join(local_folder_prefix, str(self.nsti.n), model.modelName)
        elif model.type in ['PSPICE', 'XYCE']:
            local_folder = os.path.join(local_folder_prefix, self.nsti.n_s_t_i, model.modelName, str(model.simulationNumber))
        local_folder = str(Path.resolve(Path(local_folder)))
        return local_folder

    def _add_nsti_to_file_name(self, file_name: str, nsti: NSTI):
        '''
        Function to add the NSTI suffix between the base file name and its extension
        :param file_name: Name of the file to edit
        :param nsti: NSTI object. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number
        :return: Name of the edited file
        '''

        base_name, extension = os.path.splitext(file_name)
        new_file_name = f"{base_name}_{nsti.n_s_t_i}{extension}"
        return new_file_name

    def _reset_variables_to_pass(self):
        '''
        Initialize or reset the dictionary that will be used to pass variable values from an output file to a model data object
        :return:
        '''
        self.variables_to_pass = {key: {
            'variables_to_modify_pre_cosim': ParametersToModify(),
            'variables_to_modify_cosim': ParametersToModify(),
            'variables_to_modify_post_cosim': ParametersToModify(),
        } for key in self.cosim_data.Simulations}  # Assign blank_entry to all models

    def _check_convergence(self, model: Union[sim_Generic, sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE], verbose: bool = None):
        """
        # all variable checks must be fulfilled to pass convergence check
        # either relative_tolerance or absolute_tolerance must be fulfilled to pass convergence check

        :return:
        :rtype:
        """

        #TODO allow checking convergence on a scalar variable, not just on a vector
        #TODO allow checking convergence on max/min/aveg values rather than on a vector

        verbose = verbose if verbose is not None else self.verbose  # if verbose is not defined, take its value from self

        # Define local folder
        local_folder = self.__find_local_source_folder(model=model)
        if not self.nsti.t in self.dict_convergence_variables[model.name]:
            self.dict_convergence_variables[model.name][self.nsti.t] = {}
        self.dict_convergence_variables[model.name][self.nsti.t][self.nsti.i] = {}
        # Perform the converge checks
        for check_to_perform in model.convergence_checks_cosim:
            if verbose: print(f'Performing convergence check for model {model.name} on variable {check_to_perform.var_name}.')

            # Check whether to add an NSTI suffix between the base name and the extension of the old file name. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number
            file_name_relative_path = self._add_nsti_to_file_name(check_to_perform.file_name_relative_path, nsti=self.nsti) if check_to_perform.flag_add_nsti_to_file_name else check_to_perform.file_name_relative_path
            # Get variable value from the source file. Supported formats: .csd, .csv, .mat
            original_file = Path(Path(local_folder), file_name_relative_path).resolve()
            var_value = get_signals_from_file(full_name_file=original_file, list_signals=check_to_perform.var_name, dict_variable_types={})

            # Add convergence variable values to self.self.dict_convergence_variables
            self.self.dict_convergence_variables[model.name][self.nsti.t][self.nsti.i][check_to_perform.var_name] = var_value
            if check_to_perform.time_var_name:
                # Add time vector of the convergence variable values to self.self.dict_convergence_variables
                time_var_value = get_signals_from_file(full_name_file=original_file, list_signals=check_to_perform.time_var_name, dict_variable_types={})
                self.self.dict_convergence_variables[model.name][self.nsti.t][self.nsti.i][check_to_perform.time_var_name] = time_var_value

            # At the first iteration, always return False (no convergence reached yet)
            if self.nsti.i == 0:
                if verbose: print(f'Model {model.name}. Simulation set {self.nsti.s}. Time window {self.nsti.t}.')
                return False
            else:
                old_var_value = self.self.dict_convergence_variables[model.name][self.nsti.t][self.nsti.i-1][check_to_perform.var_name]
                if check_to_perform.time_var_name:
                    # Interpolate the variable over the time vector (use the time vector of the previous iteration)
                    old_time_var_value = self.self.dict_convergence_variables[model.name][self.nsti.t][self.nsti.i-1][check_to_perform.time_var_name]
                    new_var_value_interpolated = interp1d(time_var_value, var_value)(old_time_var_value)
                    var_value = new_var_value_interpolated  # Use the interpolated values

                # Perform relative-tolerance check
                rel_error = abs(var_value - old_var_value) / abs(old_var_value)
                # Perform absolute-tolerance check
                abs_error = abs(var_value - old_var_value)
                # Check whether converge criteria are met
                if rel_error < check_to_perform.relative_tolerance or abs_error <= check_to_perform.absolute_tolerance:
                    flag_converged = True
                    print(f'Model {model.name}. Simulation set {self.nsti.s}. Time window {self.nsti.t}. Convergence reached at iteration {self.nsti.i}. Absolute tolerance: {abs_error} <= {check_to_perform.absolute_tolerance}. Relative tolerance: {rel_error} <= {check_to_perform.relative_tolerance}.')
                else:
                    flag_converged = False
                    print(f'Model {model.name}. Simulation set {self.nsti.s}. Time window {self.nsti.t}. Convergence not yet reached at iteration {self.nsti.i}. Absolute tolerance: {abs_error}. Relative tolerance: {rel_error}.')
                return flag_converged
