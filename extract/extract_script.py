import re 
import pandas as pd
from time import sleep
from playwright.sync_api import sync_playwright

dict_storage = {
    'title':[],
    'price':[]
}


def run_extract():
    with sync_playwright() as p:

        try:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--start-maximized'
                ]
            )

            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                device_scale_factor=1
            )
            page = context.new_page()

            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # Navegação até página do estado
            page.goto('https://www.olx.com.br/imoveis/venda/estado-go')

            # Container que armazena cada container
            container_cards = page.locator('.AdListing_adListContainer__ALQla')
            # Armazena o iteravel de cada card
            cards = container_cards.locator('.olx-adcard.olx-adcard__horizontal').all()

            # Itrera sob cada card
            for card in cards:

                # Conteudo do card
                content = card.locator('.olx-adcard__content')
                # Titulo do card
                topbody = content.locator('.olx-adcard__topbody')
                # Titulo do card
                title = topbody.get_by_test_id('adcard-link').text_content()

                # Local que fica valor
                medium_body = content.locator('.olx-adcard__mediumbody')

                # Valor do imovel
                valor = medium_body.locator('.olx-adcard__price').text_content()

                # Incrementando o dicionário
                dict_storage['title'].append(title)
                dict_storage['price'].append(valor.replace('R$ ','').strip())

        except Exception as e:
            print(f'Erro: {e}')

        page.close()
        browser.close()

        return dict_storage
    


def transform(dictionary : dict) -> pd.DataFrame:

    df = pd.DataFrame(dictionary)

    df['price'] = df['price'].str.replace('.','').astype(int)

    return df

if __name__ == '__main__':
    
    try:

        dicionario = run_extract()

        df = transform(dicionario)

        print(df)

    except Exception as e:

        print(f'Erro: {e}')


