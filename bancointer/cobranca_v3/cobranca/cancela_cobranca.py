# recupera_cobranca.py
from bancointer.utils.ambient import Ambient
from bancointer.utils.constants import PATH_COBRANCAS, HOST_SANDBOX, HOST
from bancointer.utils.exceptions import BancoInterException, Erro, ErroApi
from bancointer.utils.http_utils import HttpUtils


class CancelaCobranca(object):
    def __init__(self, ambiente: Ambient, client_id, client_secret, cert):
        """Metodo construtor da classe.

        Args:
            client_id (str): Client Id obtido no detalhe da tela de aplicações no IB.
            client_secret (str): Client Secret obtido no detalhe da tela de aplicações no IB.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert
        self.http_util = HttpUtils(
            HOST_SANDBOX if ambiente.SANDBOX else HOST, client_id, client_secret, cert
        )
        print(f"AMBIENTE: {ambiente.value}")

    def cancelar(self, codigo_solicitacao, motivo_cancelamento):
        """Cancela uma cobrança emitida atraves do seu `codigo_solicitacao`.

        Args:
            codigo_solicitacao (string <uuid>): Codigo unico da cobrança.
            motivo_cancelamento (string): Motivo pelo qual a cobrança está sendo cancelada.

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados do boleto.
        """

        path = f"{PATH_COBRANCAS}/{codigo_solicitacao}/cancelar"
        payload = {"motivoCancelamento": motivo_cancelamento}
        try:
            # Converting the request to JSON
            response = self.http_util.make_post(path, payload)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            return response
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.CancelaCobranca.cancelar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.CancelaCobranca: {e}")
            raise BancoInterException("Ocorreu um erro no SDK", Erro(502, e))
