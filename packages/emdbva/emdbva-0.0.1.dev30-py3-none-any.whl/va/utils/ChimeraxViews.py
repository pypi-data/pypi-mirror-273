import json
import os
import re
import sys
import glob
import subprocess
from distutils.spawn import find_executable
from va.utils.misc import scale_image, out_json
from va.metrics.contour_level_predicator import *


class ChimeraxViews:

    def __init__(self, chimerax_bin_dir, input_json=None, va_dir=None):
        self.input_json = input_json
        self.va_dir = os.path.dirname(self.input_json) if input_json else va_dir
        if self.input_json:
            with open(input_json, 'r') as f:
                self.json_data = json.load(f)
        else:
            self.json_data = None
            print('There is no json file data.')

        self.chimerax = chimerax_bin_dir


    def get_root_data(self, data_type):
        """
            Get the root json data based on the input json file and the data type

        :param data_type: a string of full path name of the json file
        """

        root_data = None
        if data_type in self.json_data.keys():
            root_data = self.json_data[data_type]
            try:
                del root_data['err']
            except:
                print('There is/are %s model(s).' % len(root_data))
        else:
            print(f'{data_type} json result is')

        return root_data

    def write_residue_cxc(self, colors, residues, map_name, model_name, data_type):
        """
            Write a ChimeraX cxc file for generating surfaces with model cases
        :param colors: list of colors
        :param residues: list of residues e.g., A:321 THR
        :param map_name: a string of input file name
        :param model_name: a string of input model name
        :param data_type: a string of surface type, e.g., residue_local_resolution
        """

        if data_type:
            cur_type = data_type.replace('_', '')
            chimerax_file_name = f'{map_name}_{model_name}_{cur_type}_chimerax.cxc'
        else:
            cur_type = ''
            chimerax_file_name = f'{map_name}_{model_name}_chimerax.cxc'

        surface_file_name = '{}/{}_{}'.format(self.va_dir, map_name, model_name)
        model = f'{self.va_dir}/{model_name}'
        with open(f'{self.va_dir}/{chimerax_file_name}', 'w') as fp:
            fp.write(f'open {model} format mmcif\n')
            fp.write('show selAtoms ribbons\n')
            fp.write('hide selAtoms\n')

            for (color, residue) in zip(colors, residues):
                chain, restmp = residue.split(':')
                # Not sure if all the letters should be replaced
                # res = re.sub("\D", "", restmp)
                res = re.findall(r'-?\d+', restmp)[0]
                fp.write(
                    f'color /{chain}:{res} {color}\n'
                )
            fp.write(
                'set bgColor white\n'
                'lighting soft\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_z{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'turn x -90\n'
                'turn y -90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_y{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'view orient\n'
                'turn x 90\n'
                'turn z 90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_x{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'close all\n'
                'exit'
            )

            return chimerax_file_name

    def write_maps_cxc(self, map_name, map_two, data_type):
        """
            Write a ChimeraX cxc file for generating surfaces with model cases
        :param map_name: a string of input file name
        :param map_two: a string of input model name
        :param data_type: a string of surface type, e.g., residue_local_resolution
        """

        if data_type:
            cur_type = data_type.replace('_', '')
            chimerax_file_name = f'{map_name}_{cur_type}_chimerax.cxc'
        else:
            cur_type = ''
            chimerax_file_name = f'{map_name}_chimerax.cxc'

        map_fullname = f'{self.va_dir}/{map_name[:-4]}_rawmap.map'
        # mask_fullname = f'{self.va_dir}/{map_name}_relion/mask/{map_name}_mask.mrc'

        surface_file_name = '{}/{}'.format(self.va_dir, map_name)
        with open(f'{self.va_dir}/{chimerax_file_name}', 'w') as fp:
            fp.write(f'open {map_fullname} format ccp4\n')
            fp.write(f'open {map_two} format ccp4\n')
            if data_type == 'map_local_resolution':
                a = mrcfile.open(map_fullname)
                d = a.data
                raw_contour = f'{calc_level_dev(d)[0]}'
                fp.write('color sample #1 map #2 palette bluered\n')
                fp.write(f'volume #1 step 1 level {raw_contour}\n')
                fp.write('hide #!2 models\n')
            if data_type == 'map_mask':
                # prepare for map and mask overlay views here
                pass

            fp.write(
                'set bgColor white\n'
                'lighting soft\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_z{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'turn x -90\n'
                'turn y -90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_y{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'view orient\n'
                'turn x 90\n'
                'turn z 90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_x{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'close all\n'
                'exit'
            )

            return chimerax_file_name

    def run_chimerax(self, chimerax_file_name):
        """
            Run ChimeraX to produce the surface views

        :param chimerax_file_name: a string of ChimeraX cxc file
        """
        errs = []
        chimerax = self.chimerax
        model_name = chimerax_file_name.split('_')[1]
        bin_display = os.getenv('DISPLAY')
        try:
            if not bin_display:
                subprocess.check_call(f'{chimerax} --offscreen --nogui {self.va_dir}/{chimerax_file_name}',
                                      cwd=self.va_dir, shell=True)
                print('Colored models were produced.')
            else:
                subprocess.check_call(f'{chimerax}  {self.va_dir}/{chimerax_file_name}', cwd=self.va_dir, shell=True)
                print('Colored models were produced.')

            return None
        except subprocess.CalledProcessError as e:
            err = 'Saving model {} fit surface view error: {}.'.format(model_name, e)
            errs.append(err)
            sys.stderr.write(err + '\n')

            return errs

    def rescale_view(self, map_name, model_name=None, data_type=None):
        """
            Scale views and produce corresponding dictionary

        :param map_name: a string of input map name
        :param model_name: a string of input model name
        :param data_type: a string of view type
        """

        original = {}
        scaled = {}
        result = {}
        used_data_type = data_type.replace('_', '')
        for i in 'xyz':
            if model_name is None:
                image_name = f'{map_name}_{i}{used_data_type}.jpeg'
            else:
                image_name = f'{map_name}_{model_name}_{i}{used_data_type}.jpeg'
            full_image_path = f'{self.va_dir}/{image_name}'
            if os.path.isfile(full_image_path):
                scaled_image_name = scale_image(full_image_path, (300, 300))
                original[i] = image_name
                scaled[i] = scaled_image_name
        result['original'] = original
        result['scaled'] = scaled

        return result

    def get_views(self, map_name, root_data=None, data_type=None):
        """
            Based on the information produce views and save to json file

        :param root_data: root data from input json file
        :param map_name: a string of input map nanme
        :param data_type: a string of view type
        """

        if root_data:
            num_model = len(root_data)
            for i in range(num_model):
                output_json = {}
                json_dict = {}
                cur_model = root_data[str(i)]
                keylist = list(cur_model.keys())
                colors = None
                residues = None
                model_name = None
                for key in keylist:
                    if key != 'name':
                        colors = cur_model[key]['color']
                        residues = cur_model[key]['residue']
                    else:
                        model_name = cur_model[key]
                chimerax_file_name = self.write_residue_cxc(colors, residues, map_name, model_name, data_type)
                out = self.run_chimerax(chimerax_file_name)
                surfaces_dict = self.rescale_view(map_name, model_name, data_type)
                json_dict[model_name] = surfaces_dict
                output_json[f'{data_type}_views'] = json_dict

                output_json_file = f"{map_name}_{model_name}_{data_type.replace('_', '')}.json"
                output_json_fullpath = f'{self.va_dir}/{output_json_file}'
                out_json(output_json, output_json_fullpath)
        else:

            output_json = {}

            local_resolution_map_glob = glob.glob(f'{self.va_dir}/{map_name}_relion/*_locres.mrc')
            local_resolution_map = local_resolution_map_glob[0] if len(local_resolution_map_glob) > 0 else None
            chimerax_file_name = self.write_maps_cxc(map_name, local_resolution_map, data_type)
            out = self.run_chimerax(chimerax_file_name)
            surfaces_dict = self.rescale_view(map_name,None, data_type)
            output_json[f'{data_type}_views'] = surfaces_dict

            output_json_file = f"{map_name}_{data_type.replace('_', '')}.json"
            output_json_fullpath = f'{self.va_dir}/{output_json_file}'
            out_json(output_json, output_json_fullpath)




