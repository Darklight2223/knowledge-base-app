import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyA2ugeGf1DZHgNcwPD5lJtxOvou68cSunM")

# List embedding models with full details
print("Embedding Models Details:\n")
for model in genai.list_models():
    if 'embedContent' in model.supported_generation_methods:
        print(f"Name: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Input Token Limit: {getattr(model, 'input_token_limit', 'N/A')}")
        print(f"  Output Token Limit: {getattr(model, 'output_token_limit', 'N/A')}")
        # Print all available attributes
        for attr in dir(model):
            if not attr.startswith('_'):
                try:
                    val = getattr(model, attr)
                    if not callable(val):
                        print(f"  {attr}: {val}")
                except:
                    pass
        print()
