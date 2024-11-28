class MemecoinAMM:
    def __init__(self, eth_price, coin_name, coin_supply, initial_eth, initial_tokens):
        self.eth_price = eth_price  # ETH price in USD
        self.coin_name = coin_name  # Token name
        self.coin_supply = coin_supply  # Total token supply
        self.eth_reserve = initial_eth  # Initial ETH in liquidity pool
        self.token_reserve = initial_tokens  # Initial tokens in liquidity pool
        self.k = self.eth_reserve * self.token_reserve  # Constant product
    
    def get_price(self):
        # Token price in ETH
        return self.eth_reserve / self.token_reserve
    
    def get_usd_price(self):
        # Token price in ETH
        return self.get_price()  * self.eth_price
    
    def get_market_cap(self):
        # Market cap in USD
        return self.get_price() * self.coin_supply * self.eth_price
    
    def get_volume(self):
        # Total liquidity in the pool in USD
        return (self.eth_reserve * self.eth_price) + (self.token_reserve * self.get_price() * self.eth_price)
    
    def trade(self, eth_amount=0, token_amount=0):
        """Handle a trade. If eth_amount > 0, it's a buy. If token_amount > 0, it's a sell."""
        if eth_amount > 0:
            # Buying tokens with ETH
            new_eth_reserve = self.eth_reserve + eth_amount
            new_token_reserve = self.k / new_eth_reserve
            tokens_bought = self.token_reserve - new_token_reserve
            self.eth_reserve = new_eth_reserve
            self.token_reserve = new_token_reserve
            return tokens_bought
        elif token_amount > 0:
            # Selling tokens for ETH
            new_token_reserve = self.token_reserve + token_amount
            new_eth_reserve = self.k / new_token_reserve
            eth_received = self.eth_reserve - new_eth_reserve
            self.eth_reserve = new_eth_reserve
            self.token_reserve = new_token_reserve
            return eth_received
        else:
            return 0
    
    def status(self):
        print(f"Coin Name: {self.coin_name}")
        print(f"Market Cap: ${self.get_market_cap():,.2f}")
        print(f"Token Price: {self.get_price():.6f} ETH")
        print(f"Token price in usd: ${self.get_usd_price()}")
        print(f"Liquidity Volume: ${self.get_volume():,.2f}")
        print(f"ETH Reserve: {self.eth_reserve:.6f} ETH")
        print(f"Token Reserve: {self.token_reserve:,.6f} {self.coin_name}")
    
    def help(self):
        print("""
Available Commands:
    help - Show this help message
    status - Show market status (market cap, price, volume)
    buy [eth_amount] - Buy tokens with ETH
    sell [eth_amount] - Sell tokens for ETH
        """)

# Example usage
if __name__ == "__main__":
    # Initialize the AMM
    amm = MemecoinAMM(
        eth_price=3590,  # ETH price in USD
        coin_name="MEME",
        coin_supply=1337_000_000,  # Total MEME supply
        initial_eth=5,  # Initial ETH in the pool
        initial_tokens=133_700_000  # Initial MEME in the pool
    )
    print(f"Inital supply {amm.coin_supply}")
    
    while True:
        cmd = input("Enter command (type 'help' for options): ").strip().lower()
        if cmd == "help":
            amm.help()
        elif cmd == "status":
            amm.status()
        elif cmd.startswith("buy"):
            try:
                eth_amount = float(cmd.split()[1])
                tokens_bought = amm.trade(eth_amount=eth_amount)
                print(f"You bought {tokens_bought:.6f} {amm.coin_name} for {eth_amount:.6f} ETH.")
            except (IndexError, ValueError):
                print("Invalid input. Use: buy [eth_amount]")
        elif cmd.startswith("sell"):
            try:
                eth_amount = float(cmd.split()[1])
                tokens_sold = eth_amount / amm.get_price()
                eth_received = amm.trade(token_amount=tokens_sold)
                print(f"You sold {tokens_sold:.6f} {amm.coin_name} for {eth_received:.6f} ETH.")
            except (IndexError, ValueError):
                print("Invalid input. Use: sell [eth_amount]")
        elif cmd == "exit":
            print("Exiting the simulation. Goodbye!")
            break
        else:
            print("Unknown command. Type 'help' for available commands.")
