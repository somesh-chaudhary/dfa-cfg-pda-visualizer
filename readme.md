# 🔁 Automata Project

This is a simple web app that turns regular expressions into:

- ✅ **DFA** (Deterministic Finite Automata)  
- ✅ **CFG** (Context-Free Grammar)  
- ✅ **PDA** (Pushdown Automaton)

It also lets you check whether a string is accepted by the DFA—complete with a step-by-step animation.

---

## 🛠️ Built With

- **Streamlit** — for the web interface  
- **Graphviz** — for graph visualizations of DFA and PDA  

---

## 🔤 Regular Expressions Supported

1. `(aba+bab) (a+b)* (bab) (a+b)* (a+b+ab+ba) (a+b+aa)*`  
2. `((101 + 111 + 101) + (1+0+11)) (1 + 0 + 01)* (111 + 000 + 101) (1+0)*`

---

## 🚀 How to Use

1. Pick a regular expression from the dropdown menu  
2. The app will show you the **DFA**, and its matching **CFG** and **PDA** below  
3. Enter a string and click **Validate** to see if it’s accepted  
4. Watch the DFA animation and see the result ✅ or ❌

---

## 🧠 Project Structure

### `app.py`  
Contains the Streamlit app—UI, inputs, DFA display, and animation.

### `utils.py`  
Contains:
- Regex, DFA, CFG, and PDA data  
- Helper functions for visualizing and validating automata  

---

## 👨‍💻 Team

- Somesh Chaudhary  
- Uddeshya Yadav  
- Lakshya Hada  
