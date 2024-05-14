from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Polygon, Geometry
import json

def calc(json_data):
    vertices = json.loads(json_data)
    polygon = Polygon(vertices['vertices'])
    geom = Geometry(polygon)
    geom.create_mesh(mesh_sizes=100.0)

    section = Section(geom)
    section.calculate_geometric_properties()
    return section.get_area(), section.get_c(), section.get_ic()