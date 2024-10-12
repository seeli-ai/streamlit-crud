# -*- coding: utf-8 -*-
import streamlit as st
import repository as repo
from models import User
from CrudDialog import CrudDialog, DialogState
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import numpy as np

class UserDialogState(DialogState):
    def __init__(self):
        super().__init__()
        self.item: User = None



class UserDialog(CrudDialog):

    dlg_title = "User"
    name = "User"

    # repo functions
    add_func =  staticmethod(repo.create_empty_user)
    read_all_func = staticmethod(repo.get_all_users)
    read_one_func = staticmethod(repo.get_user_by_id)
    delete_func = staticmethod(repo.delete_user)
    save_func = staticmethod(repo.update_user)
    
    func_left = []
    func_right = []
    extra_left = []
    extra_right = []

    show_id_in_grid = False



    def set_item(self, item: User):
        super().set_item(item)


    def create_initial_state(self):
        return UserDialogState()
        
    def load_data_for_gird(self):
        print("load_data_for_gird")
        items = self.read_all_func()
        
        self.state.grid_data = items

        self.state.data_frame = pd.DataFrame([(item.id, item.userid, item.name, item.age, item.is_active) for item in self.state.grid_data], 
                        columns=["Id", 'User Id', 'Name', 'Age', 'Is Active'])

    def show_grid(self):
        print("show_grid")
        df = self.state.data_frame.copy()
        df['Id'] = df['Id'].astype(np.int32)
        df['User Id'] = df['User Id'].astype(str)
        df['Name'] = df['Name'].astype(str)
        df['Age'] = df['Age'].astype(np.int32)
        df['Is Active'] = df['Is Active'].astype(np.bool)

        selected_item = self.grid_display(df)
        return selected_item


        
        

    def show_form(self):
        with st.form(key="form"):
            self.state.item.userid = st.text_input("UserId", value=self.state.item.userid)
            self.state.item.name = st.text_input("Name", value=self.state.item.name)
            self.state.item.age = st.number_input("Age", value=self.state.item.age)
            self.state.item.is_active = st.checkbox("Is Active", value=self.state.item.is_active)
            buttons =  self.add_buttons()
    
        self.handle_buttons(buttons)
    
    def save(self):
        return self.save_func(self.state.id, 
                              userid=self.state.item.userid, 
                              name=self.state.item.name, 
                              age=self.state.item.age, 
                              is_active=self.state.item.is_active)

UserDialog()

