from module import mysql, re, load_dotenv, os

class Database:
        
        def __init__(self):
                self.conecta_bd()
                self.montarTabela()


        def conecta_bd(self):
                
                self.conn = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD')
                )
                self.cursor = self.conn.cursor()
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(os.getenv('DB_NAME')))
                self.conn.database = os.getenv('DB_NAME')

                print('Conectando ao banco de dados')

        def desconecta_bd(self):
            self.conn.close()
            print('Desconectando ao banco de dados')

        def montarTabela(self):
           
            self.acoes_info = self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS acoes_info (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    ticker VARCHAR(10) NOT NULL,
                    precoAtual DECIMAL(10, 2) NOT NULL,
                    dividendYield VARCHAR(10),
                    ultimoDividendo DECIMAL(10, 2),
                    precoMin12m DECIMAL(10, 2),
                    precoMax12m DECIMAL(10, 2),
                    oscilacaoDia VARCHAR(10),
                    oscilacaoAno VARCHAR(10),
                    cnpj VARCHAR(20),
                    logo VARCHAR(255),
                    siteRI VARCHAR(255));
                    """
            )

            self.conn.commit()
            print('Bando de dados criado')
            self.desconecta_bd()

        def validar_dados(self, dados):
            obrigatorios = ['ticker', 'precoAtual']
            for campo in obrigatorios:
                if campo not in dados:
                    raise ValueError(f"Campo obrigatório '{campo}' está ausente.")

            if not isinstance(dados['ticker'], str):
                raise TypeError("O campo 'ticker' deve ser uma string.")
            if not isinstance(dados['precoAtual'], (int, float)):
                raise TypeError("O campo 'precoAtual' deve ser um número.")

            if 'cnpj' in dados and dados['cnpj']:
                cnpj_pattern = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$|^\d{14}$'
                if not re.match(cnpj_pattern, dados['cnpj']):
                    raise ValueError("CNPJ inválido.")

            if 'siteRI' in dados and dados['siteRI']:
                if not re.match(r'^https?://', dados['siteRI']):
                    raise ValueError("URL do site de RI inválida.")

        def inserir_acao(self, dados):
            try:
                self.validar_dados(dados)
                self.conecta_bd()

                query = """
                    INSERT INTO acoes_info (
                        ticker, precoAtual, dividendYield, ultimoDividendo,
                        precoMin12m, precoMax12m, oscilacaoDia, oscilacaoAno,
                        cnpj, logo, siteRI
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                valores = (
                    dados.get('ticker'),
                    dados.get('precoAtual'),
                    dados.get('dividendYield'),
                    dados.get('ultimoDividendo'),
                    dados.get('precoMin12m'),
                    dados.get('precoMax12m'),
                    dados.get('oscilacaoDia'),
                    dados.get('oscilacaoAno'),
                    dados.get('cnpj'),
                    dados.get('logo'),
                    dados.get('siteRI'),
                )

                self.cursor.execute(query, valores)
                self.conn.commit()

                return {"status": "sucesso", "mensagem": "Ação inserida com sucesso"}
            except (ValueError, TypeError) as e:
                return {"status": "erro", "mensagem": str(e)}
            except mysql.connector.Error as err:
                return {"status": "erro", "mensagem": f"Erro no banco de dados: {err}"}
            except Exception as e:
                return {"status": "erro", "mensagem": f"Erro inesperado: {e}"}
            finally:
                self.desconecta_bd()

        def get_all(self):
            try:
                self.conecta_bd()

                self.cursor.execute("SELECT * FROM acoes_info")
                resultados = self.cursor.fetchall()

                colunas = [col[0] for col in self.cursor.description]
                dados = [dict(zip(colunas, linha)) for linha in resultados]

                return {"status": "sucesso", "dados": dados}
            except mysql.connector.Error as err:
                return {"status": "erro", "mensagem": f"Erro ao buscar dados: {err}"}
            finally:
                self.desconecta_bd()


        def get_acao(self, ticker):
            try:
                self.conecta_bd()

                self.cursor.execute("SELECT * FROM acoes_info WHERE ticker = %s", (ticker,))
                resultado = self.cursor.fetchone()

                if resultado:
                    colunas = [col[0] for col in self.cursor.description]
                    dado = dict(zip(colunas, resultado))
                    return {"status": "sucesso", "dados": dado}
                else:
                    return {"status": "erro", "mensagem": f"Ação com ticker '{ticker}' não encontrada."}
            except mysql.connector.Error as err:
                return {"status": "erro", "mensagem": f"Erro ao buscar dado: {err}"}
            finally:
                self.desconecta_bd()
