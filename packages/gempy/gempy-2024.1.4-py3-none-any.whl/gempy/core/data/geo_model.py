﻿import pprint
import warnings
from dataclasses import dataclass, field
from typing import Sequence, Optional

import numpy as np

import gempy_engine.core.data.engine_grid
from gempy_engine.core.data import Solutions
from gempy_engine.core.data.geophysics_input import GeophysicsInput
from gempy_engine.core.data.raw_arrays_solution import RawArraysSolution
from gempy_engine.core.data import InterpolationOptions
from gempy_engine.core.data.input_data_descriptor import InputDataDescriptor
from gempy_engine.core.data.interpolation_input import InterpolationInput
from .orientations import OrientationsTable
from .structural_frame import StructuralFrame
from gempy_engine.core.data.transforms import Transform, GlobalAnisotropy
from .grid import Grid

"""
TODO:
    - [ ] StructuralFrame will all input points chunked on Elements. Here I will need a property to put all
    together to feed to InterpolationInput

"""


@dataclass
class GeoModelMeta:
    """
    Container for metadata associated with a GeoModel.

    Attributes:
        name (str): Name of the geological model.
        creation_date (str): Date of creation of the model.
        last_modification_date (str): Last modification date of the model.
        owner (str): Owner of the geological model.
    """

    name: str
    creation_date: str
    last_modification_date: str
    owner: str


