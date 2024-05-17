import streamlit as st
import streamlit_float
from __init__ import text_component
import streamlit_antd_components as sac

st.set_page_config(layout="wide")

if "test" not in st.session_state:
    st.session_state["test"] = None

if "st_float_" not in st.session_state:
    st.session_state["st_float_"] = None

st.session_state["st_float_"] = streamlit_float.float_init()

st.session_state["st_float_"] 

st.sidebar.write("Hi")
st.markdown(
        """
            <style>
                section[data-testid="stSidebar"]{
                    background-color:#111;
                }
            </style>
        """, unsafe_allow_html=True
    )
# with st.sidebar:
    # st.markdown(
    #     """
    #         <style>
    #             section[data-testid="stSidebar"]{
    #                 background-color:#111;
    #             }
    #         </style>
    #     """, unsafe_allow_html=True
    # )
data = [
    {"index":0, "label":"My Subscriptions"},
    {"index":1, "label":"Logout", "icon":"ri-logout-box-r-line"}
]

if "count" not in st.session_state:
    st.session_state["count"] = 0
    



def on_change():
    selection = st.session_state["foo"]
    st.session_state["count"] = selection
    # st.session_state["test"][0].write(f"Selection changed to {selection}")

def counter():
    st.session_state['count'] += 1
    # st.session_state["test"][0].write(st.session_state["count"])

with st.container():
    num_clicks = text_component(data=data, styles=None, on_change=on_change, key="foo")
    # streamlit_float.float_parent(css="top:1%; position:fixed; left:72%;")
    streamlit_float.float_parent(css="top:1%; position:absolute; right:0;")
    # st.write(num_clicks)
    st.session_state["test"] = st.columns(1)

btn = sac.buttons(
    items=['button1', 'button2', 'button3'],
    index=0,
    format_func='title',
    align='center',
    direction='horizontal',
    on_change=counter,
    shape='round',
    compact=False,
    return_index=False,
    key="testing"
)

st.radio("radio", ["one", "two"], on_change=counter)

st.session_state["test"][0].write(st.session_state["count"])
