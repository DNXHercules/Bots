from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()

#login

driver.get("https://lex.education/")

time.sleep(1)

perfilUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/sso-login-profile/div/sso-login-layout/div/div[2]/section/lex-card/div/a[3]/div')))
time.sleep(2)
perfilUsuario.click()

loginUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-input/mat-form-field/div/div[1]/div[2]/input')))
loginUsuario.send_keys('jaqueline.floriano@dnx.tec.br')

senhaUsuario = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
senhaUsuario.send_keys('Maple@0405') 

entrarUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
entrarUsuario.click() 

complementarCadastro = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
complementarCadastro.click()

#Escolas
# elementos_div = driver.find_elements(By.CSS_SELECTOR,"body > sso-root > lex-user-portal-page > lex-backdrop > div > div > main > section.user-portal-page__content__section.user-portal-page__content__schools > lex-card > div")
elementos_div = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")


# Filtrar elementos que contêm o texto "Maple Bear"
elementos_filtrados = []

for elemento in elementos_div:
    titulo_elemento = elemento.find_element(By.XPATH, "/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[1]/lex-card/div/a[1]/div")
    texto_titulo = titulo_elemento.text
       
    # Verificar se o texto "Maple Bear" está presente no título
    if "maple bear" in texto_titulo.lower():
        elementos_filtrados.append(elemento)

adicionadoCord =[]
naoCadastrados = []
errosEscolas = []

indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

if elementos_filtrados:
    
    for indice in indices: #range(1,len(elementos_filtrados)):
        
    #for indice in indices:
        time.sleep(5)
        
        titulo_elemento = elementos_filtrados[indice].find_element(By.CSS_SELECTOR, "h3")
        nomeEscola = titulo_elemento.text
       
        try:
            try:
                elementos_filtrados[indice].click()
                
            except StaleElementReferenceException:
                print("Erro")
                # # Se ocorrer StaleElementReferenceException, recarregue o elemento e tente clicar novamente
                # WebDriverWait(driver, 10).until(EC.staleness_of(elementos_filtrados[indice]))
                # primeiro_elemento = driver.find_elements(By.CSS_SELECTOR, "div.cards-container__info")[indice]
                # primeiro_elemento.click()
                # time.sleep(5)
                
            time.sleep(5) #otimizar
            cadAdministrador = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            cadAdministrador.click()

            aba_atual = driver.window_handles[-1]
            driver.switch_to.window(aba_atual)                   

            time.sleep(5)

            try:
                # Wait for the element to be clickable
                menuUsuarios = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/usuarios']")))
                # Click on the element
                menuUsuarios.click()
            except StaleElementReferenceException:
                # If the element is stale, find it again and retry
                menuUsuarios = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/usuarios']")))
                menuUsuarios.click()

            filtrarNome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-list-filter-user/form/div[1]/div[1]/input')))
            filtrarNome.send_keys('40997778806')
            filtrarNome.send_keys(Keys.ENTER)
            time.sleep(4)
            filtrarNome.send_keys(Keys.ENTER)
            
            textoNenhumRegistro = False # inicializacao (pode er qualquer coisa)

            try:
                # Esperar até que o elemento esteja presente na página
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.no-data")))
                
                textoNenhumRegistro = True # -> Significa que não existem cadastros

            except TimeoutException:
                textoNenhumRegistro = False # Significa que existe algum cadastro
            
            # textoNenhumRegistro for falso, significa que encontrou alguem, assumimos que é a pessoa
            # textoNenhumRegistro for true, significa que nao encontrou a pessoa
            
            if textoNenhumRegistro == False: # Se existe cadastro, vamos colocar o perfil
                
                entrarCadastro = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-lex-table/div[2]/div[2]/div/div[6]/div/span")))
                entrarCadastro.click()
                
                
                SecretarioAdicionado = False
                
                try:
                
                    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/seb-form-table-component/div/div/table/tbody/tr[2]/td[1]/span')))
                    time.sleep(1)
                    CoordenadorAdicionado = True
                                        
                except TimeoutException:
                    CoordenadorAdicionado = False
                
                if CoordenadorAdicionado == True:
                    
                    time.sleep(10)
                    
                    colocarPerfilSecretario = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                    colocarPerfilSecretario.send_keys("Secretaria")
                    colocarPerfilSecretario.send_keys(Keys.ENTER)
                    
                    #time.sleep(5)

                    #selecionarPerfilCoordenador = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/div[2]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div[14]')))
                    

                    time.sleep(5)
                    
                    clicarVincularPerfil = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/div[2]/div[2]/button')))
                    clicarVincularPerfil.click()
                    
                    time.sleep(10)
                     
                    salvarCadastro = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[7]/div/seb-buttons-form-completion/div/button[2]/div/span")))
                    salvarCadastro.click()
                    
                    print("Adicionado Perfil Secretaria", nomeEscola)
                    adicionadoCord.append(indice)
                    print(indice)
                    
                    driver.close()
                    first_tab = driver.window_handles[0]
                    driver.switch_to.window(first_tab)
                else:
                    print(f"[{indice}] Ja cadastrado como secretaria Escola: {nomeEscola}")
                    driver.close()
                    first_tab = driver.window_handles[0]
                    driver.switch_to.window(first_tab)        
            else:
                
                print(f"[{indice}] Não está cadastrado Escola: {nomeEscola}")
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)  
            
        #print erro
        except Exception as error:
            
            print(f"[{indice}] Deu erro na escola: {nomeEscola}")
            errosEscolas.append(indice)
            
            if len(driver.window_handles) > 1:
                driver.close()
            first_tab = driver.window_handles[0]
            driver.switch_to.window(first_tab)  
            
print("Lista não cadastrados: ")
print(naoCadastrados)

print("Lista erros: ")
print(errosEscolas)