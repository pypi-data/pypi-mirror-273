# import classes from the esbmtk library
from esbmtk import (
    Model,  # the model class
    Species,  # the reservoir class
    Species2Species,  # the connection class
    Source,  # the source class
    Sink,  # sink class
    Q_,  # Quantity operator
)

# define the basic model parameters
M = Model(
    stop="3 Myr",  # end time of model
    timestep="1 kyr",  # upper limit of time step
    element=["Phosphor"],  # list of element definitions
)

# boundary conditions
F_w =  M.set_flux("45 Gmol", "year", M.P) # P @280 ppm (Filipelli 2002)
tau = Q_("100 year")  # PO4 residence time in surface boxq
F_b = 0.01  # About 1% of the exported P is buried in the deep ocean
thc = "20*Sv"  # Thermohaline circulation in Sverdrup

# Source definitions
Source(
    name="weathering",
    species=M.PO4,
    register=M,  # i.e., the instance will be available as M.weathering
)
Sink(
    name="burial",
    species=M.PO4,
    register=M,  #
)

# reservoir definitions
Species(
    name="S_b",  # box name
    species=M.PO4,  # species in box
    register=M,  # this box will be available as M.S_b
    volume="3E16 m**3",  # surface box volume
    concentration="0 umol/l",  # initial concentration
)
Species(
    name="D_b",  # box name
    species=M.PO4,  # species in box
    register=M,  # this box will be available M.D_b
    volume="100E16 m**3",  # deeb box volume
    concentration="0 umol/l",  # initial concentration
)

Species2Species(
    source=M.weathering,  # source of flux
    sink=M.S_b,  # target of flux
    rate=F_w,  # rate of flux
    id="river",  # connection id
    ctype="regular",
)

Species2Species(  # thermohaline downwelling
    source=M.S_b,  # source of flux
    sink=M.D_b,  # target of flux
    ctype="scale_with_concentration",
    scale=thc,
    id="downwelling_PO4",
    # ref_reservoirs=M.S_b, defaults to the source instance
)
Species2Species(  # thermohaline upwelling
    source=M.D_b,  # source of flux
    sink=M.S_b,  # target of flux
    ctype="scale_with_concentration",
    scale=thc,
    id="upwelling_PO4",
)

Species2Species(  #
    source=M.S_b,  # source of flux
    sink=M.D_b,  # target of flux
    ctype="scale_with_concentration",
    scale=M.S_b.volume / tau,
    id="primary_production",
)

Species2Species(  #
    source=M.D_b,  # source of flux
    sink=M.burial,  # target of flux
    ctype="scale_with_flux",
    ref_flux=M.flux_summary(filter_by="primary_production", return_list=True)[0],
    scale=F_b,
    id="burial",
)

M.run()
M.plot([M.S_b, M.D_b])
M.save_data()
