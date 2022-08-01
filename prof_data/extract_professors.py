import pandas as pd

list_countries = ['USA','Canada','Australia']

def create_prof_db_base_on_country(db, final_dst,index, list_countries=list_countries):
    main_df = pd.DataFrame()
    for country in list_countries:
        if db.at[index, country] == "TRUE":
            sub_df = pd.read_excel(f'prof_data/{country}.xlsx', index_col=0)
            main_df = main_df.append(sub_df)

    main_df.to_excel(final_dst)
    return main_df


# In[22]:


def selected_prof_based_on_seed_Research_interests( data_path, seed_set_research_interests,
                                                   threshhold_research_interests ,
                                                   max_number_of_itteration_on_generalizing_research_interests,):

    data = pd.read_excel(data_path, index_col=0)
    data.head()

    data = data.fillna("--")
    student_research_intrests = set(seed_set_research_interests)
    
    
    counter = 1
    initial_len_student_reserach_interests = 0
    len_student_reserach_interests = len(student_research_intrests)
    
    list_research_interests_scores = []
    
    set_already_known_research_interest = set()
    
    
    for initial_research_interest in seed_set_research_interests:
        print((initial_research_interest,1))
        set_already_known_research_interest.add(initial_research_interest)
        list_research_interests_scores.append((initial_research_interest,1))
    
    
    
    while( initial_len_student_reserach_interests != len_student_reserach_interests) and (counter< 1+max_number_of_itteration_on_generalizing_research_interests):
        counter += 1
 #       print(counter)
 #       print(f"it was {initial_len_student_reserach_interests} and it is {len_student_reserach_interests}")
        student_new_reserach_interests = []
        initial_len_student_reserach_interests = len_student_reserach_interests

        data2 = []
        for student_research_intrest in student_research_intrests:
            for i in range(len(data)):
                if student_research_intrest in data.iloc[i,6].title():
            #        print(data.iloc[i,6])
                    for ri in data.iloc[i,6].split(", "):
                        data2.append(ri.title())

        data2 = pd.DataFrame(data2)
        ser = data2.value_counts()
        ser = ser.loc[ser> threshhold_research_interests]

        for i in range(len(ser)):
            student_new_reserach_interests.append(ser.index[i][0])
            student_research_intrests.add(ser.index[i][0])
            
            
        for student_new_research_interest in student_new_reserach_interests:
            
            if student_new_research_interest not in set_already_known_research_interest:
                
                set_already_known_research_interest.add(student_new_research_interest)
                list_research_interests_scores.append((student_new_research_interest,counter))
                print((student_new_research_interest,counter))
   

 #    student_research_intrests.add(set(student_new_reserach_interests))

        len_student_reserach_interests = len(student_research_intrests)

    indexes = []
    for research_interest in student_research_intrests:
 #       print(research_interest)
        for i in range(len(data)):
            if research_interest in data.iloc[i,6]:
                indexes.append(i)
                
                
    return data.iloc[indexes], list_research_interests_scores, len(seed_set_research_interests)


# In[23]:


def organize_based_on_priority(selected_data, list_scores, len_seed):
    dict_scores = dict(list_scores)
    dict_scores_update = dict([(key,1/dict_scores[key]) for key in dict_scores.keys()])
    dict_scores_update
    scale = 100/len_seed
    selected_data["Similarity_Percentage"] = 0
    
    for i in range(len(selected_data)):
        prof_research_interests = selected_data.iloc[i,6].split(", ")
        score = 0
        for ri in prof_research_interests:

            if ri in dict_scores_update.keys():
                score += dict_scores_update[ri]
    #        print(ri)


        selected_data["Similarity_Percentage"].iloc[i] = score * scale
    static_scale = 100 - selected_data.Similarity_Percentage.max()
    selected_data["Similarity_Percentage"] += static_scale
    
    final_data = selected_data.sort_values("Similarity_Percentage",ascending=0).drop_duplicates('Name')
    return final_data


# In[25]:


def exctract_best_proffesors(data_path,final_path, list_ri, strictness, expandability):
    selected_data, list_scores, len_seed  = selected_prof_based_on_seed_Research_interests(data_path,list_ri,strictness, expandability)
    final_data = organize_based_on_priority(selected_data, list_scores, len_seed)
    final_data.to_excel(final_path)
    return final_data

