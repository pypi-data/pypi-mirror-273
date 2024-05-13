from typing import (List, Union, Dict, Literal, Optional)

from pydantic import BaseModel, Field, validator, ConfigDict


############################
# General parameters
class Model(BaseModel):
    """
        Level 2: Class for information on the model
    """
    name: Optional[str] = None
    version: Optional[str] = None
    case: Optional[str] = None
    state: Optional[str] = None

class General(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    cosim_name: Optional[str] = None
    model: Model = Model()

############################
# Co-simulation folders
# class CosimulationFolders(BaseModel):
#     """
#         Level 1: Class for co-simulation folders
#     """
#     local_COSIM_folder: str = None
#     local_PyCoSim_folder: str = None
#     path_model_folder: str = None  # TODO: maybe this key should be deleted, since each model could be read from different libraries for different models, see key "modelFolder"
#     settings_file_path: str = Field(default=None, description="relative path to settings file with file name of settings.user.yaml. This relative path is folder path")

############################
# Simulation configurations - one for simulation tool

class ConvergenceChecks(BaseModel):
    """
        Level 2: Class to define convergence checks to perform
    """
    file_name_relative_path: Optional[str] = Field(default=None, description="Name of the file with variable from which the convergence should be read")
    flag_add_nsti_to_file_name: Optional[bool] = Field(default=None, description="If True, add an NSTI suffix between the base name and the extension of the file name. The NSTI refers to the source model. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number")
    var_name: Optional[str] = Field(default=None, description="Name of the convergence variable")
    time_var_name: Optional[str] = Field(default=None, description="Name of the variable defining the time verctor. If defined, the variable values will be interpolated over the time vector before being compared.")
    relative_tolerance: Optional[float] = Field(default=None, description="Relative tolerance applied to the convergence check (either relative_tolerance or absolute_tolerance must be fulfilled to pass the convergence check)")
    absolute_tolerance: Optional[float] = Field(default=None, description="Absolute tolerance applied to the convergence check (either relative_tolerance or absolute_tolerance must be fulfilled to pass the convergence check)")

class ParametersToModify(BaseModel):
    """
        Level 2: Class to define parameters to modify
    """
    variables_to_change: List[str] = []
    variables_values: List = []

class FileToCopy(BaseModel):
    old_file_name_relative_path: Optional[str] = Field(default=None, description="Name of the file to copy")
    flag_add_nsti_to_old_file_name: Optional[bool] = Field(default=None, description="If True, add an NSTI suffix between the base name and the extension of the old file name. The NSTI refers to the source model. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number")
    target_model: Optional[str] = Field(default=None, description="Name of the simulation model")
    new_file_name_relative_path: Optional[str] = Field(default=None, description="New name of the file to copy. If null, don't change the name")
    flag_add_nsti_to_new_file_name: Optional[bool] = Field(default=None, description="If True, add an NSTI suffix between the base name and the extension of the new file name. The NSTI refers to the target model, not the source model. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number")

class FilesToCopy(BaseModel):
    pre_cosim: List[FileToCopy] = Field(default=[FileToCopy()], description="Files to copy after the pre-cosimulation")
    cosim: List[FileToCopy] = Field(default=[FileToCopy()], description="Files to copy after the cosimulation")
    post_cosim: List[FileToCopy] = Field(default=[FileToCopy()], description="Files to copy after the post-cosimulation")

class VariableToCopy(BaseModel):
    file_name_relative_path: Optional[str] = Field(default=None, description="Path of the file that contains the variable to copy (supported formats: .csd, .csv, .mat)")
    flag_add_nsti_to_file_name: Optional[bool] = Field(default=None, description="If True, add an NSTI suffix between the base name and the extension of the file name. The NSTI refers to the source model. NSTI: N=simulation number. S=simulation set. T=time window. I=Iteration number")
    var_name: Optional[str] = Field(default=None, description="Name of the variable to copy (header name is a .csv or .csd file, or variable name in a .mat file")
    target_model: Optional[str] = Field(default=None, description="Name of the simulation model")
    model_var_name: Optional[str] = Field(default=None, description="Name of the BuilderModel key to which the variable value will be assigned")
    model_config = ConfigDict(protected_namespaces=())

class VariablesToCopy(BaseModel):
    pre_cosim: List[VariableToCopy] = Field(default=[VariableToCopy()], description="Variables to copy after the pre-cosimulation")
    cosim: List[VariableToCopy] = Field(default=[VariableToCopy()], description="Variables to copy after the cosimulation")
    post_cosim: List[VariableToCopy] = Field(default=[VariableToCopy()], description="Variables to copy after the post-cosimulation")


class sim_Generic(BaseModel): # TODO add/edit keys
    """
        Level 1: Class of FiQuS simulation configuration
    """
    name: Optional[str] = None
    modelFolder: Optional[str] = None  # TODO: is this needed?
    modelName: Optional[str] = None
    modelCase: Optional[str] = None
    flag_run_pre_cosim: Optional[bool] = Field(default=None, description="Flag to enable (True) or disable (false) pre-cosim solution")
    flag_run_cosim: Optional[bool] = Field(default=None, description="Flag to enable (True) or disable (false) cosim solution")
    flag_run_post_cosim: Optional[bool] = Field(default=None, description="Flag to enable (True) or disable (False) post-cosim solution")
    convergence_checks_cosim: List[ConvergenceChecks] = Field(default=[], description="List of convergence checks to perform during each time window (all variable checks must be fulfilled to pass the convergence check)")
    variables_to_modify_pre_cosim: ParametersToModify = ParametersToModify()
    variables_to_modify_cosim: ParametersToModify = ParametersToModify()
    variables_to_modify_post_cosim: ParametersToModify = ParametersToModify()
    files_to_copy_after: FilesToCopy = FilesToCopy()
    variables_to_copy_after: VariablesToCopy = VariablesToCopy()

class sim_FiQuS(sim_Generic): # TODO add/edit keys
    """
        Level 1: Class of FiQuS simulation configuration
    """
    type: Literal['FiQuS']

class sim_LEDET(sim_Generic):
    """
        Level 1: Class of LEDET simulation configuration
    """
    type: Literal['LEDET']

class sim_PSPICE(sim_Generic):
    """
        Level 1: Class of PSPICE simulation configuration
    """
    type: Literal['PSPICE']
    configurationFileName: Optional[str] = None
    externalStimulusFileName: Optional[str] = None
    initialConditions: Dict[str, Union[float, int]] = {}
    skipBiasPointCalculation: Optional[bool] = None

class sim_XYCE(sim_Generic):
    """
        Level 1: Class of XYCE simulation configuration
    """
    type: Literal['XYCE']
    configurationFileName: Optional[str] = None
    externalStimulusFileName: Optional[str] = None
    initialConditions: Dict[str, Union[float, int]] = {}
    skipBiasPointCalculation: Optional[bool] = None

############################
# Co-simulation port
# class CosimPortModel(BaseModel):
#     input_model: Optional[str] = None
#     input_variable_component: Optional[str] = None
#     input_variable_name: Optional[str] = None
#     input_variable_coupling_parameter: Optional[str] = None
#     input_variable_type: Optional[str] = None
#     output_model: Optional[str] = None
#     output_variable_component: Optional[str] = None
#     output_variable_name: Optional[str] = None
#     output_variable_coupling_parameter: Optional[str] = None
#     output_variable_type: Optional[str] = None

class CosimPortVariable(BaseModel):
    variable_names: List[str] = []
    variable_coupling_parameter: Optional[str] = None
    variable_types: List[str] = []

class CosimPortModel(BaseModel):
    components: List[str] = []
    inputs: Dict[str, CosimPortVariable] = {}
    outputs: Dict[str, CosimPortVariable] = {}

class CosimPort(BaseModel):
    """
    Class for co-simulation port to be used within PortDefinition
    """
    Models: Dict[str, CosimPortModel] = {}


############################
# Co-simulation settings
class ConvergenceClass(BaseModel):
    """
        Level 2: Class for convergence options
    """
    convergenceVariables: Dict[str, Union[str, None]] = {}
    relTolerance: Dict[str, Union[float, int, None]] = {}
    absTolerance: Dict[str, Union[float, int, None]] = {}

class Time_WindowsClass(BaseModel):
    """
        Level 2: Class for time window options
    """
    t_0: Optional[List[Union[float, int]]] = []
    t_end: Optional[List[Union[float, int]]] = []
    t_step_max: Optional[Dict[str, List[Union[float, int]]]] = {}

class Options_runClass(BaseModel):
    """
        Level 2: Class for co-simulation run options
    """
    executionOrder: Optional[List[int]] = []
    executeCleanRun: Optional[List[bool]] = []

class CosimulationSettings(BaseModel):
    """
        Level 1: Class for co-simulation settings
    """
    Convergence: ConvergenceClass = ConvergenceClass()
    Time_Windows: Time_WindowsClass = Time_WindowsClass()
    Options_run: Options_runClass = Options_runClass()

class CosimulationSettings(BaseModel):
    """
        Level 1: Class for co-simulation settings
    """
    Convergence: ConvergenceClass = ConvergenceClass()
    Time_Windows: Time_WindowsClass = Time_WindowsClass()
    Options_run: Options_runClass = Options_runClass()


############################
# COSIM options
class Options_COSIMClass(BaseModel):
    """
        Level 1: Class for co-simulation settings
    """
    solverPaths: Dict[str, str] = Field(default={}, description="Dictionary containing the paths to the solvers used by each simulation defined in the 'Simulations' key. The keys of this dictionary must match the keys of the 'Simulations' dictionary.")


############################
# pyCOSIM options
class Options_PyCoSimClass(BaseModel):
    """
        Level 1: Class for co-simulation settings
    """
    dummy_entry: Optional[str] = Field(default=None, description="Dummy place holder for some options")




############################
# Highest level
class DataModelCosim(BaseModel):
    """
        **Class for the STEAM inputs**

        This class contains the data structure of STEAM model inputs for cooperative simulations (co-simulations).

        :return: DataCosim object
    """

    GeneralParameters: General = General()
    # Folders: CosimulationFolders = CosimulationFolders()
    Simulations: Dict[str, Union[sim_FiQuS, sim_LEDET, sim_PSPICE, sim_XYCE]] = {}
    # ModifyParameters: Dict[str, ?]: {}  #TODO
    PortDefinition: Dict[str, CosimPort] = {}
    Settings: CosimulationSettings = CosimulationSettings()
    Options_COSIM: Options_COSIMClass = Options_COSIMClass()
    Options_PyCoSim: Options_PyCoSimClass = Options_PyCoSimClass()


    @validator('Simulations')
    def validate_Simulations(cls, Simulations):
        for key, value in Simulations.items():
            value.name = key
        return Simulations

    # def __init__(self, **data):
    #     super().__init__(**data)
    #     for key, value in self.Simulations.items():
    #         value.name = key
    #     print('aa')