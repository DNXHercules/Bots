from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import codecs

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

TIMEOUT_HOMEPAGE = 31

time.sleep(10)

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

deuErro = []
errosEscolas =[]
naoEnturmados = []
enturmados = []
indices = [16]



if elementos_filtrados:
    
    for indice in indices:#range(5,len(elementos_filtrados)):
        time.sleep(3)
        
    #for indice in range(6):
        
        titulo_elemento = elementos_filtrados[indice].find_element(By.CSS_SELECTOR, "h3")
        nomeEscola = titulo_elemento.text

        time.sleep(3)
       
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
                
            time.sleep(10) #otimizar
            cadAdministrador = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            cadAdministrador.click()

            time.sleep(3)

            aba_atual = driver.window_handles[-1]
            driver.switch_to.window(aba_atual) 
            
            time.sleep(3)  

            menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
            menuTurmas.click()

            time.sleep(3)
            
            UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[1]/ng-select/div/div/div[2]/input")))
            UnidadesEscolher.click()
            
            unidades = driver.find_elements(By.XPATH, "//div[@class='ng-dropdown-panel-items scroll-host']//div[@class='ng-option']")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                        
            codigoTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[2]/input")))
            codigoTurma.send_keys("SUPORTE2026")
            
            filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
            filtrarCodigo.click()
            
            time.sleep(2)
            
            turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and @title='SUPORTE LEX 2026' and text()='SUPORTE LEX 2026']"
            )
            time.sleep(4)
            
            if turmaExiste:
                print("Turma já existe na Escola:", nomeEscola)
                time.sleep(4)
                clicarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div")))
                clicarTurma.click()
                
                time.sleep(4)
                
                timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "gabriela.santos@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "leticia.oliveira@dnx.tec.br", "yasmin.martins@maplebear.com.br", "toddle@maplebear.com.br"] 
                        # timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "fernanda.vieira@dnx.tec.br"] 

                time.sleep(4)
                
                for pessoa in timeLexToddle:
                    
                    try:
                        
                        if pessoa:
                            time.sleep(4)
                            inserirUsuariosTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                            inserirUsuariosTurma.click()
                            inserirUsuariosTurma.send_keys(pessoa)
                            time.sleep(2)
                            inserirUsuariosTurma.send_keys(Keys.ENTER)
                            time.sleep(2)
                            inserirUsuariosTurma.send_keys(Keys.ENTER)
                            
                            time.sleep(4)
                            
                            selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input')))
                            selecionarPerfil.click()
                            selecionarPerfil.send_keys("Coordenador")
                            selecionarPerfil.send_keys(Keys.ENTER)

                            # selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[3]/input")))
                            # selecionarPerfilCoordenador.send_keys("Coordenador")
                            # selecionarPerfilCoordenador.send_keys(Keys.ENTER)
                            
                            adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                            adicionarUsuarios.click()
                            
                            inserirUsuariosTurma.send_keys(Keys.CONTROL,"A")
                            inserirUsuariosTurma.send_keys(Keys.DELETE)
                            
                            print("Usuário:", pessoa, "adicionado a turma!")
                            
                            WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                            continue
                        
                        else:
                            print(f"Erro ao adicionar o usuário {pessoa}")
                            errosEscolas.append(indice)
                        
                            
                    except:
                        continue
                    
                
                clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/seb-buttons-form-completion/div/button[2]")))
                clicarSalvar.click()
                
                time.sleep(5)
                print(nomeEscola, ": Criado Turma Suporte LEX 2025")
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

            
            else:
                print("Turma não existe na Escola:", nomeEscola)  
                
                # criarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-titlebar/div/div/div[2]/div/lex-button/button")))
                # criarTurma.click()
                
                # time.sleep(1)
                
                # UnidadesTeste = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/div")))
                # UnidadesTeste.click()
                
                # unidades = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div")

                # if unidades:
                #     for unidade in unidades:
                #         if unidade.text == nomeEscola:
                #             unidade.click()
                #             break
                #         else:
                #             print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                
                # #Ano curso
                # ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
                # ano2025.click()
                
                # clicarAno2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "//html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                # clicarAno2025.click()

                # #Seleciona a séria
                # serieCurso =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
                # serieCurso.send_keys("Year 1 2025")
                
                # try:
        
                #     #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                #     #serieElementary.click
                #     time.sleep(1)
                #     year1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div/span")
                    
                #     if year1:
                    
                #         #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                #         #serieCurso.send_keys("YEAR 1")
                #         serieCurso.send_keys(Keys.ENTER)
                #         print("adicionado Y1", nomeEscola)
                    
                #     else:
                #         time.sleep(1)
                #         serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
                #         serieSK.click()
                #         serieSK.send_keys(Keys.CONTROL, "A")
                #         serieSK.send_keys(Keys.DELETE)
                #         serieSK.click()
                #         serieSK.send_keys("SENIOR KINDERGARTEN 2025")
                #         serieSK.send_keys(Keys.ENTER)
                #         print("Adicionado SK", nomeEscola)
                # except:
                #     print("A unidade não possui SK ou Year 1:", nomeEscola) 
                #     serieCurso.click()
                #     clicar1Item =   WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select")))      
                #     clicar1Item.click()
                    
                    
                    
                # #Inserir código
                # inserirCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[1]/input")))
                # inserirCodigo.send_keys("SUPORTE2025")
                
                # #inserir nome da turma
                # inserirNomeTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[2]/input")))
                # inserirNomeTurma.send_keys("SUPORTE LEX 2025")
                
                # clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/seb-buttons-form-completion/div/button[2]/div")))
                # clicarSalvar.click()
                
                # time.sleep(5)
                # print(nomeEscola, ": Criado Turma Suporte LEX 2025")
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                
        except Exception as error:
    
            print("Deu erro na escola: ", nomeEscola)
            print(indice)
            print(error)
            deuErro.append(indice)
            errosEscolas.append(indice)
            if len(driver.window_handles) > 1:
                driver.close()
            first_tab = driver.window_handles[0]
            driver.switch_to.window(first_tab)  

print("Lista erros: ")
print(errosEscolas)   
