"""
STEP File Processor for face coloring and orientation
"""

import os
import numpy as np

# Try different import patterns for different OCC distributions
try:
    # For cadquery-ocp (recommended)
    from OCP import STEPControl_Reader, TopExp_Explorer, TopAbs_FACE, BRep_Tool
    from OCP import gp_Pnt, gp_Vec, gp_Dir, gp_Ax3, gp_Trsf, BRepBuilderAPI_Transform
    from OCP import Quantity_Color, XCAFPrs_Style, XCAFPrs_IndexedDataMapOfShapeStyle
    from OCP import TCollection_AsciiString, TDF_Label, XCAFDoc_ColorTool
    from OCP import STEPCAFControl_Reader, TDocStd_Document, XCAFApp_Application
    from OCP import TCollection_ExtendedString
    from OCP import STEPControl_Writer, Interface_Static
    from OCP import Bnd_Box, BRepBndLib
    print("Using OCP (cadquery-ocp)")
except ImportError:
    try:
        # For pythonocc-core (pip)
        from OCC.Core import STEPControl_Reader, TopExp_Explorer, TopAbs_FACE, BRep_Tool
        from OCC.Core import gp_Pnt, gp_Vec, gp_Dir, gp_Ax3, gp_Trsf, BRepBuilderAPI_Transform
        from OCC.Core import Quantity_Color, XCAFPrs_Style, XCAFPrs_IndexedDataMapOfShapeStyle
        from OCC.Core import TCollection_AsciiString, TDF_Label, XCAFDoc_ColorTool
        from OCC.Core import STEPCAFControl_Reader, TDocStd_Document, XCAFApp_Application
        from OCC.Core import TCollection_ExtendedString
        from OCC.Core import STEPControl_Writer, Interface_Static
        from OCC.Core import Bnd_Box, BRepBndLib
        print("Using OCC.Core (pythonocc-core)")
    except ImportError:
        try:
            # For OCC (conda-forge)
            from OCC.Core.STEPControl_Reader import STEPControl_Reader
            from OCC.Core.TopExp import TopExp_Explorer
            from OCC.Core.TopAbs import TopAbs_FACE
            from OCC.Core.BRep_Tool import BRep_Tool
            from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax3, gp_Trsf
            from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
            from OCC.Core.Quantity import Quantity_Color
            from OCC.Core.XCAFPrs import XCAFPrs_Style, XCAFPrs_IndexedDataMapOfShapeStyle
            from OCC.Core.TCollection import TCollection_AsciiString, TCollection_ExtendedString
            from OCC.Core.TDF import TDF_Label
            from OCC.Core.XCAFDoc import XCAFDoc_ColorTool
            from OCC.Core.STEPCAFControl_Reader import STEPCAFControl_Reader
            from OCC.Core.TDocStd import TDocStd_Document
            from OCC.Core.XCAFApp import XCAFApp_Application
            from OCC.Core.STEPControl_Writer import STEPControl_Writer
            from OCC.Core.Interface import Interface_Static
            from OCC.Core.Bnd import Bnd_Box
            from OCC.Core.BRepBndLib import BRepBndLib
            print("Using OCC.Core (conda-forge)")
        except ImportError:
            print("Error: No OCC/OCCP module found. Please install cadquery-ocp or pythonocc-core")
            raise ImportError("No OCC/OCCP module found")


