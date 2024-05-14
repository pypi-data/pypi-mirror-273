import pika
import threading
import typing
import logging
import os
import signal
import time


class Rabbit():
    def __init__(self, host: str, port: int, virtualhost: str, username: str, password: str, reconnect: bool = False, reconnect_delay: int = 300, continue_execution: bool = False):
        '''
        Metodo de comunicação com o rabbit nele pode ser encontrado métodos como:
            getMessages(Capturar as mensagens de uma fila )
            postMessage(Enviar mensagem para uma fila)
            close_connection(Metodo utilizado para fechar a conexão)
        Existem os parametros basicos que devem ser fornecidos como host,port,etc, mas existem demais parametros:
            reconnect: bool = False:
                Se deseja que o fluxo faça um reconnect automatico em alguns casos para se recuperar de erros.
            reconnect_delay: int = 300:
                Quanto tempo em segundos deseja que ele tenta ficar se reconectando.
            continue_execution: bool = False
                Se deseja que a execução codigo continue após a conexão ser estabelecida, caso for definida como True, 
                    a reconexão em caso de falha não será possivel.
        '''
        self.host: str = host
        self.port: int = port
        self.virtualhost: str = virtualhost
        self.username: str = username
        self.password: str = password
        self.channel = None
        self.consume_thread = None
        self.SelectConn = None
        self.confirmed_messages = set()
        self.reconnect: bool = reconnect
        self.reconnect_delay_client: int = reconnect_delay
        self.reconnect_delay_system: int = reconnect_delay
        self.qtd_reconnects: int = 0
        self.continue_execution: bool = continue_execution

    def getMessages(self, queue: str, exchange: str, message_handler: typing.Callable, limit_get_messages: int) -> None:
        '''
            Get messages the queue!
            Recived: 
                queue - queue to get messages
                message_handler - method executed after having each message
                limit_get_messages - number of messages that will be taken from the queue
        '''
        while (True):
            if not callable(message_handler):
                raise TypeError(
                    "Necessary implemention the message_handler must be a callable function")

            if not queue:
                raise ValueError("Queue parameter is mandatory")

            try:
                if exchange is None or exchange.strip() == '':
                    exchange = self.virtualhost

                if not self.__is_connected():
                    self.__connect()

                if not bool(limit_get_messages):
                    limit_get_messages = 1
                self.__receive_message(
                    queue, exchange, message_handler, limit_get_messages)

                if self.continue_execution:
                    break
            except pika.exceptions.AMQPConnectionError:
                logging.error("Connection was closed, retrying...")
                continue
            except pika.exceptions.StreamLostError:
                logging.error("The stream was lost, retrying...")
                continue
            except ConnectionResetError:
                logging.error("Connection was reset, retrying...")
                continue
            except pika.exceptions.AMQPChannelError as err:
                logging.error(
                    "Caught a channel error: {}, stopping...".format(err))
                self.reconnect = False
                break
            except KeyboardInterrupt:
                self.reconnect = False
                break
            except Exception as e:
                logging.error(
                    "Error receiving message from rabbit: {} ".format(e).encode('ascii', 'ignore'), stack_info=True)
                self.reconnect = False
                break
            finally:
                if not self.continue_execution:
                    if self.reconnect:
                        if self.qtd_reconnects >= 10 and self.qtd_reconnects < 30:
                            self.reconnect_delay_system = 3600
                        elif self.qtd_reconnects >= 30 and self.qtd_reconnects <= 50:
                            self.reconnect_delay_system = 7200
                        else:
                            self.reconnect = False

                        if self.qtd_reconnects >= 10:
                            logging.info(
                                f'Passou de {self.qtd_reconnects} reconexões, irá aguardar {str(self.reconnect_delay_system)} segundos para tentar uma nova reconexão!')

                        time.sleep(self.reconnect_delay_system)
                        self.qtd_reconnects += 1
                        print(
                            f'Quantidade de reconexões: {str(self.qtd_reconnects)}')
                    else:
                        self.channel.stop_consuming()
                        if self.SelectConn.is_open:
                            self.SelectConn.close()
                        os.kill(os.getpid(), signal.SIGINT)
                        break

    def postMessage(self, queue: str, exchange: str, message: str) -> bool:
        '''
            Send messages the rabbit
        '''
        if not queue:
            raise ValueError("Queue parameter is mandatory")
        try:

            if exchange is None or exchange.strip() == '':
                exchange = self.virtualhost

            if not self.__is_connected():
                self.__connect()
            return self.__send_message(queue, exchange, message)

        except Exception as e:
            logging.error(
                f"Error the send message to rabbit: {str(e)} ", stack_info=True)

    def __is_connected(self) -> bool:
        """
            Returns True if the RabbitMQ connection is established, otherwise False.
        """
        if self.channel and not self.channel.is_closed:
            return True
        return False

    def __connect(self) -> None:
        # Create a credentials object with the provided username and password
        credentials = pika.PlainCredentials(self.username, self.password)
        # Create a connection parameters object with the provided host, port, and credentials
        parameters = pika.ConnectionParameters(
            self.host, self.port, self.virtualhost, credentials)
        # Create a SelectConnection with the provided parameters and a callback method to handle the established connection
        self.SelectConn = pika.BlockingConnection(parameters)
        # Start the connection's I/O loop in a separate thread
        self.channel = self.SelectConn.channel()
        if not self.channel.is_closed and self.qtd_reconnects > 0:
            self.qtd_reconnects = 0
            self.reconnect_delay_system = self.reconnect_delay_client

    def __send_message(self, queue: str, exchange: str, message: str) -> bool:
        '''
            Send messages the rabbit
        '''
        if not queue:
            raise ValueError("Queue parameter is mandatory")
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.queue_bind(
                queue=queue, exchange=exchange, routing_key=queue)
            self.channel.basic_publish(
                exchange=exchange, routing_key=queue, body=message)

            return True
        except Exception as e:
            logging.error(
                f"Error the send message to rabbbit: {str(e)} ", stack_info=True)
            return False

    def __receive_message(self, queue: str, exchange: str, message_handler: typing.Callable, limit_get_messages: int) -> None:
        '''
            Connect the rabbit consume messages the queue and return message in the method "process_message"
            Recived: 
                queue - queue to get messages
                message_handler - method executed after having each message
                limit_get_messages - number of messages that will be taken from the queue
        '''
        def callback(ch, method, properties, body):
            message_handler(ch, method, properties, body)

        self.channel.basic_qos(prefetch_count=limit_get_messages)
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(
            queue=queue, exchange=exchange, routing_key=queue)
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=False)

        if self.continue_execution:
            self.consume_thread = threading.Thread(
                target=self.channel.start_consuming)
            self.consume_thread.start()
        else:
            self.channel.start_consuming()

    def close_connection(self):
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
        except Exception as e:
            logging.error(
                f"Error closing connection: {str(e)} ", stack_info=True)
