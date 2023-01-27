import re
import time
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


email = str(input('Digite o email: '))
password = getpass()
link_pesquisa = 'https://www.linkedin.com/search/results/people/?keywords=tech%20recruiter&origin=CLUSTER_EXPANSION&sid=4d5'


navegador = webdriver.Firefox()
navegador.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
navegador.find_element('xpath', '//*[@id="username"]').send_keys(email)
navegador.find_element('xpath', '//*[@id="password"]').send_keys(password)
navegador.find_element('xpath', '/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()
url = navegador.current_url
tabela = []
erros = 0
navegador.get(link_pesquisa)


for i in range(0, 10, 1):
    while url != link_pesquisa:
        url = navegador.current_url
        time.sleep(3)

    navegador.execute_script("window.scrollTo(0, 1080)")
    time.sleep(1)
    site = BeautifulSoup(navegador.page_source, 'html.parser')
    botoes = site.findAll('button', attrs={'class': 'artdeco-button artdeco-button--2 artdeco-button--secondary ember-view'})
    try:
        for botao in botoes:
            botao = str(botao)
            ember = botao[botao.find('id="ember') + 9:botao.find('"><!-- -->')]
            xpath = f'//*[@id="ember{ember}"]'
            navegador.find_element('xpath', xpath).click()
            site = BeautifulSoup(navegador.page_source, 'html.parser')
            try:
                add = site.find('button', attrs={'aria-label': 'Enviar agora'})
                add = str(add)
                ember = add[add.find('id="ember') + 9:add.find('"><!-- -->')]
                xpath = f'//*[@id="ember{ember}"]'
                navegador.find_element('xpath', xpath).click()
            except:
                print('Não adcionado')
            try:
                close = site.find('button', attrs={'aria-label': 'Fechar'})
                close = str(close)
                ember = close[close.find('id="ember') + 9:close.find('"> <li-icon aria')]
                xpath = f'//*[@id="ember{ember}"]'
                navegador.find_element('xpath', xpath).click()
            except:
                print('Nada aberto')
            site = BeautifulSoup(navegador.page_source, 'html.parser')

        idember = site.find('button', attrs={'aria-label': 'Avançar'})
        idember = str(idember)
        idember = re.sub('[-<>!/"]', '', idember[idember.find('id="ember') + 9:idember.find('type="button') - 2])
        xpath = f'//*[@id = "ember{idember}"]'
        time.sleep(2)
        navegador.find_element('xpath', xpath).click()
        time.sleep(2)
        url = navegador.current_url
        link_pesquisa = navegador.current_url
    except:
        print('pagina não encontrada')
        navegador.refresh()
        time.sleep(5)
        erros += 1
        if erros >= 50:
            break
        continue
