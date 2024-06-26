# import json
# import openai
# import time
# import pandas as pd
# import matplotlib.pyplot as plt
# import streamlit as st
# import yfinance as yf
# import datetime
# @st.cache_data(max_entries=1000, ttl=3600 * 24 * 7)  # Cache up to 1000 entries for 7 days
# def cache_chat_history():
#     if 'messages' not in st.session_state:
#         st.session_state['messages'] = []
#     return st.session_state['messages']

# # Retrieve the cached chat history
# chat_history = cache_chat_history()
# API_KEY="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"

# openai.api_key=API_KEY

# def get_stock_price(ticker):
#     return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)

# def calculate_SMA(ticker,window):
#     data=yf.Ticker(ticker).history(period='1y').Close
#     return str(data.rolling(window=window).mean().iloc[-1])

# def calculate_EMA(ticker,window):
#     data=yf.Ticker(ticker).history(period='1y').Close
#     return str(data.ewm(span=window,adjust=False).mean().iloc[-1])

# def calculate_RSI(ticker):
#     data=yf.Ticker(ticker).history(period='1y').Close
#     delta=data.diff()
#     up=delta.clip(lower=0)
#     down=-1*delta.clip(upper=0)
#     ema_up=up.ewm(com=14-1,adjust=False).mean()
#     ema_down=down.ewm(com=14-1,adjust=False).mean()
#     rs=ema_up/ema_down
#     return str(100-(100/(1+rs)).iloc[-1])

# def calculate_MACD(ticker):
#     data=yf.Ticker(ticker).history(period='1y').Close
#     short_EMA=data.ewm(span=12,adjust=False).mean()
#     long_EMA=data.ewm(span=26,adjust=False).mean()
#     MACD=(short_EMA-long_EMA)
#     signal=MACD.ewm(span=9,adjust=False).mean()
#     MACD_histogram=MACD-signal
#     return f'{MACD[-1]},{signal[-1]},{MACD_histogram[-1]}'


# def plot_stock_price(ticker):
#     data=yf.Ticker(ticker).history(period='1y')
#     plt.figure(figsize=(10,5))
#     plt.plot(data.index,data.Close)
#     plt.title('{ticker}Stock Price over Last year')
#     plt.xlabel('Date')
#     plt.ylabel('Stock Price ($)')
#     plt.grid(True)
#     plt.savefig('stock.png')
#     plt.close()


# functions =[
#     {
#         "name":"get_stock_price",
#         "description":"Gets the latest stock price given the ticker symbol of  company",
#         "parameters":{
#             "type":"object",
#             "properties":{
#                 "ticker":{
#                     "type":"string",
#                     "description":"The ticker symbol for a company"
#                 }
#             },
#             "required":["ticker"]
#         }
#     },
#     {
#         "name":"calculate_SMA",
#         "description":"Calculate the simple moving average for  a given stock ticket and a window",
#         "parameters":{
#             "type":"object",
#             "properties":{
#                 "ticker":{
#                     "type":"string",
#                     "description":"The ticker symbol for a company"
#                 },
#                 "window":{
#                     "type":"integer",
#                     "description":"The timeframe to consider when calculating the SMA"

#                 }
#             },
#             "required":["ticker","window"]
#         },
#     },
#     {
#         "name":"calculate_EMA",
#         "description":"Calculate the exponential moving average for  a given stock ticket and a window",
#         "parameters":{
#             "type":"object",
#             "properties":{
#                 "ticker":{
#                     "type":"string",
#                     "description":"The ticker symbol for a company"
#                 },
#                 "window":{
#                     "type":"integer",
#                     "description":"The timeframe to consider when calculating the EMA"

#                 }
#             },
#             "required":["ticker","window"]
#         },
#     },
#     {
#         "name":"calculate_RSI",
#         "description":"Calculate the RSI for  a given stock ticker",
#         "parameters":{
#             "type":"object",
#             "properties":{
#                 "ticker":{
#                     "type":"string",
#                     "description":"The ticker symbol for a company"
#                 },
#             },
#             "required":["ticker"]
#         },

