from email.policy import strict
import streamlit as st
from send_gmail import send_gmail
from streamlit_option_menu import option_menu
import pandas as pd
import json
import time
from  streamlit_lottie import st_lottie



## -------------     Initialise some variables
months_of_year = [
    'January','February','March',
    'April', 'May', 'June',
    'July','Agusut','September',
    'October','November','December'                
    ]
if 'is_signed_in' not in st.session_state:
    st.session_state.is_signed_in = False
if 'show_verification' not in st.session_state:
    st.session_state.show_verification = False
if 'verification_code_claimed_by_user' not in st.session_state:
    st.session_state.verification_code_claimed_by_user = -1
if 'real_verification_code' not in st.session_state:
    st.session_state.real_verification_code = -2
if 'sign_up_mail' not in st.session_state:
    st.session_state.sign_up_mail = None
if 'sign_up_name' not in st.session_state:
    st.session_state.sign_up_name = None
if 'new_data' not in st.session_state:
    st.session_state.new_data = None
##--------------     Define some functions
def show_lottie_animation(path):
    with open(path) as f:
        animation = json.load(f)
    return  st_lottie(animation,height=300,width=300)



##---------------    First page to sign in or sign up
if not st.session_state.is_signed_in:

    ##   ************** Side Bar before signing in
    with st.sidebar:
        selected_page_before_sign_in = option_menu(
            menu_title = 'Pages',
            options = ['Sign in','Sign up'],
            orientation = 'horizontal'
        )

        if st.session_state.show_verification:
            st.header(f'Verify your mail: {st.session_state.sign_up_mail}')
            st.session_state.verification_code_claimed_by_user = st.number_input('verification code',step=1,min_value=100000,max_value=999999,)
            verify_button = st.button('Verify')
            resened_verification_code_button = st.button('Resend Verification code')

            if verify_button:
            
                # the code is correct
                if st.session_state.verification_code_claimed_by_user == st.session_state.real_verification_code:
                    st.success('You are registered sucessfully')
                    df = pd.read_excel('db_streamlit.xlsx',index_col=0)
                    df = df.append(st.session_state.new_data,ignore_index=True)
                    df.to_excel('db_streamlit.xlsx')
                    st.write('Data is added to df')
                    st.write('Now you can Sign in')
                    time.sleep(2)
                    selected_page_before_sign_in = 'Sign in'
                    st.session_state.show_verification = False
                    st.experimental_rerun()

                else:
                    st.error('This is not the vrification code that we had sent you')

            if resened_verification_code_button:
                st.session_state.real_verification_code = send_gmail(st.session_state.sign_up_mail,st.session_state.sign_up_name)


            

    
    if selected_page_before_sign_in == 'Sign in':
        if not st.session_state.is_signed_in:
            st.title('Sign in')
            username = st.text_input('Your email adress')
            password = st.text_input('Password')
            sign_in_button = st.button('Sign in')

            if sign_in_button:
                df = pd.read_excel('db_streamlit.xlsx',index_col=0)
                try:
                    st.session_state.index = list(df.email_address).index(username)
                    confirmed_pass = df.iloc[st.session_state.index].password
                except:
                    st.session_state.index = -1


                
                
                if st.session_state.index == -1:
                    st.error('there is no account with this email adress')
                
                elif password == confirmed_pass:
                    st.success('You are Sined in Sucessfully')
                    st.session_state.is_signed_in = True
                    st.session_state.sign_up_name = df.iloc[st.session_state.index].first_name
                    st.experimental_rerun()


                else:
                    st.error('Your username and pass does not match')
 
    if selected_page_before_sign_in == 'Sign up':
        st.title('Sign Up')
        email_address = st.text_input('Email Adress')
        first_name = st.text_input('First name')
        family_name = st.text_input('Family name')
        birth_day_year = st.number_input('birthday year',min_value=1950,max_value=2018)
        birth_day_month = st.selectbox('birthday month',options=months_of_year)
        birth_day_day = st.number_input('birthday day in month',min_value=1,max_value=31)
        major = st.text_input('you current major')
        next_major = st.text_input('the next major you are wiiling to apply for')
        current_education = st.selectbox('current education',options=['Diploma','B.Sc','M.Sc','Ph.D.'])
        last_gpa = st.number_input(f'Please enter your {current_education} GPA')
        username = st.text_input('Username')
        password = st.text_input('Password')
        password_repeat = st.text_input('Repeat Password')
        submit_sign_up = st.button('Submit')

        if submit_sign_up:
            st.session_state.sign_up_mail = email_address
            st.session_state.sign_up_name = first_name
            df = pd.read_excel('db_streamlit.xlsx',index_col=0)
            set_emails = set(df.email_address)
            new_data = {
                'index' : len(df)+1,
                'email_address': email_address,
                'first_name': first_name,
                'family_name' : family_name,
                'birth_day_year' : birth_day_year,
                'birth_day_month' : birth_day_month,
                'birth_day_day' : birth_day_day,
                'major' : major,
                'next_major': next_major,
                'current_education': current_education,
                'last_gpa' : last_gpa,
                'usernmae' : username,
                'password' : password,
                }

            if email_address in set_emails:
                st.error('This Email is already registered')


            elif not all(new_data.values()):
                st.error('Please Enter all the Values')
                for empty_el_key in new_data.keys():
                    if not new_data[empty_el_key]:
                        st.error(f'{empty_el_key} is empty')


            elif password != password_repeat:
                st.error('Please Double check your password and its confirmation')

            else:
                st.session_state.show_verification = True
                st.session_state.real_verification_code = send_gmail(st.session_state.sign_up_mail,st.session_state.sign_up_name)
                st.session_state.new_data = new_data
                'Please Verify your account now'
                st.experimental_rerun()




