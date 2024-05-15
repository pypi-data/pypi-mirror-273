import time
from typing import Tuple, Any
import sys
import numpy as np
import pandas as pd
import os
from pathlib import Path
from dataclasses import asdict
from scipy.interpolate import RegularGridInterpolator
from scipy.signal import find_peaks
import steammaterials
from steam_sdk.data.DataTFM import General
from steam_sdk.data.DataTFM import HalfTurns
from steam_sdk.data.DataTFM import Strands
from steam_sdk.data.DataTFM import PC
from steam_sdk.data.DataTFM import Options
from steam_sdk.data.DataTFM import IFCC
from steam_sdk.data.DataTFM import ISCC
from steam_sdk.data.DataTFM import ED
from steam_sdk.data.DataTFM import Wedge
from steam_sdk.data.DataTFM import CB
from steammaterials.STEAM_materials import STEAM_materials
matpath: str = os.path.dirname(steammaterials.__file__)
import matplotlib.pyplot as plt
import time

class BuilderTFM:
    """
           Class to generate TFM models
    """

    def __init__(self, magnet_name: str = None, builder_LEDET= None, flag_build: bool = True,
                  output_path: str = None, path_input_file: str = None, TFM_inputs=None, Magnet_data=None ):
        """
             Object is initialized by defining TFM variable structure and default parameter descriptions, starting from
             the magnet_name and the builder_LEDET model. The class can also calculate various passive effects, depending on the flag values.

            :param magnet_name: name of the analyzed magnet
            :param builder_LEDET: builderLEDET object corresponding to that magnet
            :param flag_build: defines whether the model has to be build
            :param frequency: frequency of measurements
            :param T: temperature of measurements
            :param f_mag: field-factor for each strand
            :param f_mag_X: field-factor for each strand along X axis
            :param f_mag_Y: field-factor for each strand along Y axis
            :param output_path: path to save the generated lib file
            :param flag_Roxie: if True it uses the field-factors calculated from Roxie, else it uses the field-factors provided as parameter
            :param flag_IFCC: if True includes the Inter Filament Coupling Current effect
            :param flag_ISCC: if True includes the Inter Strands Coupling Current effect
            :param flag_Wedge: if True includes the Wedge effect
            :param flag_CB: if True includes the Cold Bore effect
            :param flag_ED: if True includes the Eddy Currents effect in the Copper Sheath
        """
        # TODO I_magnet
        # TODO lib_path
        # TODO hard coded path to steam models
        # Data structures
        self.General = General()
        self.HalfTurns = HalfTurns()
        self.Strands = Strands()
        self.Options = Options()
        self.PC = PC()
        self.IFCC = IFCC()
        self.ISCC = ISCC()
        self.ED = ED()
        self.Wedge = Wedge()
        self.CB = CB()
        self.magnet_name = Magnet_data.name
        self.path_input_file = path_input_file

        if flag_build:
            if not builder_LEDET or not self.magnet_name:
                 raise Exception('Cannot build model without providing BuilderLEDET object with Inputs dataclass and magnet_name')

            # Translate the Inputs dataclass of BuilderLEDET in a dictionary
            LedetInputs = asdict(builder_LEDET.Inputs)
            self.LedetInputs = LedetInputs
            self.LedetAuxiliary = builder_LEDET.Auxiliary
            self.LedetOptions = builder_LEDET.Options
            self.TFM_inputs = TFM_inputs
            self.Magnet_data = Magnet_data

            self.M_CB_Wedge = TFM_inputs.M_CB_Wedge
            self.T = TFM_inputs.T
            self.Field_interp_value = Magnet_data.Field_interp_value

            # TODO: HardCoded values
            self.General.I_magnet = 1
            self.General.lib_path = f"D:\\Code_new\\steam_analyses\\mbrd_tfm\\local_library\\lib\\{magnet_name}_TFM_General.lib"
            # self.General.path_input_file = f"D:\\Code_new\\\steam_analyses\\mbrd_tfm\\local_library\\magnets\\{magnet_name}\\input"
            self.General.path_input_file = f"D:\\Code_new\\\steam_sdk\\tests\\builders\\model_library\\magnets\\{magnet_name}\\input"
            self.Wedge.RRR_Wedge = np.array([50])

            self.conductor_to_group = np.array(builder_LEDET.model_data.CoilWindings.conductor_to_group)

            self.translateModelDataToTFMGeneral()
            self.translateModelDataToTFMHalfTurns()
            self.translateModelDataToTFMStrands()
            self.setOptions()
            self.change_coupling_parameter(output_path=output_path)

    def translateModelDataToTFMGeneral(self):
        """
            This function saves the appropriate BuilderLEDET Inputs dataclass values for the General dataclass attributes.
        """
        self.setAttribute(self.General, 'magnet_name', self.magnet_name)
        self.setAttribute(self.General, 'magnet_length', self.LedetInputs['l_magnet'])
        nT = self.LedetInputs['nT']
        self.setAttribute(self.General, 'num_HalfTurns', np.sum(nT))
        bins = max(self.conductor_to_group)
        self.setAttribute(self.General, 'bins', bins)
        L_mag = self.Magnet_data.L_mag
        self.setAttribute(self.General, 'L_mag', L_mag)
        C_ground = self.Magnet_data.C_ground
        self.setAttribute(self.General, 'C_ground', C_ground)


    def translateModelDataToTFMHalfTurns(self):
        """
             This function saves the appropriate BuilderLEDET Inputs dataclass values for the HalfTurns dataclass attributes.
             The saved data are arrays with len equal to the total number of HalfTurns
         """
        # Values that can't be directly obtained from the Inputs dataclass
        nT = self.LedetInputs['nT']
        HalfTurns_to_group = np.repeat(np.arange(len(nT)) + 1, nT)
        self.setAttribute(self.HalfTurns, 'HalfTurns_to_group', HalfTurns_to_group)
        Group_to_coil_sections = np.array(self.LedetInputs['GroupToCoilSection'])
        HalfTurns_to_coil_sections = Group_to_coil_sections[HalfTurns_to_group - 1]
        self.setAttribute(self.HalfTurns, 'HalfTurns_to_coil_sections', HalfTurns_to_coil_sections)
        HalfTurns_to_conductor = self.conductor_to_group[HalfTurns_to_group - 1]
        self.setAttribute(self.HalfTurns, 'HalfTurns_to_conductor', HalfTurns_to_conductor)
        nc = np.repeat(nT, nT)
        self.setAttribute(self.HalfTurns, 'Nc', nc)

        # Values that can be directly obtained from the Inputs dataclass
        for keyInputData, value in self.LedetInputs.items():
            keyTFM = lookupModelDataToTFMHalfTurns(keyInputData)
            if keyTFM in self.HalfTurns.__annotations__:
                if isinstance(value, list):
                    self.setAttribute(self.HalfTurns, keyTFM, np.array(value))
                else:
                    self.setAttribute(self.HalfTurns, keyTFM, value[HalfTurns_to_group - 1])

        # Fitting value for ISCL, varying between C=1 (Ns=8) and C=1.15 (Ns=40) [-]
        # Reference: Arjan's Thesis, Chapter 4, Page 78, Equation 4.31
        C_strand = 0.0046875 * self.HalfTurns.n_strands + 0.9625
        self.setAttribute(self.HalfTurns, 'C_strand', C_strand)


    def translateModelDataToTFMStrands(self):
        """
             This function saves the appropriate BuilderLEDET Inputs dataclass values for the Strands dataclass attributes.
             Arrays with len equal to the entire number of strands make up the saved data.
         """
        self.calculate_field_contributions()
        strands_to_CS = np.repeat(self.HalfTurns.HalfTurns_to_coil_sections, self.HalfTurns.n_strands)
        self.setAttribute(self.Strands, 'strands_to_coil_sections', strands_to_CS)
        strands_to_conductor = np.repeat(self.HalfTurns.HalfTurns_to_conductor, self.HalfTurns.n_strands)
        self.setAttribute(self.Strands, 'strands_to_conductor', strands_to_conductor)
        for keyLedetData, value in self.LedetInputs.items():
            keyTFM = lookupModelDataToTFMStrands(keyLedetData)
            if keyTFM in self.Strands.__annotations__:
                repeated_value = np.repeat(value[self.HalfTurns.HalfTurns_to_group - 1], self.HalfTurns.n_strands)
                self.setAttribute(self.Strands, keyTFM, repeated_value)

    def setOptions(self):
        """
            This function sets to the Option DataClass the flags fto know which effects should be included in the magnet model

            :param flag_PC: if True includes the Persistent Current effect
            :param flag_IFCC: if True includes the Inter Filament Coupling Current effect
            :param flag_ISCC: if True includes the Inter Strands Coupling Current effect
            :param flag_Wedge: if True includes the Wedge effect
            :param flag_CB: if True includes the Cold Bore effect
            :param flag_ED: if True includes the Eddy Currents effect in the Copper Sheath
        """
        if self.T < min(self.LedetInputs['Tc0_NbTi_ht_inGroup']):
            flag_SC = True
        else:
            flag_SC = False
        self.setAttribute(self.Options, 'flag_SC', flag_SC)

        for keyTFMData, value in self.TFM_inputs.__dict__.items():
            if keyTFMData.startswith('flag'):
                self.setAttribute(self.Options, keyTFMData, value)


    def calculate_field_contributions(self):
        '''
        Calculates the field in each filament of the MB magnet - ROXIE Edition
        This function returns the calculated field contributions from ROXIE for the magnet
        '''
        ## Field in all filaments when fully powering the magnet


        f_mag_Roxie, f_mag_X_Roxie, f_mag_Y_Roxie = self.retrieve_field_contributions_Roxie()

        local_library_path = os.path.join(Path(self.General.path_input_file).resolve(), 'TFM_input')
        name = self.General.magnet_name
        mapping = np.vectorize(lambda t: complex(t.replace('i', 'j')))

        full_file_Comsol = Path(os.path.join(local_library_path, f'Field_Map_{name}.csv')).resolve()
        df_Comsol = pd.read_csv(full_file_Comsol, header=None, dtype=str, na_filter=False)
        frequency = np.array(df_Comsol.iloc[1, 2::2]).astype(float)
        df_Comsol = mapping(df_Comsol.values[2:, 2:]).T
        f_mag_X_Comsol = np.sqrt(np.real(df_Comsol[::2, :] * np.conjugate(df_Comsol[::2, :]))) * np.sign(f_mag_X_Roxie)
        f_mag_Y_Comsol = np.sqrt(np.real(df_Comsol[1::2, :] * np.conjugate(df_Comsol[1::2, :]))) * np.sign(f_mag_Y_Roxie)
        f_mag_Comsol = np.sqrt(f_mag_X_Comsol ** 2 + f_mag_Y_Comsol ** 2)

        self.frequency = frequency

        self.setAttribute(self.Strands, 'f_mag_X_Roxie', f_mag_X_Roxie)
        self.setAttribute(self.Strands, 'f_mag_Y_Roxie', f_mag_Y_Roxie)
        self.setAttribute(self.Strands, 'f_mag_Roxie', f_mag_Roxie)
        self.setAttribute(self.Strands, 'f_mag_X_Comsol', f_mag_X_Comsol)
        self.setAttribute(self.Strands, 'f_mag_Y_Comsol', f_mag_Y_Comsol)
        self.setAttribute(self.Strands, 'f_mag_Comsol', f_mag_Comsol)


    def calculate_PC(self, frequency: np.ndarray, T: float, fMag: np.ndarray, flag_coupling:bool = True, flag_save:bool=False) -> np.ndarray:
        '''
        Function that calculates the equivalent circuit parameter for the persistent currents and save them to the
        PC dataclass

        :param frequency: Frequency vector
        :param T: temperature vector, to be used in the interaction with Eddy-currents
        :param f_mag: field-factor for each strand
        '''

        l_magnet = self.General.magnet_length
        ds_filamentary = self.Strands.d_filamentary
        dws = self.Strands.diameter
        strands_to_conductor = self.Strands.strands_to_conductor
        strands_to_CS = self.Strands.strands_to_coil_sections
        RRR = self.Strands.RRR
        bins = self.General.bins
        n_strands = np.sum(self.HalfTurns.n_strands)

        # Calculating constants
        mu0 = 4 * np.pi / 10 ** 7
        w = 2 * np.pi * frequency.reshape(len(frequency), 1)

        B = self.General.I_magnet*fMag
        rho_el_0 = self.rhoCu_nist(T=T, RRR=RRR, B=B[0, :])

        tb_strand = dws - ds_filamentary

        # Calculate the equivalent circuit parameter
        tau_ed = mu0 / 2 * (dws / 2 * tb_strand / 2) / rho_el_0
        if flag_coupling:
            alpha2 = 1 / np.sqrt(np.sqrt((1 + (w * tau_ed) ** 2)))
        else:
            alpha2 = np.ones(w.shape)

        M_temp = (np.pi / 4 * l_magnet * ds_filamentary * fMag * alpha2) ** 2
        Lm = np.array([mu0 * np.pi / 4 * l_magnet] * len(frequency))
        M_if_Pc = mu0 * np.pi / 8 * l_magnet
        I_Pc = np.array([0, 0])

        idx_valid = np.where(strands_to_CS - 1 < strands_to_CS / 2)[0]
        # M_pc = np.sqrt(np.sum(M_temp[:, idx_valid], axis=1))
        L_repeated = np.tile(Lm, n_strands)
        L_pc = np.reshape(L_repeated, (len(frequency), n_strands), order='F')
        STC_repeated = np.tile(strands_to_conductor, len(frequency))
        STC_pc = np.reshape(STC_repeated, (len(frequency), n_strands), order='F')

        L_pc = np.squeeze(L_pc[:, idx_valid])
        STC_pc = np.squeeze(STC_pc[:, idx_valid])
        M_temp = np.squeeze(M_temp[:, idx_valid])

        L_bin, R_bin, M_bin = bin_components(frequency=frequency, L=L_pc, R=STC_pc, M=M_temp, bins=bins, sort_on='R', flag_PC=True)

        if flag_save:
            self.setAttribute(self.PC, 'M', M_bin)
            self.setAttribute(self.PC, 'I', I_Pc)
            self.setAttribute(self.PC, 'L', L_bin)
            self.setAttribute(self.PC, 'M_IF_PC', M_if_Pc)
        else:
            return L_bin, I_Pc, M_bin


    def calculate_IFCC(self, frequency: np.ndarray, T: float, fMag: np.ndarray, flag_coupling: bool = True, flag_save: bool = False) -> np.ndarray:
        '''
        Calculates the equivalent IFCL coupling loops for a given temperature and field

        :param frequency: Frequency vector
        :param T: temperature vector
        :param f_mag: field-factor for each strand
        '''

        w = 2 * np.pi * frequency.reshape(len(frequency), 1)
        mu0 = 4 * np.pi / 10 ** 7
        mu0_eff = 4 * np.pi / 10 ** 7

        # Setting all required parameters for the MB magnet
        f_ro_eff = self.Strands.f_rho_effective
        l_mag = self.General.magnet_length
        dws = self.Strands.diameter
        ds_filamentary = self.Strands.d_filamentary
        strands_to_CS = np.repeat(self.HalfTurns.HalfTurns_to_coil_sections, self.HalfTurns.n_strands)
        RRR = self.Strands.RRR
        Lp_f = self.Strands.fil_twist_pitch
        bins = self.General.bins

        # Resistivity calculations
        B = self.General.I_magnet*fMag
        rho_el_0 = self.rhoCu_nist(T=T, RRR=RRR*f_ro_eff, B=B[0, :]) + 1e-12
        rho_el_Outer = self.rhoCu_nist(T=T, RRR=RRR, B=B[0, :]) + 1e-12

        idx_valid = np.where(strands_to_CS - 1 < strands_to_CS / 2)[0]

        # Calculating the coupled loop equivalent parameter
        beta_if = (Lp_f / (2 * np.pi)) ** 2 * 1 / (rho_el_0)
        tau_if = mu0_eff / 2 * beta_if

        tb_strand = dws - ds_filamentary
        tau_ed = mu0 / 2 * ((dws / 2) * (tb_strand / 2)) / rho_el_Outer
        if flag_coupling:
            alpha2 = 1 / np.sqrt((1 + (w * (tau_ed)) ** 2))
        else:
            alpha2 = np.ones(w.shape)
        alpha = 1 / np.sqrt((1 + (w * (tau_if)) ** 2))
        dB = w * fMag * alpha * alpha2

        # Standard method
        I_if = beta_if * ds_filamentary * dB
        P_if = tau_if / (2 * mu0_eff) * ds_filamentary ** 2 * np.pi * l_mag * dB ** 2
        # Power formula proposed in Arjans thesis - not working in XYCE
        # I_if = np.sqrt(np.pi / (2*w)) * beta_if * dS * dB
        # P_if = 2*dS**2*l_mag*np.pi/4*(2*tau_if*np.pi*w)/mu0*(f_mag*alpha)**2

        I_tot_im = I_if * alpha
        I_tot_re = I_if * alpha * w * tau_if
        # I_tot_re = np.sqrt(I_if ** 2 - I_tot_im ** 2)
        I_if = I_tot_re + 1j * I_tot_im

        R_if = P_if / np.real((I_if * np.conjugate(I_if)))
        L_if = np.ones((len(frequency), 1)) * tau_if * R_if[0, :]
        M_if = (1j * w.reshape(len(frequency), 1) * L_if * I_if + I_if * R_if) / (1j * w.reshape(len(frequency), 1) * 1)
        # M_if = np.sqrt(np.real(M_if) ** 2 + np.imag(M_if) ** 2)

        R_if = np.squeeze(R_if[:, idx_valid])
        L_if = np.squeeze(L_if[:, idx_valid])
        M_if = np.squeeze(M_if[:, idx_valid])
        I_if = np.squeeze(I_if[:, idx_valid])

        L_if_bin, R_if_bin, M_if_bin, I_if_bin = bin_components(frequency, L_if, R_if, M_if,  sort_on='R', bins=bins, I=I_if)

        if flag_save:
            self.setAttribute(self.IFCC, 'M', M_if_bin)
            self.setAttribute(self.IFCC, 'R', R_if_bin)
            self.setAttribute(self.IFCC, 'L', L_if_bin)
            self.setAttribute(self.IFCC, 'P', P_if)
            self.setAttribute(self.IFCC, 'tau', tau_if)
        else:
            return L_if_bin, R_if_bin, M_if_bin


    def calculate_ISCC(self, frequency: np.ndarray, T: float, fMag_X: np.ndarray, fMag_Y: np.ndarray, flag_save: bool = False) -> np.ndarray:
        '''
        Function that calculates the power loss and induced currents by ISCL and derives the equivalent circuit parameter

        :param frequency: Frequency vector
        :param T: temperature vector
        :param f_mag_X_all: field-factor along X axis for each strand
        :param f_mag_Y_all: field-factor along Y axis for each strand

        :return f_mag_X_return: return field-factor along X axis for each strand
        :return f_mag_Y_all: return field-factor along Y axis for each strand
        '''
        f = frequency
        w = 2 * np.pi * f.reshape(len(f), 1)  #

        l_mag = self.General.magnet_length
        mu0 = 4 * np.pi / 10 ** 7

        dws = self.HalfTurns.diameter
        rotation_block = self.HalfTurns.rotation_ht
        mirror_block = self.HalfTurns.mirror_ht
        alphasRAD = self.HalfTurns.alphaDEG_ht * np.pi / 180
        bins = self.General.bins
        fsc = self.HalfTurns.fsc
        n_strands = self.HalfTurns.n_strands
        Lp_s = self.HalfTurns.strand_twist_pitch
        wBare = self.HalfTurns.bare_cable_width
        hBare = self.HalfTurns.bare_cable_height_mean
        Nc = self.HalfTurns.Nc
        C = self.HalfTurns.C_strand
        R_c = self.HalfTurns.Rc
        HalfTurns_to_CS = self.HalfTurns.HalfTurns_to_coil_sections
        RRR = self.HalfTurns.RRR
        f_ro_eff = self.HalfTurns.f_rho_effective

        alphas = np.repeat((np.pi/2 * mirror_block/2 - (mirror_block - 1) * alphasRAD - rotation_block/180 * np.pi), n_strands)
        f_magPerp = np.transpose(-fMag_X * np.sin(alphas) + fMag_Y * np.cos(alphas))
        r_magPerp = np.transpose(fMag_X * np.cos(alphas) + fMag_Y * np.sin(alphas))
        B_temp = np.sqrt(fMag_X ** 2 + fMag_Y ** 2).T

        ## Reverse action:
        ## fMag_X = r_magPerp.T*np.cos(alphas)-f_magPerp.T*np.sin(alphas)
        ## fMag_Y = r_magPerp.T*np.sin(alphas)+f_magPerp.T*np.cos(alphas)

        f_magPerp_ht = np.zeros((self.General.num_HalfTurns, len(frequency)))
        r_magPerp_ht = np.zeros((self.General.num_HalfTurns, len(frequency)))
        alphas_ht = np.zeros((self.General.num_HalfTurns, 1))
        B_ht = np.zeros((self.General.num_HalfTurns, len(frequency)))
        tempS = 0
        for i in range(len(n_strands)):
            f_magPerp_ht[i] = np.average(f_magPerp[tempS:tempS + n_strands[i], :], axis=0)
            r_magPerp_ht[i] = np.average(r_magPerp[tempS:tempS + n_strands[i], :], axis=0)
            alphas_ht[i] = np.average(alphas[tempS:tempS + n_strands[i]])
            B_ht[i] = np.average(B_temp[tempS:tempS + n_strands[i], :], axis=0)
            tempS = tempS + n_strands[i]

        alpha_c = wBare / hBare
        idx_valid = np.where(HalfTurns_to_CS - 1 < HalfTurns_to_CS / 2)[0]

        rho_el_Outer = self.rhoCu_nist(T=T, B=B_ht[:, 0], RRR=RRR*f_ro_eff) + 1e-12
        rho_C_Strands = R_c / (rho_el_Outer * (n_strands ** 2 - n_strands) / (2 * Lp_s * alpha_c)) #Eq. 4.33 in Arjans Thesis p. 78

        #  Calculating the equivalent circuit parameter
        beta_is = 1 / 120 * Lp_s / R_c * n_strands * (n_strands - 1) * wBare / hBare
        tau_is = mu0 * beta_is
        factor_tau = alpha_c * Nc / (alpha_c + C * (Nc - 1))  # Eq. 4.41 in Arjans Thesis p.89
        # tau_is = 1.65e-08 * (Lp_s * (n_strands ** 2 - 4 * n_strands)) / R_c * factor_tau  # Eq. 4.31 in Arjans Thesis p.78

        alpha = 1 / np.sqrt((1 + (w * tau_is) ** 2))
        dB = w * abs(f_magPerp_ht.T) * alpha

        P_is = l_mag * beta_is * dB ** 2 * wBare * hBare
        I_is = beta_is * hBare * dB

        I_tot_im = I_is * alpha
        I_tot_re = I_is * alpha * w * tau_is
        #I_tot_re = np.sqrt(I_is ** 2 - I_tot_im ** 2)
        I_is = I_tot_re + 1j * I_tot_im

        # Calculate equivalent parameter
        R_is = P_is / np.real((I_is*np.conjugate(I_is)))
        L_is = np.ones((len(f), 1)) * tau_is * R_is[0, :]
        M_is = (1j * w.reshape(len(f), 1) * L_is * I_is + I_is * R_is) / (1j * w.reshape(len(f), 1) * 1)
        # M_is = np.sqrt(np.real(M_is) ** 2 + np.imag(M_is) ** 2)

        # Calculate warm resistance of a strand-pitch
        if not self.Options.flag_SC:
            ## Add the warm part to account for ISCL in non-superconducting state
            rho_el_Outer = self.rhoCu_nist(T, B_ht[:, 0], RRR*f_ro_eff) + 1e-12
            alpha_st = np.arctan(wBare/(Lp_s/2)) #Half twist-pitch as Lp is the full length until its back at the beginning
            l_strand = 2 * wBare / np.sin(alpha_st) + 2 * hBare  # twice as we go back AND forth
            A_strand = (1 - fsc) * np.pi * (dws / 2) ** 2
            R_strand = rho_el_Outer * l_strand / A_strand

            R_c_warm = 2e-3 * rho_C_Strands * rho_el_Outer * (n_strands** 2 - n_strands) / (2 * Lp_s * alpha_c)
            R_c_N = R_c_warm + R_strand
            # fT = 1/(1.9)**0.08*T**(0.08)
            # fT = 2*1/(np.log(1.9)**0.186)*np.log(T)**0.186
            fT = 2.5 * 1 / (np.log(1.9) ** 0.3179) * np.log(T) ** 0.3179
            tau_is_N = 1.65e-8 * C * 1 / (2 * fT) * (Lp_s * (n_strands ** 2 - 4 * n_strands)) / R_c_N * factor_tau  # Equation 4.31 in Arjans Thesis P.78 and Eq. 4.41
            # beta_is_N = tau_is_N/ mu0
            beta_is_N = 1 / 120 * fT * Lp_s / R_c_N * n_strands * (n_strands - 1) * wBare / hBare # 60 works well for 290 K

            ## Adjust the components again on the new time constant
            alpha = 1 / np.sqrt((1 + (w * tau_is_N) ** 2))
            dB = w * f_magPerp_ht.T * alpha

            P_is = l_mag * beta_is_N * dB ** 2 * wBare * hBare
            I_is = beta_is_N * hBare * dB
            I_tot_im = I_is * alpha
            I_tot_re = abs(I_is * alpha * w * tau_is_N)
            I_is = I_tot_re + 1j * I_tot_im

            # Calculate equivalent parameter
            R_is = P_is/np.real((I_is*np.conjugate(I_is)))
            L_is = np.ones((len(f), 1)) * tau_is_N * R_is[0, :]
            M_is = (1j * w.reshape(len(f), 1) * L_is * I_is + I_is * R_is) / (1j * w.reshape(len(f), 1) * 1)
            # M_is = np.sqrt(np.real(M_is) ** 2 + np.imag(M_is) ** 2)

        # ## Calculate the return field
        # Assuming a current line on each side of the cable
        # Average distance to each strand is hence: (1/2*(dS_outer/2 + (nS/2-1)*dS_outer)), neglecting hBare
        # Twice, as we have one line on each side -> both generating the same field
        B_return = (2 * (mu0 * np.abs(I_is)) / np.pi * 1 / (1 / 2 * (dws / 2 + (n_strands / 2 - 1) * dws)))
        # dB_return = (B_return/tau_is)

        # f_mag_X_return_ht = r_magPerp_ht*np.cos(alphas_ht)-B_return.T*np.sin(alphas_ht)
        # f_mag_Y_return_ht = r_magPerp_ht*np.sin(alphas_ht)+B_return.T*np.cos(alphas_ht)
        ratio_Breturn = B_return / B_ht.T

        f_mag_X_return = np.zeros((len(f), fMag_X.shape[1]))
        f_mag_Y_return = np.zeros((len(f), fMag_Y.shape[1]))

        tempS = 0
        for i in range(len(n_strands)):
            f_mag_X_return[:, tempS:tempS + n_strands[i]] = np.transpose(ratio_Breturn[:, i] * fMag_X[:, tempS:tempS + n_strands[i]].T)
            f_mag_Y_return[:, tempS:tempS + n_strands[i]] = np.transpose(ratio_Breturn[:, i] * fMag_Y[:, tempS:tempS + n_strands[i]].T)
            # f_mag_X_return[:, tempS:tempS + nS[i]] = np.transpose(f_mag_X_all[:, tempS:tempS + nS[i]].T*0 + dB_return[:,i])
            # f_mag_Y_return[:, tempS:tempS + nS[i]] = np.transpose(f_mag_Y_all[:, tempS:tempS + nS[i]].T*0 + dB_return[:,i])
            tempS = tempS + n_strands[i]

        R_is = np.squeeze(R_is[:, idx_valid])
        L_is = np.squeeze(L_is[:, idx_valid])
        M_is = np.squeeze(M_is[:, idx_valid])
        I_is = np.squeeze(I_is[:, idx_valid])
        P_is = np.squeeze(P_is[:, idx_valid])

        L, R, M, Iis = bin_components(f, L_is, R_is, M_is, bins=bins, I=I_is)
        _, _, _, Pis = bin_components(f, L_is, R_is, M_is, bins=bins, I=P_is)
        I_des = np.sqrt(Pis / R)
        I = np.real(Iis) * I_des / abs(Iis) + 1j * np.imag(Iis) * I_des / abs(Iis)

        if flag_save:
            self.setAttribute(self.ISCC, 'M', M)
            self.setAttribute(self.ISCC, 'R', R)
            self.setAttribute(self.ISCC, 'L', L)
            self.setAttribute(self.ISCC, 'P', P_is)
            self.setAttribute(self.ISCC, 'I', I)
            if not self.Options.flag_SC:
                self.setAttribute(self.ISCC, 'tau', tau_is_N)
            else:
                self.setAttribute(self.ISCC, 'tau', tau_is)
        else:
            return L, R, M, f_mag_X_return, f_mag_Y_return


    def calculate_ED(self, frequency: np.ndarray, T: float, fMag: np.ndarray, flag_coupling: bool = True, flag_save: bool = False) -> np.ndarray:
        '''
        Calculates the equivalent coupling loops in the outer copper sheet for a given temperature and field

        :param frequency: Frequency vector
        :param T: temperature vector
        :param f_mag: field-factor for each strand
        '''

        f = frequency
        w = 2 * np.pi * f.reshape(len(f), 1)

        bins = self.General.bins
        l_mag = self.General.magnet_length
        RRR = self.Strands.RRR
        rws = self.Strands.diameter / 2
        strands_to_CS = self.Strands.strands_to_coil_sections

        if not self.Options.flag_SC:  # TODO - check if needed or not
            r_filamentary = self.Strands.d_filamentary / 2 * 0.5
        else:
            r_filamentary = self.Strands.d_filamentary / 2


        B = self.General.I_magnet * fMag
        rho_el_0 = self.rhoCu_nist(T=T, B=B[0, :], RRR=RRR) + 1e-12
        mu0 = 4 * np.pi / 10 ** 7  # mu0 = 4 * np.pi / 10 ** 7 / (1 - fsc)  #
        tb_strand = rws - r_filamentary
        idx_valid = np.where(strands_to_CS - 1 < strands_to_CS / 2)[0]
        rho_el_0 = rho_el_0 + 1e-12

        # Calculating time constant, correction factor and field derivative
        tau_ed = mu0 / 2 * ((rws) * tb_strand) / rho_el_0
        # tau_ed = mu0 / 8 * dS_outer**2 / rho_el_0 ## Formula from Turck79
        alpha = 1 / np.sqrt((1 + (w * tau_ed) ** 2))
        dB = w * fMag

        # Skindepth
        skinDepth = np.sqrt(2 * rho_el_0 / (w * mu0))
        idx_s = np.argmin(abs(skinDepth - (1 - 1 / np.exp(1)) * tb_strand), axis=0)

        # Calculating the power loss
        P_DC = ((rws) ** 4 - (r_filamentary) ** 4) * np.pi / (4 * rho_el_0) * (dB * alpha) ** 2  # Derivation, not assuming twist
        # P_DC = tau_ed/mu0/2 * (1-(dS_inner/dS_outer)**2) * (dB*alpha)**2 # Formula from Turck
        # P_DC = v3 * v1v2/(v1v2+1)*beta_if*(dB*alpha)**2 # Formula from Arjan's thesis

        P_AC = skinDepth ** 3 / (2 * rho_el_0) * dB ** 2 * np.pi * (rws)  # Standard derivation
        # P_AC = dB ** 2 * skinDepth/(w*4*mu0*dS_outer) #Formula from Turck1979

        P_tot = np.zeros((P_DC.shape))
        for j in range(P_DC.shape[1]):
            P_t = [P_DC[:idx_s[j], j], P_AC[idx_s[j]:, j]]
            P_tot[:, j] = np.concatenate(P_t).ravel()
        P_tot = P_tot * l_mag
        # Calculating the induced current
        I_tot = 2 * tb_strand / (3 * rho_el_0) * (tb_strand ** 2 - 3 * tb_strand * rws + 3 * rws ** 2) * (dB * alpha)
        I_tot_im = I_tot * alpha
        I_tot_re = I_tot * alpha * w * tau_ed
        #I_tot_re = np.sqrt(I_tot ** 2 - I_tot_im ** 2)
        I_tot = I_tot_re + 1j * I_tot_im

        P_tot = np.squeeze(P_tot[:, idx_valid])
        I_ed = np.squeeze(I_tot[:, idx_valid])
        tau_ed = tau_ed[idx_valid]

        # Calculating the coupled loop equivalent parameter
        R_ed = P_tot / np.real(I_ed * np.conjugate(I_ed))
        L_ed = np.ones((len(f), 1)) * tau_ed * R_ed[0, :]
        M_ed = (1j * w * L_ed * I_ed + I_ed * R_ed) / (1j * w * 1)
        # M_ed = np.real(M_ed) ** 2 + np.imag(M_ed) ** 2

        if not flag_coupling:
            L, R, M, Ied = bin_components(f, L_ed, R_ed, M_ed, bins=bins, I=I_ed)
            _, _, _, Ped = bin_components(f, L_ed, R_ed, M_ed, bins=bins, I=P_tot)
            I_des = np.sqrt(Ped / R)
            Ied = np.real(Ied) * I_des / abs(Ied) + 1j * np.imag(Ied) * I_des / abs(Ied)
        else:
            L, R, M = bin_components(f, L_ed, R_ed, M_ed, bins=bins)

        if flag_save:
            self.setAttribute(self.ED, 'M', M)
            self.setAttribute(self.ED, 'R', R)
            self.setAttribute(self.ED, 'L', L)
            self.setAttribute(self.ED, 'P', P_tot)
            self.setAttribute(self.ED, 'I', Ied)
            self.setAttribute(self.ED, 'tau', tau_ed)
        else:
            return L, R, M


    def calculate_Wedge(self, T: float):
        '''
        Function that calculates the equivalent parameter for eddy currents in the copper Wedge
        It takes the Temperature. It then calculates the resistivity and
        interpolates the current and power from pre-simulated values.

        '''
        rho_W = self.rhoCu_nist(T=T, RRR=self.Wedge.RRR_Wedge, B=np.array([0]))
        P_tot, I_tot, tau_W, frequency = self.interpolate(rho=rho_W, case='Wedge')
        w = 2 * np.pi * frequency
        P_tot = P_tot * self.General.magnet_length

        # Calculating the coupled loop equivalent parameter
        # R_W = P_tot / I_tot ** 2
        R_W = P_tot / np.real((I_tot * np.conjugate(I_tot)))
        L_W = tau_W * R_W[0]
        L_W = np.repeat(L_W, len(R_W))
        M_W = (1j * w * L_W * I_tot + I_tot * R_W) / (1j * w * 1)
        # M_W = np.sqrt(np.real(M_W*np.conjugate(M_W))) # Checked: is the same as the line below
        # M_W = np.sqrt(np.real(M_W) ** 2 + np.imag(M_W) ** 2)
        # M_W = np.transpose(np.ones(M_W.shape).transpose() * M_W


        self.setAttribute(self.Wedge, 'P', P_tot)
        self.setAttribute(self.Wedge, 'I', I_tot)
        self.setAttribute(self.Wedge, 'tau', tau_W)
        self.setAttribute(self.Wedge, 'L', L_W)
        self.setAttribute(self.Wedge, 'R', R_W)
        self.setAttribute(self.Wedge, 'M', M_W)

    def calculate_CB(self, T: float):
        '''
        Function that calculates the equivalent parameter for eddy currents in the cold bore.
        It takes the Temperature. It then calculates the resistivity and
        interpolates the current and power from pre-simulated values.
        '''

        rho_CB = self.rhoSS_nist(T=T)
        P_tot, I_tot, tau_CB, frequency = self.interpolate(rho=rho_CB, case='CB')
        w = 2 * np.pi * frequency
        P_tot = P_tot * self.General.magnet_length

        # Calculating the coupled loop equivalent parameter
        # R_W = P_tot / I_tot ** 2
        R_CB = P_tot / np.real((I_tot * np.conjugate(I_tot)))
        L_CB = tau_CB * R_CB[0]
        L_CB = np.repeat(L_CB, len(R_CB))
        M_CB = (1j * w * L_CB * I_tot + I_tot * R_CB) / (1j * w * 1)
        # M_W = np.sqrt(np.real(M_W*np.conjugate(M_W))) # Checked: is the same as the line below
        # M_W = np.sqrt(np.real(M_W) ** 2 + np.imag(M_W) ** 2)
        # M_W = np.transpose(np.ones(M_W.shape).transpose() * M_W
        self.setAttribute(self.CB, 'P', P_tot)
        self.setAttribute(self.CB, 'I', I_tot)
        self.setAttribute(self.CB, 'tau', tau_CB)
        self.setAttribute(self.CB, 'L', L_CB)
        self.setAttribute(self.CB, 'R', R_CB)
        self.setAttribute(self.CB, 'M', M_CB)


    def interpolate(self, rho: np.ndarray, case: str) -> np.ndarray:
        '''
        Helper function that takes a CPS group and temperature, fits the respective resistivity to it and interpolates from other resistivity values
        '''

        name = self.General.magnet_name
        path = Path(self.General.path_input_file).resolve()
        df_P = pd.read_csv(os.path.join(path, 'TFM_input', f'{name}_PowerLoss_{case}_Interpolation.csv')).dropna(axis=1)
        df_I = pd.read_csv(os.path.join(path, 'TFM_input', f'{name}_InducedCurrent_{case}_Interpolation.csv')).dropna(axis=1)
        frequency = df_P['f'].values[1:]
        resistivities = np.array(df_P.iloc[0, 1:]).astype(float)
        order = np.argsort(resistivities)
        resistivities = resistivities[order]

        P_temp = np.zeros((len(frequency),))
        I_temp_real = np.zeros((len(frequency),))
        I_temp_imag = np.zeros((len(frequency),))

        for i in range(len(frequency)):
            P_res = df_P.loc[df_P['f'] == frequency[i]].reset_index(drop=True).values[0][1:]
            P_res = P_res[order]
            P_temp[i] = np.interp(rho[0], resistivities, P_res)
            I_res = df_I.loc[df_I['f'] == frequency[i]].reset_index(drop=True).values[0][1::2]
            I_res = I_res[order]
            I_temp_real[i] = np.interp(rho[0], resistivities, I_res)
            I_res = df_I.loc[df_I['f'] == frequency[i]].reset_index(drop=True).values[0][2::2]
            I_res = I_res[order]
            I_temp_imag[i] = np.interp(rho[0], resistivities, I_res)
        I_tot = I_temp_real + 1j * I_temp_imag
        I_tot = np.real(np.sqrt(I_tot * np.conjugate(I_tot)))

        P_tot = P_temp

        tau_index = calculate_tau_index(P_tot=P_tot)
        tau = 1 / (frequency[tau_index])


        return P_tot, I_tot, tau, frequency

    def change_coupling_parameter(self, output_path: str, force_lib_path: Path = None):
        '''
        Main function of TFM_model
        Changes the equivalent coupling loop parameters for the MB magnet.

        :param T: measurement temperature
        :param output_path: path to save the generated lib file

        '''
        # HARDCODED f_rho_eff

        if output_path is not None:

            if force_lib_path:
                self.General.lib_path = Path(force_lib_path).resolve()
                self.General.new_lib_path = Path(output_path).resolve()
            else:
                self.General.lib_path = Path(self.General.lib_path).resolve()
                self.General.new_lib_path = Path(output_path).resolve()

            frequency = self.frequency
            bins = self.General.bins
            T = self.T
            f_rho_original = self.Strands.f_rho_effective
            f_mag_Roxie= self.Strands.f_mag_Roxie
            Mutual_dict = {}

            # Inter-Strands Coupling Currents
            if self.Options.flag_ISCC:
                f_mag_X_ISCC = self.Strands.f_mag_X_Roxie
                f_mag_Y_ISCC = self.Strands.f_mag_Y_Roxie
                L_ISCC, R_ISCC, M_ISCC, f_mag_X_ISCC_return, f_mag_Y_ISCC_return = self.calculate_ISCC(frequency=frequency, T=T, fMag_X=f_mag_X_ISCC, fMag_Y=f_mag_Y_ISCC, flag_save=False)
                self.calculate_ISCC(frequency=frequency, T=T, fMag_X=f_mag_X_ISCC, fMag_Y=f_mag_Y_ISCC, flag_save=True)
                self.General.lib_path = change_library_EqLoop(self.General.lib_path, 'ISCC', frequency, self.ISCC.L, self.ISCC.R, self.ISCC.M, bins=bins,
                                                 force_new_name=self.General.new_lib_path)

            # Persistent currents and magnetization
            if self.Options.flag_PC:
                self.setAttribute(self.Strands, 'f_rho_effective', f_rho_original)
                if self.Options.flag_ISCC:
                    f_mag_PC = np.maximum(f_mag_Roxie - np.sqrt(f_mag_X_ISCC_return ** 2 + f_mag_Y_ISCC_return ** 2), 1e-12)
                    L_PC_ISCC, I_PC_ISCC, M_PC_ISCC = self.calculate_PC(frequency=frequency, T=T, fMag=f_mag_PC, flag_coupling=False, flag_save=False)
                    Mutual_dict['M_PC_ISCC'] = M_PC_ISCC
                if self.Options.flag_ED:
                    L_PC_ED, I_PC_ED, M_PC_ED = self.calculate_PC(frequency=frequency, T=T, fMag=f_mag_Roxie, flag_coupling=True, flag_save=False)
                    Mutual_dict['M_PC_ED'] = M_PC_ED
                self.calculate_PC(frequency=frequency, T=T, fMag=f_mag_Roxie, flag_coupling=False, flag_save=True)
                self.General.lib_path = change_library_EqLoop(self.General.lib_path, 'PC', frequency, self.PC.L, np.array([]), self.PC.M, bins=bins,
                                                 force_new_name=self.General.new_lib_path)

            # Inter-Filament Coupling Currents
            if self.Options.flag_IFCC:
                self.setAttribute(self.Strands, 'f_rho_effective', f_rho_original*0.3)#Change rho_eff to 0.6
                if self.Options.flag_ISCC:
                    f_mag_IFCC = np.maximum(f_mag_Roxie - np.sqrt(f_mag_X_ISCC_return ** 2 + f_mag_Y_ISCC_return ** 2), 1e-12)
                    L_IFCC_ISCC, R_IFCC_ISCC, M_IFCC_ISCC = self.calculate_IFCC(frequency=frequency, T=T, fMag=f_mag_IFCC, flag_coupling=False, flag_save=False)
                    Mutual_dict['M_IFCC_ISCC'] = M_IFCC_ISCC
                if self.Options.flag_ED:
                    L_IFCC_ED, R_IFCC_ED, M_IFCC_ED = self.calculate_IFCC(frequency=frequency, T=T, fMag=f_mag_Roxie, flag_coupling=True, flag_save=False)
                    Mutual_dict['M_IFCC_ED'] = M_IFCC_ED
                self.calculate_IFCC(frequency=frequency, T=T, fMag=f_mag_Roxie, flag_coupling=False, flag_save=True)
                self.General.lib_path = change_library_EqLoop(self.General.lib_path, 'IFCC', frequency, self.IFCC.L, self.IFCC.R, self.IFCC.M, bins=bins,
                                                 force_new_name=self.General.new_lib_path)

            # Eddy currents in the copper sheath
            if self.Options.flag_ED:
                self.setAttribute(self.Strands, 'f_rho_effective', f_rho_original)
                if self.Options.flag_ISCC:
                    f_mag_ED = np.maximum(f_mag_Roxie - np.sqrt(f_mag_X_ISCC_return ** 2 + f_mag_Y_ISCC_return ** 2), 1e-12)
                    L_ED_ISCC, R_ED_ISCC, M_ED_ISCC = self.calculate_ED(frequency=frequency, T=T, fMag=f_mag_ED, flag_coupling=True, flag_save=False)
                    Mutual_dict['M_ED_ISCC'] = M_ED_ISCC

                self.calculate_ED(frequency=frequency, T=T, fMag=f_mag_Roxie, flag_coupling=False, flag_save=True)
                self.General.lib_path = change_library_EqLoop(self.General.lib_path, 'ED', frequency, self.ED.L, self.ED.R, self.ED.M, bins=bins,
                                                 force_new_name=self.General.new_lib_path)

            if self.Options.flag_Wedge:
                self.calculate_Wedge(T=T)
                self.General.lib_path = change_library_EqLoop(self.General.lib_path, 'Wedge', frequency, self.Wedge.L, self.Wedge.R, self.Wedge.M, bins=bins,
                                                              force_new_name=self.General.new_lib_path)
                M_W = self.calculate_Coupling_Components(Effect='Wedge')
                Mutual_dict.update(M_W)

            if self.Options.flag_CB:
                self.calculate_CB(T=T)
                self.General.lib_path = change_library_EqLoop(self.General.lib_path, 'CB', frequency, self.CB.L, self.CB.R, self.CB.M, bins=bins,
                                                              force_new_name=self.General.new_lib_path)
                M_CB = self.calculate_Coupling_Components(Effect='CB')
                Mutual_dict.update(M_CB)

            if len(Mutual_dict) != 0:
                self.calculate_Mutual_Coupling(Mutual_dict)

            attributes = [value for attr, value in vars(self.Options).items() if (attr != 'flag_SC' and attr != 'flag_BS')]

            # Check if all the flags of the effects in the Option class are True, in that case it means that the inductance matrix needs to be checked
            if all(value for value in attributes):
                self.check_inductance_matrix_losses(Mutual_dict)

            # Check if all the flags of the effects in the Option class are False, in that case it means that no lib file has been generated yet,
            # but since the Output path is not None we still need to generate it
            if all(not value for value in attributes):
                # The value to be sent to change_library_EqLoop needs to have the as .shape[1] the number of bins
                value = np.zeros((1, self.General.bins))
                self.General.lib_path = change_library_EqLoop(self.General.lib_path, 'ABC', value, value, value, value, bins=bins, force_new_name=self.General.new_lib_path)


    def calculate_Mutual_Coupling(self, Mutual_dict: dict):
        ''' This function calculates the Mutual Coupling between two different efefcts, starting from the M_coupled dictionary'''
        frequency = self.frequency
        bins = self.General.bins
        for key, value in Mutual_dict.items():
            first_effect = key.split('_')[-2]
            second_effect = key.split('_')[-1]
            M_first_effect = self.getAttribute(first_effect, 'M')
            I_second_effect = self.getAttribute(second_effect, 'I')
            if second_effect == 'Wedge' or second_effect == 'CB':
                # If the second effect is Wedge or CB, the I don't have the size [freq,bins], so it must be modified to have it
                I_second_effect = np.expand_dims(I_second_effect, axis=1)
                I_second_effect = np.repeat(I_second_effect, bins, axis=1)
            M_key = f'M_{first_effect}_{second_effect}'
            M_value = (M_first_effect - value) / I_second_effect

            for i in range(bins):
                self.General.lib_path = change_library_MutualCoupling(self.General.lib_path, f'{M_key}_{i + 1}', frequency, M_value[:, i])


    def calculate_Coupling_Components(self, Effect: str) -> dict:
        ''' This function calculates the Mutual Coupling between the conductor losses and the Effect
            Effect: Wedge or CB'''

        M_dict = {}
        # Retrieve f_mag, f_mag_X and f_mag_Y from the Comsol field files specific for each effect
        f_mag, f_mag_X, f_mag_Y = self.retrieve_field_contributions_COMSOL(Effect)
        frequency = self.frequency
        T = self.T

        # Retrieve the Option class attributes as dictionary
        options_dict = vars(self.Options)
        for flag, value in options_dict.items():
            if flag != 'flag_SC' and flag != 'flag_Wedge' and flag != 'flag_CB' and value == True:
                # If the flag of an effect is set and the effect is not 'CB' or 'Wedge', takes the name of the effect
                eff_coupled = flag.split('_')[-1]
                if eff_coupled == 'ISCC':
                    # Calls the calculate function of the corresponding effect and calculates the M
                    _, _, M, _, _ = getattr(self, f'calculate_{eff_coupled}')(frequency=frequency, T=T, fMag_X=f_mag_X, fMag_Y=f_mag_Y, flag_save=False)
                else:
                    # Calls the calculate function of the corresponding effect and calculates the M
                    _, _, M = getattr(self, f'calculate_{eff_coupled}')(frequency=frequency, T=T, fMag=f_mag, flag_coupling=True, flag_save=False)
                # Save the new M in the dictionary
                M_dict[f'M_{eff_coupled}_{Effect}'] = M

        return M_dict

    def read_COMSOL_field_file(self, Effect: str = None) -> np.ndarray:
        '''
        '''

        f_mag_X_Roxie = self.Strands.f_mag_X_Roxie
        f_mag_Y_Roxie = self.Strands.f_mag_Y_Roxie
        f_mag_X_Comsol = self.Strands.f_mag_X_Comsol
        f_mag_Y_Comsol = self.Strands.f_mag_Y_Comsol

        if Effect is not None:
            _, f_mag_X_all, f_mag_Y_all = self.retrieve_field_contributions_COMSOL(Effect=Effect)

            f_X_diff = f_mag_X_all * np.sign(f_mag_X_Roxie) - f_mag_X_Comsol
            f_Y_diff = f_mag_Y_all * np.sign(f_mag_Y_Roxie) - f_mag_Y_Comsol

            f_X = f_mag_X_Roxie + f_X_diff
            f_Y = f_mag_Y_Roxie + f_Y_diff
            f_mag = np.sqrt(f_X ** 2 + f_Y ** 2)

            return f_mag, f_X, f_Y


    def retrieve_field_contributions_COMSOL(self, Effect: str = None) -> np.ndarray:
        '''
        Retrieve the strand field contributions, simulated by COMSOL and saved in .csv
        :return: f_mag
        '''

        local_library_path = os.path.join(Path(self.General.path_input_file).resolve(), 'TFM_input')
        value = self.Field_interp_value
        frequency = self.frequency

        Param = []
        files_Field = []
        df_array_X = []
        df_array_Y = []

        if value is None:
            value = self.T

        for dir in os.listdir(local_library_path):
            if dir.startswith('Field_Map'):
                if Effect in dir:
                    parameter = dir.replace('.csv','').split('_')[-1]
                    Param.append(float(parameter))
                    files_Field.append(dir)

        Param = np.array(Param)
        files_Field = np.array(files_Field)

        if float(value) in Param:
            closest_Param = np.array([value])
        elif(value < Param.min() or value > Param.max()):
            raise Exception('Error: Parameter out of range')
        else:
            closest_indices = np.argsort(np.abs(Param - value))[:4]
            closest_Param = Param[closest_indices]

        for i in range(len(closest_Param)):
            file = os.path.join(local_library_path, files_Field[i])
            df_COMSOL = pd.read_csv(file, header=None, dtype=str, na_filter=False)
            mapping = np.vectorize(lambda t: complex(t.replace('i', 'j')))
            df_COMSOL = mapping(df_COMSOL.values[2:, 2:]).T
            df_X = np.real(df_COMSOL[::2, :] * np.conjugate(df_COMSOL[::2, :]))
            df_Y = np.real(df_COMSOL[1::2, :] * np.conjugate(df_COMSOL[1::2, :]))
            df_array_X.append(df_X)
            df_array_Y.append(df_Y)

        order = np.argsort(closest_Param)
        closest_Param = closest_Param[order]

        # Interpolate the X and Y direction for a given rho
        df_array_X = np.array(df_array_X)
        df_array_X = df_array_X[order]
        df_array_Y = np.array(df_array_Y)
        df_array_Y = df_array_Y[order]


        if len(closest_Param) != 1:
            interp_X = RegularGridInterpolator((closest_Param, frequency), df_array_X)
            new_points_X = (np.array([value]), frequency) # value = Parameter to interpolate for = input
            f_mag_X = interp_X(new_points_X)

            interp_Y = RegularGridInterpolator((closest_Param, frequency), df_array_Y)
            new_points_Y = (np.array([value]), frequency)
            f_mag_Y = interp_Y(new_points_Y)
        else:
            f_mag_X = df_array_X[0, :, :]
            f_mag_Y = df_array_Y[0, :, :]

        f_mag = np.sqrt(f_mag_X + f_mag_Y)
        f_mag_X = np.sqrt(f_mag_X)
        f_mag_Y = np.sqrt(f_mag_Y)

        return f_mag, f_mag_X, f_mag_Y


    def retrieve_field_contributions_Roxie(self) -> np.ndarray:

        Bx = self.LedetAuxiliary.Bx
        By = self.LedetAuxiliary.By
        Iref = self.LedetOptions.Iref

        f_mag_X = Bx / Iref
        f_mag_Y = By / Iref
        B_E = np.sqrt(Bx ** 2 + By ** 2)

        f_mag = np.sqrt(f_mag_X ** 2 + f_mag_Y ** 2)
        peakB_superPos = np.max(f_mag * Iref)
        peakB_real = np.max(B_E)
        f_peakReal_Superposition = peakB_real / peakB_superPos

        f_mag_X_all = f_mag_X * f_peakReal_Superposition
        f_mag_Y_all = f_mag_Y * f_peakReal_Superposition

        frequency = np.logspace(0, 6, 120+1)
        self.frequency=frequency
        f_mag_X_all = np.repeat(f_mag_X_all[:, np.newaxis], len(frequency), axis=1).T
        f_mag_Y_all = np.repeat(f_mag_Y_all[:, np.newaxis], len(frequency), axis=1).T
        f_mag = np.repeat(f_mag[:, np.newaxis], len(frequency), axis=1).T

        return f_mag, f_mag_X_all, f_mag_Y_all

    def check_inductance_matrix_losses(self, Mutual_dict: dict):

        frequency = self.frequency
        bins = self.General.bins
        options_dict = vars(self.Options)
        Effects = []
        # Looping through all the attributes in the Option class to get the Effects name
        for flag, value in options_dict.items():
            if flag != 'flag_SC' and flag != 'flag_BS':
                Effect = flag.split('_')[-1]
                Effects.append(Effect)
        Effects = np.repeat(np.array(Effects), bins)
        Effects = np.insert(Effects, 0, 'Mag').astype(str)
        L_matrix_list = []

        for freq in range(len(frequency)):
            # Creating the matrix and filling it with 0
            L_matrix = np.zeros((len(Effects), len(Effects)))
            for eff in range(len(Effects)):
                    if eff == 0:  # Checking if the Effect[eff] == 'Mag'
                        L_matrix[0, 0] = self.General.L_mag
                    else:
                        if Effects[eff-1] == Effects[eff]: # Checking if it's not the first time that we encounter this effect in the dict
                            count_bin += 1  # If it's not the first time, the bin counting must be incremented
                        else:
                            count_bin = 0  # If it is the first time, the bin counting is set to zero

                        # Filling the matrix with the L values along the diagonal and the M values symmetrically
                        # on the first row and on the first column, selecting the right values according to count_bin
                        if Effects[eff] == 'Wedge' or Effects[eff] == 'CB':
                            L_matrix[0, eff] = self.getAttribute(Effects[eff], 'M')[freq]
                            L_matrix[eff, 0] = self.getAttribute(Effects[eff], 'M')[freq]
                            L_matrix[eff, eff] = self.getAttribute(Effects[eff], 'L')[freq]
                        else:
                            L_matrix[0, eff] = self.getAttribute(Effects[eff], 'M')[freq, count_bin]
                            L_matrix[eff, 0] = self.getAttribute(Effects[eff], 'M')[freq, count_bin]
                            L_matrix[eff, eff] = self.getAttribute(Effects[eff], 'L')[freq, count_bin]

                        for key, value in Mutual_dict.items():
                            if Effects[eff] in key:  # For each key of the dict, check if the current effect is contained in it
                                for l in range(len(Effects)):  # If yes, find the other effect contained in the same key
                                    if l != 0 and eff != l and Effects[l] in key:
                                        if Effects[l - 1] != Effects[l]:
                                            # Take the first effect with that name and then select the right column index
                                            # and the right value by selecting the same count_bin of the Effects[eff] element
                                            L_matrix[eff, l+count_bin] = value[freq, count_bin]
            L_matrix_list.append(L_matrix)

        for i in range(len(L_matrix_list)):
            if not is_positive_definite(L_matrix_list[i]):
                raise Exception(f'Matrix not positive definite for frequency {frequency[i]}')


    def rhoCu_nist(self, T: float, RRR: np.ndarray, B: np.ndarray) -> np.ndarray:
        '''
        Helper function to calculate resistivity of copper. Taken from steam-materials library

        :param T: Temperature
        :return: array of resistivities
        '''

        T_ref_RRR = 273
        # Make T of the same size of B and RRR
        T_flatten = np.tile(T, (len(B), 1)).flatten()
        # Create numpy2d by stacking B, RRR, and T along axis 0
        numpy2d = np.vstack((T_flatten, B, RRR, T_ref_RRR * np.ones_like(T_flatten)))
        sm_cp_rho = STEAM_materials('CFUN_rhoCu_v1', numpy2d.shape[0], numpy2d.shape[1], matpath)
        RhoCu = sm_cp_rho.evaluate(numpy2d)

        return RhoCu

    def rhoSS_nist(self, T: float) -> np.ndarray:
        '''
        Helper function to calculate resistivity of copper. Taken from steam-materials library

        :param T: Temperature
        :return: array of resistivities
        '''
        T_flatten = np.tile(T, (1)).flatten()
        # Create numpy2d by stacking B, RRR, and T along axis 0
        sm_cp_rho = STEAM_materials('CFUN_rhoSS_v1', 1, 1, matpath)
        RhoSS = sm_cp_rho.evaluate(T_flatten)

        return RhoSS

    def setAttribute(self, TFMclass, attribute: str, value):
        try:
            setattr(TFMclass, attribute, value)
        except:
            setattr(getattr(self, TFMclass), attribute, value)


    def getAttribute(self, TFMclass, attribute: str):
        try:
            return getattr(TFMclass, attribute)
        except:
            return getattr(getattr(self, TFMclass), attribute)