#     },
#     {
#          "name":"calculate_MACD",
#         "description":"Calculate the MACD for  a given stock ticker ",
#         "parameters":{
#             "type":"object",
#             "properties":{
#                 "ticker":{
#                     "type":"string",
#                     "description":"The ticker symbol for a company"
#                 },
#             },
#             "required":["ticker"]
#         },
#     },
#     {
#          "name":"plot_stock_price",
#         "description":"Plot the stockprice  for the last year given the  ticker symbol of a company",
#         "parameters":{
#             "type":"object",
#             "properties":{
#                 "ticker":{
#                     "type":"string",
#                     "description":"The ticker symbol for a company"
#                 },
#             },
#             "required":["ticker"]
#         },
#     }
# ]
# available_functions={
#     'get_stock_price': get_stock_price,
#     'calculate_SMA': calculate_SMA,
#     'calculate_EMA': calculate_EMA,
#     'calculate_MACD': calculate_MACD,
#     'calculate_RSI': calculate_RSI,
#     'plot_stock_price': plot_stock_price


# }
# if 'messages' not in st.session_state:
#     st.session_state['messages']=[]

# st.title('Stock Analysis Chatbot Assistant')
# user_input=st.text_input('Enter your message:')
# if user_input:
#     try:
#         st.session_state['messages'].append({'role':'user','content':f'{user_input}'})

#         response = openai.ChatCompletion.create(
#             model='gpt-3.5-turbo',
#             messages=st.session_state['messages'],
#             functions=functions,
#             function_call='auto'

#         )
#         response_message=response['choices'][0]['message']
#         if response_message.get('function_call'):
#             function_name=response_message['function_call']['name']
#             function_args=json.loads(response_message['function_call']['arguments'])
#             if function_name in ['get_stock_price','plot_stock_price','calculate_RSI','calculate_MACD']:
#                 args_dict={'ticker':function_args.get('ticker')}
#             elif function_name in [ 'calculate_SMA','calculate_EMA']:
#                 args_dict={'ticker':function_args.get('ticker'),'window':function_args.get('window')} 
#             function_to_call = available_functions[function_name]
#             function_response = function_to_call(**args_dict)
#             if function_name == 'plot_stock_price':
#                 st.image('stock.png')
#             else:
#                 st.session_state['messages'].append(response_message) 
#                 st.session_state['messages'].append(
#                     {'role': 'function',
#                      'name': function_name,
#                      'content': function_response
#                      }
#                 )
#                 second_response = openai.ChatCompletion.create(
#                     model='gpt-3.5-turbo',
#                     messages=st.session_state['messages']
#                 )
#                 st.text(second_response['choices'][0]['message']['content'])
#                 st.session_state['messages'].append({'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
#                 chat_history.append({'role': 'user', 'content': f'{user_input}'})
#         else:
#             st.text(response_message['content'])
#             st.session_state['messages'].append({'role': 'assistant', 'content':response_message['content']})
#             chat_history.append({'role': 'assistant', 'content': response_message['content']})

#     except Exception as e:
#         raise e          




import json
import openai
import time
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

API_KEY = "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"
openai.api_key = API_KEY

# ... (function definitions) ...
def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)

def calculate_SMA(ticker,window):
    data=yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])

def calculate_EMA(ticker,window):
    data=yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window,adjust=False).mean().iloc[-1])

def calculate_RSI(ticker):
    data=yf.Ticker(ticker).history(period='1y').Close
    delta=data.diff()
    up=delta.clip(lower=0)
    down=-1*delta.clip(upper=0)
    ema_up=up.ewm(com=14-1,adjust=False).mean()
    ema_down=down.ewm(com=14-1,adjust=False).mean()
    rs=ema_up/ema_down
    return str(100-(100/(1+rs)).iloc[-1])

