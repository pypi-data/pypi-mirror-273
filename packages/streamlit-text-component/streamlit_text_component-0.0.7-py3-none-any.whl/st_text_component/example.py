import streamlit as st
# import streamlit_float
from __init__ import text_component, _text_component
import streamlit_antd_components as sac

st.set_page_config(layout="wide")

# if "testing" not in st.session_state:
#     st.session_state["testing"] = None

# def change_data_categories_for_heroes_index(value=None): 

#     st.session_state["testing"] = st.session_state["one_two_three"]

# get_subscription_config_data = [
#                     {"index":0, "label":"Get Subscription", "icon":"ri-money-dollar-circle-line"},
#                     {"index":1, "label":"Get Paid", "icon":"ri-money-dollar-circle-line"}
#                 ]
# text_component(get_subscription_config_data, on_change=change_data_categories_for_heroes_index, key="one_two_three")

# st.write(st.session_state["testing"]) 


if "testing_work" not in st.session_state:
    st.session_state["testing_work"] = None 

def change_data_categories_for_heroes_index():

    st.session_state["testing_work"] = st.session_state["test"]

sac.segmented(
                items=[
                        sac.SegmentedItem(label='Hero Profile'), 
                        sac.SegmentedItem(label='Skills Profile'), 
                        sac.SegmentedItem(label='Damage'),
                        # sac.SegmentedItem(label='Match Ups'),
                        # sac.SegmentedItem(label='Map')
                    ], index=0, label='', align='center', size='sm', radius='sm', bg_color='transparent', divider=False, on_change=change_data_categories_for_heroes_index, key="test"
            )

st.write(st.session_state["testing_work"])