def lookupModelDataToTFMHalfTurns(key: str):
    """
           Retrieves the correct HalfTurnsTFM parameter name for a DataModelMagnet input
    """
    lookup = {
        'nStrands_inGroup': 'n_strands',
        'wBare_inGroup': 'bare_cable_width',
        'hBare_inGroup': 'bare_cable_height_mean',
        'Lp_s_inGroup': 'strand_twist_pitch',
        'R_c_inGroup': 'Rc',
        'RRR_Cu_inGroup': 'RRR',
        'ds_inGroup': 'diameter',
        'f_SC_strand_inGroup': 'fsc',
        'f_ro_eff_inGroup': 'f_rho_effective',

        'alphasDEG': 'alphaDEG_ht',
        'rotation_block': 'rotation_ht',
        'mirror_block': 'mirror_ht'
    }

    returned_key = lookup[key] if key in lookup else None
    return returned_key


def lookupModelDataToTFMStrands(key: str):
    """
           Retrieves the correct StrandsTFM parameter name for a DataModelMagnet input
    """
    lookup = {
        'df_inGroup': 'filament_diameter',
        'ds_inGroup': 'diameter',
        'f_SC_strand_inGroup': 'fsc',
        'f_ro_eff_inGroup': 'f_rho_effective',
        'Lp_f_inGroup': 'fil_twist_pitch',
        'RRR_Cu_inGroup': 'RRR',
        'dfilamentary_inGroup': 'd_filamentary',
        'dcore_inGroup': 'd_core',
    }

    returned_key = lookup[key] if key in lookup else None
    return returned_key


