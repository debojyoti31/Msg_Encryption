import numpy as np
import streamlit as st
import io

def generate_key(n: int, low: int, high: int) -> np.ndarray:
    A = np.random.randint(low, high, size=(n, n))
    while np.linalg.matrix_rank(A) < n:
        A = np.random.randint(low, high, size=(n, n))
    return A






st.set_page_config(page_title="Key", page_icon=":key:")

st.title('Encryption Key WebApp')
st.write('---')
st.write("[Use WebApp for Msg Encryption](https://debojyoti31-simple-msg-encryption.streamlit.app/)")

with st.container():

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

