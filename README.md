# 🚀 Intelligent BDD & Playwright Automator

This application is a **Low-Code Test Automation Tool** designed to bridge the gap between business requirements (BDD) and technical execution. By leveraging **Python**, **PySide6**, and **Playwright's Codegen**, it allows users to record web interactions and automatically transform them into structured BDD scenarios and executable Python test scripts.

---

## 🌟 Key Features
* **Visual Recording:** Uses Playwright's "machine learning-like" discovery to record browser actions without manual XPath/CSS selector mapping.
* **BDD Integration:** Automatically generates `.feature` files and corresponding Python steps.
* **Smart Storage:** Organizes tests systematically into a dedicated automation folder structure.
* **RPA Ready:** Capable of handling complex web workflows as a systematic robot.

---

## 🛠 Project Management (Makefile)

The project includes a `Makefile` to automate environment setup and execution using `uv`. Below is a detailed description of all available commands.

### Command Reference

| Command | Description |
| :--- | :--- |
| `make install` | Uses `uv sync` to install all Python dependencies defined in the project. |
| `make setup` | Performs a full environment initialization. Installs dependencies and downloads the necessary Playwright browser binaries (Chromium) with system dependencies. |
| `make run-ui` | Launches the **BDDForm** graphical interface (PySide6) where you can manage and record new tests. |
| `make test` | Executes the test suite using the **Behave** framework to validate all `.feature` scenarios. |
| `make codegen` | Manually opens the Playwright Inspector to record a session at a default URL (Google). |
| `make update` | Updates the `uv.lock` file and upgrades all dependencies to their latest compatible versions. |
| `make clean` | Removes temporary files, `__pycache__`, and clears previously generated scripts to keep the workspace tidy. |
| `make help` | Displays a summary of all available Makefile commands directly in the terminal. |
| `make test-clean` | Cleaning tests in cache. |

---

## 🚀 Quick Start

1.  **Clone the repository**
2.  **Setup the environment:**
    ```bash
    make setup
    ```
3.  **Launch the application:**
    ```bash
    make run-ui
    ```
4.  **Record your first test:** Click the **"Record Test"** button, perform your actions in the browser, and close it to generate the code automatically.

---

## 📂 Project Structure
* `/automation`: Destination for all generated `.feature` and `.py` files.
* `src/`: Application logic and UI components.
* `features/`: Standard BDD feature definitions.