def bin_components(frequency: np.ndarray, L: np.ndarray, R: np.ndarray, M: np.ndarray, bins: int, sort_on: str = 'L',
                   I: np.ndarray = np.array([]), flag_PC:bool=False) -> np.ndarray:
    '''
    Helper function that bins components into n bins, based on a sorting on a specific variable out of R,L,M

    :param frequency: frequency vector
    :param L: L-vector
    :param R: R-vector
    :param M: M_vector
    :param bins: number of bins to be separated
    :param sort_on: Which variable to sort on
    :return: 3 np.ndarray in the order: L,R,M that are binned into n_bins
    '''

    if sort_on == 'L':
        if np.all(np.isclose(L, L[0, 0])):
            sort_on = 'R_bin'
        else:
            sort_on = 'L_bin'
    elif sort_on == 'R':
        sort_on = 'R_bin'
    elif sort_on == 'M':
        sort_on = 'M_bin'
    else:
        raise Exception(f'Do not understand sort_on: {sort_on} - Only R, L, M')

    f = frequency
    R_bin = np.zeros((len(f), bins))
    M_bin = np.zeros((len(f), bins), dtype=np.complex_)
    s_r = np.zeros((len(f), bins))
    s_i = np.zeros((len(f), bins))
    L_bin = np.zeros((len(f), bins))
    I_bin = np.zeros((len(f), bins), dtype=np.complex_)
    for j in range(len(f)):
        # Bin the resistivities and take the mean of their M
        df = pd.DataFrame.from_dict({'R_bin': np.nan_to_num(R[j, :])})
        df['M_bin'] = np.nan_to_num(M[j, :])
        df['L_bin'] = np.nan_to_num(L[j, :])
        if len(I) != 0:
            df['I_bin'] = np.nan_to_num(I[j, :])
        x = pd.cut(df[sort_on], np.linspace(min(df[sort_on]) * 0.9, max(df[sort_on]) * 1.1, bins + 1))
        x = x.cat.rename_categories(np.linspace(1, bins, bins).astype(int))
        df['bins'] = x
        df = df.dropna(subset=['bins'])

        for i in range(1, bins + 1):
            df.loc[df['bins'] == i, 'R_bin'] = np.average(df.loc[df['bins'] == i, 'R_bin'])
            df.loc[df['bins'] == i, 'L_bin'] = np.average(df.loc[df['bins'] == i, 'L_bin'])
            if len(I) != 0:
                df.loc[df['bins'] == i, 'I_bin'] = np.sum(df.loc[df['bins'] == i, 'I_bin'])
            # df.loc[df['bins'] == i, 'R_bin'] = np.nanmedian(df.loc[df['bins'] == i, 'R_bin'])
            # df.loc[df['bins'] == i, 'L_bin'] = np.nanmedian(df.loc[df['bins'] == i, 'L_bin'])
            M_sel = df.loc[df['bins'] == i, 'M_bin']
            s_r[j, bins - i] = np.mean(np.round(np.sign(np.real(M_sel))), 0)
            s_i[j, bins - i] = np.mean(np.round(np.sign(np.imag(M_sel))), 0)
            if flag_PC:
                df.loc[df['bins'] == i, 'M_bin'] = np.sqrt(np.sum(M_sel))
            else:
                df.loc[df['bins'] == i, 'M_bin'] = np.sqrt(np.sum(M_sel ** 2))
        df = df.drop_duplicates().reset_index(drop=True).drop('bins', axis=1)
        df = df.loc[~(df == 0).all(axis=1)]

        R_bin[j, :] = df['R_bin']
        M_bin[j, :] = df['M_bin']
        L_bin[j, :] = df['L_bin']
        if len(I) != 0:
            I_bin[j, :] = df['I_bin']

    M_bin = s_r * abs(np.real(M_bin)) + 1j * s_i * abs(np.imag(M_bin))
    if len(I) != 0:
        return L_bin, R_bin, M_bin, I_bin
    else:
        return L_bin, R_bin, M_bin


