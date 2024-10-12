
# A framework for easy crud in streamlit

[
    ![Open in Remote - Containers](
        https://xebia.com/wp-content/uploads/2023/11/v1.svg    )
](
    https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/seeli-ai/streamlit-crud.git
)

## How to use

All the code for the framework is in the CrudDialog.py file. You can copy this file to your project and use it as a module.

In the file UserDialog.py you can see an example of how to use the framework.
It is recommended to copy this file to your project and modify it to your needs.

Here are the steps to modify the UserDialog.py file to your needs:

- dialog_title: The title of the dialog
- name: The name of the dialog. Has to be unique in your app.
- the function to call in your repository to manipulate the data
- Extra buttons and their functions if needed

- There is a class to handle the state of the dialog. You have to add the state.item and specify the type of the item.
- Then you have to specify the dataframe that you want to use in the grid to select the item. This is done in the method `load_data_for_gird` This dataframe has to have an a column with the id of the item and this column has to be named `Id`. By setting the field `show_id_in_grid` you can specify if you want to show the id in the grid or not.
- In the method `show_grid` you have to specify the datatypes of your columns in the grid. 
- Next you have to specify the form fields that you want to show in the dialog. This is done in the method `show_form`. You have to specify the type of the field and the label that you want to show. You can also specify if the field is required or not.
- And then you have to specify the save function that is called when the save button is clicked. 
- Don't forget to add the creation of the dialog as your last statement below the class definition.




