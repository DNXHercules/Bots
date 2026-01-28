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

def login(driver):

    TIMEOUT_LOGIN = 20

    driver.get("https://lex.education/")

    perfilUsuario = WebDriverWait(driver, TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user-portal-profile"]/lex-card/div/a[3]/div/div[2]/h3')))
    perfilUsuario.click()
    time.sleep(3)

    loginUsuario = WebDriverWait(driver, TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-input/mat-form-field/div/div[1]/div[2]/input')))
    loginUsuario.send_keys('jaqueline.floriano@dnx.tec.br')

    senhaUsuario = WebDriverWait(driver,TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
    senhaUsuario.send_keys('Maple@0405') 

    entrarUsuario = WebDriverWait(driver, TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
    entrarUsuario.click()

def dismissCompletarCadastr(driver):

    TIMEOUT_HOMEPAGE = 31

    complementarCadastro = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
    complementarCadastro.click()

def pegarEscolas(driver):

    TIMEOUT_HOMEPAGE = 31

    # Encontrar os cards antes, para não dar erro
    WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.cards-container__info")))

    cardsEscolas = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")

    cardsEscolas = cardsEscolas [0:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

    return cardsEscolas

def pegarCursos2026(driver, cardsEscolas, arquivo):

    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[253:260] # Remove a escola Mapple bear demonstração e o card "Administrador"

    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(2)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        
        time.sleep(1)   # Delay necessário
          
        menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "//li[a[@href='/cursos']]"))) 
        menuCursos.click()

        time.sleep(1)

        # Clicar no filtro de escola
        filtroEscola= WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filterCourseId"]/div/div/div[3]/input')))
        filtroEscola.click()

        time.sleep(1)

        try:
            
            # Pega as unidades
            unidades = driver.find_elements(By.XPATH, "//span[contains(@class, 'ng-option-label')]")

            if len(unidades) > 1:

                for unidade in unidades:
                    if unidade.text == nomeEscola:  # verifica se o card bate com a unidade
                        unidade.click()
                        break
            else:
                print("Escola com apenas uma unidade: ", nomeEscola)
        except:
            print("******Exception: Escola com apenas uma unidade: ", nomeEscola)
            
        # Clicar no filtro
        filtroAno= WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]/input')))
        filtroAno.click()

        # Selecionar o ano 2025
        selecionarAno = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]')))
        selecionarAno.click()

        # Clicar no botão Filtrar
        clicarFiltrar = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button')))
        clicarFiltrar.click()

        time.sleep(2)

        listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

        if len(listaCursos) == 1:
            print(f"{nomeEscola}, Nenhum")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Nenhum\n")
            
        else:
            
            # Remover o header da tabela
            listaCursos = listaCursos[1:]
            listaCursosStr = []

            for curso in listaCursos:
                                    
                #Encontre todas as colunas dentro da linha atual
                colunas = curso.find_elements(By.CSS_SELECTOR, '.table-text')
                nomeCurso = colunas[0].get_attribute('title')
                listaCursosStr.append(nomeCurso)

            print(f"{nomeEscola}, {listaCursosStr}")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, {listaCursosStr}\n")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