def change_library_EqLoop(path_file: Path, element: str, frequency: np.ndarray, L_eq: np.ndarray, R_eq: np.ndarray, M_eq: np.ndarray, bins: int = 2, force_new_name: Path = ''):
    '''
    Helper function that changes the TFM magnet .lib file and includes in Table function the given R,L,M parameter

    element = Element, for which the RLM to be inserted e.g. BS, CPS, ED ...

    If L_eq, M_eq or R_eq are empty, they will not be written
    '''
    if bins==1:
        if L_eq.size: L_eq = L_eq.reshape((len(L_eq), 1))
        if R_eq.size: R_eq = R_eq.reshape((len(R_eq), 1))
        if M_eq.size: M_eq = M_eq.reshape((len(M_eq), 1))


    #### Creating string for equivalent inductance
    str_L = []
    if L_eq.size:
        for i in range(bins):
            str_group_L = f'.FUNC L_{element}_{i+1}(1)					'+'{TABLE{FREQ} =  '
            L = L_eq[:,i]
            for j in range(len(frequency)):
                str_group_L = str_group_L + f'({frequency[j]},{L[j]})     '
            str_group_L = str_group_L + '}\n'
            str_L.append(str_group_L)

    #### Creating string for equivalent resistance
    str_R = []
    if R_eq.size:
        for i in range(bins):
            str_group_R = f'.FUNC R_{element}_{i + 1}(1)					' + '{TABLE{FREQ} =  '
            R = R_eq[:, i]
            for j in range(len(frequency)):
                str_group_R = str_group_R + f'({frequency[j]},{R[j]})     '
            str_group_R = str_group_R + '}\n'
            str_R.append(str_group_R)

    #### Creating string for equivalent mutual inductance
    str_M = []
    if M_eq.size:
        for i in range(bins):
            str_group_M = f'.FUNC M_{element}_{i + 1}(1)					' + '{TABLE{FREQ} =  '
            M = M_eq[:, i]
            for j in range(len(frequency)):
                str_group_M = str_group_M + f'({frequency[j]},{np.real(M[j])}+{np.imag(M[j])}J)     '
            str_group_M = str_group_M + '}\n'
            str_M.append(str_group_M)

    ## Opening library file
    lib_path = path_file
    with open(lib_path) as f:
        lines = f.readlines()

    ## Changing elements in library
    for k in range(len(lines)):
        line = lines[k]
        for i in range(bins):
            if line.startswith(f'.FUNC L_{element}_{i+1}') and str_L:
                lines[k] = str_L[i]
            elif line.startswith(f'.FUNC R_{element}_{i+1}') and str_R:
                lines[k] = str_R[i]
            elif line.startswith(f'.FUNC M_{element}_{i+1}') and str_M:
                lines[k] = str_M[i]

    text_lib = ''.join(lines)

    if not force_new_name:
        new_lib_path = Path('..//lib//MB_TFM_General_Adjusted.lib').resolve()
    else:
        new_lib_path = force_new_name
    with open(new_lib_path, 'w') as f:
        f.write(text_lib)
    return new_lib_path

