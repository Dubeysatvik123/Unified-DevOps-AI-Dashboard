# 🚀 Unified DevOps + AI Dashboard

A modern, interactive dashboard built with [Streamlit](https://streamlit.io/) that unifies DevOps automation, AI/ML tools, and productivity utilities in a single, visually appealing interface.

---

## Features

- **Integrated Modules:**  
  - Docker & Kubernetes Automation  
  - Machine Learning (Regression, ANN, Classification)  
  - GenAI & Prompt Engineering  
  - Infrastructure as Code (IaC)  
  - Linux & Python Utilities  
  - Github Automation  
  - Web Development Tools  
  - Agentic AI & Testing Agents  
  - Real-time Analytics & AIOps

- **Modern UI:**  
  - Custom CSS for a sleek, dark-themed look  
  - Sidebar profile card and navigation  
  - Animated feature cards and statistics

- **Extensible Architecture:**  
  - Modular loading system for easy expansion  
  - Error handling for module imports and execution

- **Web & JS Tools:**  
  - Media capture, speech recognition, ChatGPT integration, social media sharing, and Google search via JavaScript snippets

---

## Getting Started

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Pillow](https://python-pillow.org/) (`PIL`)

### Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/mine-menur.git
cd mine-menur/project
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run app.py
```

---

## Usage

- Use the sidebar to select modules and navigate between AI, DevOps, ML, and development tools.
- Each module is loaded dynamically; errors are shown in the sidebar if a module fails to load.
- The home page provides an overview and highlights key features.
- Web development tools include JavaScript code snippets for browser-based functionality.

---

## Project Structure

```
project/
├── app.py
├── modules/
│   ├── dockermenu.py
│   ├── GENAI.py
│   ├── github_automation.py
│   ├── iac.py
│   ├── kubernetesmenue.py
│   ├── linux.py
│   ├── ml_regress.py
│   ├── promptengineeing.py
│   ├── pythonmenu.py
│   ├── testingagent.py
│   ├── project.py
│   └── webdev.py
├── README.md
└── requirements.txt
```

---

## Author

**Satvik Dubey**  
Team No: 73  
[Profile Image](https://github.com/Dubeysatvik123/Images/blob/main/Satvik.jpg?raw=true)

---

## License

Specify your license here (e.g., MIT).

---

## Acknowledgements

- Built with ❤️ using Streamlit and Python.
- Inspired by modern DevOps and AI workflows.