def pegarCNPJ(driver, cardsEscolas, arquivo):

    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[26:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(2)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        time.sleep(1)   # Delay necessário
        
        listaUnidades = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
        
        while len(listaUnidades) == 1:
            time.sleep(1)
            listaUnidades = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
        
        listaUnidades = listaUnidades[1:10]
                
        for unidade in listaUnidades:
            colunas = unidade.find_elements(By.CSS_SELECTOR, '.lex-table-column')
            
            nomeFantasia = colunas[2].text
            cnpj = colunas[4].text
            
            if nomeFantasia == nomeEscola:
                print(nomeFantasia," ", cnpj)
                with codecs.open(arquivo, "a","utf-8") as file:
                    file.write(f"{nomeEscola},{cnpj}\n")
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

def cadastrarTurmas(driver, cardsEscolas, arquivo):
    
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[240:255] # Remove a escola Mapple bear demonstração e o card "Administrador"
    errosEscolas =[]


    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(5)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(8)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(5)
        
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
        
        time.sleep(3)

        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        time.sleep(5)
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
                
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
        
        else:
            criarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-titlebar/div/div/div[2]/div/lex-button/button")))
            criarTurma.click()
            
            time.sleep(4)
            
            UnidadesTeste = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/div")))
            UnidadesTeste.click()
            
            unidades = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
            
            #Ano curso
            ano2026 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
            ano2026.click()
            
            clicarAno2026 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "//html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            clicarAno2026.click()

            #Seleciona o curso, vou deixar caso precise para criar turma para árvore
            '''serieCurso =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
            serieCurso.send_keys("Year 1 2026")
            
            try:
    
                #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                #serieElementary.click
                time.sleep(1)
                year1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div/span")
                
                if year1:
                
                    #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                    #serieCurso.send_keys("YEAR 1")
                    serieCurso.send_keys(Keys.ENTER)
                    print("adicionado Y1", nomeEscola)
                
                else:
                    time.sleep(3)
                    serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
                    serieSK.click()
                    serieSK.send_keys(Keys.CONTROL, "A")
                    serieSK.send_keys(Keys.DELETE)
                    serieSK.click()
                    serieSK.send_keys("SENIOR KINDERGARTEN 2025")
                    serieSK.send_keys(Keys.ENTER)
                    print("Adicionado SK", nomeEscola)
            except:
                print("A unidade não possui SK ou Year 1:", nomeEscola) 
                serieCurso.click()
                clicar1Item =   WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select")))      
                clicar1Item.click()'''
                
            # abrir a opção de selecionar o segmento
            campoSegmento = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//ng-select[@bindlabel='segmentName']//input"
                ))
            )
            campoSegmento.click()

            # clica no ELEMENTARY
            opcaoElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[@class='ng-option-label' and text()='Elementary']"
                ))
            )
            opcaoElementary.click()

            print("Segmento selecionado: Elementary")

            try:
                campoSerie = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//ng-select[@bindlabel='gradeName']//input"
                    ))
                )
                campoSerie.click()

                opcaoYear1 = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//span[@class='ng-option-label' and (text()='Year 01' or text()='Year 1')]"
                    ))
                )
                opcaoYear1.click()
                print("Série selecionada: Year 01")

            except TimeoutException:
                print("Year 01 NÃO encontrado. Alterando para Early Childhood...")

                #Caso não ache o Elementary ele procura o early
                campoSegmento = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//ng-select[@bindlabel='segmentName']//input"
                    ))
                )
                campoSegmento.click()

                opcaoEarly = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//span[@class='ng-option-label' and text()='Early Childhood']"
                    ))
                )
                opcaoEarly.click()
                print("Segmento selecionado: Early Childhood")

                #e seleciona o SK
                campoSerie = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//ng-select[@bindlabel='gradeName']//input"
                    ))
                )
                campoSerie.click()

                opcaoSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[@class='ng-option-label' and (text()='Senior Kindergarten' or text()='Senior Kinder')]"
                    ))
                )
                opcaoSK.click()

                print("Série selecionada: Senior Kindergarten")

            #Inserir código
            inserirCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[1]/input")))
            inserirCodigo.send_keys("SUPORTE2026")
            
            #inserir nome da turma
            inserirNomeTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[2]/input")))
            inserirNomeTurma.send_keys("SUPORTE LEX 2026")

            time.sleep(2)
            
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/seb-buttons-form-completion/div/button[2]/div")))
            clicarSalvar.click()
            
            time.sleep(5)
            print(nomeEscola, ": Criado Turma Suporte LEX 2025")

            #clica no botão "Entendi" após criação da turma

            botaoEntendi = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class,'btn-success') and normalize-space()='Entendi']"
                ))
            )
            botaoEntendi.click()

            print("Cliquei em Entendi!")
            time.sleep(2)

            #Entra novamente na turma, espera apágina recarregar para poder clicar na turma novamente
            
            turma_xpath = "//span[contains(text(), 'SUPORTE LEX 2026')]"

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, turma_xpath))
            )

            turma_temp = driver.find_element(By.XPATH, turma_xpath)

            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", turma_temp)
            time.sleep(2)

            turma = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, turma_xpath))
            )

            nomeTurma = turma.text

            turma.click()

            print("Turma encontrada:", nomeTurma)
            print("Turma já existe na Escola:", nomeEscola)

            time.sleep(2)

                #clica no botão inserir produto 
            adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-primary') and .//i[contains(text(),'add')]]")
                )
            )
            adicionarProduto.click()
            print("Janela de adicionar produto aberta.")
            time.sleep(2)

            #espera carregar a tabela
            modalAberto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.visibility_of_element_located((
                    (By.XPATH, "//div[contains(@class,'modal-dialog')]//table//tbody/tr")
                ))
            )

            #lcaliza o produto Toddle
            linhaToddle = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//td[normalize-space()='Toddle']/parent::tr"
                ))
            )

                #clica no produto Toddle
            botaoAddToddle = linhaToddle.find_element(By.XPATH, ".//button[contains(@class,'modal__add-button')]")
            botaoAddToddle.click()
            print("Toddle selecionado.")

        
            #clica em confirmar os produtos 
            btnAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//div[contains(@class,'modal-footer')]//button[contains(text(),'Adicionar')]"
                ))
            )
            btnAdicionar.click()

            time.sleep(2)

            #Adiciona os usuários
                
            timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "gabriela.santos@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "leticia.oliveira@dnx.tec.br", "yasmin.martins@maplebear.com.br", "toddle@maplebear.com.br"] 
                        # timeLexToddle 

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
                        time.sleep(2)   
                        inserirUsuariosTurma.send_keys(Keys.CONTROL,"A")
                        inserirUsuariosTurma.send_keys(Keys.DELETE)
                            
                        print("Usuário:", pessoa, "adicionado a turma!")
                            
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                        
                    else:
                        print(f"Erro ao adicionar o usuário {pessoa}")
                        errosEscolas.append(cardsEscolas)
                        
                            
                except:
                    continue

            time.sleep(3)
            
            botaoSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class,'button-add') and .//span[text()='Salvar']]"
                ))
            )
            botaoSalvar.click()
            print("Turma salva com sucesso!")

            #fecha e vai para a próxima
            WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.invisibility_of_element_located((
                    By.XPATH,
                    "//seb-edit-class"
                ))
            )

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
                                
def verificarTurmas(driver, cardsEscolas, arquivo):
    
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[69:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"


    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(5)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
        
        time.sleep(2)
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(1)
        
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
        codigoTurma.send_keys("SUPORTE2025")
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
                
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        
        else:
            print("Turma não cadastrada:", nomeEscola)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
            
def posicoesEscolas(driver):
    
    
    

    TIMEOUT_HOMEPAGE = 30

    # Espera até que os elementos estejam presentes
    WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cards-container__info"))
    )

    # Localiza os cards
    cardsEscolas = driver.find_elements(By.CSS_SELECTOR, "div.cards-container__info")

    # Remove itens indesejados
    cardsEscolas = cardsEscolas[1:-1]  
   
    # Itera e captura os nomes
    for index, escola in enumerate(cardsEscolas, start=1):  
        nomeEscola = escola.find_element(By.CSS_SELECTOR, "h3").text  
        print(f"{index} - {nomeEscola}")  

