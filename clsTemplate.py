################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  27-May-2023               ####
#### Modified On: 26-Nov-2023               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the template for    ####
#### OpenAI prompts to get the correct      ####
#### response.                              ####
####                                        ####
################################################

# Template to use for the system message prompt
templateVal_1 = """
    You are a helpful assistant, answer the question accurately based on the above data with the supplied source file details. Only relevant content needs to publish. Please do not provide the facts or the texts that results crossing the max_token limits. Based on the following documents:\n\n

    If you feel like you don't have enough information to answer the question, say "I don't know".
    """
