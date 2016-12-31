import os

from Generator import InstanceGenerator
from InputOutput import OutputWriter

CONFIG_DIR = '../config_files'
DB_PATH = '../db/tp3s.db'
TP3S_OUT_DIR = '../instance'


def generate_instance():
    generator = InstanceGenerator(CONFIG_DIR,
                                  DB_PATH)
    for configfile in os.listdir(CONFIG_DIR):
        if configfile.endswith('.config'):
            print 'Generating instance using config file', configfile
            generator.config_path = os.path.join(CONFIG_DIR, configfile)
            inst = generator.gen_instance()
            # parse the config name
            outfilename = configfile.replace('.config', '.tp3s')
            outfilename = outfilename.replace('config', '')
            out = OutputWriter(os.path.join(TP3S_OUT_DIR, outfilename))
            out.write_instance(inst)



if __name__ == '__main__':
    generate_instance()