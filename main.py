import requests
import json
import os

ARQUIVO = 'favoritos.json'

def carregar_favoritos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_favoritos(favoritos):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(favoritos, f, indent=4, ensure_ascii=False)

def buscar_animal(nome):
    url = f"https://api.api-ninjas.com/v1/animals?name={nome}"
    headers = {"X-Api-Key": "X7azIJYItHHO5JzML7FoAlJv3KMuaj4UW34tX2x0"}
    resposta = requests.get(url, headers=headers)
    
    if resposta.status_code == 200 and resposta.json():
        return resposta.json()[0]
    return None

def exibir_animal(animal):
    print(f"\n🐾 {animal['name']}")
    print(f"   Dieta: {animal.get('characteristics', {}).get('diet', 'N/A')}")
    print(f"   Habitat: {animal.get('characteristics', {}).get('habitat', 'N/A')}")
    print(f"   Tempo de vida: {animal.get('characteristics', {}).get('lifespan', 'N/A')}")

def menu():
    favoritos = carregar_favoritos()
    
    while True:
        print("\n==== API DE ANIMAIS ====")
        print("1 - Buscar animal")
        print("2 - Ver favoritos")
        print("3 - Sair")
        
        opcao = input("\nEscolha: ")
        
        if opcao == "1":
            nome = input("Nome do animal (em inglês): ")
            animal = buscar_animal(nome)
            
            if animal:
                exibir_animal(animal)
                salvar = input("\nSalvar nos favoritos? (s/n): ")
                if salvar.lower() == "s":
                    favoritos.append(animal)
                    salvar_favoritos(favoritos)
                    print("Salvo!")
            else:
                print("Animal não encontrado.")
        
        elif opcao == "2":
            if favoritos:
                print("\n Seus favoritos:")
                for a in favoritos:
                    exibir_animal(a)
            else:
                print("Nenhum favorito ainda.")
        
        elif opcao == "3":
            print("Até mais!")
            break

menu() 