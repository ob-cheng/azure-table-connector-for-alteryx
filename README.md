<div align="center">

# Azure Table Connector for Alteryx

[![License](https://img.shields.io/badge/License-MIT-black.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-black.svg?style=flat-square)](https://www.python.org/)

A Python-based utility to read up to five Azure Table Storage tables with your Alteryx Python tool.

</div>

## ⚠️ Security Warning
**Do not hardcode your AccountKey.** 
- This repository includes a `.gitignore` that prevents `.csv` and `.xlsx` files from being committed.
- It is highly recommended to use Alteryx Text Input or encrypted parameters for credentials.

## Requirements
- `azure-data-tables` (Python library)

## Version Selection

### 1. Local Designer (`azure_table_script.py`)
Designed for users running Alteryx Designer on local machines.
- **Dependency Handling**: If `azure-data-tables` is not found, the script automatically installs it into the user's `%APPDATA%` folder. This bypasses the need for Windows Administrator privileges.
- **Compliance**: Note that while this technically works without admin rights, you should verify that installing libraries to your user profile aligns with your company's IT security and compliance policies.

### 2. Alteryx Gallery / Server (`azure_table_script_gallery.py`)
Designed for workflows running on Alteryx Server worker nodes.
- **Dependency Handling**: This version assumes libraries are already installed on the server.
- **Troubleshooting**: If you see a "ModuleNotFoundError" on the Gallery, ask your Server Admin to run `pip install azure-data-tables` on the worker nodes.

## Configuration

### 1. Workflow Setup
Connect a **Text Input** tool to the Python tool (Anchor #1). Each row in your input is automatically mapped to a numbered output anchor.

<div align="center">
  <img src="assets/workflow.png" alt="Alteryx Workflow Example" width="250" />
</div>

#### Input #1 Column Structure
| Anchor | StorageAccount | AccountKey | TableName | EndpointSuffix |
| :--- | :--- | :--- | :--- | :--- |
| **Output 1** | `account_a` | `key_a` | `Table_01` | `core.windows.net` |
| **Output 2** | `account_a` | `key_a` | `Table_02` | `core.windows.net` |
| **Output 3** | `account_b` | `key_b` | `Table_03` | `core.windows.net` |
| **Output 4** | `account_b` | `key_b` | `Table_04` | `core.windows.net` |
| **Output 5** | `account_c` | `key_c` | `Table_05` | `core.windows.net` |

> [!TIP]
> `EndpointSuffix` is optional. If left blank, it defaults to `core.windows.net`.

### 2. Implementation
1. Paste the code from the chosen `.py` file into the Alteryx Python tool.
2. Ensure your Text Input is connected to anchor **#1**.
3. Run the workflow.

---

<div align="center">
Feel free to fork this project or leave a star if it helped your workflow.
</div>
