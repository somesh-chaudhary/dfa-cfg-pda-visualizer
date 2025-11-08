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
        
        /* Additional selectors for Streamlit branding */
        div[data-testid="stToolbar"] > div:last-child { display: none !important; }
        .stApp > footer { display: none !important; }
        .stApp > div[data-testid="stDecoration"] { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        /* Fully remove Streamlit header */
        [data-testid="stHeader"] { display: none !important; }
        .stAppHeader { display: none !important; }

        /* Make text more bold for better readability */
        h1, h2, h3, h4, h5, h6 { font-weight: 800 !important; }
        p, span, label, li { font-weight: 600 !important; }
        .stMarkdown { font-weight: 600 !important; }
        .stText { font-weight: 600 !important; }
        .stButton > button { font-weight: 700 !important; }
        [data-baseweb="select"] { font-weight: 600 !important; }
        input, textarea { font-weight: 600 !important; }

        /* Darker text colors for readability */
        .stApp, .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        p, span, label, li { color: #111111 !important; }
        summary, [data-testid="stExpanderDetails"], [data-testid="stAlertContainer"] { color: #111111 !important; }

        /* Make specific sections white background */
        summary { background-color: #ffffff !important; }
        [data-testid="stExpanderDetails"] { background-color: #ffffff !important; }
        [data-testid="stAlertContainer"] { background-color: #ffffff !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
        # Set disable for string_input and validate_button
        if st.session_state.regex_input == "--- Select ---":
            st.session_state.disabled = True
        else:
            st.session_state.disabled = False
        
        # Set placeholder text for string_input
        if st.session_state.regex_input == utils.regex_options[1]:
            st.session_state.placeholder_text = "abaababbab"
        elif st.session_state.regex_input == utils.regex_options[2]:
            st.session_state.placeholder_text = "101110001"
        else:
            st.session_state.placeholder_text = ""  
        
        # Clear string_input
        st.session_state.string_input = ""
    

    # Create container to group blocks of code
    title_con = st.container()
    st.divider()
    regex_to_dfa_con = st.container()
    cfg_and_pda_exp = st.expander("Show CFG and PDA Conversion")

    # Code block for title and description
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

    # Code block for regex to dfa feature
    with regex_to_dfa_con:
        st.subheader("Regex to DFA, CFG, & PDA")
        st.markdown(
            '''
            1. Select a given Regex from the select box. The application will perform the conversion and display 
            the resulting DFA on the screen. Its corresponding CFG and PDA will be displayed on an expander below the DFA.
            2. Enter a string to check if it is valid for the DFA and then the program will check the 
            validity of the string by checking each state through an animation.
            '''
            )
        
        # Select box input to select regex
        regex_input = st.selectbox(
            label = "Select a Regular Expression",
            options = utils.regex_options,
            key="regex_input",
            on_change=regex_input_callbk
        )
        
        # Text input for string validation
        string_input = st.text_input(
            label = "Enter a string to check its validity for displayed DFA",
            key="string_input",
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder_text
        )
        
        # Validate button to run string validation
        validate_button = st.button(
            label = "Validate",
            disabled=st.session_state.disabled
        )
        
        # Output for regex_input, display dfa, cfg, and pda of selected regex
        current_dfa = None  # Initialize to avoid unbound variable error
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

        # Output for string_input, play validation animation on displayed dfa
        if validate_button or string_input:
            # Ensure current_dfa is defined before proceeding
            if current_dfa is None:
                st.error("Please select a regular expression first.", icon="❌")
            else:
                string_input = string_input.replace(" ", "")  # Removes any whitespaces

                # Check if string_input is empty
                if len(string_input) == 0:
                    st.error("Empty/Invalid Input", icon="❌")
                
                # Check if string_input has characters not in the alphabet of selected regex
                elif not all(char in current_dfa["alphabet"] for char in string_input):
                    st.error(f"String '{string_input}' contains invalid characters, please only use characters from the alphabet: {current_dfa['alphabet']}", icon="❌")
                
                else:
                    st.write(f"Entered String: `{string_input}`")
                    is_valid, state_checks = utils.validate_dfa(current_dfa, string_input)
                    utils.animate_dfa_validation(current_dfa, state_checks)
                    if is_valid:
                        st.success(f"The string '{string_input}' is valid for the DFA.", icon="✔️")
                    else:
                        st.error(f"The string '{string_input}' is not valid for the DFA.", icon="❌")


    st.markdown(
         """
         <style>
         /* Force white backgrounds for expander header/content and alerts */
         summary,
         [data-testid="stExpanderDetails"],
         [data-testid="stAlertContainer"] {
             background-color: #ffffff !important;
         }

        /* Code blocks: make background white and text dark */
        [data-testid="stCodeBlock"],
        .stMarkdown pre,
        .stMarkdown code,
        pre,
        code {
            background-color: #ffffff !important;
            color: #111111 !important;
        }

        /* Inputs, textareas, selects, and combobox controls: white background */
        input,
        textarea,
        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="select"],
        div[role="combobox"] {
            background-color: #ffffff !important;
            color: #111111 !important;
        }

        /* Select box selected value text */
        [data-baseweb="select"] input,
        [data-baseweb="select"] [role="button"] {
            color: #111111 !important;
        }

        /* Disabled inputs should also be white */
        input[disabled],
        textarea[disabled] {
            background-color: #ffffff !important;
            color: #666666 !important;
        }

        /* Force white background for select dropdown container and button */
        [data-baseweb="select"] > div,
        [data-baseweb="select"] [role="button"],
        [data-baseweb="popover"] {
            background-color: #ffffff !important;
            color: #111111 !important;
        }

        /* Force black text in select box display value */
        [data-baseweb="select"] [role="button"] *,
        [data-baseweb="select"] span,
        [data-baseweb="select"] div {
            color: #111111 !important;
        }

        /* Force white background for buttons */
        button[data-testid="stBaseButton-secondary"],
        .st-emotion-cache-18oifn0 {
            background-color: #ffffff !important;
            color: #111111 !important;
        }

        /* Force white background for alert containers */
        div[data-testid="stAlertContainer"],
        .stAlertContainer {
            background-color: #ffffff !important;
        }

        /* Alert container text should be dark */
        div[data-testid="stAlertContainer"] *,
        div[data-testid="stAlert"] * {
            color: #111111 !important;
        }

         /* Force white background for expander content */
         div[data-testid="stExpanderDetails"],
         .st-emotion-cache-1lks9j9 {
             background-color: #ffffff !important;
         }

         /* Expander content text should be dark */
         div[data-testid="stExpanderDetails"] *,
         [data-testid="stExpanderDetails"] p,
         [data-testid="stExpanderDetails"] code,
         [data-testid="stExpanderDetails"] pre {
             color: #111111 !important;
         }
         
         /* Buttons: ensure white background but keep page containers untouched */
         button[data-testid="stBaseButton-secondary"],
         button[data-testid="stBaseButton-primary"] {
             background-color: #ffffff !important;
             color: #111111 !important;
         }

         /* Force button text to be black */
         button[data-testid="stBaseButton-secondary"] p,
         button[data-testid="stBaseButton-primary"] p,
         button[data-testid="stBaseButton-secondary"] span,
         button[data-testid="stBaseButton-primary"] span,
         button[data-testid="stBaseButton-secondary"] div,
         button[data-testid="stBaseButton-primary"] div,
         button p,
         button span,
         button div {
             color: #111111 !important;
             font-weight: 700 !important;
         }

         /* Additional selectbox wrappers (chevron container) */
         [data-baseweb="select"] svg {
             color: #111111 !important;
         }

         /* Select dropdown menu items */
         [role="listbox"],
         [role="listbox"] li,
         [role="option"] {
             background-color: #ffffff !important;
             color: #111111 !important;
         }

         /* Dropdown option text */
         [role="option"] span,
         [role="option"] div {
             color: #111111 !important;
         }
         </style>
         """,
         unsafe_allow_html=True,
     )


if __name__ == "__main__":
    main()





