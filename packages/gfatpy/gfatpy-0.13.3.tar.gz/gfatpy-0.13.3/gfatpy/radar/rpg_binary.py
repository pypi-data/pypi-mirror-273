from pathlib import Path
import numpy as np

from rpgpy import read_rpg
from rpgpy.spcutil import scale_spectra

class rpg():
    def __init__(self, path: Path):
        self.path = path        
        self.type = path.name.split(".")[0].split("_")[-1]
        self.level = int(path.name.split(".")[-1][-1])
        self._raw = None
        self._header = None
        self._data = None

    @property
    def raw(self) -> dict:
        if self._raw is None:            
            _, self._raw = read_rpg(self.path)
        return self._raw
    
    @property
    def header(self) -> dict:
        if self._header is None:            
            self._header, _ = read_rpg(self.path)
        return self._header

    @property
    def data(self) -> dict:
        if self._data is None:            
            self._data = self.enhanced_data(self.header, self.raw)
        return self._data

    @classmethod
    def enhanced_data(cls, header: dict, raw: dict) -> dict:
        data = raw.copy()        
        spec_tot = scale_spectra(raw["TotSpec"], header["SWVersion"])
        data['VSpec'] = spec_tot - raw["HSpec"] - 2 * raw["ReVHSpec"]
        data['sZDR'] = 10*np.log10(data['HSpec']) - 10*np.log10(data['VSpec'])        
        data['sZDRmax'] = np.max(data['sZDR'], axis=2)
        return data
    
    # def merge_chirps(self) -> dict:
    #     if self.level == 0:
    #         data = merge_chirps_lv0(self.header, self.raw)
    #     return data


    # def plot(self, variable: str | None = None, **kwargs):        
    #     if self.type == "ZEN":
    #         self.plot_zen(variable, **kwargs)
    #     elif self.type == "PPI":
    #         self.plot_ppi(variable, **kwargs)
    #     elif self.type == "RHI":
    #         self.plot_rhi(variable, **kwargs)
    #     else:
    #         raise ValueError(f"Type {self.type} is not valid")

    # def plot_zen(self, variable: str | list[str] | None = None, **kwargs):
        
    #     range_limits = kwargs.get('range_limits', (0, 12.))
        
        
    #     if variable is None:
    #         variables_to_plot = ["dBZe"]
    #     if isinstance(variable, str):
    #         variables_to_plot = [variable]
    #     elif isinstance(variable, list):
    #         variables_to_plot = variable
    #     else:
    #         raise ValueError(f"Variable {variable} is not valid")        
        
    #     data = self.data
    #     data['range'] = data['range']/1e3
    #     list_of_figs, list_of_paths = [], []        
    #     for var in variables_to_plot:
    #         if var not in self.data:
    #             raise ValueError(f"Variable {var} is not in the file")
            
    #         vmin, vmax = RADAR_PLOT_INFO['limits'][var]
    #         fig, ax = plt.subplots(
    #             figsize=(10, 7)
    #         )  # subplot_kw=dict(projection='polar')

    #         pcm = self.data[f"{var}"].plot(x='time', ax=ax, vmin=vmin, vmax=vmax)
            
    #         ax.set_xlabel("Time, [UTC]")
    #         ax.set_ylim(*range_limits)
    #         ax.set_ylabel("Range, [km]")

    #         #Get current colorbar and shrink it 0.7, and set 'units' as label
            

    #         # cbar = plt.colorbar(pcm, ax=ax, shrink=0.7)
    #         if "units" in data[var].attrs:
    #             units = data[var].attrs['units']
    #         else:
    #             units = "?"
    #         pcm.set_label(f"{var}, [{units}]")
            
    #         ax.set_title(f"{data.time.values[0]}")            
            
    #         fig.tight_layout()
    #         list_of_figs.append(fig)
    #         if kwargs.get('savefig', False):
    #             output_dir = kwargs.get("output_dir", Path.cwd())   
    #             filepath = output_dir / self.path.name.replace(".nc", f"_{var}.png")
    #             dpi = kwargs.get("dpi", 300)    
    #             fig.savefig(filepath, dpi=dpi)
    #             plt.close(fig)
    #             list_of_paths.append(filepath)
    #     return list_of_figs, list_of_paths


    # def plot_ppi(self, variable: str | None = None, **kwargs) -> tuple[list[Figure], list[Path]]:
    #     if variable is None:
    #         variables_to_plot = ["dBZe"]
    #     elif isinstance(variable, str):
    #         variables_to_plot = [variable]
    #     elif isinstance(variable, list):
    #         variables_to_plot = variable
    #     else:
    #         raise ValueError(f"Variable {variable} is not valid")

    #     # sort data['azimuth'] as increasing and sort the rest of the data accordingly
    #     data = self.data.sortby("azimuth")
    #     x, y = ppi_to_cartessian(data["range"], data["azimuth"], data["elevation"])
    #     mdata = data.mean(dim="time")
    #     list_of_figs, list_of_paths = [], []
    #     for var in variables_to_plot:
    #         if var not in mdata:
    #             raise ValueError(f"Variable {var} is not in the file")
    #         vmin, vmax = RADAR_PLOT_INFO["limits"][var]
    #         fig, ax = plt.subplots(
    #             figsize=(10, 10)
    #         )  # subplot_kw=dict(projection='polar')
    #         pcm = ax.pcolormesh(
    #             x/1e3, y/1e3, data[var].values.T, vmin=vmin, vmax=vmax, shading="gouraud"
    #         )
    #         #Include title with time and elevation angle
    #         ax.set_xlim(*RADAR_PLOT_INFO["limits"]["ppi"]["x"])
    #         ax.set_ylim(*RADAR_PLOT_INFO["limits"]["ppi"]["y"])
    #         ax.set_xlabel("East-West distance from radar [km]")
    #         ax.set_ylabel("North-South distance from radar [km]")
    #         circular_grid(ax, radius = ax.get_xticks())
    #         ax.set_aspect("equal")
    #         cbar = plt.colorbar(pcm, ax=ax, shrink=0.7)
    #         if "units" in data[var].attrs:
    #             units = data[var].attrs['units']
    #         else:
    #             units = "?"
    #         cbar.set_label(f"{var}, [{units}]")
    #         ax.set_title(f"{data.time.values[0]}. Elevation: {data.elevation.values[0]}")            
    #         fig.tight_layout()
    #         list_of_figs.append(fig)
    #         if kwargs.get('savefig', False):
    #             output_dir = kwargs.get("output_dir", Path.cwd())
    #             filepath = output_dir / self.path.name.replace(".nc", f"_{var}.png")
    #             dpi = kwargs.get("dpi", 300)    
    #             fig.savefig(filepath, dpi=dpi)
    #             plt.close(fig)
    #             list_of_paths.append(filepath)
    #     return list_of_figs, list_of_paths


    # def plot_rhi(self, variable: str | None = None, **kwargs):
    #     if variable is None:
    #         variables_to_plot = ["dBZe"]
    #     elif isinstance(variable, str):
    #         variables_to_plot = [variable]
    #     elif isinstance(variable, list):
    #         variables_to_plot = variable
    #     else:
    #         raise ValueError(f"Variable {variable} is not valid")

    #     label_angle = kwargs.get("label_angle", None)
    #     circular_grid = kwargs.get("circular_grid", False)

    #     # sort data['azimuth'] as increasing and sort the rest of the data accordingly
    #     data = self.data.sortby("elevation")
    #     constante_azimuth_angle = data["azimuth"].values[0]
    #     x, y = rhi_to_cartessian(data["range"], data["azimuth"], data["elevation"])
    #     mdata = data.mean(dim="time")
    #     list_of_figs, list_of_paths = [], []
    #     for var in variables_to_plot:
    #         if var not in mdata:
    #             raise ValueError(f"Variable {var} is not in the file")
    #         vmin, vmax = RADAR_PLOT_INFO["limits"][var]
    #         fig, ax = plt.subplots(
    #             figsize=(10, 10)
    #         )  # subplot_kw=dict(projection='polar')
    #         pcm = ax.pcolormesh(x/1e3, y/1e3, 
    #             data[var].values.T, 
    #             vmax = vmin,
    #             vmin = vmax,
    #             shading='gouraud'
    #         )
    #         ax.set_title(f"{str(data.time.values[0]).split('.')[0]} | Azimuth: {constante_azimuth_angle:.1f}°")
    #         ax.set_xlim(*RADAR_PLOT_INFO["limits"]["rhi"]["x"])
    #         ax.set_ylim(*RADAR_PLOT_INFO["limits"]["rhi"]["y"])
    #         ax.set_xlabel(f"Distance from radar, [km]")
    #         ax.set_ylabel("Height distance from radar, [km]")
    #         if circular_grid:
    #             if label_angle is None:
    #                 label_angle = np.min(self.data["elevation"].values)-5
    #             circular_grid(ax, radius = ax.get_xticks(), label_angle=label_angle)
    #         ax.set_aspect("equal")
    #         cbar = plt.colorbar(pcm, ax=ax, shrink=0.7)
    #         if "units" in data[var].attrs:
    #             units = data[var].attrs['units']
    #         else:
    #             units = "?"
    #         cbar.set_label(f"{var}, [{units}]")
    #         fig.tight_layout()
    #         list_of_figs.append(fig)
    #         if kwargs.get('savefig', False):
    #             output_dir = kwargs.get("output_dir", Path.cwd())
    #             filepath = output_dir / self.path.name.replace(".nc", f"_{var}.png")
    #             dpi = kwargs.get("dpi", 300)    
    #             fig.savefig(filepath, dpi=dpi)
    #             plt.close(fig)
    #             list_of_paths.append(filepath)
    #     return list_of_figs, list_of_paths



    # def read_rpg_spectra(self):
    #     pass

    # def read_rpg_spectra_header(self):
    #     pass

    # def __str__(self) -> str:
    #     return super().__str__()
    