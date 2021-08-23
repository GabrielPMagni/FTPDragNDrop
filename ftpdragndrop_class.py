from ftplib import FTP, FTP_TLS

class FTPDragNDrop:

    def __init__(self) -> None:
        self._user = ''
        self._password = ''
        self._host = ''
        self._port = ''
        self._secure = 'true'
        self._conf_file = 'ftp_example.conf'
        self._user_keyword = 'USER='
        self._password_keyword = 'PASS='
        self._host_keyword = 'HOST='
        self._port_keyword = 'PORT='
        self._secure_keyword = 'SECURE='

    def _open_file(self):
        try:
            return open(self._conf_file, 'r')
        except IOError as e:
            print('Erro ao abrir arquivo de configuração')
            exit(1)
        except Exception as e:
            print(f'Erro inesperado ao tentar abrir arquivo de configuração: \n\n\t{str(e)}')
            exit(1)


    def read_conf(self):
        conf_file = self._open_file()
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


    def show_conf(self):
        print(f'USER: {self._user}\nPASSWORD: {self._password}\nHOST: {self._host}\nPORT: {self._port}\nSECURE: {self.print_is_secure()}')


    def _is_secure(self):
        return self._secure == 'true'

    def print_is_secure(self):
        return 'YES' if self._is_secure() else 'NO'


    def has_valid_conf(self):
        is_valid_user = self._user != ''
        is_valid_password = self._password != ''
        is_valid_host = self._host != ''
        is_valid_port = self._port != ''

        if is_valid_user and is_valid_password and is_valid_host and is_valid_port:
            return True
        return False

    def test_connection(self):
        if not self.has_valid_conf():
            print('Configuração inválida ou imcompleta. Não foi possível estabelecer conexão.')
            return False
        if self._is_secure():
            ftp = FTP_TLS(self._host)
        else:
            ftp = FTP(self._host)
        ftp.login(user=self._user, passwd=self._password)