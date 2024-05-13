import os
from pathlib import Path
from typing import Optional, Dict

import streamlit as st
import streamlit.components.v1 as components

from oceanum.eidos import Eidos


# Tell streamlit that there is a component called streamlit_eidos,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_eidos", path=str(frontend_dir)
)


# Create the python function that will be called
def st_eidos(eidos=None, height=500, events=None):
    """Create a EIDOS visualisation in Streamlit.

    Parameters
    ==========
    eidos : eidoslib.Eidos instance
        The EIDOS visualisation to render.
    height : int, default 500
        The height of the map in pixels.
    events : list, default None
        A list of events to listen for. Can be one or more of:
        - 'click'
        - 'hover'

    Returns
    =======
    component_value : dict
        A dictionary containing the dictionary of an EIDOS event.
    """

    if eidos is None or not isinstance(eidos, Eidos):
        raise ValueError("First argument must be an instance of Eidos")

    renderer = os.environ.get("EIDOS_RENDERER", "https://render.eidos.oceanum.io")
    print(f"Using renderer at {renderer}")

    component_value = _component_func(
        key=eidos.id,
        height=height,
        spec=eidos.model_dump(),
        events=events if events else ["click"],
        renderer=renderer,
    )

    return component_value
