try:
    import argparse
    from ftpdragndrop_class import FTPDragNDrop
except ImportError:
    print('Erro ao importar bibliotecas necessárias.')
    exit(1)

parser = argparse.ArgumentParser(prog='Transferir Arquivos')
parser.add_argument('--arquivo', type=str, help='Nome do arquivo a ser transferido')

args = parser.parse_args()

ftp_obj = FTPDragNDrop()

def main():
    ftp_obj.read_conf()
    ftp_obj.show_conf()
    ftp_obj.test_connection()


main()