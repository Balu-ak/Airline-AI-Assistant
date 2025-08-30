#!/usr/bin/env python
# coding: utf-8

# In[1]:


# imports

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr


# In[2]:


# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-5"
openai = OpenAI()


# In[3]:


system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."


# In[4]:


# This function looks rather simpler than the one from my video, because we're taking advantage of the latest Gradio updates

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

gr.ChatInterface(fn=chat, type="messages").launch()


# In[8]:


# Let's start by making a useful function

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
#available_cities = list(ticket_prices.keys())

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")

def get_available_cities():
    """Gets the complete list of cities where tickets are available."""
    print("Tool 'get_available_cities' called.")
    return list(ticket_prices.keys())


# In[9]:


get_ticket_price("Berlin")
type(available_cities)


# In[10]:


print("Available Cities:", get_available_cities())


# In[11]:


# There's a particular dictionary structure that's required to describe our function:

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city', If the customer ask what cities we can provide ticket prices for? just return the whole list of cities.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}


# In[14]:


available_cities_schema = {
    "name": "get_available_cities",
    "description": "Get the complete list of available cities for which a ticket price can be looked up.",
    "parameters": {
        # This part is crucial: it must be an object schema, even if there are no parameters.
        "type": "object",
        "properties": {},
        "required": []
    }
}


# In[15]:


# And this is included in a list of tools:

#tools = [{"type": "function", "function": price_function}]

tools = [
    {
        "type": "function",
        "function": price_function
    },
    {
        "type": "function",
        "function": available_cities_schema # <-- Added the new tool here
    }
]


# In[16]:


def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        
        # This unpacking now works correctly because handle_tool_call always returns 3 values
        tool_response, city, available_cities = handle_tool_call(message)
        
        messages.append(message)
        messages.append(tool_response) # Append the tool's response
        
        # Call the model again with the tool's output
        response = openai.chat.completions.create(model=MODEL, messages=messages)
    
    return response.choices[0].message.content


# In[18]:


# --- Tool Call Handler ---

def handle_tool_call(message):
    """
    Handles calls for different tools and consistently returns three values.
    """
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    tool_call_id = tool_call.id
    
    print(f"Handling tool call for function: '{function_name}'")

    city_context = None
    available_cities_list = None
    content = ""

    if function_name == "get_ticket_price":
        # Logic for the price-checking tool
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get('destination_city')
        price = get_ticket_price(city)
        content = json.dumps({"destination_city": city, "price": price})
        city_context = city # Set the city context

    elif function_name == "get_available_cities":
        # Logic for the available cities tool
        cities = get_available_cities()
        content = json.dumps({"available_cities": cities})
        available_cities_list = cities # Set the available cities list

    else:
        # Handle cases where the tool name is unknown
        content = json.dumps({"error": f"Tool '{function_name}' not found."})

    # Construct the final response dictionary
    response = {
        "role": "tool",
        "content": content,
        "tool_call_id": tool_call_id
    }
    
    # ALWAYS return three values to match the unpacking in the chat function
    return response, city_context, available_cities_list


# In[22]:


gr.ChatInterface(fn=chat, type="messages").launch(share = True, inbrowser =True)


# In[ ]:




