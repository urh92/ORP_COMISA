import json

class ConfigLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        # Load the configuration right here instead of recursively creating a new ConfigLoader.
        self.config = self.load_config()
        if self.config:
            self.y_label = self.config.get('y_label')
            self.predictors = self.config.get('predictors')
            self.co_variates = self.config.get('co_variates')
            self.y_dict = self.config.get('y_dict')
            self.model_type = self.config.get('model_type')
            self.output_folder = self.config.get('output_folder')
            self.psg_criterion = self.config.get('psg_criterion')
            self.drop_score_cols = self.config.get('drop_score_cols')
            self.drop_corr_cols = self.config.get('drop_corr_cols')
            self.variable_type = self.config.get('variable_type')
        else:
            self.y_label = self.predictors = self.co_variates = self.y_dict = self.model_type = self.output_folder = \
                self.psg_criterion = self.drop_score_cols = self.drop_corr_cols = self.variable_type = None

    def load_config(self):
        """Load configuration settings from a JSON file."""
        try:
            with open(self.filepath, 'r') as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            print(f"Error: The file '{self.filepath}' does not exist.")
            return None
        except json.JSONDecodeError:
            print("Error: Invalid JSON in the configuration file.")
            return None


if __name__ == "__main__":
    config_loader = ConfigLoader('config.json')
    if config_loader.config is None:
        print("Failed to load configuration.")
    else:
        print("Configuration loaded successfully:")
        print("Y label:", config_loader.y_label)
        print("Predictors:", config_loader.predictors)
        print("Co-variates:", config_loader.co_variates)
        print("Y dict:", config_loader.y_dict)
        print("Model type:", config_loader.model_type)
        print("Output folder:", config_loader.output_folder)
        print("PSG criterion", config_loader.psg_criterion)
        print("Drop score columns", config_loader.drop_score_cols)
        print("Variable type", config_loader.variable_type)
