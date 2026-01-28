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

perfilUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user-portal-profile"]/lex-card/div/a[3]/div/div[2]/h3')))
perfilUsuario.click()

loginUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-input/mat-form-field/div/div[1]/div[2]/input')))
loginUsuario.send_keys('jaqueline.floriano@dnx.tec.br')

senhaUsuario = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
senhaUsuario.send_keys('Maple@0405') 

entrarUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
entrarUsuario.click() 

time.sleep(2)

complementarCadastro = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
complementarCadastro.click()

#Escolas
elementos_div = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")

# Filtrar elementos que contêm o texto "Maple Bear"
elementos_filtrados = []

for elemento in elementos_div:
    titulo_elemento = elemento.find_element(By.CSS_SELECTOR, "h3")
    texto_titulo = titulo_elemento.text
       
    # Verificar se o texto "Maple Bear" está presente no título
    if "maple bear" in texto_titulo.lower():
        elementos_filtrados.append(elemento)

indices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
naoCadastrados = []
errosEscolas = []

if elementos_filtrados:
    
    for indice in indices: #range(5,len(elementos_filtrados)): 
        time.sleep(1)
        

        titulo_elemento = elementos_filtrados[indice].find_element(By.CSS_SELECTOR, "h3")
        nomeEscola = titulo_elemento.text
       
        try:
            try: 
                elementos_filtrados[indice].click()
            except StaleElementReferenceException:
                print("Erro")

            time.sleep(5) #otimizar
            cadAdministrador = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            cadAdministrador.click()
            time.sleep(4)

            aba_atual = driver.window_handles[-1]
            driver.switch_to.window(aba_atual)  
            time.sleep(5)                 

            menuUsuarios = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/usuarios']")))
            menuUsuarios.click()

            filtrarNome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-list-filter-user/form/div[1]/div[1]/input')))
            filtrarNome.send_keys('42836701897')  #Adicionar CPF do Usuário sem pontos
            filtrarNome.send_keys(Keys.ENTER)
            time.sleep(2)
            filtrarNome.send_keys(Keys.ENTER)
            
            nenhum_registro = False

            try:
                # Esperar até que o elemento esteja presente na página
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.no-data")))
                
                # Se a exceção não for acionada, definir a variável para True
                nenhum_registro = True

            except TimeoutException:
                pass

            if(nenhum_registro):
                novoUsuario = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-usuario/seb-titlebar/div/div/div[2]/div/lex-button/button/span')))
                novoUsuario.click()       
                time.sleep(2)
                nomeCompleto = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-user/div/form/div/div[1]/div[2]/input')))
                nomeCompleto.send_keys("Jamille Marques da Silva") #Adicionar nome do usuário a ser cadastrado
                time.sleep(2)
                dataNascimento = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-user/div/form/div/div[1]/div[3]/div/seb-datepicker/form/div/input')))
                dataNascimento.send_keys("29/03/1995") #Adicionar a data de nascimento
                time.sleep(2)
                cpfNumero = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-user/div/form/div/div[2]/div[1]/input')))
                cpfNumero.send_keys("42836701897") #Adicionar CPF do Usuário sem pontos
                time.sleep(2)
                #celularNumero = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-user/div/form/div/div[2]/div[3]/intl-input/div/div/input')))
                #celularNumero.send_keys("12981856171")
                
                emailText = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-user/div/form/div/div[3]/div[1]/input')))
                emailText.send_keys('jamille.silva@mbcentral.com.br') #Adicionar o E-mail
                time.sleep(2)
                perfilAdicionar = ["Admin Escola", "Coordenador"]  #Os perfis que vocês quiserem adicionar, precisa digitar aqui exatamente como é na LEX
                time.sleep(2)
                # perfilSelecionar = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-user/div/form/section[1]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                # perfilSelecionar.send_keys("Admin Operação")
                # perfilSelecionar.send_keys(Keys.ENTER)

                # criarPerfil = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, " /html/body/seb-root/div[3]/div/seb-new-user/div/form/section[1]/div[2]/div[2]/button")))
                # criarPerfil.click()
                
                for perfil in perfilAdicionar:
                    
                    perfilSelecionar = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-user/div/form/section[1]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                    perfilSelecionar.send_keys(perfil)
                    perfilSelecionar.send_keys(Keys.ENTER)

                    criarPerfil = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, " /html/body/seb-root/div[3]/div/seb-new-user/div/form/section[1]/div[2]/div[2]/button")))
                    criarPerfil.click()
                    
                    perfilSelecionar.send_keys(Keys.CONTROL, "A")
                    perfilSelecionar.send_keys(Keys.DELETE)
                
                salvarCadastro = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-user/div/section[2]/div/seb-buttons-form-completion/div/button[2]")))
                salvarCadastro.click()
                time.sleep(10)
                 
                # Switch to the first tab
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)                        
                print("Cadastro realizado ", nomeEscola)

            else:
                print("Já cadastrado na Escola: ", nomeEscola)
                print(indice)
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)  
                
        except Exception as error:
            print("Deu erro na escola: ", nomeEscola)
            print(indice)
            #print(error)
            
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