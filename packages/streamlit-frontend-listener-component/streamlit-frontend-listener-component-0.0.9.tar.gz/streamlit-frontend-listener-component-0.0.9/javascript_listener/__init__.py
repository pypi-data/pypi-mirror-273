import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _javascript_listener_frontend = components.declare_component( 

        "javascript_listener_frontend",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _javascript_listener_frontend = components.declare_component("javascript_listener_frontend", path=build_dir)


# ".custom-sidebar > .navigation-container > .navigation > .label-icon-container"
def javascript_listener_frontend(initialValue=None, listenerClassPatter=None, key=None, default=None):
    
    component_value = _javascript_listener_frontend(initialValue=initialValue, listenerClassPatter=listenerClassPatter, key=key, default=default)

    return component_value
