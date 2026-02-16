from modules.utils.misc import get_args, load_config


def main(config):
    agent = config['agent']

    agent.run()

"""
Generate a code to train a audio model for a KWS task. Assume that I have a csv located at data/dataset.csv with the columns "path", "label". The path refer to the filepath of an audio file and the label is a keyword. Train a model to classify among the labels in the dataset using tensorflow framework.
"""


if __name__ == "__main__":
    args = get_args()

    config_path = args.get("config")
    config = load_config(config_path)

    main(config)