class StepProcessor:
    """Main class for processing STEP files with face coloring and orientation"""
    
    def __init__(self):
        self.reader = None
        self.shape = None
        self.document = None
        self.color_tool = None
        
    def load_step_file(self, file_path):
        """Load a STEP file and return the shape"""
        try:
            # Create STEP reader
            self.reader = STEPControl_Reader()
            
            # Read the file
            status = self.reader.ReadFile(file_path)
            if status != 1:  # IFSelect_RetDone
                raise Exception(f"Failed to read STEP file: {file_path}")
            
            # Transfer to shape
            self.reader.TransferRoots()
            nb_shapes = self.reader.NbShapes()
            
            if nb_shapes == 0:
                raise Exception("No shapes found in STEP file")
            
            # Get the first shape (assuming single solid)
            self.shape = self.reader.Shape(1)
            
            return self.shape
            
        except Exception as e:
            raise Exception(f"Error loading STEP file: {str(e)}")
    
    def orient_shape(self, shape, orientation_criteria=None):
        """Orient the shape based on specified criteria"""
        if orientation_criteria is None:
            orientation_criteria = "auto"  # Default to automatic orientation
        
        # For now, implement basic orientation logic
        # This can be extended based on specific requirements
        
        if orientation_criteria == "auto":
            # Calculate bounding box and orient based on principal axes
            bbox = self._get_bounding_box(shape)
            center = bbox.Center()
            
            # Simple orientation: align with coordinate system
            # This is a placeholder - implement specific orientation logic as needed
            return shape
        
        return shape
    
    def color_faces(self, shape, coloring_criteria=None):
        """Color faces of the shape based on specified criteria"""
        if coloring_criteria is None:
            coloring_criteria = {"method": "random"}  # Default coloring
        
        # Create a new document for colored output
        app = XCAFApp_Application.GetApplication()
        self.document = app.NewDocument(TCollection_ExtendedString("STEP"))
        
        # Get color tool
        self.color_tool = XCAFDoc_ColorTool.Set(self.document.Main())
        
        # Process faces
        face_colors = self._assign_face_colors(shape, coloring_criteria)
        
        return face_colors
    
    def _get_bounding_box(self, shape):
        """Get bounding box of the shape"""
        from OCC.Core import Bnd_Box, BRepBndLib
        bbox = Bnd_Box()
        BRepBndLib.Add(shape, bbox)
        return bbox
    
    def _assign_face_colors(self, shape, criteria):
        """Assign colors to faces based on criteria"""
        colors = []
        face_colors = {}
        
        # Generate colors based on criteria
        if criteria.get("method") == "random":
            colors = self._generate_random_colors(10)  # Generate 10 random colors
        elif criteria.get("method") == "gradient":
            colors = self._generate_gradient_colors(10)
        else:
            # Default colors
            colors = [
                Quantity_Color(1.0, 0.0, 0.0, 1),  # Red
                Quantity_Color(0.0, 1.0, 0.0, 1),  # Green
                Quantity_Color(0.0, 0.0, 1.0, 1),  # Blue
                Quantity_Color(1.0, 1.0, 0.0, 1),  # Yellow
                Quantity_Color(1.0, 0.0, 1.0, 1),  # Magenta
            ]
        
        # Assign colors to faces
        face_index = 0
        explorer = TopExp_Explorer(shape, TopAbs_FACE)
        
        while explorer.More():
            face = explorer.Current()
            color_index = face_index % len(colors)
            face_colors[face] = colors[color_index]
            face_index += 1
            explorer.Next()
        
        return face_colors
    
    def _generate_random_colors(self, count):
        """Generate random colors"""
        colors = []
        for i in range(count):
            r = np.random.random()
            g = np.random.random()
            b = np.random.random()
            colors.append(Quantity_Color(r, g, b, 1))
        return colors
    
    def _generate_gradient_colors(self, count):
        """Generate gradient colors from blue to red"""
        colors = []
        for i in range(count):
            t = i / (count - 1) if count > 1 else 0
            r = t
            g = 0.5 * (1 - abs(2 * t - 1))
            b = 1 - t
            colors.append(Quantity_Color(r, g, b, 1))
        return colors
    
    def save_colored_step(self, shape, face_colors, output_path):
        """Save the colored shape as a new STEP file"""
        try:
            # Create STEP writer with colors
            writer = STEPCAFControl_Reader()
            
            # This is a simplified approach - in practice, you'd need to properly
            # set up the document with colored faces
            # For now, we'll save the basic shape
            
            from OCC.Core import STEPControl_Writer, Interface_Static
            step_writer = STEPControl_Writer()
            
            # Set precision
            Interface_Static.SetCVal("write.step.schema", "AP203")
            Interface_Static.SetCVal("write.step.unit", "MM")
            
            # Transfer shape
            step_writer.Transfer(shape, 1)
            
            # Write file
            status = step_writer.Write(output_path)
            if status != 1:
                raise Exception(f"Failed to write STEP file: {output_path}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Error saving colored STEP file: {str(e)}")
    
    def process_file(self, input_path, output_path, orientation_criteria=None, coloring_criteria=None):
        """Main processing function"""
        try:
            # Load STEP file
            shape = self.load_step_file(input_path)
            
            # Orient shape
            oriented_shape = self.orient_shape(shape, orientation_criteria)
            
            # Color faces
            face_colors = self.color_faces(oriented_shape, coloring_criteria)
            
            # Save colored STEP file
            self.save_colored_step(oriented_shape, face_colors, output_path)
            
            return True
            
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
