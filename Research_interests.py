import streamlit as st
import pandas as pd
import json
from streamlit_lottie import st_lottie

def show_lottie_animation(path):
    with open(path) as f:
        animation = json.load(f)
        return st_lottie(animation,height=300,width=300)



if "list_research_interests" not in st.session_state:
    st.session_state.list_research_interests = []
if "key_counter" not in st.session_state:
    st.session_state.key_counter = 0


st.header('Research Interests')

plcae_holder = st.empty()
st.session_state.research_interest = (plcae_holder.text_input('Enter your research interest and click Add'
                        ,key = f"{st.session_state.key_counter}"))
st.session_state.key_counter += 1
st.session_state.research_interest
left , right = st.columns(2)



with left:

    add_research_intersrs = st.button('Add')
    if add_research_intersrs:   
#           st.experimental_rerun()
        st.write(st.session_state.research_interest)
        st.session_state.list_research_interests.append(st.session_state.research_interest.capitalize())
        st.session_state.research_interest = (plcae_holder.text_input('Enter your research interest and click Add',key = f"{st.session_state.key_counter}"))
        st.session_state.key_counter += 1

        final_set = pd.DataFrame({"Your Research Interests" :list(set(st.session_state.list_research_interests))})
        st.dataframe(final_set)
    st.subheader(st.session_state.research_interest)
        
        
        


with right:
    submit_research_intersrs = st.button('Submit Selected Research Intersts')
    show_lottie_animation("reserach_animation.json")
    if submit_research_intersrs:
        if len(final_set) < 1:
            st.warning('No Research Interest Has Been Selected')


        else:
            st.success(f"You Have Chosen {len(final_set)} Research Interesrs Successfulluy")
            "Please go and set parameters in the next page"




