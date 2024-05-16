# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# Import required packages

import os
import time
import pandas as pd
import shutil
import re
from powerbiclient import Report, models
from powerbiclient.authentication import InteractiveLoginAuthentication
device_auth = InteractiveLoginAuthentication()

# Function to render powerbi report in Jupyter notebook
def render_pbi_report(url):
    group_id = re.search(r'groups/([^/]+)/', url).group(1)
    report_id = re.search(r'reports/([^/]+)/', url).group(1)
    
    report = Report(group_id = group_id, report_id = report_id, auth = device_auth)
    return report


# Extract visual table data from each visual of the report
def get_visual_data(report,df_name,ROOT_PATH,report_name):
    responses = []
    main_column_list = []

    master_folder = os.path.join(ROOT_PATH,report_name)
    visual_data_folder = os.path.join(ROOT_PATH,report_name,"visual_data_folder")
    llm_response_folder = os.path.join(ROOT_PATH,report_name,"llm_response")
    analysis_folder = os.path.join(ROOT_PATH,report_name,"analysis")
    report_folder = os.path.join(ROOT_PATH,report_name,"reports")
    read_folder = os.path.join(ROOT_PATH,report_name,"read_folder")

    Page_id_list,Visual_ID_list,Page_Name_list,Title_list,Visualization_list = [],[],[],[],[]

    if not os.path.exists(master_folder):
        os.makedirs(master_folder)  
    if not os.path.exists(analysis_folder):
        os.makedirs(analysis_folder)
    if not os.path.exists(read_folder):
        os.makedirs(read_folder) 
    
    report_pages=report.get_pages()
    Page_id = []
    Page_Name = []
    Visual_ID = []
    Visualization = []
    Title = []

    for report_page in report_pages:
        if report_page['visibility'] == 0 and report_page['isActive'] == True:
            #print(f"Page_id: {report_page['name']}, Page_Name: {report_page['displayName']}, Visibility: {report_page['visibility']}")
            Page_id.append(report_page['name'])
            Page_Name.append(report_page['displayName'])
            report_visuals=report.visuals_on_page(report_page["name"])
            for report_visual in report_visuals:
                try:
                    title = report_visual['title']
                except:
                    title = None

                #print(f"Visual ID: {report_visual['name']}, Visualization Type:{report_visual['type']}, Title: {title}")
                Visual_ID.append(report_visual['name'])
                Visualization.append(report_visual['type'])
                Title.append(title)


    Page_id = Page_id * len(Visual_ID)
    Page_Name = Page_Name * len(Visual_ID)
    data = list(zip(Page_id, Page_Name, Visual_ID, Visualization, Title))
    df = pd.DataFrame(data, columns=["Page_id", "Page_Name", "Visual_ID", "Visualization", "Title"])
    dont_consider = ["actionButton", "basicShape", "textbox","image","shape","qnaVisual"]
    df_name = df[~df["Visualization"].isin(dont_consider)]
    new_df = df_name
    Page_id_list = list(new_df["Page_id"])
    Visual_ID_list = list(new_df["Visual_ID"])
    Page_Name_list = list(new_df["Page_Name"])
    Title_list = list(new_df["Title"])
    Visualization_list = list(new_df["Visualization"])
    
    #print(f'{list(final_df["Page_Name"])}; {list(final_df["Title"])}; {list(final_df["Visualization"])}')
    #folder_pathname = os.path.join(ROOT_PATH, report_name)
    for i in range(len(Page_id_list)):
        try:
            print(f'Entered try loop {i} : {Page_id_list[i]} ; {Visual_ID_list[i]}')
            viz_data=report.export_visual_data(Page_id_list[i],Visual_ID_list[i])
            #print(f'viz_data : {viz_data}')
            file_path = os.path.join(read_folder, f"{report_name}_{Page_Name_list[i]}_{Title_list[i]}.csv")
            print(file_path)
            with open(file_path, "w") as file:
                file.write(viz_data)
            dummy2 = pd.read_csv(file_path)
            if "Unnamed: 0" in dummy2:
                dummy2.drop(columns = "Unnamed: 0", axis = 1, inplace = True)
            dummy3_columns = dummy2.columns.tolist()
            main_column_list.append(dummy3_columns)
            dummy2.to_csv(file_path)
        except:
            pass
    
    
    return new_df