def adicionarUsuariosTurmas(driver, cardsEscolas,arquivo):
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[240:255] # Remove a escola Mapple bear demonstração e o card "Administrador"


    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(5)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(5)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(1)
        
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
        codigoTurma.send_keys("SUPORTE2025")
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        time.sleep(3)
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
        time.sleep(3)
        
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            time.sleep(2)
            clicarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div")))
            clicarTurma.click()
            
            time.sleep(1)
            
            
            timeLexToddle = ["washington.santos@sebsa.com.br"] 
                       # timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "fernanda.vieira@dnx.tec.br"] 
            
            for pessoa in timeLexToddle:
                
                try:
                    
                    if pessoa:
                        time.sleep(5)
                        inserirUsuariosTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                        inserirUsuariosTurma.click()
                        time.sleep(3)
                        inserirUsuariosTurma.send_keys(pessoa)
                        time.sleep(3)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        time.sleep(3)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        
                        time.sleep(5)
                        
                        selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input')))
                        selecionarPerfil.click()
                        #selecionarPerfil.send_keys("Coordenador")

                        selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]")))
                        selecionarPerfilCoordenador.click()
                        
                        time.sleep(5)
                        
                        adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                        adicionarUsuarios.click()
                        
                        print("Usuário:", pessoa, "adicionado a turma!")
                        
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                           
                except:
                    continue
                
            time.sleep(5)
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/seb-buttons-form-completion/div/button[2]")))
            time.sleep(5)
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
                                          
