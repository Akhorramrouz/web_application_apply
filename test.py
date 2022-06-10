def load_research_interest_page():
    import streamlit as st
    import pandas as pd
    import json
    from streamlit_lottie import st_lottie

    def show_lottie_animation(path):
        with open(path) as f:
            animation = json.load(f)
        return  st_lottie(animation,height=300,width=300)

    left, right = st.columns(2)
    if "counter_research_interest" not in st.session_state:
        st.session_state.counter_research_interest = 0

    if "l" not in st.session_state:
        st.session_state.l = []

    if "i" not in st.session_state:
        st.session_state.i = st.empty()



    with left:
        st.header("Your Research Intersts")
        st.session_state.r = st.session_state.i.text_input("please enter your reserach intersts",key = f"{st.session_state.counter_research_interest}",)
        st.session_state.r
        if st.button('Add'):
            st.session_state.l.append(st.session_state.r.title())
            st.session_state.counter_research_interest += 1
            ri = st.session_state.i.text_input("please enter your reserach intersts",key = f"{st.session_state.counter_research_interest}",)

            st.session_state.l = list(set(st.session_state.l))
            ri_df = pd.DataFrame({'Selected Research Intersts' : st.session_state.l})
            st.dataframe(ri_df)


    with right:
        show_lottie_animation('reserach_animation.json')
