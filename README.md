# crypto_tax
Exports buy and sell transactions to csv based for tax reporting. Separates buy and sell transactions to match each sell with its most recent preceding buy (depending on parameter; see #1 below). `#buildinpublic`

1. `method` Parameter: This parameter specifies whether to use "FIFO" or "LIFO". The function will default to "FIFO" if no input is given.
    - First In, First Out (FIFO): Under FIFO, the assets you acquired first are considered sold first. This can be advantageous in a market where prices are rising because selling older (likely cheaper) assets could lead to a higher cost basis, potentially resulting in lower capital gains and tax liability.
    - Last In, First Out (LIFO): Under LIFO, the most recently acquired assets are considered sold first. This approach could be beneficial if you’ve recently purchased assets at a higher price, as a higher cost basis can reduce taxable gains. However, LIFO may not always be allowed under the IRS rules for every situation and often requires consistent application to avoid triggering red flags or penalties.
    - Specific Identification: The IRS does allow for specific identification for cryptocurrency, which means you can select specific units to sell based on their acquisition date and cost. However, to use this method, you must maintain detailed records and be able to track each asset's purchase date and cost basis.

2. Conditional Inventory Selection: The function now checks the method parameter to decide whether to take the first or last item in the crypto_inventory list.
3. Inventory Update: After each partial sale, the function updates the buy inventory, removing records when they’re fully sold.
4. Short-Term or Long-Term Determination: The holding term is calculated based on the number of days between buy and sell.
   
For more, see my thread on X: https://x.com/beginnercapital/status/1855477243612442855

# To run: Use FIFO method (default)
`df_report = calculate_crypto_taxes('path/to/your/crypto_transactions.csv', method='FIFO')`

# Use LIFO method
`df_report = calculate_crypto_taxes('path/to/your/crypto_transactions.csv', method='LIFO')`

# Enhancements
- Fetch intraday prices