def cadastrarProdutos(driver, cardsEscolas, arquivo): #cadastrar Toddle
    
        with codecs.open(arquivo, "a","utf-8") as file:
            file.write(f"\n\nNova execução\n\n")
    
        TIMEOUT_HOMEPAGE = 30

        cardsEscolas = cardsEscolas[250:252] # Remove a escola Mapple bear demonstração e o card "Administrador"

        for escola in cardsEscolas:
            nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
            
            # Clica no card da escola
            escola.click()

            time.sleep(7)   # Delay necessário

            # Espera enconrar o card Administrador e clica
            cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
            
            if h3_element.text != "Administrador":
                print(f"{nomeEscola}, Sem acesso ao painel Administrador")
                with codecs.open(arquivo, "a","utf-8") as file:
                    file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
                continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

            cardAdministrador.click()

            time.sleep(8)

            novaAba = driver.window_handles[-1]
            driver.switch_to.window(novaAba)

            if driver.current_url == "about:blank":
                print("Página inválida detectada ('about:blank'). Fechando a aba.")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])    
                time.sleep(1)   # Delay necessário
            
            menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[2]/a"))) 
            menuCursos.click()

            time.sleep(7)

            UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
            UnidadesEscolher.click()
            
            unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
        
            filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
            filtrarAno.click()
            
            time.sleep(5)
            
            filtrar2026 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            filtrar2026.click()
            
            time.sleep(5)
            
            clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
            clicarFiltrar.click()
            
            time.sleep(10)
            
            clicarFiltrar.click()
            
            time.sleep(10)
            
            listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            
            quantidade_cursos = int(len(listaCursos))
            
            for i in range(1, quantidade_cursos):
            
                time.sleep(6)
                
                print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")

                listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

                curso = listaCursos[i]
                print(f"Clicando no curso {i}: {curso.text}")
                texto_do_curso = curso.text
                curso.click()

                adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[2]/div/button")))
                adicionarProduto.click()
                
                time.sleep(5)
                
                if "YEAR" in texto_do_curso:
                
                    buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                    # buscarProduto.send_keys("SLM+ / Toddle - Colaboradores")

                    # time.sleep(2)
                    
                    # clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                    # clicarAcao.click()
                    
                    # time.sleep(2)
                    
                    # buscarProduto.click()
                    # buscarProduto.send_keys(Keys.CONTROL, "A")
                    # buscarProduto.send_keys(Keys.DELETE)
                    buscarProduto.send_keys("Toddle")
                    
                    # time.sleep(2)
                    
                    # clicarAcao2 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div > div:nth-child(4) > div > button")))
                    # clicarAcao2.click()
                    # time.sleep(2)
                    
                    # buscarProduto.click()
                    # buscarProduto.send_keys(Keys.CONTROL, "A")
                    # buscarProduto.send_keys(Keys.DELETE)
                    # buscarProduto.send_keys("ÁRVORE - MAPLE BEAR")
                    
                else: 
                    buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                    # buscarProduto.send_keys("SLM+ / Toddle - Colaboradores - Early")
                    
                    # clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                    # clicarAcao.click()
                    
                    # buscarProduto.click()
                    # buscarProduto.send_keys(Keys.CONTROL, "A")
                    # buscarProduto.send_keys(Keys.DELETE)
                    buscarProduto.send_keys("Toddle")

                    time.sleep(5)
                try:
                    nomeProduto = driver.find_elements(By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content")
                    time.sleep(7)
                    
                    if nomeProduto[0].text == "Nenhum registro!":
                        
                        btnCancelarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[1]")))
                        btnCancelarProduto.click()
                        
                        time.sleep(5)
                        
                        btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                        btnCancelar.click()
                        
                        time.sleep(5)
                        
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                        
            
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2026 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2026.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                        
                        time.sleep(10)
                    else:
                        linhas = driver.find_elements(By.CSS_SELECTOR, "div.lex-table-row")

                        for linha in linhas:
                            try:
                                nome = linha.find_element(By.CSS_SELECTOR, "span.table-text").get_attribute("title").strip()
                            except:
                                continue

                            if nome == "Toddle":
                                print("Produto encontrado!")

                                botao = linha.find_element(By.CSS_SELECTOR, "button.js-action")
                                driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                                time.sleep(2)
                                botao.click()
                                print("Clique efetuado no botão correto!")
                                break
                        else:
                            print("Produto não encontrado!")

                        time.sleep(10)
                
                        clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[2]")))
                        clicarAdicionar.click()
                        
                        time.sleep(10)
                                                    
                                                    
                        salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-buttons-form-completion/div/button[2]")))
                        salvarCurso.click()
                    
                        time.sleep(5)
                        
                        print("Adicionado Toddle no", texto_do_curso, nomeEscola)
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        time.sleep(3)
                    
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                            
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2026 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2026.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                                            
                        time.sleep(3)
                
                except:
                    print("Erro na escola", nomeEscola)
                    
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
                
        
        '''   
                time.sleep(2)
                try:
                    
                    listaProdutos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
                    
                    for produto in listaProdutos:
                        
                    
                    if texto_produto == 'SLM+ / Toddle':
                        time.sleep(2)
                        
                        btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                        btnCancelar.click()
                        
                        time.sleep(5)
                        
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                        
                        time.sleep(4)
                        
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        time.sleep(5)
                
                        clicarFiltrar.click()
                        
                        print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                        
                        time.sleep(5)
                    
                    else:
                    
                        time.sleep(5)
                        
                        adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[2]/div/button")))
                        adicionarProduto.click()
                        
                        time.sleep(5)
                        
                        if "YEAR" in texto_do_curso:
                        
                            buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProduto.send_keys("SLM+ / Toddle - Colaboradores")

                            time.sleep(2)
                            
                            clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                            clicarAcao.click()
                            
                            buscarProduto.click()
                            buscarProduto.send_keys(Keys.CONTROL, "A")
                            buscarProduto.send_keys(Keys.DELETE)
                            buscarProduto.send_keys("ÁRVORE - MAPLE BEAR")
                            
                        else: 
                            buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProduto.send_keys("SLM+ / Toddle - Colaboradores - Early")

                            time.sleep(2)
                        
                        clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        clicarAcao.click()

                        time.sleep(5)
                        
                        clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[2]")))
                        clicarAdicionar.click()
                        
                        time.sleep(10)
                        
                        salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-buttons-form-completion/div/button[2]")))
                        salvarCurso.click()
                        
                        time.sleep(10)
                        
                        print("Adicionado Toddle no", texto_do_curso, nomeEscola)
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        time.sleep(10)
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                    
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        time.sleep(1)
                
                        clicarFiltrar.click()
                                    
                        time.sleep(3)
                except:
                    print("Erro na escola", nomeEscola)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
                '''
               
def cadastrarProdutos(driver, cardsEscolas, arquivo):#cadatrar pearson 
    
        with codecs.open(arquivo, "a","utf-8") as file:
            file.write(f"\n\nNova execução\n\n")
    
        TIMEOUT_HOMEPAGE = 30

        cardsEscolas = cardsEscolas[253:254] # Remove a escola Mapple bear demonstração e o card "Administrador"

        for escola in cardsEscolas:
            nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
            
            # Clica no card da escola
            escola.click()

            time.sleep(4)   # Delay necessário

            # Espera enconrar o card Administrador e clica
            cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
            
            if h3_element.text != "Administrador":
                print(f"{nomeEscola}, Sem acesso ao painel Administrador")
                with codecs.open(arquivo, "a","utf-8") as file:
                    file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
                continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

            cardAdministrador.click()

            time.sleep(4)

            novaAba = driver.window_handles[-1]
            driver.switch_to.window(novaAba)

            if driver.current_url == "about:blank":
                print("Página inválida detectada ('about:blank'). Fechando a aba.")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])    
                time.sleep(4)   # Delay necessário
            
            menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[2]/a"))) 
            menuCursos.click()

            time.sleep(4)

            UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
            UnidadesEscolher.click()
            
            unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
            
            time.sleep(2)
        
            filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
            filtrarAno.click()
                        
            filtrar2026 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            filtrar2026.click()
                        
            clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
            clicarFiltrar.click()
            
            time.sleep(5)
            
            clicarFiltrar.click()
            
            time.sleep(5)
            #aqui você insere os cursos que deseja que ele clique
            cursos_desejados = [
                "YEAR 1 2026",
                "YEAR 2 2026",
                "YEAR 3 2026",
                "YEAR 4 2026",
                "YEAR 5 2026",
                "YEAR 6 2026",
                "YEAR 7 2026",
                "YEAR 8 2026",
                "YEAR 9 2026"
            ]

            # Mostra uma lista com dos cursos que foram listados anteriomente quais tem na escola
            listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row'))
            )
            cursos_da_escola = []
            for c in listaCursos:
                linhas = c.text.strip().split("\n")
                for linha in linhas:
                    cursos_da_escola.append(linha.strip())

            # Filtra apenas os YEAR que realmente existem
            cursos_encontrados = []
            for desejado in cursos_desejados:
                for item in cursos_da_escola:
                    if desejado in item:
                        cursos_encontrados.append(desejado)
                        break

            # Se não tiver os cursos vai pular para a próxima escola
            if not cursos_encontrados:
                print(f"A escola {nomeEscola} não possui YEAR 2026. Pulando.")
                with codecs.open(arquivo, "a", "utf-8") as file:
                    file.write(f"{nomeEscola} - Nenhum curso YEAR disponível.\n")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                continue

            print(f"Cursos YEAR encontrados na escola {nomeEscola}: {cursos_encontrados}")

            # PROCESSAR CURSO POR CURSO
            for curso_nome in cursos_encontrados:

                # Atualiza a lista após cada retorno
                listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row'))
                )

                # Localiza o curso exato
                curso_elemento = None
                for c in listaCursos:
                    if curso_nome in c.text:
                        curso_elemento = c
                        break

                if not curso_elemento:
                    print(f"Não encontrei o curso {curso_nome}. Pulando.")
                    continue

                print(f"Clicando no curso YEAR: {curso_nome}")
                curso_elemento.click()
                time.sleep(3)

                # Abri tela para adicionar produto
                adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Adicionar produto')]/parent::button"))
                )
                adicionarProduto.click()
                time.sleep(3)

                # Selecionar produto
                linhas = driver.find_elements(By.CSS_SELECTOR, "div.lex-table-row")

                produto_encontrado = False

                for linha in linhas:
                # Captura todos os spans e divs da linha
                    textos_elementos = linha.find_elements(By.XPATH, ".//*[self::span or self::div]")
                    textos = [e.get_attribute("title") or e.text for e in textos_elementos]
                    textos = [t.strip() for t in textos if t]

                # Verifica se essa linha contém o produto desejado
                    if any("Pearson Resources" in t for t in textos):
        
        # Encontra o botão js-action dentro da linha
                        try:
                            botao = linha.find_element(
                                By.XPATH,
                                ".//button[contains(@class,'js-action')]"
                            )

                            driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                            time.sleep(2)
                            botao.click()

                            print("Clique no Pearson Resources efetuado!")

                        except Exception as e:
                            print(f"Erro ao clicar no botão do produto: {e}")
                        
                        produto_encontrado = True
                        break

                if not produto_encontrado:
                    print("Produto Pearson Resources não encontrado!")
                    cancelar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Cancelar')]"))
                    )
                    cancelar.click()
                    time.sleep(2)
                    voltar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-cancel"))
                    )
                    voltar.click()
                    continue

    # Confirmar adição
                clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Adicionar')]"))
                )
                clicarAdicionar.click()
                time.sleep(2)

    # Salvar curso
                try:
    # garante que a área onde o botão está já carregou
                    container = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.actions-section"))
                    )

    # localiza o botão "Salvar" corretamente
                    salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Salvar']]"))
                    )

    # rola para deixar o botão no centro da tela
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", salvarCurso)
                    time.sleep(2)

    # clica via JavaScript (mais confiável)
                    driver.execute_script("arguments[0].click();", salvarCurso)

                    print(" Botão SALVAR clicado com sucesso!")

                except Exception as e:
                    print(" Erro ao clicar no botão SALVAR:", e)
                    raise 
    # VOLTAR PARA A LISTA DE CURSOS DA ESCOLA
                time.sleep(4)

                UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                UnidadesEscolher.click()
                        
                time.sleep(3)
                    
                unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                if unidades:
                    for unidade in unidades:
                        if unidade.text == nomeEscola:
                            unidade.click()
                            break
                        else:
                            print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                            
                filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                filtrarAno.click()
                        
                filtrar2026 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                filtrar2026.click()
                        
                clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                clicarFiltrar.click()
                                            
                time.sleep(3)       
                    
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

