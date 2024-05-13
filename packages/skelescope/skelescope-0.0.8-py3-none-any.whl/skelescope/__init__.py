import importlib.metadata
import pathlib
import pandas as pd
import numpy as np
import secrets
import hashlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("skelescope")   
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


def get_segments(swc_df, segments_meta):
    node_props = {}
    segments = {}

    for _, row in swc_df.iterrows():
        node_id = row.node_id
        node_props[node_id] = {
            "point": [row.x, row.y, row.z, row.radius],
            "parent": row.parent_id,
            "segments" : []
        }

    for segment_idx, segment in enumerate(segments_meta):
        assert len(segment) >= 2

        segments[segment_idx] = {
            "parent_segment" : -1,
            "children_segments" : [],
            "nodes": segment,
            "points" : []
        }
        for node in segment:
            node_props[node]["segments"].append(segment_idx)     

    for node_id, props in node_props.items():   
        if(len(props["segments"]) > 1):
            props["point"].append(1) # is bifurcation
        else:
            props["point"].append(0)

    for segment_idx, segment in segments.items():
        for node in segment["nodes"]:
            props = node_props[node]
            segment["points"].append(props["point"])

        segment_root_node = sorted(segment["nodes"])[0]
        parent_node_id = node_props[segment_root_node]["parent"]

        if(parent_node_id != -1):
            connected_segment_ids = set(node_props[parent_node_id]["segments"]) - set([segment_idx])
            if(len(connected_segment_ids)):
                parent_segment_id = connected_segment_ids.pop()
                segments[parent_segment_id]["children_segments"].append(segment_idx)
                segment["parent_segment"] = parent_segment_id 

    return segments


def generate_random_hash(length):
    random_bytes = secrets.token_bytes(length)
    return hashlib.sha256(random_bytes).hexdigest()[:length]


class Skelescope(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    segments = traitlets.Dict({}).tag(sync=True)
    synapses = traitlets.List([]).tag(sync=True)
    
    selected_segments = traitlets.List([]).tag(sync=True)
    selected_synapses = traitlets.List([]).tag(sync=True)
    
    camera_zoom_step = traitlets.Float(10).tag(sync=True)
    
    show_branches = traitlets.Bool(True).tag(sync=True)

    show_synapses = traitlets.Bool(True).tag(sync=True)
    synapse_radius = traitlets.Float(0.2).tag(sync=True)

    show_arrows = traitlets.Bool(False).tag(sync=True)
    arrow_length = traitlets.Float(3.0).tag(sync=True)
    arrow_shaft_radius = traitlets.Float(0.2).tag(sync=True)
    arrow_cone_radius = traitlets.Float(0.7).tag(sync=True)
    arrow_cone_position = traitlets.Float(0.6).tag(sync=True)
    arrow_offset_segment_ends = traitlets.Float(5.0).tag(sync=True)
    arrow_interval = traitlets.Float(7.0).tag(sync=True)

    abstraction_level = traitlets.Float(0.0).tag(sync=True)
    default_radius = traitlets.Float(0.2).tag(sync=True)

    neuron_position = traitlets.List([]).tag(sync=True)
    neuron_rotation = traitlets.List([]).tag(sync=True)

    show_axes_global = traitlets.Bool(False).tag(sync=True)
    show_axis_local_primary = traitlets.Bool(False).tag(sync=True)
    axis_local_primary_points = traitlets.List([0,0,0,0,1,0]).tag(sync=True)
    axis_local_primary_radius = traitlets.Float(1.0).tag(sync=True)

    viewer_id = traitlets.Unicode("").tag(sync=True)
    listen_to = traitlets.List([]).tag(sync=True) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.viewer_id = f"skelescope_{generate_random_hash(8)}"
            
    def add_neuron(self, swc_df, synapse_df=None, segments_meta=None):
        if(segments_meta is None):
            raise NotImplementedError("segments_meta is required")
        
        self.segments = get_segments(swc_df, segments_meta)

        if synapse_df is not None:
            assert isinstance(synapse_df, pd.DataFrame)
            assert "x" in synapse_df.columns
            assert "y" in synapse_df.columns
            assert "z" in synapse_df.columns
            has_synapse_type = "type" in synapse_df.columns
            has_synapse_node_id = "node_id" in synapse_df.columns
            
            synapses_flat = []
            for _, row in synapse_df.iterrows():
                synapse = [row.x, row.y, row.z]

                if has_synapse_type:
                    synapse.append(row.type)
                else:
                    synapse.append("unknown") 
                
                if has_synapse_node_id:
                    synapse.append(row.node_id)
                else:
                    synapse.append(-1)

                synapses_flat.append(synapse)
            self.synapses = synapses_flat