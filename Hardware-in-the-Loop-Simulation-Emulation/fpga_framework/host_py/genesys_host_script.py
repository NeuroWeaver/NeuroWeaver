

"""Genesys Host Script: Top level script for calling functions to forward execution to FPGA"""

from genesys_driver import GenesysDriver

def execute_on_fpga(driver:GenesysDriver)
    driver.init_buffers_b2b()
