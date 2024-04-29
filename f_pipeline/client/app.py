import streamlit as st
import requests

def get_bath_value():
    bathrooms = st.radio("Number of Bathrooms", ["1", "2", "3", "4", "5"])
    return int(bathrooms)

def get_bhk_value():
    bhk = st.radio("Number of BHK", ["1", "2", "3", "4", "5"])
    return int(bhk)

def estimate_price(sqft, bhk, bathrooms, location):
    url = "http://127.0.0.1:5000/predict_home_price"
    data = {
        "total_sqft": sqft,
        "bhk": bhk,
        "bath": bathrooms,
        "location": location
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("estimated_price")
    else:
        return None

def main():
    st.title("Home Price Estimator")
    
    sqft = st.number_input("Total Sqft")
    bhk = get_bhk_value()
    bathrooms = get_bath_value()
    location = st.selectbox("Location", ["Location A", "Location B", "Location C"])
    
    if st.button("Estimate Price"):
        estimated_price = estimate_price(sqft, bhk, bathrooms, location)
        if estimated_price is not None:
            st.success(f"Estimated Price: {estimated_price} Lakh")
        else:
            st.error("Failed to estimate price. Please try again later.")

if __name__ == "__main__":
    main()
