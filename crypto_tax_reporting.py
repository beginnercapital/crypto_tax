import pandas as pd

def calculate_crypto_taxes(file_path, method='FIFO'):
    """
    Calculate capital gains for cryptocurrency transactions using FIFO or LIFO method.
    
    Parameters:
    - file_path (str): Path to the CSV file containing transactions.
    - method (str): Accounting method, either 'FIFO' (default) or 'LIFO'.
    
    Returns:
    - pd.DataFrame: A DataFrame containing each sale's gain/loss and holding term.
    """
    
    # Load the data from CSV
    df = pd.read_csv(file_path, parse_dates=['transaction_date'])
    
    # Ensure required columns are present
    required_columns = {'transaction_date', 'transaction_type', 'amount', 'crypto_type', 'price_usd'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"The CSV file must contain the following columns: {required_columns}")
    
    # Calculate USD equivalent for each transaction
    df['usd_equivalent'] = df['amount'] * df['price_usd']

    # Separate rows into buys and sells, handling crypto-to-crypto trades
    buys = df[(df['transaction_type'].str.lower() == 'buy') | 
              ((df['transaction_type'].str.lower() == 'trade') & (df['usd_equivalent'] > 0))]
    sells = df[(df['transaction_type'].str.lower() == 'sell') | 
               ((df['transaction_type'].str.lower() == 'trade') & (df['usd_equivalent'] < 0))]
    
    # Sort by date to facilitate FIFO and LIFO handling
    buys = buys.sort_values('transaction_date', ascending=(method == 'FIFO'))
    sells = sells.sort_values('transaction_date')
    
    # Dictionary to keep track of remaining buy amounts
    crypto_inventory = {crypto: [] for crypto in df['crypto_type'].unique()}
    
    transactions_data = []

    # Process each sell
    for _, sell_row in sells.iterrows():
        crypto_type = sell_row['crypto_type']
        amount_to_sell = sell_row['amount']
        sell_price = sell_row['price_usd']
        sell_date = sell_row['transaction_date']
        
        gain_loss = 0
        term = 'short-term'
        
        while amount_to_sell > 0:
            if not crypto_inventory[crypto_type]:
                raise ValueError(f"No sufficient {crypto_type} inventory to cover the sale.")
            
            # Choose the first (FIFO) or last (LIFO) buy based on the method
            buy_row = crypto_inventory[crypto_type][0] if method == 'FIFO' else crypto_inventory[crypto_type][-1]
            
            buy_amount = min(buy_row['amount'], amount_to_sell)
            buy_cost = buy_amount * buy_row['price_usd']
            sale_value = buy_amount * sell_price
            gain_loss += sale_value - buy_cost

            # Determine holding period and term
            holding_period = (sell_date - buy_row['date']).days
            term = 'long-term' if holding_period > 365 else 'short-term'
            
            # Update inventory
            buy_row['amount'] -= buy_amount
            if buy_row['amount'] == 0:
                if method == 'FIFO':
                    crypto_inventory[crypto_type].pop(0)
                else:
                    crypto_inventory[crypto_type].pop(-1)

            amount_to_sell -= buy_amount
            
            transactions_data.append({
                'crypto_type': crypto_type,
                'transaction_date_buy': buy_row['date'],
                'transaction_date_sell': sell_date,
                'amount': buy_amount,
                'purchase_price': buy_row['price_usd'],
                'sale_price': sell_price,
                'gain_loss': sale_value - buy_cost,
                'term': term
            })

    # Create a DataFrame for results
    result_df = pd.DataFrame(transactions_data)

    # Save or display report
    result_df.to_csv("crypto_tax_report.csv", index=False)
    print(f"Crypto tax report saved to 'crypto_tax_report.csv' using {method} method.")
    return result_df