def calculate_MACD(ticker):
    data=yf.Ticker(ticker).history(period='1y').Close
    short_EMA=data.ewm(span=12,adjust=False).mean()
    long_EMA=data.ewm(span=26,adjust=False).mean()
    MACD=(short_EMA-long_EMA)
    signal=MACD.ewm(span=9,adjust=False).mean()
    MACD_histogram=MACD-signal
    return f'{MACD[-1]},{signal[-1]},{MACD_histogram[-1]}'


def plot_stock_price(ticker):
    data=yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10,5))
    plt.plot(data.index,data.Close)
    plt.title('{ticker}Stock Price over Last year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()


functions =[
    {
        "name":"get_stock_price",
        "description":"Gets the latest stock price given the ticker symbol of  company",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The ticker symbol for a company"
                }
            },
            "required":["ticker"]
        }
    },
    {
        "name":"calculate_SMA",
        "description":"Calculate the simple moving average for  a given stock ticket and a window",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The ticker symbol for a company"
                },
                "window":{
                    "type":"integer",
                    "description":"The timeframe to consider when calculating the SMA"

                }
            },
            "required":["ticker","window"]
        },
    },
    {
        "name":"calculate_EMA",
        "description":"Calculate the exponential moving average for  a given stock ticket and a window",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The ticker symbol for a company"
                },
                "window":{
                    "type":"integer",
                    "description":"The timeframe to consider when calculating the EMA"

                }
            },
            "required":["ticker","window"]
        },
    },
    {
        "name":"calculate_RSI",
        "description":"Calculate the RSI for  a given stock ticker",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The ticker symbol for a company"
                },
            },
            "required":["ticker"]
        },

    },
    {
         "name":"calculate_MACD",
        "description":"Calculate the MACD for  a given stock ticker ",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The ticker symbol for a company"
                },
            },
            "required":["ticker"]
        },
    },
    {
         "name":"plot_stock_price",
        "description":"Plot the stockprice  for the last year given the  ticker symbol of a company",
        "parameters":{
            "type":"object",
            "properties":{
                "ticker":{
                    "type":"string",
                    "description":"The ticker symbol for a company"
                },
            },
            "required":["ticker"]
        },
    }
]
available_functions={
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_MACD': calculate_MACD,
    'calculate_RSI': calculate_RSI,
    'plot_stock_price': plot_stock_price


}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title('Stock Analysis Chatbot Assistant')

# Display the chat history
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.markdown(f"**User:** {message['content']}")
    elif message['role'] == 'assistant':
        st.markdown(f"**Assistant:** {message['content']}")
    elif message['role'] == 'function':
        st.markdown(f"**Function Response ({message['name']}):** {message['content']}")

user_input = st.text_input('Enter your message:')
if user_input:
    try:
        st.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=st.session_state['messages'],
            functions=functions,
            function_call='auto'
        )
        response_message = response['choices'][0]['message']
        if response_message.get('function_call'):
            function_name = response_message['function_call']['name']
            function_args = json.loads(response_message['function_call']['arguments'])
            if function_name in ['get_stock_price', 'plot_stock_price', 'calculate_RSI', 'calculate_MACD']:
                args_dict = {'ticker': function_args.get('ticker')}
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**args_dict)
            if function_name == 'plot_stock_price':
                st.image('stock.png')
            else:
                st.session_state['messages'].append(response_message)
                st.session_state['messages'].append(
                    {'role': 'function', 'name': function_name, 'content': function_response}
                )
                second_response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=st.session_state['messages']
                )
                st.session_state['messages'].append(
                    {'role': 'assistant', 'content': second_response['choices'][0]['message']['content']}
                )
                st.markdown(f"**Assistant:** {second_response['choices'][0]['message']['content']}")
        else:
            st.session_state['messages'].append({'role': 'assistant', 'content': response_message['content']})
            st.markdown(f"**Assistant:** {response_message['content']}")

    except Exception as e:
        raise e