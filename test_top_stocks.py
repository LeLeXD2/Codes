from predictor import top_stocks


stocks = top_stocks(5)


print("\n================================")
print("TOP 5 ML STOCKS")
print("================================")


if not stocks:

    print("No BUY stocks found.")

else:

    for i, stock in enumerate(stocks, 1):

        print(
            f"{i}. {stock['Ticker']} | "
            f"Return: {stock['Predicted_Return']:.2%} | "
            f"Rank: {stock['Rank']:.2%} | "
            f"Signal: {stock['Signal']}"
        )