def fazerTudoTurma(driver, cardsEscolas,arquivo):
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[240:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"


    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(5)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(1)
        
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
        codigoTurma.send_keys("SUPORTE2025")
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        time.sleep(3)
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
        time.sleep(3)
        
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            time.sleep(2)
            clicarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div")))
            clicarTurma.click()
            
            time.sleep(1)
            
            apagarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-class > form > div.page-content.fade-in-up > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > ng-select > div > div > div.ng-input > input[type=text]")))
            time.sleep(1)
            apagarCurso.click()
            time.sleep(1)
            apagarCurso.send_keys(Keys.BACKSPACE)
            
            time.sleep(1)
            
            btnSemCursoEntendi =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[8]/div/div/div/div[3]/button")))
            btnSemCursoEntendi.click()
            
            #Ano curso
            ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
            ano2025.send_keys("2025")
            ano2025.send_keys(Keys.ENTER)
            
            #Preenche Segmento e Série
            
            try:
                
                segmentoElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/div/div/div[2]/input")))
                segmentoElementary.click
                segmentoElementary.send_keys("Elementary")
                
                time.sleep(1)
                
                serieElementary1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div")
                
                if serieElementary1:
                    
                    time.sleep(1)
                    segmentoElementary.send_keys(Keys.ENTER)
                    time.sleep(2)
                    serieEntendi = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[4]/div/div/div/div[3]/button")))
                    serieEntendi.click()
                    time.sleep(2)
                    
                    seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                    time.sleep(2)
                    #seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    #seriecurso1.click()
                    seriecurso1.send_keys("Year 01")
                    time.sleep(2)
                    seriecurso1.send_keys(Keys.ENTER)
                    
                    serieEntendiCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[5]/div/div/div/div[3]/button")))
                    time.sleep(5)
                    serieEntendiCurso.click()
                    time.sleep(2)
                    print("Adicionado Year 1", nomeEscola)
                    
                    # serieCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    # serieCurso.send_keys("Year 01")
                    # serieCurso.send_keys(Keys.ENTER)

                
                else:
                    time.sleep(1)
                    segmentoElementary.send_keys(Keys.CONTROL,"A")
                    segmentoElementary.send_keys(Keys.DELETE)
                    segmentoElementary.send_keys("Early")
                    segmentoElementary.send_keys(Keys.ENTER)
                    
                    serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                    serieSK.send_keys("SENIOR KINDERGARTEN")
                    serieSK.send_keys(Keys.ENTER)
                    print("Adicionado SK", nomeEscola)
                    
                    
            except:
                print("Deu erro na escola", nomeEscola, cardsEscolas) 
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                
            
            btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
            btnAddProduto.click()
            
            produtos = ["SLM+ / Toddle - Família e Alunos", "SLM+ / Toddle - Colaboradores", "ÁRVORE - MAPLE BEAR","Plataforma de Excelência Maple Bear"]
            
            for produto in produtos:
            
                buscarProdutoTurma =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/div[1]/div[1]/div/input")))
                buscarProdutoTurma.send_keys(produto)
                
                btnAddProdutoBuscar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/table/tbody/tr/td[4]/button")))
                btnAddProdutoBuscar.click()
                
                buscarProdutoTurma.click()
                buscarProdutoTurma.send_keys(Keys.CONTROL,"A")
                buscarProdutoTurma.send_keys(Keys.DELETE)
                
                print("Adicionado produto: ", produto)
                
                time.sleep(1)
            
            btnAdicionarTodosProdutos =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[3]/button[2]")))
            btnAdicionarTodosProdutos.click()
            
            time.sleep(3)
                
            timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "fernanda.vieira@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "toddle@maplebear.com.br"] 
            
            for pessoa in timeLexToddle:
                
                try:
                    
                    if pessoa:
                        time.sleep(2)
                        inserirUsuariosTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                        inserirUsuariosTurma.click()
                        inserirUsuariosTurma.send_keys(pessoa)
                        time.sleep(2)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        
                        time.sleep(1)
                        
                        selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input')))
                        selecionarPerfil.click()
                        #selecionarPerfil.send_keys("Coordenador")

                        selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]")))
                        selecionarPerfilCoordenador.click()
                        
                        time.sleep(1)
                        
                        adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                        adicionarUsuarios.click()
                        
                        print("Usuário:", pessoa, "adicionado a turma!")
                        
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                    
                    else:
                        print(f"Erro ao adicionar o usuário {pessoa}")
                    
                        
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
            
            criarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-titlebar/div/div/div[2]/div/lex-button/button")))
            criarTurma.click()
            
            time.sleep(1)
            
            UnidadesTeste = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/div")))
            UnidadesTeste.click()
            
            unidades = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
            
            #Ano curso
            ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
            ano2025.send_keys("2025")
            ano2025.send_keys(Keys.ENTER)
                
            #Inserir código
            inserirCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[1]/input")))
            inserirCodigo.send_keys("SUPORTE2025")
            
            #inserir nome da turma
            inserirNomeTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[2]/input")))
            inserirNomeTurma.send_keys("SUPORTE LEX 2025")

            try:
                
                segmentoElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/div/div/div[2]/input")))
                segmentoElementary.click
                segmentoElementary.send_keys("Elementary")
                
                time.sleep(1)
                
                serieElementary1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div")
                
                if serieElementary1:
                
                    segmentoElementary.send_keys(Keys.ENTER)
                    serieEntendi = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[4]/div/div/div/div[3]/button")))
                    serieEntendi.click()
                    
                    seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                   
                    #seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    #seriecurso1.click()
                    seriecurso1.send_keys("Year 01")
                    seriecurso1.send_keys(Keys.ENTER)
                    
                    # serieCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    # serieCurso.send_keys("Year 01")
                    # serieCurso.send_keys(Keys.ENTER)
                    
                    serieEntendiCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[4]/div/div/div/div[3]/button")))
                    time.sleep(2)
                    serieEntendiCurso.click()
                    
                    btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                    btnAddProduto.click()
                    
                    produtos = ["SLM+ / Toddle - Família e Alunos", "SLM+ / Toddle - Colaboradores", "ÁRVORE - MAPLE BEAR","Plataforma de Excelência Maple Bear"]
                    
                    try:
                        for produto in produtos:
                        
                            buscarProdutoTurma =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProdutoTurma.send_keys(produto)
                            
                            btnAddProdutoBuscar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/table/tbody/tr/td[4]/button")))
                            btnAddProdutoBuscar.click()
                            
                            buscarProdutoTurma.click()
                            
                            print("Adicionado produto: ", produto)
                            
                            time.sleep(1)
                        
                            btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                            btnAddProduto.click()
                    except (TimeoutException) as e:
                        print(f"Não foi possível adicionar o produto: {produto}. Erro: {e}")
                
                else:
                    time.sleep(1)
                    segmentoElementary.send_keys(Keys.CONTROL,"A")
                    segmentoElementary.send_keys(Keys.DELETE)
                    segmentoElementary.send_keys("Early")
                    segmentoElementary.send_keys(Keys.ENTER)
                    
                    serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                    serieSK.send_keys("SENIOR KINDERGARTEN")
                    serieSK.send_keys(Keys.ENTER)
                    print("Adicionado SK", nomeEscola)
                    
                    btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                    btnAddProduto.click()
                    
                    produtos = ["SLM+ / Toddle - Colaboradores - Early", "SLM+ / Toddle - Família e Alunos - Early","Plataforma de Excelência Maple Bear"]
                    
                    try:
                    
                        for produto in produtos:
                        
                            buscarProdutoTurma =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProdutoTurma.send_keys(produto)
                            
                            btnAddProdutoBuscar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/table/tbody/tr/td[4]/button")))
                            btnAddProdutoBuscar.click()
                            
                            buscarProdutoTurma.click()
                            
                            print("Adicionado produto: ", produto)
                        
                            btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                            btnAddProduto.click()
                            
                    except (TimeoutException) as e:
                        print(f"Não foi possível adicionar o produto: {produto}. Erro: {e}") 
                        
                time.sleep(1)
                
            except:
                print("A unidade não possui SK ou Year 1:", nomeEscola) 
                clicar1Item =   WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select")))      
                clicar1Item.click()
            
                btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                btnAddProduto.click()
                       
            time.sleep(3)
                
            timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "fernanda.vieira@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "toddle@maplebear.com.br"] 
            
            for pessoa in timeLexToddle:
                
                try:
                    
                    if pessoa:
                        time.sleep(2)
                        inserirUsuariosTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                        inserirUsuariosTurma.click()
                        inserirUsuariosTurma.send_keys(pessoa)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        
                        time.sleep(1)
                        
                        selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input')))
                        selecionarPerfil.click()
                        #selecionarPerfil.send_keys("Coordenador")

                        selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]")))
                        selecionarPerfilCoordenador.click()
                        
                        time.sleep(1)
                        
                        adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                        adicionarUsuarios.click()
                        
                        print("Usuário:", pessoa, "adicionado a turma!")
                        
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                    
                    else:
                        print(f"Erro ao adicionar o usuário {pessoa}")
                    
                        
                except:
                    continue
            
            time.sleep(1)
            
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/seb-buttons-form-completion/div/button[2]/div")))
            time.sleep(1)
            clicarSalvar.click()
            
            time.sleep(5)
            print(nomeEscola, ": Turma Atualizada para 2025")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
                              