@dataclass(init=False)
class GeoModel:
    """
    Class representing a geological model.

    """

    meta: GeoModelMeta  #: Meta-information about the geological model, like its name, creation and modification dates, and owner.
    structural_frame: StructuralFrame  #: The structural information of the geological model.
    grid: Grid  #: The general grid used in the geological model.

    # region GemPy engine data types
    _interpolation_options: InterpolationOptions  #: The interpolation options provided by the user.
    geophysics_input: GeophysicsInput = None  #: The geophysics input of the geological model.

    transform: Transform = None  #: The transformation used in the geological model for input points.

    interpolation_grid: gempy_engine.core.data.engine_grid.EngineGrid = None  #: Optional grid used for interpolation. Can be seen as a cache field.
    _interpolationInput: InterpolationInput = None  #: Input data for interpolation. Fed by the structural frame and can be seen as a cache field.
    _input_data_descriptor: InputDataDescriptor = None  #: Descriptor of the input data. Fed by the structural frame and can be seen as a cache field.

    # endregion
    _solutions: gempy_engine.core.data.solutions.Solutions = field(init=False, default=None)  #: The computed solutions of the geological model. 

    legacy_model: "gpl.Project" = None  #: Legacy model (if available). Allows for backward compatibility.

    def __init__(self, name: str, structural_frame: StructuralFrame, grid: Grid, interpolation_options: InterpolationOptions):
        # TODO: Fill the arguments properly
        self.meta = GeoModelMeta(
            name=name,
            creation_date=None,
            last_modification_date=None,
            owner=None
        )

        self.structural_frame = structural_frame  # ? This could be Optional

        self.grid = grid
        self._interpolation_options = interpolation_options
        self.transform = Transform.from_input_points(
            surface_points=self.surface_points_copy,
            orientations=self.orientations_copy
        )

    def __repr__(self):
        # TODO: Improve this
        return pprint.pformat(self.__dict__)

    def update_transform(self, auto_anisotropy: GlobalAnisotropy = GlobalAnisotropy.NONE, anisotropy_limit: Optional[np.ndarray] = None):
        self.transform = Transform.from_input_points(
            surface_points=self.surface_points_copy,
            orientations=self.orientations_copy
        )

        self.transform.apply_anisotropy(anisotropy_type=auto_anisotropy, anisotropy_limit=anisotropy_limit)


    @property
    def interpolation_options(self) -> InterpolationOptions:
        n_octree_lvl = self._interpolation_options.number_octree_levels  # * we access the private one because we do not care abot the extract mesh octree level

        octrees_set: bool = n_octree_lvl > 1
        resolution_set = bool(self.grid.active_grids_bool[0])  # 0 corresponds

        # Create a tuple representing the conditions
        match (octrees_set, resolution_set):
            case (True, False):
                self._interpolation_options.block_solutions_type = RawArraysSolution.BlockSolutionType.OCTREE
            case (True, True):
                warnings.warn("Both octree levels and resolution are set. The default grid for the `raw_array_solution`"
                              "and plots will be the dense regular grid. To use octrees instead, set resolution to None in the "
                              "regular grid.")
                self._interpolation_options.block_solutions_type = RawArraysSolution.BlockSolutionType.DENSE_GRID
            case (False, True):
                self._interpolation_options.block_solutions_type = RawArraysSolution.BlockSolutionType.DENSE_GRID
            case (False, False):
                raise ValueError("The resolution of the grid is not set. Please set the resolution of the grid or "
                                 "the number of octree levels in InterpolationOptions.number_octree_levels.")

        self._interpolation_options.cache_model_name = self.meta.name
        return self._interpolation_options

    @interpolation_options.setter
    def interpolation_options(self, value):
        self._interpolation_options = value

    @property
    def solutions(self) -> Solutions:
        return self._solutions
    
    @solutions.setter
    def solutions(self, value):
        self._solutions = value

        # * Set solutions per group
        if self._solutions.raw_arrays is not None:
            for e, group in enumerate(self.structural_frame.structural_groups):
                group.kriging_solution = RawArraysSolution(  # ? Maybe I need to add more fields, but I am not sure yet
                    scalar_field_matrix=self._solutions.raw_arrays.scalar_field_matrix[e],
                    block_matrix=self._solutions.raw_arrays.block_matrix[e],
                )

        # * Set solutions per element
        for e, element in enumerate(self.structural_frame.structural_elements[:-1]):  # * Ignore basement
            dc_mesh = self._solutions.dc_meshes[e] if self._solutions.dc_meshes is not None else None
            # TODO: These meshes are in the order of the scalar field
            element.vertices = (self.transform.apply_inverse(dc_mesh.vertices) if dc_mesh is not None else None)
            element.edges = (dc_mesh.edges if dc_mesh is not None else None)

        # * Reordering the elements according to the scalar field
        for e, order_per_structural_group in enumerate(self._solutions._ordered_elements):
            elements = self.structural_frame.structural_groups[e].elements
            reordered_elements = [elements[i] for i in order_per_structural_group]
            self.structural_frame.structural_groups[e].elements = reordered_elements

    @property
    def surface_points_copy(self):
        """This is a copy! Returns a SurfacePointsTable for all surface points across the structural elements"""
        surface_points_table = self.structural_frame.surface_points
        if self.transform is not None:
            surface_points_table.model_transform = self.transform
        return surface_points_table

    @property
    def surface_points(self):
        raise AttributeError("This property can only be set, not read. You can access the copy with `surface_points_copy` or"
                             "the original on the individual structural elements.")

    @surface_points.setter
    def surface_points(self, value):
        self.structural_frame.surface_points = value

    @property
    def orientations_copy(self) -> OrientationsTable:
        """This is a copy! Returns a OrientationsTable for all orientations across the structural elements"""
        orientations_table = self.structural_frame.orientations
        if self.transform is not None:
            orientations_table.model_transform = self.transform
        return orientations_table

    @property
    def orientations(self) -> OrientationsTable:
        raise AttributeError("This property can only be set, not read. You can access the copy with `orientations_copy` or"
                             "the original on the individual structural elements.")

    @orientations.setter
    def orientations(self, value):
        self.structural_frame.orientations = value

    @property
    def interpolation_input_copy(self):
        if self.structural_frame.is_dirty is False:
            return self._interpolationInput
        
        self._interpolationInput = InterpolationInput.from_structural_frame(
            structural_frame=self.structural_frame,
            grid=self.grid,
            transform=self.transform
        )

        return self._interpolationInput

    @property
    def input_data_descriptor(self) -> InputDataDescriptor:
        # TODO: This should have the exact same dirty logic as interpolation_input
        return self.structural_frame.input_data_descriptor

    def add_surface_points(self, X: Sequence[float], Y: Sequence[float], Z: Sequence[float],
                           surface: Sequence[str], nugget: Optional[Sequence[float]] = None) -> None:
        raise NotImplementedError("This method is deprecated. Use `gp.add_surface_points` instead")
