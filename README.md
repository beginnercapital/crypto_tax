# crypto_tax
Exports buy and sell transactions to csv based for tax reporting. My thread on X: https://x.com/beginnercapital/status/1855477243612442855

To run: 
# Use FIFO method (default)
df_report = calculate_crypto_taxes('path/to/your/crypto_transactions.csv', method='FIFO')

# Use LIFO method
df_report = calculate_crypto_taxes('path/to/your/crypto_transactions.csv', method='LIFO')
