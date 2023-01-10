import numpy as np
import streamlit as st
import io
from io import StringIO

def text_to_matrix(text):
  # Split the text into a list of words
  words = text.split()
  # Find the longest word
  max_len = len(max(words, key=len))
  # Add spaces to the end of each word to make them all the same length
  for i in range(len(words)):
    words[i] = words[i] + " " * (max_len - len(words[i]))
  # Create a matrix by transposing the list of words
  matrix1 = [[ord(row[i]) for row in words] for i in range(max_len)]
  matrix = np.transpose(matrix1)
  # Convert the matrix to a numpy array
  matrix = np.array(matrix)
  return matrix

def encode(matrix, key):
  # Multiply the matrix by the key
  encoded = np.matmul(matrix, key)
  # Print the encoded matrix
  return encoded


def decode(encoded, key):
  # Find the inverse of the key matrix
  key_inv = np.linalg.inv(key)
  # Multiply the encoded matrix by the inverse of the key matrix
  matrix1 = np.matmul(encoded, key_inv)
  matrix = np.rint(np.transpose(matrix1))
  matrix2 = matrix.astype(int)


  # Find the number of rows in the matrix
  num_rows = len(matrix2[0])
  # Create a list of words by reading the matrix column by column
  words = [''.join([chr(row[i]) for row in matrix2]) for i in range(num_rows)]
  # Strip the extra spaces from the end of each word
  words = [word.rstrip() for word in words]
  # Join the words into a single string and return it
  return " ".join(words)











st.set_page_config(page_title="Encryption", page_icon=":shushing_face:")

st.title('Simple Msg Encryption WebApp')
st.write('---')


with st.container():


        option = st.radio('**Select Operation Type**',('Encode', 'Decode'))
        
        if option == 'Encode':


          input_option = st.radio('**Select Input Type**',('Write Msg', 'Upload txt File'))
          if input_option == 'Write Msg':
            input_text = st.text_area('**Text to Encode**', '''Shhh! don't read it!''')
          if input_option == 'Upload txt File':
            uploaded_text = st.file_uploader("Upload txt file Here")
            input_text = ''
            if uploaded_text is not None:
              input_text = StringIO(uploaded_text.getvalue().decode("utf-8")).read()

          input_text += ' -- Created By DM31'
            
          matrix_text= text_to_matrix(input_text)
            
          if st.button('Check Key Shape'):
            st.write('Key shape should be',matrix_text.shape[1])
          st.write("[Use WebApp to Generate Key](https://debojyoti31-msg-encryption-key.streamlit.app/)")
          uploaded_key = st.file_uploader("Upload Key Here")  
            
          if st.button('Encode'):
            key = np.genfromtxt(uploaded_key)
              
            try:   
              encoded_msg = encode(matrix_text, key)
            except:
              st.write('Error! Check Key Shape')
              
            with io.BytesIO() as buffer:
                np.savetxt(buffer, encoded_msg)
                st.download_button(
                label="Download encoded msg as CSV",
                data = buffer, # Download buffer
                file_name = 'encoded_msg.csv',
                mime='text/csv'
                    ) 
        


        
        if option == 'Decode':

          uploaded_msg = st.file_uploader("Upload Encoded Msg Here")
          uploaded_key = st.file_uploader("Upload the key Here")
          if st.button('Decode'):
            key = np.genfromtxt(uploaded_key)
            msg = np.genfromtxt(uploaded_msg)
            try:    
              decoded = decode(msg, key)
            except:
              st.write('Error! Check Key Shape')

            st.download_button(
            label="Download decoded msg as txt",
            data=decoded,
            file_name='decoded_msg.txt',
            mime='text/plane',
            )
