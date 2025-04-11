import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json
import os
from datetime import datetime
 

# Set page configuration
st.set_page_config(
    page_title="Emergency Information - India",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and improved visibility
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #121212;
        color: #f0f0f0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
    }
    
    /* Headers and titles */
    .emergency-header {
        color: white;
        background-color: #d32f2f;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.3em;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Contact cards */
    .contact-card {
        background-color: #2c2c2c;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #d32f2f;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Guideline cards */
    .guideline-card {
        background-color: #2c2c2c;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #1976d2;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Success messages */
    .success-message {
        color: #81c784;
        font-weight: bold;
        padding: 10px;
        background-color: rgba(46, 125, 50, 0.2);
        border-radius: 5px;
        border-left: 4px solid #2e7d32;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #1e3a5f;
        color: #b3e5fc;
    }
    
    /* Error messages */
    .stError {
        background-color: #5f1e1e;
        color: #ffcdd2;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #e0e0e0;
    }
    
    /* Text content */
    p {
        font-size: 16px;
        color: #e0e0e0;
        margin-bottom: 5px;
    }
    
    /* Code blocks */
    pre {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 5px;
        color: #e0e0e0;
        font-size: 15px;
        border-left: 3px solid #555;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #d32f2f;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background-color: #b71c1c;
    }
    
    /* Form inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #333333;
        color: #f0f0f0;
        border: 1px solid #555;
        border-radius: 4px;
    }
    
    /* Selectbox */
    .stSelectbox>div>div>div {
        background-color: #333333;
        color: #f0f0f0;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #2c2c2c;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background-color: #2c2c2c;
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Section containers */
    .css-1r6slb0, .css-1inwz65, .css-1of3kdb {
        background-color: #2c2c2c;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Footer styling */
    .footer {
        background-color: #d32f2f;
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin-top: 30px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .footer h3 {
        color: white;
        font-size: 22px;
        margin-bottom: 15px;
    }
    
    .footer p {
        color: white;
        font-size: 18px;
        margin: 5px 0;
    }
    
    /* Custom section containers */
    .info-box {
        background-color: #263238;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #0277bd;
    }
    
    /* Section headings with icons */
    .section-heading {
        display: flex;
        align-items: center;
        font-weight: bold;
        font-size: 20px;
        color: #e0e0e0;
        margin-bottom: 15px;
    }
    
    .section-heading svg {
        margin-right: 10px;
        fill: #d32f2f;
    }
    
    /* Two-tone cards */
    .two-tone-card {
        background-color: #2c2c2c;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .card-header {
        background-color: #d32f2f;
        color: white;
        padding: 10px 15px;
        font-weight: bold;
        font-size: 18px;
    }
    
    .card-body {
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'emergency_contacts' not in st.session_state:
    st.session_state.emergency_contacts = [
        {"name": "National Emergency Number", "type": "Emergency", "phone": "112", "address": "All India"},
        {"name": "Police", "type": "Police", "phone": "100", "address": "All India"},
        {"name": "Fire", "type": "Fire", "phone": "101", "address": "All India"},
        {"name": "Ambulance", "type": "Medical", "phone": "108", "address": "All India"},
        {"name": "Women Helpline", "type": "Helpline", "phone": "1091", "address": "All India"},
        {"name": "Child Helpline", "type": "Helpline", "phone": "1098", "address": "All India"}
    ]

if 'guidelines' not in st.session_state:
    st.session_state.guidelines = [
        {"title": "Fire Emergency", "content": "1. Call 101 immediately\n2. Evacuate the building using stairs, not elevators\n3. Cover nose and mouth with wet cloth while escaping\n4. If clothes catch fire - Stop, Drop, and Roll\n5. Meet at designated assembly point"},
        {"title": "Medical Emergency", "content": "1. Call 108 for ambulance\n2. Provide first aid if trained\n3. Do not move the injured person unless necessary\n4. Keep the person comfortable and monitor vital signs\n5. Have person's Aadhaar card/ID ready if possible"},
        {"title": "Natural Disaster - Flood", "content": "1. Move to higher ground immediately\n2. Avoid walking or driving through flood waters\n3. Follow evacuation orders from authorities\n4. If trapped, call 1078 (Disaster Management)"},
        {"title": "Natural Disaster - Earthquake", "content": "1. Drop to the ground\n2. Take cover under sturdy furniture\n3. Hold on until shaking stops\n4. Avoid doorways, windows, and exterior walls\n5. If outdoors, stay in the open away from buildings"}
    ]

if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {
        "name": "",
        "address": "",
        "phone": "",
        "aadhaar": "",
        "blood_group": "",
        "medical_conditions": "",
        "allergies": "",
        "medications": "",
        "emergency_contact_name": "",
        "emergency_contact_phone": ""
    }

if 'user_location' not in st.session_state:
    st.session_state.user_location = {"lat": 28.6139, "lon": 77.2090}  # Default: New Delhi

# Function to save data to file
def save_data():
    data = {
        "emergency_contacts": st.session_state.emergency_contacts,
        "guidelines": st.session_state.guidelines,
        "personal_info": st.session_state.personal_info,
        "user_location": st.session_state.user_location
    }
    with open("emergency_data.json", "w") as f:
        json.dump(data, f)

# Function to load data from file
def load_data():
    if os.path.exists("emergency_data.json"):
        with open("emergency_data.json", "r") as f:
            data = json.load(f)
            st.session_state.emergency_contacts = data.get("emergency_contacts", st.session_state.emergency_contacts)
            st.session_state.guidelines = data.get("guidelines", st.session_state.guidelines)
            st.session_state.personal_info = data.get("personal_info", st.session_state.personal_info)
            st.session_state.user_location = data.get("user_location", st.session_state.user_location)

# Try to load existing data
try:
    load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")

# Sidebar navigation
st.sidebar.markdown('<h2 style="color: #d32f2f;">🚨 आपातकालीन जानकारी</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<h3 style="color: #e0e0e0;">Emergency Information</h3>', unsafe_allow_html=True)
page = st.sidebar.radio("Navigate", ["Quick Access", "Manage Contacts", "Manage Guidelines", "Personal Information", "Nearby Services"])

# Display current date and time in the sidebar
st.sidebar.markdown("---")
current_time = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
st.sidebar.markdown(f"**Current time:** {current_time}")

# Important Indian emergency numbers
st.sidebar.markdown("---")
st.sidebar.markdown('<h4 style="color: #d32f2f;">Important Helplines</h4>', unsafe_allow_html=True)
st.sidebar.markdown("""
- **Emergency**: 112
- **Police**: 100
- **Fire**: 101
- **Ambulance**: 108
- **Women Helpline**: 1091
- **Child Helpline**: 1098
- **Disaster Management**: 1078
- **COVID-19 Helpline**: 1075
""")

# Quick Access Page
if page == "Quick Access":
    st.markdown('<div class="emergency-header"><h1>🚨 Emergency Quick Access</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Emergency Contacts Section
    with col1:
        st.markdown('<div class="section-heading"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57-.35-.11-.74-.03-1.02.24l-2.2 2.2c-2.83-1.44-5.15-3.75-6.59-6.59l2.2-2.21c.28-.26.36-.65.25-1C8.7 6.45 8.5 5.25 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1zM19 12h2c0-4.97-4.03-9-9-9v2c3.87 0 7 3.13 7 7zm-4 0h2c0-2.76-2.24-5-5-5v2c1.66 0 3 1.34 3 3z"></path></svg>Emergency Contacts</div>', unsafe_allow_html=True)
        if st.session_state.emergency_contacts:
            for contact in st.session_state.emergency_contacts:
                st.markdown(f"""
                <div class="two-tone-card">
                    <div class="card-header">{contact['name']}</div>
                    <div class="card-body">
                        <p><strong>Type:</strong> {contact['type']}</p>
                        <p><strong>Phone:</strong> {contact['phone']}</p>
                        <p><strong>Address:</strong> {contact['address']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No emergency contacts added yet. Go to Manage Contacts to add some.")
    
    # Guidelines Section
    with col2:
        st.markdown('<div class="section-heading"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"></path></svg>Emergency Guidelines</div>', unsafe_allow_html=True)
        if st.session_state.guidelines:
            for guideline in st.session_state.guidelines:
                st.markdown(f"""
                <div class="two-tone-card">
                    <div class="card-header" style="background-color: #1976d2;">{guideline['title']}</div>
                    <div class="card-body">
                        <pre>{guideline['content']}</pre>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No guidelines added yet. Go to Manage Guidelines to add some.")
    
    # Personal Emergency Info
    st.markdown('<div class="section-heading"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"></path></svg>Personal Emergency Information</div>', unsafe_allow_html=True)
    if st.session_state.personal_info["name"]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="two-tone-card">
                <div class="card-header" style="background-color: #ff9800;">Personal Information</div>
                <div class="card-body">
                    <p><strong>Name:</strong> {st.session_state.personal_info['name']}</p>
                    <p><strong>Address:</strong> {st.session_state.personal_info['address']}</p>
                    <p><strong>Phone:</strong> {st.session_state.personal_info['phone']}</p>
                    <p><strong>Aadhaar:</strong> {st.session_state.personal_info['aadhaar']}</p>
                    <p><strong>Blood Group:</strong> {st.session_state.personal_info['blood_group']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="two-tone-card">
                <div class="card-header" style="background-color: #ff9800;">Medical Information</div>
                <div class="card-body">
                    <p><strong>Medical Conditions:</strong> {st.session_state.personal_info['medical_conditions']}</p>
                    <p><strong>Allergies:</strong> {st.session_state.personal_info['allergies']}</p>
                    <p><strong>Medications:</strong> {st.session_state.personal_info['medications']}</p>
                    <p><strong>Emergency Contact:</strong> {st.session_state.personal_info['emergency_contact_name']} - {st.session_state.personal_info['emergency_contact_phone']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            <p>No personal information added yet. Go to Personal Information to add your details.</p>
        </div>
        """, unsafe_allow_html=True)

# Manage Contacts Page
elif page == "Manage Contacts":
    st.markdown('<div class="emergency-header"><h1>📞 Manage Emergency Contacts</h1></div>', unsafe_allow_html=True)
    
    # Display existing contacts
    if st.session_state.emergency_contacts:
        st.markdown('<div class="section-heading">Existing Contacts</div>', unsafe_allow_html=True)
        contact_df = pd.DataFrame(st.session_state.emergency_contacts)
        st.dataframe(contact_df, use_container_width=True)
        
        # Delete contacts
        st.markdown('<div class="section-heading">Delete Contacts</div>', unsafe_allow_html=True)
        selected_indices = st.multiselect(
            "Select contacts to delete:", 
            range(len(st.session_state.emergency_contacts)),
            format_func=lambda i: st.session_state.emergency_contacts[i]['name']
        )
        
        if selected_indices and st.button("Delete Selected Contact"):
            for index in sorted(selected_indices, reverse=True):
                del st.session_state.emergency_contacts[index]
            save_data()
            st.markdown('<div class="success-message">Contacts deleted successfully!</div>', unsafe_allow_html=True)
            st.experimental_rerun()
    
    # Add new contact
    st.markdown('<div class="section-heading">Add New Contact</div>', unsafe_allow_html=True)
    with st.form("contact_form"):
        name = st.text_input("Name")
        contact_type = st.selectbox("Contact Type", ["Police", "Fire", "Medical", "Family", "Friend", "Helpline", "Other"])
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        
        submit_button = st.form_submit_button("Add Contact")
        if submit_button:
            if name and phone:
                new_contact = {
                    "name": name,
                    "type": contact_type,
                    "phone": phone,
                    "address": address
                }
                st.session_state.emergency_contacts.append(new_contact)
                save_data()
                st.markdown('<div class="success-message">Contact added successfully!</div>', unsafe_allow_html=True)
            else:
                st.error("Name and Phone are required!")

# Manage Guidelines Page
elif page == "Manage Guidelines":
    st.markdown('<div class="emergency-header"><h1>📋 Manage Emergency Guidelines</h1></div>', unsafe_allow_html=True)
    
    # Display existing guidelines
    if st.session_state.guidelines:
        st.markdown('<div class="section-heading">Existing Guidelines</div>', unsafe_allow_html=True)
        for i, guideline in enumerate(st.session_state.guidelines):
            st.markdown(f"""
            <div class="two-tone-card">
                <div class="card-header" style="background-color: #1976d2;">{guideline['title']}</div>
                <div class="card-body">
                    <pre>{guideline['content']}</pre>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Delete guidelines
        st.markdown('<div class="section-heading">Delete Guidelines</div>', unsafe_allow_html=True)
        selected_indices = st.multiselect(
            "Select guidelines to delete:", 
            range(len(st.session_state.guidelines)),
            format_func=lambda i: st.session_state.guidelines[i]['title']
        )
        
        if selected_indices and st.button("Delete Selected Guidelines"):
            for index in sorted(selected_indices, reverse=True):
                del st.session_state.guidelines[index]
            save_data()
            st.markdown('<div class="success-message">Guidelines deleted successfully!</div>', unsafe_allow_html=True)
            st.experimental_rerun()
    
    # Add new guideline
    st.markdown('<div class="section-heading">Add New Guideline</div>', unsafe_allow_html=True)
    with st.form("guideline_form"):
        title = st.text_input("Title")
        content = st.text_area("Content (use numbered list for steps)")
        
        submit_button = st.form_submit_button("Add Guideline")
        if submit_button:
            if title and content:
                new_guideline = {
                    "title": title,
                    "content": content
                }
                st.session_state.guidelines.append(new_guideline)
                save_data()
                st.markdown('<div class="success-message">Guideline added successfully!</div>', unsafe_allow_html=True)
                st.experimental_rerun()
            else:
                st.error("Title and Content are required!")

# Personal Information Page
elif page == "Personal Information":
    st.markdown('<div class="emergency-header"><h1>👤 Personal Emergency Information</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-heading">Update Your Personal Information</div>', unsafe_allow_html=True)
    with st.form("personal_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.personal_info["name"])
            address = st.text_area("Home Address", value=st.session_state.personal_info["address"])
            phone = st.text_input("Phone Number", value=st.session_state.personal_info["phone"])
            aadhaar = st.text_input("Aadhaar Number (optional)", value=st.session_state.personal_info["aadhaar"])
            blood_group = st.selectbox("Blood Group", 
                                      ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                      index=0 if not st.session_state.personal_info["blood_group"] else 
                                      ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(st.session_state.personal_info["blood_group"]))
        
        with col2:
            medical_conditions = st.text_area("Medical Conditions", value=st.session_state.personal_info["medical_conditions"])
            allergies = st.text_area("Allergies", value=st.session_state.personal_info["allergies"])
            medications = st.text_area("Current Medications", value=st.session_state.personal_info["medications"])
        
        st.markdown('<div class="section-heading">Emergency Contact</div>', unsafe_allow_html=True)
        emergency_contact_name = st.text_input("Emergency Contact Name", value=st.session_state.personal_info["emergency_contact_name"])
        emergency_contact_phone = st.text_input("Emergency Contact Phone", value=st.session_state.personal_info["emergency_contact_phone"])
        
        submit_button = st.form_submit_button("Save Personal Information")
        if submit_button:
            st.session_state.personal_info = {
                "name": name,
                "address": address,
                "phone": phone,
                "aadhaar": aadhaar,
                "blood_group": blood_group,
                "medical_conditions": medical_conditions,
                "allergies": allergies,
                "medications": medications,
                "emergency_contact_name": emergency_contact_name,
                "emergency_contact_phone": emergency_contact_phone
            }
            save_data()
            st.markdown('<div class="success-message">Personal information updated successfully!</div>', unsafe_allow_html=True)

# Nearby Services Page
elif page == "Nearby Services":
    st.markdown('<div class="emergency-header"><h1>🗺️ Nearby Emergency Services</h1></div>', unsafe_allow_html=True)
    
    # Update user location
    st.markdown('<div class="section-heading">Set Your Location</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        lat = st.number_input("Latitude", value=st.session_state.user_location["lat"], format="%.6f")
    
    with col2:
        lon = st.number_input("Longitude", value=st.session_state.user_location["lon"], format="%.6f")
    
    st.markdown("""
    <div class="info-box">
        <p><strong>Find your coordinates:</strong></p>
        <p>1. Open Google Maps</p>
        <p>2. Long press on your location</p>
        <p>3. Copy the coordinates displayed at the bottom</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Update Location"):
        st.session_state.user_location = {"lat": lat, "lon": lon}
        save_data()
        st.markdown('<div class="success-message">Location updated successfully!</div>', unsafe_allow_html=True)
    
    # Display map with emergency services
    st.markdown('<div class="section-heading">Emergency Services Near You</div>', unsafe_allow_html=True)
    
    # Create a map centered at the user's location
    m = folium.Map(location=[st.session_state.user_location["lat"], st.session_state.user_location["lon"]], 
                  zoom_start=13, 
                  tiles="CartoDB dark_matter")  # Dark theme map
    
    # Add marker for user location
    folium.Marker(
        [st.session_state.user_location["lat"], st.session_state.user_location["lon"]],
        popup="Your Location",
        icon=folium.Icon(color="blue", icon="user", prefix="fa"),
    ).add_to(m)
    
    # Add sample emergency services (these would be replaced with actual data in a production app)
    emergency_services = [
        {"name": "City Hospital", "type": "Hospital", "lat": st.session_state.user_location["lat"] + 0.01, "lon": st.session_state.user_location["lon"] + 0.01},
        {"name": "Police Station", "type": "Police", "lat": st.session_state.user_location["lat"] - 0.01, "lon": st.session_state.user_location["lon"] + 0.01},
        {"name": "Fire Station", "type": "Fire", "lat": st.session_state.user_location["lat"] + 0.01, "lon": st.session_state.user_location["lon"] - 0.01},
        {"name": "Government Hospital", "type": "Hospital", "lat": st.session_state.user_location["lat"] - 0.01, "lon": st.session_state.user_location["lon"] - 0.01},
        {"name": "Pharmacy", "type": "Pharmacy", "lat": st.session_state.user_location["lat"] + 0.005, "lon": st.session_state.user_location["lon"] + 0.005}
    ]
    
    for service in emergency_services:
        icon_color = "red" if service["type"] == "Hospital" else "green" if service["type"] == "Police" else "orange" if service["type"] == "Fire" else "blue"
        icon_name = "plus" if service["type"] == "Hospital" else "shield" if service["type"] == "Police" else "fire" if service["type"] == "Fire" else "medkit"
        
        folium.Marker(
            [service["lat"], service["lon"]],
            popup=f"{service['name']} ({service['type']})",
            icon=folium.Icon(color=icon_color, icon=icon_name, prefix="fa"),
        ).add_to(m)
    
    # Display the map
    folium_static(m)
    
    st.markdown("""
    <div class="info-box">
        <p>Note: This shows sample emergency services for demonstration. In a real application, it would connect to government APIs to get actual emergency service locations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Allow adding custom emergency services
    st.markdown('<div class="section-heading">Add Custom Emergency Service</div>', unsafe_allow_html=True)
    with st.form("service_form"):
        service_name = st.text_input("Service Name")
        service_type = st.selectbox("Service Type", ["Hospital", "Police", "Fire", "Pharmacy", "Blood Bank", "Other"])
        service_lat = st.number_input("Service Latitude", format="%.6f", value=st.session_state.user_location["lat"])
        service_lon = st.number_input("Service Longitude", format="%.6f", value=st.session_state.user_location["lon"])
        
        if st.form_submit_button("Add Service"):
            # This would typically save to a database
            st.markdown('<div class="success-message">Service added! Note: In this demo, custom services are not permanently saved.</div>', unsafe_allow_html=True)
            # In a real application, you would add this service to a database or persistent storage
            st.experimental_rerun()

# Footer section
st.markdown("""
<div class="footer">
    <h3>🚨 Emergency Information System - India</h3>
    <p>Keep your emergency contacts and information updated</p>
    <p>For actual emergencies, always call the national emergency number: 112</p>
</div>
""", unsafe_allow_html=True)