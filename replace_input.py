import numpy as np
import importlib.util
import os

template_dir = "/ptmp/mpa/ankitad/athenapk/turb_template"
input_path = os.path.join(template_dir, "input.py")

spec = importlib.util.spec_from_file_location("input", input_path)
inp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inp)


def tag_replace(filedata, tag, value):
    return filedata.replace(tag, str(value))

def athinput_replace(template_data):
    template_data = tag_replace(template_data, "!!NX1!!", inp.nx_box[0])
    template_data = tag_replace(template_data, "!!NX2!!", inp.nx_box[1])
    template_data = tag_replace(template_data, "!!NX3!!", inp.nx_box[2])

    template_data = tag_replace(template_data, "!!NX_MB1!!", inp.nx_mb[0])
    template_data = tag_replace(template_data, "!!NX_MB2!!", inp.nx_mb[1])
    template_data = tag_replace(template_data, "!!NX_MB3!!", inp.nx_mb[2])

    template_data = tag_replace(template_data, "!!L_BOX!!", inp.L_box)
    template_data = tag_replace(template_data, "!!RHO0!!", inp.rho0)
    template_data = tag_replace(template_data, "!!T_FLOOR!!", inp.T_floor)
    template_data = tag_replace(template_data, "!!P0!!", inp.p0)
    template_data = tag_replace(template_data, "!!P_FLOOR!!", inp.p_floor)
    template_data = tag_replace(template_data, "!!K_PEAK!!", inp.k_peak)
    template_data = tag_replace(template_data, "!!CORR_TIME!!", inp.corr_time)
    template_data = tag_replace(template_data, "!!ACCEL_RMS!!", inp.accel_rms)
    template_data = tag_replace(template_data, "!!TLIM!!", inp.tlim)
    template_data = tag_replace(template_data, "!!DT_HST!!", inp.dt_hst)
    template_data = tag_replace(template_data, "!!DT_HDF!!", inp.dt_hdf)
    template_data = tag_replace(template_data, "!!DT_RST!!", inp.dt_rst)
    template_data = tag_replace(template_data, "!!COOL!!", inp.enable_cool)
    template_data = tag_replace(template_data, "!!RESCALE_TIME!!", inp.rescale_time)
    template_data = tag_replace(template_data, "!!RESCALE_Ms!!", inp.rescale_Ms)
    template_data = tag_replace(template_data, "!!GLOBAL_HEAT!!", inp.global_heat)

    

    return template_data

