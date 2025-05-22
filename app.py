from typing import Dict, Any
from string import Template

import gradio as gr
from smolagents import ToolCallingAgent, tool, InferenceClientModel
from pokemontcgsdk import Card


PROMPT = Template("""
    You are a Pokémon TCG market analyst. For the input card: "$card" from the set: "$set", follow these instructions:
    1. Retrieve the card data with the tool: "get_card_info"
    2. With the retrieved information, analyze the card investment potential: Key Insights, Investment Analysis, Value drivers, Risks, Overall assessment, Investment grade (e.g., "High", "Medium", "Low"), Key Metric.
    3. Return the Final answer as a Markdown string output containing the retrieved card information in sections: Name, Set, Key Insights, Key Metric, Investment Analysis, Investment grade, Value drivers, Risks, Overall assessment.
    """)


PROMPT_NOTES = """
    #TCG API fields information
    ##Fields
    - name: The name of the Pokémon card.
    - set_name: The name of the set the card belongs to.
    - rarity: The rarity of the card.
    - release_date: The release date of the set.
    - printed_total: The total number of cards printed in the set.
    - updated_at: The last update date of the card data.
    - average_sell_price: The average selling price of the card.
    - low_price: The lowest price of the card.
    - trend_price: The trend price of the card.
    - suggested_price: The suggested price of the card.
    - reverse_holo_sell: The selling price of the reverse holo version of the card.
    - cardmarket_prices_reverse_holo_trend: The trend price of the reverse holo version of the card.
    - cardmarket_prices_reverse_holo_low: The lowest price of the reverse holo version of the card.
    """


def get_card_image(card_name: str, set_name: str) -> str | dict[str, str]:
    """
    Fetches the image URL of a specific Pokémon TCG card from the official Pokémon TCG API.
    Args:
        card_name (str): The name of the Pokémon TCG card.
        set_name (str): The name of the Pokémon TCG set.
    Returns:
        str: The URL of the card image.
    """
    card_name_formated_list = card_name.lower().split(' ')
    card_name_formated = f"({'AND '.join([f' name:{name} ' for name in card_name_formated_list])})"

    set_name_formated_list = set_name.lower().replace('&', '').split(' ')
    set_name_formated = f"({'AND '.join([f' set.name:{name} ' for name in set_name_formated_list])})"

    card_data = Card.where(q=f"{card_name_formated} {set_name_formated}")
    
    if len(card_data) == 0:
        return {
            "error": "Card not found",
            "card_name": card_name,
            "set_name": set_name
        }

    card_data = card_data[0]
    return card_data.images.small



@tool
def get_card_info(card_name: str, set_name: str) -> Dict[str, Any]:
    """
    Fetches detailed information about a specific Pokémon TCG card from the official Pokémon TCG API.
    Args:
        card_name (str): The name of the Pokémon TCG card.
        set_name (str): The name of the Pokémon TCG set.
    Returns:
        Dict[str, Any]: A dictionary containing detailed card information.
    """
    card_name_formated_list = card_name.lower().split(' ')
    card_name_formated = f"({'AND '.join([f' name:{name} ' for name in card_name_formated_list])})"

    set_name_formated_list = set_name.lower().replace('&', '').split(' ')
    set_name_formated = f"({'AND '.join([f' set.name:{name} ' for name in set_name_formated_list])})"

    card_data = Card.where(q=f"{card_name_formated} {set_name_formated}")
    
    if len(card_data) == 0:
        return {
            "error": "Card not found",
            "card_name": card_name,
            "set_name": set_name
        }
        
    card_data = card_data[0]
    
    field_map = {
        "url": ["cardmarket", "url"],
        "name": ["name"],
        "set_name": ["set", "series"],
        "rarity": ["rarity"],
        "release_date": ["set", "releaseDate"],
        "printed_total": ["set", "printedTotal"],
        "updated_at": ["cardmarket", "updatedAt"],
        "average_sell_price": ["cardmarket", "prices", "averageSellPrice"],
        "low_price": ["cardmarket", "prices", "lowPrice"],
        "trend_price": ["cardmarket", "prices", "trendPrice"],
        "suggested_price": ["cardmarket", "prices", "suggestedPrice"],
        "reverse_holo_sell": ["cardmarket", "prices", "reverseHoloSell"],
        "cardmarket_prices_reverse_holo_trend": ["cardmarket", "prices", "reverseHoloTrend"],
        "cardmarket_prices_reverse_holo_low": ["cardmarket", "prices", "reverseHoloLow"],
    }

    result = {}

    for key, path in field_map.items():
        try:
            value = card_data
            for attr in path:
                value = getattr(value, attr)
            result[key] = value
        except (AttributeError, TypeError):
            continue
        
    return result


