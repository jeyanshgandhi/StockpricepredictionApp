import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
from signup import signup
from login import login

# Initialize session state for login and sign-up
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "sign_up_completed" not in st.session_state:
    st.session_state.sign_up_completed = False

# Display signup page if sign-up is not completed
if not st.session_state.sign_up_completed:
    signup()

# If sign-up is completed but the user has not logged in yet, show the login page
elif not st.session_state.logged_in:
    login()

# If the user is logged in, show the main app
if st.session_state.logged_in:
    st.title("Stock Price Prediction App")

    # Select a company
    company = st.selectbox("Select a company", ['HDFC', 'ICICI', 'AXIS', 'FEDRAL', 'INDUSLND', 'YES'])
    ticker_dict = {
        'HDFC': 'HDFCBANK.NS',
        'ICICI': 'ICICIBANK.NS',
        'AXIS': 'AXISBANK.NS',
        'FEDRAL': 'FEDERALBNK.NS',
        'INDUSLND': 'INDUSINDBK.NS',
        'YES': 'YESBANK.NS'
    }

    # Load the trained model
    model_path = 'C:/Users/dsbha/Documents/Stock Project/stock_prediction_model.keras'
    model = load_model(model_path)

    # Load preprocessed data
    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, start="2010-01-01", end="2023-01-01")
        data['MA50'] = data['Close'].rolling(window=50).mean()
        data['MA100'] = data['Close'].rolling(window=100).mean()
        data['MA200'] = data['Close'].rolling(window=200).mean()
        return data

    # Plot functions (same as before)
    def plot_ma50_price(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data['Close'], label='Closing Price')
        ax.plot(data['MA50'], label='MA50')
        ax.set_title(f"{data['Close'].name} Stock Price and MA_50")
        ax.legend()
        st.pyplot(fig)

    def plot_ma100_price(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data['Close'], label='Closing Price')
        ax.plot(data['MA100'], label='MA100')
        ax.set_title(f"{data['Close'].name} Stock Price and MA_100")
        ax.legend()
        st.pyplot(fig)

    def plot_ma50_ma100_price(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data['Close'], label='Closing Price')
        ax.plot(data['MA50'], label='MA50')
        ax.plot(data['MA100'], label='MA100')
        ax.set_title(f"{data['Close'].name} Stock Price and MA_50 and MA_100")
        ax.legend()
        st.pyplot(fig)

    def plot_moving_averages(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data['Close'], label='Closing Price')
        ax.plot(data['MA50'], label='MA50')
        ax.plot(data['MA100'], label='MA100')
        ax.plot(data['MA200'], label='MA200')
        ax.set_title(f"{data['Close'].name} Stock Price and Moving Averages")
        ax.legend()
        st.pyplot(fig)

    def plot_predicted_vs_actual(actual, predicted):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(actual, label='Actual Price')
        ax.plot(predicted, label='Predicted Price')
        ax.set_title("Predicted vs Actual Prices")
        ax.legend()
        st.pyplot(fig)

    # Load company data
    ticker = ticker_dict[company]
    data = load_data(ticker)

    # Display dataset
    st.subheader("Stock Data")
    st.write(data)

    # Plot MA_50 vs Price
    st.subheader(f"{company} Stock Price and MA_50")
    plot_ma50_price(data)

    # Plot MA_100 vs Price
    st.subheader(f"{company} Stock Price and MA_100")
    plot_ma100_price(data)

    # Plot MA_50 vs MA_100 vs Price
    st.subheader(f"{company} Stock Price and MA_100 and MA_50")
    plot_ma50_ma100_price(data)

    # Plot Moving Averages vs Price
    st.subheader(f"{company} Stock Price and Moving Averages")
    plot_moving_averages(data)

    # Predicted vs Actual Prices (Placeholder for LSTM Model)
    st.subheader(f"{company} Predicted vs Actual Prices")
    actual = data['Close'][-50:]
    predicted = actual * 0.98  # Placeholder prediction (replace with actual model prediction later)
    plot_predicted_vs_actual(actual, predicted)

    # User input for features
    st.subheader("Predict Stock Prices")
    ma50 = st.number_input("Enter MA50 value")
    ma100 = st.number_input("Enter MA100 value")
    volume = st.number_input("Enter Volume")

    # Scale the user inputs like you did in training
    scaler = MinMaxScaler(feature_range=(0, 1))
    user_input = np.array([[ma50, ma100, volume]])  # Example with 3 features
    user_input_scaled = scaler.fit_transform(user_input)

    # Make predictions using the loaded model
    if st.button("Predict"):
        predicted_price = model.predict(user_input_scaled)
        predicted_price_unscaled = scaler.inverse_transform(predicted_price)  # Unscaling if needed
        st.write(f"Predicted value for the stock: {predicted_price_unscaled[0][0]:.2f}")
