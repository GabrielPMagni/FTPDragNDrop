from ftplib import FTP, FTP_TLS
import ftplib
import paramiko
from os import stat
from tqdm import tqdm

class FTPDragNDrop:

    def __init__(self) -> None:
        self._user = ''
        self._password = ''
        self._host = ''
        self._port = ''
        self._integer_port = 22
        self._secure = 'true'
        self._timeout = ''
        self._float_timeout = 0
        self._path = ''
        self._conf_file = 'ftp.conf'
        self._user_keyword = 'USER='
        self._password_keyword = 'PASS='
        self._host_keyword = 'HOST='
        self._port_keyword = 'PORT='
        self._secure_keyword = 'SECURE='
        self._timeout_keyword = 'TIMEOUT='
        self._path_keyword = 'PATH='
        self.file_to_upload = ''
        self._up_progress = ''
        self.read_conf()
        if not self.has_valid_conf():
            print('Configuração inválida ou incompleta. Não foi possível estabelecer conexão.')
            exit(1)
        self._get_integer_port()
        self._get_float_timeout()


    def _is_anonymous_login(self):
        is_empty_user = self._user == ''
        is_empty_password = self._password == ''
        if is_empty_user and is_empty_password:
            return True
        return False


    def _open_conf_file(self):
        try:
            return open(self._conf_file, 'r')
        except IOError as e:
            print('Erro ao abrir arquivo de configuração')
            exit(1)
        except Exception as e:
            print(f'Erro inesperado ao tentar abrir arquivo de configuração: \n\n\t{str(e)}')
            exit(1)


    def _is_secure(self):
        return self._secure == 'true'


    def _get_integer_port(self):
        try:
            self._integer_port = int(self._port)
        except ValueError:
            print(f'Porta para conexão não pode ser utilizada por não ser numérica: {self._port}')
            exit(1)
        except Exception as e:
            print(f'Erro inesperado ao validar porta para conexão: \n\n\t{str(e)}')
            exit(1)


    def _get_float_timeout(self):
        try:
            self._float_timeout = float(self._timeout)
        except ValueError:
            print(f'Tempo máximo para conexão não pode ser utilizada por não ser numérica: {self._timeout}')
            exit(1)
        except Exception as e:
            print(f'Erro inesperado ao validar tempo máximo para conexão: \n\n\t{str(e)}')
            exit(1)


    def _open_file_to_upload(self):
        try:
            return open(self.file_to_upload, 'rb')
        except IOError as e:
            print('Erro ao abrir arquivo para envio')
            exit(1)
        except Exception as e:
            print(f'Erro inesperado ao tentar abrir arquivo para envio: \n\n\t{str(e)}')
            exit(1)


    def _increase_progress_bar(self, chunk, max_size):
        self._up_progress.update(chunk)


    def upload_file(self):
        try:
            ftp = self.connect()
            if ftp:
                file = self._open_file_to_upload()
                file_path = file.name
                statinfo = stat(file_path)
                filename = file_path.split('\\')[-1]
                self._up_progress = tqdm(total=statinfo.st_size)
                if self._is_secure():
                    ftp.put(self.file_to_upload, ftp.getcwd()+'/'+filename, callback=self._increase_progress_bar)
                    ftp.close()
                else:
                    ftp.storbinary(f'STOR {filename}', file.write(), callback=self._increase_progress_bar)
                    ftp.quit()
                self._up_progress.close()
            else:
                print('Falha ao enviar arquivo para servidor')
        except TimeoutError:
            print('Tempo limite para conexão excedido')
            exit(1)
        except paramiko.ChannelException as e:
            print(f'Erro inesperado ao testar conexão com SFTP: \n\n\t{e.text}')
            exit(1)
        except paramiko.BadHostKeyException as e:
            print(f'Erro ao testar conexão com SFTP devido ao Host: \n\n\t{e.text}')
            exit(1)
        except paramiko.AuthenticationException as e:
            print(f'Erro na autenticação em conexão com SFTP: \n\n\t{e.text}')
            exit(1)
        except paramiko.PasswordRequiredException as e:
            print(f'Necessária senha para conexão com SFTP: \n\n\t{e.text}')
            exit(1)
        except ftplib.all_errors as e:
            print(f'Erro ao testar conexão com FTP: \n\n\t{str(e)}')
            exit(1)
        except Exception as e:
            print(f'Erro inesperado ao testar conexão com SFTP/FTP: \n\n\t{str(e)}')
            exit(1)



    def read_conf(self):
        conf_file = self._open_conf_file()
        for line in conf_file.readlines():
            if line.find(self._user_keyword) == 0:
                self._user = line[len(self._user_keyword):-1]
            elif line.find(self._password_keyword) == 0:
                self._password = line[len(self._password_keyword):-1]
            elif line.find(self._host_keyword) == 0:
                self._host = line[len(self._host_keyword):-1]
            elif line.find(self._port_keyword) == 0:
                self._port = line[len(self._port_keyword):-1]
            elif line.find(self._secure_keyword) == 0:
                self._secure = line[len(self._secure_keyword):-1]
            elif line.find(self._timeout_keyword) == 0:
                self._timeout = line[len(self._timeout_keyword):-1]
            elif line.find(self._path_keyword) == 0:
                self._path = line[len(self._path_keyword):-1]


    def show_conf(self):
        print(f'USER: {self._user}\nPASSWORD: {self._password}\nHOST: {self._host}\nPORT: {self._port}\nSECURE: {self.print_is_secure()}\nTIMEOUT: {self._timeout}\nPATH= {self._path}')


    def print_is_secure(self):
        return 'YES' if self._is_secure() else 'NO'


    def has_valid_conf(self):
        is_valid_host = self._host != ''
        is_valid_port = self._port != ''
        is_valid_path = self._path != ''
        if is_valid_host and is_valid_port and is_valid_path:
            return True
        return False


    def list_directory(self):
        try:
            ftp = self.connect()
            if ftp:
                if self._is_secure():
                    ls = ftp.listdir()
                    print(ls)
                    ftp.close()
                else:
                    ftp.retrlines('LIST')
                    ftp.quit()
                print('Fim da listagem')
            else:
                print('Falha ao listar diretório')
        except Exception as e:
            print(f'Erro inesperado ao listar diretório da conexão: \n\n\t{str(e)}')
            exit(1)


    def connect(self):
        try:
            if self._is_secure():
                transport = paramiko.Transport((self._host, self._integer_port))
                if self._is_anonymous_login():
                    transport.connect(None, '', '')
                    ftp = paramiko.SFTPClient.from_transport(transport)
                else:
                    transport.connect(None, self._user, self._password)
                    ftp = paramiko.SFTPClient.from_transport(transport)

                ftp.timeout = self._float_timeout
                ftp.chdir(self._path)
            else:
                ftp = FTP_TLS(host=self._host, timeout=self._float_timeout)
                if self._is_anonymous_login():
                    ftp.connect(port=self._integer_port)
                    ftp.login()
                else:
                    ftp.connect(port=self._integer_port)
                    ftp.login(user=self._user, passwd=self._password)
                ftp.cwd(self._path)
            return ftp
        except TimeoutError:
            print('Tempo limite para conexão excedido')
            return False
        except paramiko.ChannelException as e:
            print(f'Erro inesperado ao testar conexão com SFTP: \n\n\t{e.text}')
            return False
        except paramiko.BadHostKeyException as e:
            print(f'Erro ao testar conexão com SFTP devido ao Host: \n\n\t{e.text}')
            return False
        except paramiko.AuthenticationException as e:
            print(f'Erro na autenticação em conexão com SFTP: \n\n\t{e.text}')
            return False
        except paramiko.PasswordRequiredException as e:
            print(f'Necessária senha para conexão com SFTP: \n\n\t{e.text}')
            return False
        except ftplib.all_errors as e:
            print(f'Erro ao testar conexão com FTP: \n\n\t{str(e)}')
            return False
        except Exception as e:
            print(f'Erro inesperado ao testar conexão com SFTP/FTP: \n\n\t{str(e)}')
            return False


    def test_connection(self):
        ftp = self.connect()
        if ftp:
            if self._is_secure():
                ftp.close()
            else:
                ftp.quit()
            return True
        return False
