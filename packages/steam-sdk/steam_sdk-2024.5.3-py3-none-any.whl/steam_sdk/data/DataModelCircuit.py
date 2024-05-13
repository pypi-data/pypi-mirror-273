from pydantic import BaseModel, create_model
from typing import Any, Dict, List, Optional, Union


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
    circuit_name: Optional[str] = None
    model: Model = Model()
    additional_files: List[str] = []  # These files will be physically copied to the output folder


############################
# Auxiliary files
class Auxiliary_Files(BaseModel):
    """
        Level 1: Class for general information on the case study
        Note: These entries will be written in the netlist, but no further action will be taken (see General.additional_files)
    """
    files_to_include: List[str] = []


############################
# Stimuli
class StimuliClass(BaseModel):
    """
        Level 1: Stimulus files
    """
    stimulus_files: List[str] = []


############################
# Libraries
class LibrariesClass(BaseModel):
    """
        Level 1: Component libraries
    """
    component_libraries: List[str] = []


class Magnet(BaseModel):
    name: Optional[str] = None
    L_mag: Optional[float] = None
    C_ground: Optional[float] =None
    Field_interp_value: Optional[float] = None

class TFMClass(BaseModel):
    flag_PC: Optional[bool] = False
    flag_ISCC: Optional[bool] = False
    flag_IFCC: Optional[bool] = False
    flag_EC: Optional[bool] = False
    flag_Wedges: Optional[bool] = False
    flag_ColdBore: Optional[bool] = False
    flag_BS: Optional[bool] = False
    flag_Roxie: Optional[bool] = False
    M_IF_PC: Optional[float] = None
    M_CB_Wedges: Optional[float] = None
    T: Optional[float] = None
    Magnets: Dict[str, Magnet] = {}


############################
# Global parameters
class Global_Parameters(BaseModel):
    """
        Level 1: Global circuit parameters
    """
    global_parameters: Optional[dict] = None


############################
# Initial conditions
class InitialConditionsClass(BaseModel):
    """
        Level 1: Initial conditions parameters
    """
    initial_conditions: Optional[dict] = None


############################
# Netlist, defined as a list of Component objects
# class NetlistClass(BaseModel):
#     """
#         Level 1: Netlist
#     """
#     def __setattr__(self, key, value):
#         return object.__setattr__(self, key, value)

class Component(BaseModel):
    """
        Level 2: Circuit component
    """
    type: Optional[str] = None
    nodes: List[Union[str, int]] = []
    value: Optional[str] = None
    parameters: Optional[dict] = dict()


############################
# Simulation options
class OptionsClass(BaseModel):
    """
        Level 1: Simulation options
    """
    options_simulation: Optional[dict] = None
    options_autoconverge: Optional[dict] = None
    flag_inCOSIM: Optional[bool] = None


############################
# Analysis settings
class SimulationTime(BaseModel):
    """
        Level 2: Simulation time settings
    """
    time_start: Optional[float] = None
    time_end: Optional[float] = None
    min_time_step: Optional[float] = None
    time_schedule: Optional[dict] = None


class SimulationFrequency(BaseModel):
    """
        Level 2: Simulation frequency settings
    """
    frequency_step: Optional[str] = None
    frequency_points: Optional[float] = None
    frequency_start: Optional[str] = None
    frequency_end: Optional[str] = None


class AnalysisClass(BaseModel):
    """
        Level 1: Analysis settings
    """
    analysis_type: Optional[str] = None
    simulation_time: Optional[SimulationTime] = SimulationTime()
    simulation_frequency: Optional[SimulationFrequency] = SimulationFrequency()


############################
# Post-processing settings
class Settings_Probe(BaseModel):
    """
        Level 2: Probe settings
    """
    probe_type: Optional[str] = None
    variables: List[str] = []


class PostProcessClass(BaseModel):
    """
        Level 1: Post-processing settings
    """
    probe: Settings_Probe = Settings_Probe()


############################
# Highest level
class DataModelCircuit(BaseModel):
    '''
        **Class for the circuit netlist inputs**

        This class contains the data structure of circuit netlist model inputs.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataModelCircuit object
    '''

    GeneralParameters: General = General()
    AuxiliaryFiles: Auxiliary_Files = Auxiliary_Files()
    Stimuli: StimuliClass = StimuliClass()
    Libraries: LibrariesClass = LibrariesClass()
    GlobalParameters: Global_Parameters = Global_Parameters()
    InitialConditions: InitialConditionsClass = InitialConditionsClass()
    Netlist: Dict[str, Component] = {}
    Options: OptionsClass = OptionsClass()
    Analysis: AnalysisClass = AnalysisClass()
    PostProcess: PostProcessClass = PostProcessClass()
    TFM: Optional[TFMClass] = None
