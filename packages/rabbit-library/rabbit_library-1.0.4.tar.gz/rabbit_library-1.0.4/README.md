# Biblioteca para trabalhar com o Rabbit
- Ao instanciar a classe do Rabbit já deve ser passado os parametros de conexão e de reconexão se assim desejar.
    - Os parametros de conexão são:
        - host, port, virtualhost, username e password
    - Os parametros opcionais são:
        - reconnect: bool = False
            - Se deseja que o fluxo faça um reconnect automatico em alguns casos para se recuperar de erros.
        - reconnect_delay: int = 300
            - Quanto tempo em segundos deseja que ele tenta ficar se reconectando.
            - Valor default se nao informado é 300
        - continue_execution: bool = False
            - Se deseja que a execução codigo continue após a conexão ser estabelecida, caso for definida como True, a reconexão em caso de falha não será possivel.
        
- Nesta biblioteca pode ser encontrado os metodos:
    - getMessages
        - Pegar as mensagens de uma fila e passa a mesma para a função de callback passada para a função getMessages, exemplo:
        ````
            class example():
                def process_message(self, channel, method, properties, body):
                    pass
                def example(self):
                    self.queue.getMessages('name_queue', 'name_exchange', self.process_message, 1)
        ````
        - Parametros:
            - queue: str
                - Nome da fila que ficará escutando para ler as mensagens.
            - exchange: str
                - Nome da exchange que a fila está vinculada.
            - message_handler: typing.Callable
                - Função de processamento da mensagem recebida, serve para fazer o processamento da mensagem que está entrando na fila.
            - limit_get_messages: int
                - Quantidade de mensagens que deseja pegar por vez do rabbit, por padrão se nao informada será atribuido 1.
    - postMessage
        - Enviar uma mensagem para uma fila do rabbit.
        - Parametros:
            - queue: str
                - Nome da fila que será colocado a mensagem.
            - exchange: str
                - Nome da exchange que a fila está vinculada.
            - message: str
                - Conteúdo da mensagem que será colocado na fila.
    - close_connection
        - Realizar o fechamento da conexão com o rabbit.
# Requerimentos(DEV):
- Para poder iniciar é preciso ter instalado as dependências abaixo:
    - [Python](https://www.python.org/)
    - [Pip](https://pip.pypa.io/)
    - [Poetry](https://poetry.eustace.io/)
    - [Git](https://git-scm.com/)
    - [poethepoet](https://github.com/nat-n/poethepoet)
# Como montar a biblioteca e fazer uploud para o pypi.org
- Video de auxlilio pode ser encontrado [aqui](https://youtu.be/YpTuuGBggcE?t=828)
- Url da [biblioteca do pypi](https://pypi.org/project/rabbit-library/).
- O arquivo de LICENCE é necessário para dizer de quem é esta biblioteca, alterar de acordo com as regras e necessidade.
- Como estamos utilizando o poetry é muito simples para fazer o build e uploud para o pipy:
``` poetry publish --build -u USERNAME -p PASSWORD ```

# Testes
- Todos os testes foram desenvolvidos com o pytest, para executar os mesmos pode ser executado o comando ```poetry run coverage run -m pytest``` ou se caso tenha instalado o [poethepoet](https://github.com/nat-n/poethepoet) pode ser executado ```poe cove_tests```