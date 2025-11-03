import streamlit as st
import base64
import utils

# Streamlit interface
def main():
    # Set page title and icon
    st.set_page_config(
        page_title="Automata Project",
        page_icon="🔀"
    )

    # Hide Deploy button and Streamlit footer branding
    st.markdown(
        """
        <style>
        /* Hide Deploy button */
        [data-testid="stAppDeployButton"] { display: none !important; }
        .stAppDeployButton { display: none !important; }
        .stAppToolbar .stAppDeployButton { display: none !important; }
        [data-testid="stToolbar"] .stAppDeployButton { display: none !important; }
        .stAppDeployButton button { display: none !important; }
        
        /* Hide footer and branding */
        footer { visibility: hidden !important; }
        footer:after { visibility: hidden !important; }
        
        /* Hide "Made with Streamlit" in various locations */
        .viewerBadge_container__r5tak { display: none !important; }
        .viewerBadge_link__qRIco { display: none !important; }
        [data-testid="stDecoration"] { display: none !important; }
        
        /* Hide settings menu branding */
        .st-emotion-cache-1dp5vir { display: none !important; }
        .st-emotion-cache-nahz7x { display: none !important; }
        
        /* Fully remove Streamlit header */
        [data-testid="stHeader"] { display: none !important; }
        .stAppHeader { display: none !important; }

        /* Font weight fixes */
        h1, h2, h3, h4, h5, h6 { font-weight: 800 !important; }
        p, span, label, li { font-weight: 600 !important; }
        .stMarkdown { font-weight: 600 !important; }
        .stText { font-weight: 600 !important; }
        .stButton > button { font-weight: 700 !important; }
        input, textarea { font-weight: 600 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ✅ Force white background for dropdown + buttons (Fix for Streamlit Cloud dark mode)
    st.markdown("""
    <style>

        /* Fix Selectbox white background */
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #000000 !important;
        }

        /* Dropdown options white */
        ul[role="listbox"] {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* Text inside selected option */
        div[data-baseweb="select"] span {
            color: #000000 !important;
            font-weight: 600 !important;
        }

        /* Fix button color */
        button[kind="secondary"],
        button[kind="primary"],
        .stButton > button {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
        }

        .stButton > button:hover {
            background-color: #e6e6e6 !important;
            color: #000000 !important;
        }

        /* Input box white */
        input, textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

    </style>
    """, unsafe_allow_html=True)

    # Set background image from local file
    def set_background(image_path: str):
        try:
            with open(image_path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpg;base64,{data}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
        except Exception:
            pass

    set_background("pic.jpg")

    # Initialize streamlit session state values
    if len(st.session_state) == 0:
        st.session_state.disabled = True
        st.session_state.placeholder_text = ""
    
    # Callback function for regex_input
    def regex_input_callbk():
        if st.session_state.regex_input == "--- Select ---":
            st.session_state.disabled = True
        else:
            st.session_state.disabled = False
        
        if st.session_state.regex_input == utils.regex_options[1]:
            st.session_state.placeholder_text = "abaababbab"
        elif st.session_state.regex_input == utils.regex_options[2]:
            st.session_state.placeholder_text = "101110001"
        else:
            st.session_state.placeholder_text = ""  
        
        st.session_state.string_input = ""
    

    # UI layout
    title_con = st.container()
    st.divider()
    regex_to_dfa_con = st.container()
    cfg_and_pda_exp = st.expander("Show CFG and PDA Conversion")

    # Title block
    with title_con:
        st.title("Automata Project")
        st.markdown(
            '''
            This project is a web application that will convert the given regular expressions below to Deterministic Finite Automata (DFA), 
            Context-Free Grammars (CFG), and Pushdown Automata (PDA).

            **Regular Expressions**
            1. `(aba+bab) (a+b)* (bab) (a+b)* (a+b+ab+ba) (a+b+aa)*`
            2. `((101 + 111 + 101) + (1+0+11)) (1 + 0 + 01)* (111 + 000 + 101) (1+0)*`
            '''
            )

    # Main DFA/CFG/PDA section
    with regex_to_dfa_con:
        st.subheader("Regex to DFA, CFG, & PDA")
        st.markdown(
            '''
            1. Select a given Regex from the select box.  
            2. Enter a string to check if it is valid for the DFA.  
            '''
            )
        
        regex_input = st.selectbox(
            label="Select a Regular Expression",
            options=utils.regex_options,
            key="regex_input",
            on_change=regex_input_callbk,
        )
        
        string_input = st.text_input(
            label="Enter a string to check its validity for displayed DFA",
            key="string_input",
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder_text
        )
        
        validate_button = st.button(
            label="Validate",
            disabled=st.session_state.disabled
        )
        
        if regex_input == utils.regex_options[1]:
            current_dfa = utils.dfa_1            
            st.write("**Deterministic Finite Automaton**")
            if not string_input:
                dfa = utils.generate_dfa_visualization(current_dfa)
                st.graphviz_chart(dfa)

            with cfg_and_pda_exp:
                st.write("**Context Free Grammar**")
                st.markdown(utils.cfg_1)

                st.write("**Pushdown Automaton**")
                current_pda = utils.pda_1
                pda = utils.generate_pda_visualization(current_pda)
                st.graphviz_chart(pda)
        
        elif regex_input == utils.regex_options[2]:
            current_dfa = utils.dfa_2            
            st.write("**Deterministic Finite Automaton**")
            if not string_input:
                dfa = utils.generate_dfa_visualization(current_dfa)
                st.graphviz_chart(dfa)

            with cfg_and_pda_exp:
                st.write("**Context Free Grammar**")
                st.markdown(utils.cfg_2)
                
                st.write("**Pushdown Automaton**")
                current_pda = utils.pda_2
                pda = utils.generate_pda_visualization(current_pda)
                st.graphviz_chart(pda)

        if validate_button or string_input:
            string_input = string_input.replace(" ", "")  
            if len(string_input) == 0:
                st.error("Empty/Invalid Input", icon="❌")
            elif not all(char in current_dfa["alphabet"] for char in string_input):
                st.error(f"String '{string_input}' contains invalid characters, allowed alphabet: {current_dfa['alphabet']}", icon="❌")
            else:
                st.write(f"Entered String: `{string_input}`")
                is_valid, state_checks = utils.validate_dfa(current_dfa, string_input)
                utils.animate_dfa_validation(current_dfa, state_checks)
                if is_valid:
                    st.success(f"The string '{string_input}' is valid for the DFA.", icon="✔️")
                else:
                    st.error(f"The string '{string_input}' is not valid for the DFA.", icon="❌")


if __name__ == "__main__":
    main()





