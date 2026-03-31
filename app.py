from typing import Annotated

import typer
import requests
import json

app = typer.Typer()

def select_item(item_name: Annotated[
    str,
    typer.Option(
        prompt="Please, select your favorite pokemon type."
    )
]):
    """
    Processes a selected item by its ID.
    """
    for name in item_name:
        print(f"Selected Pokemon type: {name['name']}")

@app.command()
def main():
    print("Hello! Welcome to the Pokemon CLI! Please, select the Pokemon type you wish.")

    api_url = "https://pokeapi.co/api/v2/type"
    response = requests.get(api_url)
    if response.status_code == 200:
        print("Request successful")
    else:
        print(f"Request failed with status code: {response.status_code}")

    poke_info = response.json()

    types_of_pokemon = list(poke_info['results'])

    for i, p in enumerate(types_of_pokemon):
        typer.echo(f"  [{i+1}] {p['name']}")

    choice_str = typer.prompt("Please select an type by number")

    selected_item = int

    try:
        choice_index = int(choice_str) - 1
        if 0 <= choice_index < len(types_of_pokemon):
            selected_item = types_of_pokemon[choice_index]
            typer.echo(f"You selected: {selected_item['name']}")
        else:
            typer.echo("Invalid choice.")
            raise typer.Abort()
    except ValueError:
        typer.echo("Invalid input. Please enter a number.")
        raise typer.Abort()
    
    typer.echo("The following Pokemons have the types you've chosen: ")
    # count de pokemon 
    # olhar dentro de cada um desses counts e trazer o que tem o type selecionado 
    api_url = "https://pokeapi.co/api/v2/pokemon"
    response = requests.get(api_url)
    if response.status_code == 200:
        print("Request successful")
    else:
        print(f"Request failed with status code: {response.status_code}")

    countmon = response.json()

    pokecount = countmon['count']
    print(f"It were fetched {pokecount} pokemons.")

    list_of_pokemon = []
    for p in range(1, int(pokecount) + 1):
        try:
            api_url = f"https://pokeapi.co/api/v2/pokemon/{str(p)}"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                pass
            else:
                # print(f"Request failed with status code: {response.status_code}")
                continue # Skip the rest of this loop if the ID doesn't exist

            typemon = response.json()

            poketype = typemon['types'][0]['type']['name']

            if poketype == selected_item['name']:
                print(typemon['name'])
                
        except Exception as e:
            print(e)
        
    for p in list_of_pokemon:
        print(p)


if __name__ == "__main__":
    app()