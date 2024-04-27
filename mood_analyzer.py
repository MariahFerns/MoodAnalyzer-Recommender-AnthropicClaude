#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install anthropic


# In[2]:


import streamlit as st
import anthropic


# In[5]:


def main():
    # Set page title
    st.title('Mood Analyzer App')
    
    # Get API Key
    api_key = st.text_input('Enter your Claude Anthropic API key:', type='password')
    
    if api_key:
        # Create the Anthropic Client
        client = anthropic.Anthropic(api_key = api_key)
        
        # Get users feelings
        user_ip = st.text_area('Enter your feeling for today:')
        
        # Create submit button
        if st.button('Analyze my Mood'):
            # Create API endpoint to Anthropic
            message = client.messages.create(
                model = 'claude-3-sonnet-20240229',
                max_tokens = 689, # to reduct the number of tokens used on free version
                temperature = 0, # setting the degree of randomness
                messages = [
                    {'role':'user', 
                     'content': f'''
                         Based on the following text, can you analyze the overall sentiment 
                         expressed by the person?\n\n{user_ip}
                     '''}
                ]
            )
        
        # Join the text of all blocks into a single string
        mood_analysis_text = ' '.join( block.text for block in message.content)
        
        # Display the mood analysis
        st.markdown('**Mood Analysis**')
        st.write(mood_analysis_text)
        
        
        # Based on the analysis, define mood category
        
        mood_categories = ['Happy', 'Sad', 'Angry', 'Anxious', 'Neutral']
        
        # Categorize the mood based on keywords
        # Set the default mood category
        mood_category = 'Neutral'
        for category in mood_categories:
            if category.lower() in mood_analysis_text.lower():
                mood_category = category
                break
                
        # Display the mood category in Streamlit
        
        mood_category_diplay = f'**Mood Category:** {mood_category}'
        
        if mood_category == 'Happy':
            st.success(mood_category_diplay)
        elif mood_category == 'Sad' or mood_category == 'Angry':
            st.error(mood_category_display)
        elif mood_category == 'Anxious':
            st.warning(mood_category_display)
        else: # Neutral
            st.info(mood_category_display)
            
            
        # Based on the mood category, make recomendations
        
        if mood_category != 'Neutral':
            # Make the API call
            message = client.messages.create(
                model = 'claude3-soonet-20240229',
                max_tokens = 689,
                temperature = 0,
                messages = [
                    {'role':'user',
                     'content':f'''
                         Based on the mood analysis {mood_analysis_text} and the 
                         mood category {mood_category}, can you make some recommendations
                         that would help the user feel better.
                     '''}
                ]
            )
            
            # Create the response string
            recommendations = ' '.join( block.text for block in message.content)
            
            # Display the recommendations
            st.markdown('**Recommendations:**')
            st.write(recommendations)
            
        
        else:
            st.warning('Please enter your Anthropic API key')


# In[6]:


# Call the main function

if __name__ == '__main__':
    main()

