import streamlit as st
from repository import get_db_session
from abc import ABC, abstractmethod
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


class DialogState:
    def __init__(self):
        print("DialogState.__init__")
        self.id = 0
        self.confirm_delete = None
        self.deleting = False
        self.grid_data = []
        self.data_frame = None
        self.view_mode = "grid"

class CrudDialog(ABC):

    dlg_title = "NotSet"
    name = "NotSet"
    show_id_in_grid = True

    # repo functions
    add_func = None
    read_all_func = None
    transfer_to_one = None
    read_one_func = None
    delete_func = None
    save_func = None

    func_left = []
    func_right = []
    extra_left = []
    extra_right = []

    def __init__(self):
        print("CrudDialog.__init__")
        self.state = self.manage_state()
        self.show()

    
    def show(self):
        print("show " + self.dlg_title) 
        st.title(self.dlg_title)

        if self.state.view_mode == "grid":
            self.select_item_to_edit()
        else:
            if self.state.item is None:
                self.state.view_mode = "grid"
                st.rerun()
            else:
                self.show_form()
    
    def set_item(self, item):
        self.state.id = item.id
        self.state.item = item


    @st.dialog("Confirm Delete")
    def confirm_delete(self, item):
        print("confirm_delete")
        st.write(f"Are you sure you want to delete {item}?")
        c1, dummy, c2 = st.columns([1, 5, 1])
        if c1.button("✖️"):
            self.state.confirm_delete = False
            st.rerun()

        if c2.button("✔️"):
            self.state.confirm_delete = True
            self.state.deleting = True
                      
            st.rerun()

    @abstractmethod
    def create_initial_state(self):
        pass

    @abstractmethod
    def load_data_for_gird(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def show_form(self):
        pass

    @abstractmethod
    def show_grid(self):
        pass
    
    def manage_state(self):
        if self.name not in st.session_state:
            st.session_state[self.name] = self.create_initial_state()
            print("Created initial state for ", self.name)
        
        self.state = st.session_state[self.name]
        print("State: ", type(self.state))

        if self.state.deleting == False:
            self.state.confirm_delete = None

        return self.state
    
    def add_buttons(self):
        len_extra_left = len(self.extra_left)
        len_extra_right = len(self.extra_right)
        total_buttons = 5 + len_extra_left + len_extra_right
        columns = st.columns(total_buttons)
        buttons = []

        for i, button_text in enumerate(self.extra_left):
            buttons.append(columns[i].form_submit_button(button_text))

        for i in range(5):

            if (i == 0):
                buttons.append(columns[i + len_extra_left].form_submit_button("➕"))
            elif (i == 1):
                buttons.append(
                    columns[i + len_extra_left].form_submit_button("🗑️"))
            elif (i == 2):
                buttons.append(columns[i + len_extra_left].form_submit_button("💾"))
            elif (i == 3):
                buttons.append(
                    columns[i + len_extra_left].form_submit_button("✖️"))
            elif (i == 4):
                buttons.append(
                    columns[i + len_extra_left].form_submit_button("✔️"))
        for i, button_text in enumerate(self.extra_right):
            buttons.append(columns[i + len_extra_left +
                        5].form_submit_button(button_text))

        return buttons


    def do_cancel(self):
        self.state.id = 0
        self.state.item = None
        self.state.view_mode = "grid"
        st.rerun()


    def do_new(self):
        session = next(get_db_session())
        new_item = self.add_func(session=session)
        self.set_item(new_item)
        self.state.view_mode = "form"
        st.rerun()


    def handle_buttons(self, buttons):

        for i, button_func in enumerate(self.func_left):
            if (buttons[i]):
                button_func()
                st.stop()

        if buttons[0 + len(self.func_left)]:   # new
            print("Adding new item...")
            self.do_new()

        if buttons[1 + len(self.func_left)] or self.state.deleting:   # delete
            print("deleting...")
            self.state.is_deleting = True
            self.handle_delete_request()

        if buttons[2 + len(self.func_left)]:   # save
            print("saving...")
            self.save()

        if buttons[3 + len(self.func_left)]:  # cancel
            print("cancelling...")
            self.do_cancel()

        if buttons[4 + len(self.func_left)]:  # save and close
            print("saving and closing...")
            self.save()
            self.do_cancel()

        for i, button_func in enumerate(self.func_right):
            if (buttons[i + 5 + len(self.func_left)]):
                button_func()
                st.stop()

    def handle_delete_request(self):

        if self.state.deleting == False or self.state.item is None:
            self.state.confirm_delete = None
            return
        
        if (self.state.confirm_delete is None):
            self.confirm_delete(self.state.item)
            st.stop()
        
        if self.state.confirm_delete:
            self.delete_func(self.state.id)
            self.state.id = 0
            self.state.item = None
            self.state.deleting = False
            self.state.confirm_delete = None
            self.state.view_mode = "grid"
            st.rerun()
        else:
            self.state.confirm_delete = None
            self.state.deleting = False

    def handle_no_items(self):
        st.warning("No items found")
        if st.button("➕"):
            self.do_new()
        st.stop()

    def grid_display(self, df):

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=False, groupable=False)
        gb.configure_selection('single', use_checkbox=False, rowMultiSelectWithClick=False)
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()

        column_defs = gridOptions["columnDefs"]
        columns_to_hide = ["Id"]

        if not self.show_id_in_grid:
            for col in column_defs:
                if col["headerName"] in columns_to_hide:
                    col["hide"] = True

        grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        theme='streamlit',
        enable_enterprise_modules=True,
        height=350,
        width='100%',
        reload_data=True
        )

        selected_rows = grid_response['selected_rows']
        if selected_rows is not None and len(selected_rows) > 0:
            record = selected_rows.iloc[0]
            id = int(record['Id'])
            print("Selected Id: ", id)
            item = self.read_one_func(id)
            print("Selected Item: ", item)
            return item
        else:
            return None


    def select_item_to_edit(self):
        self.handle_delete_request()
        self.load_data_for_gird()

        if len(self.state.grid_data) == 0:
            self.handle_no_items()
            st.stop()
    
        selected_item = self.show_grid()

       
        d1,d2,d3,d4,d5,d6,d7,col1, col2, col3 = st.columns(10)
        add = col1.button("➕")
        if add:
            self.do_new()

        if selected_item is not None:
            self.set_item(selected_item)

        if self.state.item is None:
            self.state.view_mode = "grid"
            disable_buttons = True
        else:
            disable_buttons = False
        # Buttons for the grid
        delete = col2.button("🗑️", disabled=disable_buttons)
        if delete:
            self.state.deleting = True
            self.handle_delete_request()

        edit = col3.button("✏️", disabled=disable_buttons)
        if edit:
            self.state.view_mode = "form"
            st.rerun()


        print("we reached the end of select_item_to_edit")


