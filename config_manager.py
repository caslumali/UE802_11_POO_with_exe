import logging
import os
import sys

# Define o caminho padrão para o arquivo de configuração, se necessário
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')


class ConfigManager:
    def __init__(self):
        # Inicializa as configurações como um dicionário diretamente
        self.config = {
            'Paths': {
                'InputCSV': '',
                'InputGeoJSON': '',
                'OutputGeoJSON': '',
                'InconsistenciesCSV': ''
            },
            'Options': {
                'IdCSVColumn': '',
                'PropName': '',
                'IndividualPropName': '',
                'CSVSeparator': ','
            }
        }
        # Carrega as configurações do arquivo aqui, se aplicável
        # Exemplo: self.load_config_from_file()

    def load_config_from_file(self):
        # Implemente a leitura do arquivo de configuração, se necessário
        pass

    def get_config(self):
        # Retorna o dicionário de configurações
        return self.config

    def update_config(self, input_csv, input_geojson, output_geojson, inconsistencies_csv, id_csv_column, prop_name, individual_prop_name, csv_separator):
        self.config['Paths']['InputCSV'] = input_csv
        self.config['Paths']['InputGeoJSON'] = input_geojson
        self.config['Paths']['OutputGeoJSON'] = output_geojson
        self.config['Paths']['InconsistenciesCSV'] = inconsistencies_csv
        self.config['Options']['IdCSVColumn'] = id_csv_column
        self.config['Options']['PropName'] = prop_name
        self.config['Options']['IndividualPropName'] = individual_prop_name
        self.config['Options']['CSVSeparator'] = csv_separator
        # Salva as configurações no arquivo aqui, se aplicável
        # Exemplo: self.save_config_to_file()

    def save_config_to_file(self):
        # Implemente a escrita no arquivo de configuração, se necessário
        pass


# Configuração de logging básica
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Exemplo de uso
if __name__ == '__main__':
    cfg_manager = ConfigManager()
    print(cfg_manager.get_config())

    # Atualiza configurações como exemplo
    cfg_manager.update_config('meu_arquivo.csv', 'meu_geojson.geojson', 'saida.geojson',
                              'inconsistencias.csv', 'ID', 'NomePropriedade', 'NomeIndividual', ',')
    print(cfg_manager.get_config())
