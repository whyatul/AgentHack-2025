import argparse
from src.ai_meme_stock_predictor.agent.portia_agent import PortiaMemeAgent


def main():
    parser = argparse.ArgumentParser(description="CLI Meme Stock Query")
    parser.add_argument("ticker", help="Stock ticker symbol, e.g. TSLA")
    parser.add_argument("--conversation-id", default="cli", help="Conversation identifier")
    args = parser.parse_args()
    agent = PortiaMemeAgent()
    text = f"{args.ticker} memes?"
    resp = agent.handle_query(args.conversation_id, text)
    print(resp.get('response'))
    if 'details' in resp:
        print(resp['details']['explanation'])

if __name__ == "__main__":
    main()
