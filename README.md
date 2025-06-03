# Pokemon TCG Valuator Agent

## Overview

AI Agent to assess the current investment value of Pokémon TCG cards.

This project provides an AI-powered tool for evaluating the investment value of Pokémon Trading Card Game (TCG) cards. It leverages machine learning and the Pokémon TCG API to analyze card data and estimate their current market value, helping collectors and investors make informed decisions.

## Features
- Automated valuation of Pokémon TCG cards
- Interactive web UI with Gradio
- Uses the official Pokémon TCG API for up-to-date card data
- Investment analysis and key metrics
- Modern, extensible Python codebase

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
Clone the repository:
```bash
git clone https://github.com/yourusername/pokemon-tcg-valuator-agent.git
cd pokemon-tcg-valuator-agent
```
Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage
To run the app locally:
```bash
python app.py
```

This will launch a Gradio web interface in your browser.

## Try it Online

You can try the app instantly on Hugging Face Spaces:

[![Hugging Face Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/spaces.svg)](https://huggingface.co/spaces/sergiosampayo/pokemon-tcg-valuator-agent)

[https://huggingface.co/spaces/sergiosampayo/pokemon-tcg-valuator-agent](https://huggingface.co/spaces/sergiosampayo/pokemon-tcg-valuator-agent)

## Project Structure
```
├── app.py               # Main Gradio app
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
├── README.md            # Project documentation
```

## License
MIT

## Acknowledgements
- [Gradio](https://gradio.app/)
- [Pokémon TCG API](https://docs.pokemontcg.io/)