def cadastrarProdutosTodos(driver, cardsEscolas, arquivo):#cadastrar produtos em todas os cursos
    
    with codecs.open(arquivo, "a","utf-8") as file:
            file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[250:255] # Remove a escola Mapple bear demonstração e o card "Administrador"

    for escola in cardsEscolas:
            nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
            
            # Clica no card da escola
            escola.click()

            time.sleep(3)   # Delay necessário

            # Espera enconrar o card Administrador e clica
            cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
            
            if h3_element.text != "Administrador":
                print(f"{nomeEscola}, Sem acesso ao painel Administrador")
                with codecs.open(arquivo, "a","utf-8") as file:
                    file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
                continue    # Pular o codigo abaixo, pois a escola não possui o card administrador
            
            time.sleep(10)

            cardAdministrador.click()

            time.sleep(5)

            novaAba = driver.window_handles[-1]
            driver.switch_to.window(novaAba)
            
            if driver.current_url == "about:blank":
                print("Página inválida detectada ('about:blank'). Fechando a aba.")
                driver.close()  # Fecha a aba inválida

                # Verifica se ainda existem outras abas abertas
                if driver.window_handles:
                    driver.switch_to.window(driver.window_handles[0])  # Troca para a aba inicial
                    time.sleep(1)  # Pequeno delay para garantir que o foco mude corretamente

            # if driver.current_url == "about:blank":
            #     print("Página inválida detectada ('about:blank'). Fechando a aba.")
            #     driver.close()
            #     driver.switch_to.window(driver.window_handles[0])    
            #     time.sleep(1)   # Delay necessário
            
            menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[2]/a"))) 
            menuCursos.click()

            time.sleep(3)

            UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
            UnidadesEscolher.click()
            
            unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
            
            
            filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]/input")))
            filtrarAno.send_keys("2026")
            filtrarAno.send_keys(Keys.ENTER)
            
            time.sleep(2)
            filtrarAno.send_keys(Keys.ENTER)

            time.sleep(2)
            
            clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
            clicarFiltrar.click()
            
            time.sleep(5)  
            clicarFiltrar.click()    
              
            listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            
            quantidade_cursos = int(len(listaCursos))
            
            for i in range(1, quantidade_cursos):
            
                time.sleep(2)
                
                print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")

                listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

                curso = listaCursos[i]
                print(f"Clicando no curso {i}: {curso.text}")
                texto_do_curso = curso.text
                texto_normalizado = texto_do_curso.replace("\n", " ").strip()
                curso.click()

                adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Adicionar produto']]")))
                adicionarProduto.click()
                
                time.sleep(3)

                cursosearly = ["BEAR CARE 2026", "TODDLER 2026", "NURSERY 2026", "JUNIOR KINDERGARTEN 2026","SENIOR KINDERGARTEN 2026"]
                cursosfundamental1 = ["YEAR 1 2026", "YEAR 2 2026", "YEAR 3 2026", "YEAR 4 2026","YEAR 5 2026"]
                cursosfundamental2hs = ["YEAR 6 2026","YEAR 7 2026", "YEAR 8 2026", "YEAR 9 2026","YEAR 10 2026", "YEAR 11 2026", "YEAR 12 2026"]
                
                if any(curso in texto_normalizado for curso in cursosearly):
                    produtos_para_adicionar = [
                        "Árvore Early Childhood",
                        "Britannica Escola - Colaboradores",
                        "Britannica School - Colaboradores"
                    ]

                elif any(curso in texto_normalizado for curso in cursosfundamental1):
                    produtos_para_adicionar = [
                        "Britannica Escola - Colaboradores",
                        "Britannica School - Colaboradores",
                        "Árvore"
                    ]

                elif any(curso in texto_normalizado for curso in cursosfundamental2hs):
                    produtos_para_adicionar = [
                        "Britannica Escola - Colaboradores",
                        "Britannica School - Colaboradores",
                        "Árvore",
                        "Britannica School - Alunos",
                        "Britannica Escola - Alunos"
                    ]

                else:
                    produtos_para_adicionar = []

                for produto in produtos_para_adicionar:
                    print("Tentando adicionar produto:", produto)

                    buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input"
                        ))
                    )
                    buscarProduto.clear()
                    buscarProduto.send_keys(produto)

                    time.sleep(2)

                    clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            f"//div[contains(@class,'lex-table-row')][.//span[normalize-space()='{produto}']]//button[contains(@class,'js-action')]"
                        ))
                    )
                    clicarAcao.click()

                    time.sleep(2)
                         
                try:
                    nomeProduto = driver.find_elements(By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content")
                    time.sleep(3)
                    
                    if nomeProduto[0].text == "Nenhum registro!":
                        
                        btnCancelarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[1]")))
                        btnCancelarProduto.click()
                        
                        time.sleep(2)
                        
                        btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                        btnCancelar.click()
                        
                        time.sleep(5)

                        
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")   
                                
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2026 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2026.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        time.sleep(2)
                        clicarFiltrar.click()
                        print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                        
                        time.sleep(5)
                    else:
                        
                        clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[2]")))
                        clicarAdicionar.click()
                        
                        time.sleep(5)
                                                                       
                        salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-buttons-form-completion/div/button[2]")))
                        salvarCurso.click()
                    
                        time.sleep(10)
                        
                        print("Adicionado Produto no", texto_do_curso, nomeEscola)
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        time.sleep(3)
                    
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")                     
                        
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2026 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2026.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                                            
                        time.sleep(3)
                
                except:
                    print("Erro na escola", nomeEscola)
                    
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

    if len(driver.window_handles) > 1:
        driver.close()
        first_tab = driver.window_handles[0]
        driver.switch_to.window(first_tab)  
            
def inativarUsuario(driver,cardsEscolas,arquivo):
    
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 50

    cardsEscolas = [cardsEscolas[i] for i in [190, 191, 192] if i < len(cardsEscolas)]# Remove a escola Mapple bear demonstração e o card "Administrador"
    
    time.sleep(3)

    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(5)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(2)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        time.sleep(2)   # Delay necessário
          
        menuUsuario = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[5]/a"))) 
        menuUsuario.click()

        usuariosInativar = ["388.176.278-79"] #falta o luiz "451.662.058-80" , "397.194.908-88", "400.520.268-33", "329.729.308-00")
        
        for usuarios in usuariosInativar:
                
            inputCPF = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-list-filter-user/form/div[1]/div[1]/input"))) 
            inputCPF.send_keys(Keys.CONTROL + "A")
            inputCPF.send_keys(Keys.DELETE)
            time.sleep(1) 
            
            inputCPF.send_keys(usuarios)
            time.sleep(2)
            inputCPF.send_keys(Keys.ENTER)
            
            time.sleep(3)

            usuario_existe = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            
            time.sleep(3)
        
            if len(usuario_existe) == 2:
                
                time.sleep(2)
                
                cadastroUsuario = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-lex-table/div[2]/div[2]/div")))         
                cadastroUsuario.click()
                
                time.sleep(5)
                
                usuarioAtivo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-user/form/div[1]/label/span"))) 
                usuarioAtivo.click()

                notificacaoInativar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-user/seb-modal-warning/div/div/div/div[3]/button[2]"))) 
                time.sleep(1)
                notificacaoInativar.click()

                salvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[7]/div/seb-buttons-form-completion/div/button[2]/div/span"))) 
                salvar.click()
                
                time.sleep(10)
                
                print(f"{nomeEscola}, Usuário inativado ")

            
            else:  
                
                time.sleep(2)
                    
                print(f"{nomeEscola}, Usuário não existe")
                inputCPF.send_keys(Keys.CONTROL + "A")
                inputCPF.send_keys(Keys.DELETE)
                
                time.sleep(2)
                
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1) 

  
                
if __name__ == "__main__":
    
    driver = webdriver.Chrome()

    login(driver)
    dismissCompletarCadastr(driver)
    cardsEscolas = pegarEscolas(driver)
    #posicoesEscolas(driver) #verifica a posiçao das escolas
    inativarUsuario(driver, cardsEscolas,"cursosBC25.txt")
    #cadastrarProdutosTodos(driver,cardsEscolas,"cursosBC25.txt")
    #fazerTudoTurma(driver,cardsEscolas,"cursosBC25.txt")
    #adicionarUsuariosTurmas(driver, cardsEscolas, "cursosBC25.txt")
    #cadastrarTurmas(driver, cardsEscolas, "cursosBC25.txt") #cadastra turmas
    #cadastrarProdutos(driver, cardsEscolas, "cursosBC25.txt")
    #cadastrarProdutos(driver, cardsEscolas, "cursosBC25.txt")
    #posicoesEscolas(driver) #verifica a posiçao das escolas
    #verificarTurmas(driver, cardsEscolas,"cursos2025.txt" )
    #pegarCursos2026(driver,cardsEscolas,"cursos2025.txt")
    #pegarCNPJ(driver, cardsEscolas, "cnpjs2025.txt")

    
    