def change_library_MutualCoupling(path_file: Path, element: str, frequency: np.ndarray, M_eq: np.ndarray):
    '''
    Helper function that changes the mutual coupling values of element to M_eq. Can be multiple values, e.g. a
    changing coupling over frequency
    '''

    #### Creating string for equivalent mutual inductance
    str_group_M = f'.FUNC {element}(1)					' + '{TABLE{FREQ} =  '
    for j in range(len(frequency)):
        str_group_M = str_group_M + f'({frequency[j]},{np.real(M_eq[j])}+{np.imag(M_eq[j])}J)     '
    str_group_M = str_group_M + '}\n'

    ## Opening library file
    lib_path = path_file
    with open(lib_path) as f:
        lines = f.readlines()

    ## Changing elements in library
    for k in range(len(lines)):
        line = lines[k]
        if line.startswith(f'.FUNC {element}'):
            lines[k] = str_group_M

    text_lib = ''.join(lines)

    with open(path_file, 'w') as f:
        f.write(text_lib)
    return path_file

def smooth_curve(y: np.ndarray, box_pts: int, n_pad: int = 20) -> np.ndarray:
    '''
    Helper function that smoothes a curve with a box filter
    :param y: np.ndarray - Array to be smoothed
    :param box_pts: int - width of the box filter (generally 3 or 5)
    :param n_pad: int - width of zero-padding
    :return: the smoothed array
    '''
    box = np.ones(box_pts) / box_pts
    if len(y.shape)>1:
        y_smooth = np.zeros(y.shape)
        for i in range(y.shape[0]):
            y_padded = np.pad(y[i,:], n_pad, mode='constant',constant_values=(y[i,0],y[i,-1]))
            y_filtered = np.convolve(y_padded, box, mode='same')
            y_smooth[i, :] = y_filtered[n_pad:-n_pad]
    else:
        y_padded = np.pad(y, n_pad, mode='constant', constant_values=(y[0], y[-1]))
        y_smooth = np.convolve(y_padded, box, mode='same')
    return y_smooth[n_pad: -n_pad]


