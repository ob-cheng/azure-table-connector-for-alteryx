from ayx import Alteryx
import pandas as pd
import sys

# -----------------------------------------------------------------------------
# 1. Dependencies (Gallery Version)
# -----------------------------------------------------------------------------
# NOTE: This version assumes 'azure-data-tables' has been pre-installed 
# by the Server Administrator on the Gallery worker nodes.
try:
    from azure.data.tables import TableClient
except ImportError:
    print("'azure-data-tables' not found. Attempting to install via pip...")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "azure-data-tables"])
        print("Installation successful. Importing library...")
        from azure.data.tables import TableClient
    except Exception as e:
        print(f"Failed to install 'azure-data-tables': {str(e)}")
        raise ImportError("Required library 'azure-data-tables' is missing and auto-installation failed.")

# -----------------------------------------------------------------------------
# 2. Read Credentials from Input #1
# -----------------------------------------------------------------------------
df_input = Alteryx.read("#1")

if df_input.empty:
    raise ValueError("Input #1 is empty. Please provide StorageAccount, AccountKey, and TableName columns.")

# -----------------------------------------------------------------------------
# 3. Process each row and output to separate anchors
# -----------------------------------------------------------------------------
max_anchors = 5
rows_to_process = min(len(df_input), max_anchors)

for index in range(rows_to_process):
    row = df_input.iloc[index]
    output_anchor = index + 1
    
    storage_account = row['StorageAccount']
    account_key = row['AccountKey']
    table_name = row['TableName']
    
    endpoint_suffix = "core.windows.net"
    if 'EndpointSuffix' in df_input.columns and not pd.isna(row['EndpointSuffix']):
        endpoint_suffix = row['EndpointSuffix']

    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account};AccountKey={account_key};EndpointSuffix={endpoint_suffix}"

    print(f"Connecting to table '{table_name}' for Output #{output_anchor}...")

    try:
        table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
        
        # Fetch Data
        entities = table_client.list_entities()
        data = list(entities)
        
        if not data:
            df_output = pd.DataFrame()
        else:
            df_output = pd.DataFrame(data)
            cols = df_output.columns.tolist()
            if 'PartitionKey' in cols:
                cols.insert(0, cols.pop(cols.index('PartitionKey')))
            if 'RowKey' in cols:
                cols.insert(1, cols.pop(cols.index('RowKey')))
            df_output = df_output[cols]
            
        Alteryx.write(df_output, output_anchor)

    except Exception as e:
        error_msg = f"Error reading table '{table_name}': {str(e)}"
        df_error = pd.DataFrame({'Error': [error_msg], 'TableName': [table_name]})
        Alteryx.write(df_error, output_anchor)

print("Processing complete.")