class PokemonTCGAgent:
    def __init__(self):
        print("BasicAgent initialized.")
        self.agent = ToolCallingAgent(
            model=InferenceClientModel(),
            tools=[get_card_info,],
            add_base_tools=True,
            max_steps=10, 
            verbosity_level=2,
        )

    def __call__(self, card_name: str, set_name: str,) -> str:
        print(f"Agent received input card and set names: {card_name} - {set_name}...")
        answer = self.agent.run(
            PROMPT.substitute(card=card_name,
                              set=set_name),
            additional_args=dict(additional_notes=PROMPT_NOTES)
        )
        print(f"Agent returning answer: {answer}")
        return answer


def run_agent(card_name: str, set_name: str) -> str | tuple[str, None]:
    """
    Runs the agent with the provided card name and set name.
    Args:
        card_name (str): The name of the Pokémon TCG card.
        set_name (str): The name of the Pokémon TCG set.
    Returns:
        str | tuple[str, None]: The agent's response or an error message.   
    """
    # 1. Instantiate Agent
    try:
        agent = PokemonTCGAgent()
    except Exception as e:
        print(f"Error instantiating agent: {e}")
        return f"Error initializing agent: {e}", None

    # 2. Run the Agent
    print("Running agent...")
    try:
        answer = agent(card_name=card_name, set_name=set_name)
        return answer
    except Exception as e:
            print(f"Error running agent for card: {card_name}, set: {set_name}")
            return f"Error running agent: {e}", None


def run_app(card_name: str, set_name: str) -> tuple[str | dict[str, str], str | tuple[str, None]]:
    """
    Runs the app with the provided card name and set name.
    Args:
        card_name (str): The name of the Pokémon TCG card.
        set_name (str): The name of the Pokémon TCG set.
    Returns:
        tuple[str, str]: The card image URL and the agent's response.
    """
    return get_card_image(card_name, set_name), run_agent(card_name, set_name)


if __name__ == "__main__":
    print("Launching Gradio Interface for Pokemon TCG Valuator...")
    with gr.Blocks() as demo:
        gr.Interface(
            title="Pokemon TCG Card Valuator Agent",
            description="""
            \t* The Pokémon TCG Card Valuator Agent uses the [Pokémon TCG API](https://docs.pokemontcg.io/) to fetch card data from Cardmarket and analyze its investment potential.\n
            \t* The agent provides insights on the card's investment potential, including: Key insights, Investment Analysis, Value drivers, Investment grade, Key Metric, Risks, Overall assessment
            """,
            theme="soft",
            fn=run_app,
            inputs=[
                gr.Textbox(
                    label="Card Name",
                    lines=1,
                    value="Squirtle",
                ),
                gr.Textbox(
                    label="Set Name",
                    lines=1,
                    value="Stellar Crown",
                ),
            ],
            outputs=[
                gr.Image(
                    label="Card Valuation",
                ),
                gr.Markdown(
                    label="Card Valuation",
                ),
            ]
        )
    demo.launch(debug=True, share=False)