def calculate_tau_index(P_tot: np.ndarray) -> int:

    # Calculate first derivative
    dPdt = np.diff(P_tot) / P_tot[1:]
    # Calculate second derivative
    dPdt2 = np.diff(dPdt) / dPdt[1:]
    sm_dPdt2 = smooth_curve(dPdt2, 5, n_pad=1)
    # # Find first peak using specified thresholds to avoid choosing peaks due to noise
    min_peak_height = 0.02
    min_peak_prominence = 0.02
    idx_first_min = find_peaks(-sm_dPdt2, height=min_peak_height, prominence=min_peak_prominence)[0][0]
    # Calculate the sign of sm_dPdt2 after the first index to check the first time sm_dPst2 crosses 0 after the first minimum
    # and calculate tau
    sign = np.sign(sm_dPdt2)[idx_first_min:]
    indices = np.where((sign[:-1] < 0) & (sign[1:] > 0))[0][0] - 1
    tau_index = indices + idx_first_min - 1 - (len(P_tot) - len(sm_dPdt2))
    # Check for plateaus in sm_dPdt2
    plateau_indices = np.where(np.diff(sm_dPdt2) <= 0.0003)[0]
    if tau_index in plateau_indices:
        list_index = []
        index = np.where(plateau_indices == tau_index)[0][0]
        # Take the left part of the plateau (respect to tau_index) and reverse it
        plateau_indices_left = plateau_indices[:index][::-1]
        # Take the values which are -1 or -2 comparing to the previous value
        for i in range(len(plateau_indices_left)):
            if i == 0:
                list_index.append(plateau_indices_left[i])
            elif (plateau_indices_left[i - 1] - plateau_indices_left[i] <= 2):
                list_index.append(plateau_indices_left[i])
            else:
                break
        # Take the right part of the plateau (respect to tau_index)
        plateau_indices_right = plateau_indices[index + 1:]
        # Take the values which are +1 or +2 comparing to the previous value
        for i in range(len(plateau_indices_right)):
            if i == 0:
                list_index.append(plateau_indices_right[i])
            elif (plateau_indices_right[i] - plateau_indices_right[i - 1] <= 2):
                list_index.append(plateau_indices_right[i])
            else:
                break
        tau_index = int((np.min(list_index) + np.max(list_index)) / 2)

    return tau_index


def is_positive_definite(matrix):
    return np.all(np.linalg.eigvals(matrix) >= 0)