##----------------------------
if st.session_state.is_signed_in:
    log_out_button = st.button('Log Out',)
    if log_out_button:
        st.session_state.is_signed_in = False
        st.experimental_rerun()
    selected_page_after_sign_in = option_menu(
        menu_title='Pages',
        options = ['Country', 'Research Interests', 'Parameters', 'Last Check'],
        orientation='horizontal',
        icons=['map','mortarboard','motherboard']
    )



    st.write("---")
    st.subheader(f'Welcome {st.session_state.sign_up_name.capitalize()}')


    if selected_page_after_sign_in == 'Country':

        st.subheader('Let us select the countries you are going to apply for')
        left,right = st.columns(2)
        with left:
            selected_countries = st.multiselect('Select all countries you want to apply for',
            options=['Canada','Australia','United States of Amercia'])

            st.session_state.selected_country_df = pd.DataFrame({'Selected Countries' : selected_countries },)
            st.dataframe(st.session_state.selected_country_df)


        with right:
            show_lottie_animation('globe.json')

        submit_country_button = st.button('Submit Selected Country')
        if submit_country_button:
            st.write('Well Done!')
            st.write("Now Let's choose research interests" )
            go_to_research_interests_page = st.button("GO to research Interests > ")
            if go_to_research_interests_page:
                selected_page_after_sign_in = 'Research Interests'


    if selected_page_after_sign_in == 'Research Interests':

        left_ri, right_ri = st.columns(2)
        if "counter_research_interest" not in st.session_state:
            st.session_state.counter_research_interest = 0

        if "list_research_interests" not in st.session_state:
            st.session_state.list_research_interests = []

        if "input_place_holder" not in st.session_state:
            st.session_state.input_place_holder = st.empty()



        with left_ri:
            st.header("Your Research Intersts")
            st.session_state.ri = st.session_state.input_place_holder.text_input("please enter your reserach intersts",key = f"{st.session_state.counter_research_interest}",)
            st.session_state.ri
            if st.button('Add'):
                st.session_state.list_research_interests.append(st.session_state.ri.title())
                st.session_state.counter_research_interest += 1
                ri = st.session_state.input_place_holder.text_input("please enter your reserach intersts",key = f"{st.session_state.counter_research_interest}",)

                st.session_state.list_research_interests = list(set(st.session_state.list_research_interests))
                ri_df = pd.DataFrame({'Selected Research Intersts' : st.session_state.list_research_interests})
                st.dataframe(ri_df)


                df = pd.read_excel('db_streamlit.xlsx',index_col=0)
  
                
                for i in range(len(ri_df)):
                    st.session_state.index
                    f"RI_{i+1}"
                    st.write(ri_df.iloc[i])
                    df.at[st.session_state.index,f"RI_{i+1}"] = ri_df.iloc[i,0]
                st.dataframe(df)
                df.to_excel('db_streamlit.xlsx')

        with right_ri:
            show_lottie_animation('reserach_animation.json')





    if selected_page_after_sign_in == 'Parameters':
        "Let's Set The Parameters"

        strictness = st.slider('How Strict Shall We look for professors ?',min_value=1,max_value=500)

        expandability = st.slider('How Much Shall we Expand Your Research Interests?',min_value=1,max_value=4)

        submit_params = st.button("Submit Parameters")
        if submit_params:
            df = pd.read_excel('db_streamlit.xlsx',index_col=0)

            df.at[st.session_state.index,'strictness'] = strictness
            df.at[st.session_state.index,'expandability'] = expandability
            df.to_excel('db_streamlit.xlsx')


    if selected_page_after_sign_in == 'Last Check':
        df2 = pd.read_excel('db_streamlit.xlsx',index_col=0)
        df3 = df2.loc[st.session_state.index].astype('str')
        st.dataframe(df3)

        "Please Confirm the Above Data"

        final_confirmation = st.button('final_confirmation')