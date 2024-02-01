from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
import easyocr

# Configuração do WebDriver Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Caminho para o executável do Chrome
driver_path = r'"C:\Users\BINHO\Downloads\chrome-win64\chrome-win64\chrome.exe"'

# Navega até a página desejada
driver.get("http://gps.receita.fazenda.gov.br/")

# Localiza o elemento captcha
capturarImage = driver.find_element(By.XPATH, '//*[@id="captcha_challenge"]')

# Inicializa variáveis
capitBool = False

while capitBool is not True:
    try:
        # Captura a imagem e salva
        capturaImagesave = driver.execute_async_script("""
            var ele = arguments[0], callback = arguments[1];
            ele.addEventListener('load', function fn(){
                ele.removeEventListener('load', fn, false);
                var cnv = document.createElement('canvas');
                cnv.width = this.width; cnv.height = this.height;
                cnv.getContext('2d').drawImage(this, 0, 0);
                callback(cnv.toDataURL('image/jpeg').substring(22));
            }, false);
            ele.dispatchEvent(new Event('load'));
        """, capturarImage)

        # Escreve a imagem em um arquivo
        with open(r'capiturar.jpg', 'wb') as f:
            f.write(base64.b64decode(capturaImagesave))

        # Usa o EasyOCR para ler o texto da imagem
        reader = easyocr.Reader(['en'])
        result = reader.readtext('capiturar.lpg')

        # Itera sobre os resultados do OCR
        for x in result:
            capitResultado = x[1]

            # Preenche o campo de resposta captcha
            driver.find_element(By.XPATH, '//*[@id="captcha_campo_resposta"]').send_keys(capitResultado)

            # Clica no botão de consulta
            driver.find_element(By.XPATH, '//*[@id="formInicio:botaoConsultar"]').click()

    except Exception as e:
        print(f"Tentando acertar o captcha - Erro: {e}")