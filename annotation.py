import streamlit as st
import pandas as pd

# Function to read CSV file
def read_csv(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None

# Function to save CSV file
def save_csv(df, file):
    try:
        df.to_csv(file, index=False)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Error saving CSV file: {e}")

# def load_item(df, index):

#     # Editable cells


    

# Streamlit app
def main():
    st.title("CSV File Editor")

    # File upload section
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read CSV file
        if 'df' not in st.session_state:
            st.session_state.df = read_csv(uploaded_file)

        if st.session_state.df is not None:
            st.success("File uploaded successfully!")

            # Display the DataFrame
            # st.dataframe(df)

            # Navigation buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            with col3:
                if 'index' not in st.session_state:
                    st.session_state.index = 0

                current_index = st.empty()

                jump_index = st.text_input(label="Jump to Index")
                # jump_button = st.button("Jump", key="jump_button")
  
                
                            
            # Next and Previous buttons
            if col1.button("<< Previous",type='primary'):
                st.session_state.df.at[st.session_state.index, 'ans_sent'] = st.session_state.new_value

                st.session_state.index = max(0, st.session_state.index - 1)

                current_index.text(f"Row: {st.session_state.index + 1}")
                save_csv(st.session_state.df, "edited_data.csv")

                


            # Handle Jump button click
            if col3.button("Jump", key="jump_button",type='primary'):

                try:
                    
                    st.session_state.df.at[st.session_state.index, 'ans_sent'] = st.session_state.new_value

                    st.session_state.index = max(0, min(len(st.session_state.df) - 1, int(jump_index)))

                    current_index.text(f"Row: {st.session_state.index}")

                    save_csv(st.session_state.df, "edited_data.csv")

                except ValueError:
                    st.warning("Please enter a valid index.")

            if col5.button("Next >>", type='primary'):

                st.session_state.df.at[st.session_state.index, 'ans_sent'] = st.session_state.new_value

                st.session_state.index = min(len(st.session_state.df) - 1, st.session_state.index + 1)

                current_index.text(f"Row: {st.session_state.index}")

                save_csv(st.session_state.df, "edited_data.csv")
                

            col_names = ['news','masked headline', 'ans', 'calculation', 'ans_sent']
            for col in col_names:

                if col=='ans_sent':
                    response = st.session_state.df.loc[st.session_state.index, col]
                    # response = response.replace("$","\$")
                    st.session_state.new_value = st.text_area(f"Edit Response for Row {st.session_state.index + 1}", response, height=500)
                    st.session_state.df.at[st.session_state.index, col] = st.session_state.new_value
                else:
                    value = st.session_state.df.loc[st.session_state.index, col]
                    value = value.replace("$","\$")
                    st.write(f"**{col.capitalize()}**: {value}")


            # Save button
            if st.button("Save Changes",type='primary'):
                save_csv(st.session_state.df, f"edited_data.csv")
                return


if __name__ == "__main__":
    main()
