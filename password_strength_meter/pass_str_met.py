import streamlit as st
import re

def load_common_passwords(file_path='common_passwords.txt'):
    try:
        with open(file_path, 'r') as file:
            common_passwords = [line.strip().lower() for line in file]
    except FileNotFoundError:
        common_passwords = ['password', '123456', 'qwerty', 'abc123', 'letmein', 'admin', 'welcome']
    return common_passwords

def check_password_strength(password, common_passwords):
    # Check against common passwords
    if password.lower() in common_passwords:
        return 'Weak', ['Password is too common.']
    
    # Initialize variables
    feedback = []
    score = 0
    
    # Check length
    length = len(password)
    if length < 8:
        feedback.append('Password must be at least 8 characters long.')
        return 'Weak', feedback
    elif 8 <= length < 12:
        score += 1
    else:
        score += 2
    
    # Check character types
    checks = {
        'lower': re.search(r'[a-z]', password),
        'upper': re.search(r'[A-Z]', password),
        'digit': re.search(r'\d', password),
        'special': re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    }
    
    # Provide feedback and calculate score
    for key, value in checks.items():
        if value:
            score += 1
            feedback.append(f'Contains a {key} character.')
        else:
            feedback.append(f'Missing a {key} character.')
    
    # Determine strength
    if score <= 3:
        strength = 'Weak'
    elif score <= 5:
        strength = 'Medium'
    else:
        strength = 'Strong'
    
    return strength, feedback

def main():
    st.title("🔒 Password Strength Meter")
    
    password = st.text_input("Enter your password:", type="password", help="Start typing to check strength")
    
    if password:
        common_passwords = load_common_passwords()
        strength, feedback = check_password_strength(password, common_passwords)
        
        # Display strength indicator
        color_map = {'Weak': 'red', 'Medium': 'orange', 'Strong': 'green'}
        st.markdown(f"**Strength:** <span style='color:{color_map[strength]}'>{strength}</span>", unsafe_allow_html=True)
        
        # Display progress bar
        progress = {'Weak': 0.3, 'Medium': 0.6, 'Strong': 1.0}
        st.progress(progress[strength])
        
        # Display feedback
        st.subheader("Requirements Check:")
        for msg in feedback:
            if msg.startswith('Missing'):
                st.error(msg)
            elif msg.startswith('Contains'):
                st.success(msg)
            else:
                st.info(msg)

if __name__ == "__main__":
    main()