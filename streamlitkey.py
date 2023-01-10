import numpy as np
import streamlit as st
import io
from zipfile import ZipFile

def generate_key(n: int, low: int, high: int) -> np.ndarray:
    A = np.random.randint(low, high, size=(n, n))
    while np.linalg.matrix_rank(A) < n:
        A = np.random.randint(low, high, size=(n, n))
    return A

def create_all_monthly_key():
    for day in range(1,32):
        for shape in range(5,51):    
            np.savetxt(str(day)+"_"+str(shape)+"_"+".csv",generate_key(shape, 1, 10))




st.set_page_config(page_title="Key", page_icon=":key:")

st.title('Encryption Key WebApp')
st.write('---')
st.write("[Use WebApp for Msg Encryption](https://debojyoti31-simple-msg-encryption.streamlit.app/)")

with st.container():

    option = st.radio('**Select Operation Type**',('Generate Single Key', 'Generate All Keys of a month'))
    if option == 'Generate Single Key':

        shape = st.slider('Key Shape', 5, 50, 1)
        
        if st.button('Generate'):
            key = generate_key(shape, 1, 10)
              
            with io.BytesIO() as buffer:
                np.savetxt(buffer, key)
                st.download_button(
                label="Download key",
                data = buffer, # Download buffer
                file_name = 'key.csv',
                mime='text/csv'
                    ) 

    if option == 'Generate All Keys of a month':

        if st.button('Generate'):
            with st.spinner('generating....'):

                all_keys1 = []
                names1 = []  
                
                for day in range(1,32):
                    for shape in range(5,51):  
                        all_keys1.append(generate_key(shape, 1, 10))
                        names1.append(str(day)+'_'+str(shape))

                all_keys = np.array(all_keys1,dtype=object)
                names = np.array(names1)
                



                def create_zip_from_arrays(all_keys,names):
                    # Create a BytesIO object to hold the ZIP data
                    buffer = io.BytesIO()

                    # Create a ZIP archive in memory
                    with ZipFile(buffer, "w") as archive:
                        for i, array in enumerate(all_keys):
                            # Create a BytesIO object to hold the CSV data
                            csv_buffer = io.StringIO()
                            np.savetxt(csv_buffer, array, fmt='%d')
                            csv_buffer.seek(0)
                            archive.writestr(names[i]+'.csv', csv_buffer.getvalue())
                            csv_buffer.close()

                    # Move the buffer's position back to the beginning
                    buffer.seek(0)
                    return buffer

                
                buffer = create_zip_from_arrays(all_keys,names)
                st.download_button("Download ZIP", buffer.getvalue(),file_name = 'all_key.csv')
                buffer.close()
