from dp.launching.typing import BaseModel, Field, OutputDirectory, InputFilePath
from dp.launching.typing import Int, String, Enum, Float, Boolean, List, Optional, Dict
from dp.launching.cli import to_runner, default_minimal_exception_handler
from dp.launching.report import Report, ReportSection, ChartReportElement

from dflow_galaxy.app.common import DFlowOptions, setup_dflow_context, EnsembleOptions
from dflow_galaxy.res import get_res_path
from dflow_galaxy.core.log import get_logger
from dflow_galaxy.core.util import parse_string_array, str_or_none

from dflow_galaxy.workflow.tesla.main import build_tesla_workflow

from ai2_kit.core.util import dump_json, load_text, load_json
from ai2_kit.feat import catalysis as ai2cat

import ase.io
import fire

from pathlib import Path
from uuid import uuid4
import shutil
import glob
import sys
import os

from .report import gen_report

logger = get_logger(__name__)


BH_DEEPMD_DEFAULT = {
    'image_name': 'registry.dp.tech/dptech/dpmd:2.2.8-cuda12.0',
    'scass_type': 'c8_m32_1 * NVIDIA V100',
}
BH_LAMMPS_DEFAULT = BH_DEEPMD_DEFAULT

BH_CP2K_DEFAULT = {
    'image_name': 'registry.dp.tech/dptech/cp2k:11',
    'scass_type': 'c64_m256_cpu',
}

BH_PYTHON_DEFAULT = {
    'image_name': 'registry.dp.tech/dptech/prod-13325/dflow-galaxy:0.1.7-main-07745fb',
    'scass_type': 'c2_m4_cpu',
}


class KvItem(BaseModel):
    key: String = Field(
        description="Key of the item")
    value: String = Field(
        format='multi-line',
        description="Value of the item")


class ExploreItem(BaseModel):
    key: String = Field(
        description="Key of the item")
    value: String = Field(
        description="Value of the item, multiple value should be separated by comma")
    broadcast: Boolean = Field(
        default=False,
        description="Use broadcast instead of full combination")


class DeepmdSettings(BaseModel):

    compress_model: Boolean = Field(
        default=True,
        description="Compress the model after training")

    concurrency: Int = Field(
        default=4,
        description="Number of concurrent run")

    steps: Optional[Int] = Field(
        default=400000,
        description="Number of steps for DeepMD training, leave it empty will use the numb_steps defined in the input template")

    cmd: String = Field(
        default='dp',
        description="Command to run DeepMD, note that it depends on the docker image you used")

    setup_script: String = Field(
        default='',
        format='multi-line',
        description="Setup script for DeepMD simulation, note that it depends on the docker image you used")


class LammpsSetting(BaseModel):
    ensemble: EnsembleOptions = Field(
        default=EnsembleOptions.csvr,
        description='Ensemble of LAMMPS simulation')

    plumed_config: Optional[String] = Field(
        format='multi-line',
        description='Plumed configuration file for metadynamics simulation')

    explore_vars: List[ExploreItem] = Field(
        default=[
           ExploreItem(key='TEMP', value='50,100,200,300,400,600,800,1000', broadcast=False),
           ExploreItem(key='PRES', value='1', broadcast=False),
        ],
        description="Variables for LAMMPS exploration, TEMP, PRES are required, you may also add TAU_T, TAU_P, etc")

    template_vars: List[KvItem] = Field(
        default=[
            KvItem(key='POST_INIT', value='\n'.join([
                'neighbor 1.0 bin',
                'box      tilt large',
            ])),
            KvItem(key='POST_READ_DATA', value='\n'.join([
                'change_box all triclinic'
            ])),
        ],
        description="Template variables for LAMMPS exploration, you may need to modify this according to your system")

    nsteps: Int = Field(
        default=1000,
        description='Number of steps of LAMMPS simulation for the first iteration')

    timestep: Float = Field(
        default=0.0005,
        description='Time step size of LAMMPS simulation in ps')

    sample_freq: Int = Field(
        default=10,
        description='Sampling frequency of LAMMPS simulation')

    no_pbc: Boolean = Field(
        default=False,
        description='Whether to use periodic boundary condition')

    concurrency: Int = Field(
        default=20,
        description="Number of concurrent run")

    cmd: String = Field(
        default='lmp',
        description="Command to run LAMMPS, note that it depends on the docker image you used")

    setup_script: String = Field(
        default='',
        format='multi-line',
        description="Setup script for LAMMPS simulation, note that it depends on the docker image you used")


class ModelDeviation(BaseModel):
    lo: Float = Field(
        default=0.2,
        description="Lower bound of the deviation")

    hi: Float = Field(
        default=0.6,
        description="Upper bound of the deviation")

    metric: String = Field(
        default='max_devi_f',
        description="Metric to measure the deviation")


class Cp2kSettings(BaseModel):

    limit: Int = Field(
        default=50,
        description="Limit of the number of structures to be labeled for each iteration")

    concurrency: Int = Field(
        default=20,
        description="Number of concurrent run")

    cmd: String = Field(
        default='mpirun -np 64 cp2k.popt',
        description="Script to run CP2K simulation, note that it depends on the docker image")

    setup_script: String = Field(
        default = '\n'.join([
            '# guess cp2k data dir',
            '[[ -z "${CP2K_DATA_DIR}" ]] && export CP2K_DATA_DIR="$(dirname "$(which cp2k || which cp2k.psmp)")/../../data" || true',
            'source /opt/cp2k-toolchain/install/setup',
        ]),
        format='multi-line',
        description="Setup script for CP2K simulation, note that it depends on the docker image you used")


class DynacatTeslaArgs(DFlowOptions):
    deepmd_dataset : InputFilePath = Field(
        title='DeepMD Dataset',
        description="DeepMD in zip or tgz format, for example: deepmd-dataset.tgz, dp-dataset.zip")

    deepmd_input_template: Optional[InputFilePath] = Field(
        title='DeepMD Input Template',
        description="Input template file for DeepMD training, in json format, for example: deepmd.json, if not provided, the build-in template will be used")

    lammps_system_file: InputFilePath = Field(
        description="Structure file in xyz format use for LAMMPS simulation, for example h2o.xyz, the xyz file may contain multiple structures")

    cp2k_input_template: InputFilePath = Field(
        description="Input template file for CP2K simulation, for example: cp2k.inp")

    dry_run: Boolean = Field(
        default = True,
        description="Generate configuration file without running the workflow")

    max_iters: Int = Field(
        default = 7,
        description="Maximum iterations of the workflow")

    s3_prefix: Optional[String] = Field(
        description="Specify the S3 prefix of DFlow. By default a random prefix will be used for different jobs. Jobs use the same prefix will share the same working directory, which allow you to inherit the state of previous run.")

    deepmd: DeepmdSettings = Field(
        description="DeepMD settings for training")

    lammps: LammpsSetting = Field(
        description="LAMMPS settings for structure exploration")

    model_deviation: ModelDeviation = Field(
        description="Model deviation settings for screening structures")

    cp2k: Cp2kSettings = Field(
        description="CP2K settings for DFT labeling")

    output_dir : OutputDirectory = Field(
        default='./output',
        description="Output directory of LAMMPS simulation")

    deepmd_resource: Dict[String, String] = Field(
        default=BH_DEEPMD_DEFAULT,
        description="Resource configuration for DeepMD")

    lammps_resource: Dict[String, String] = Field(
        default=BH_LAMMPS_DEFAULT,
        description="Resource configuration for LAMMPS")

    cp2k_resource: Dict[String, String] = Field(
        default=BH_CP2K_DEFAULT,
        description="Resource configuration for CP2K")

    python_resource: Dict[String, String] = Field(
        default=BH_PYTHON_DEFAULT,
        description="Resource configuration for Python")


def launch_app(args: DynacatTeslaArgs) -> int:
    s3_prefix = args.s3_prefix or f'dynacat-{uuid4()}'
    logger.info(f'using s3 prefix: {s3_prefix}')
    tesla_template = get_res_path() / 'dynacat' / 'tesla_template.yml'
    # handle deepmd dataset
    dp_dataset_file = args.deepmd_dataset.get_full_path()
    dp_dataset = _unpack_dpdata(dp_dataset_file, 'init-dataset')
    dp_dataset_config = {}
    for i, d in enumerate(dp_dataset):
        dp_dataset_config[f'dpdata-{i}'] = {
            'url': d,
        }
    logger.info(f'Unpacked dpdata to {dp_dataset}')

    # build config
    shutil.copy(tesla_template, 'tesla-preset.yml')
    executor_config = _get_executor_config(args)
    workflow_config = _get_workflow_config(args, dp_dataset_config)

    # TODO: use yaml to dump config pretty
    dump_json(executor_config, 'tesla-executor.yml')
    dump_json(workflow_config, 'tesla-workflow.yml')

    # copy generated configuration to output
    os.makedirs(args.output_dir, exist_ok=True)
    os.system(f'cp tesla-*.yml {args.output_dir}')

    if args.dry_run:
        logger.info('Skip running workflow due to dry_run is set to True')
        return 0

    setup_dflow_context(args)
    workflow = build_tesla_workflow('tesla-preset.yml', 'tesla-executor.yml', 'tesla-workflow.yml',
                                    s3_prefix=s3_prefix, max_iters=args.max_iters)
    try:
        workflow.run()
    except:
        logger.exception('Failed to run workflow')
        return 1
    finally:
        # reclaim useful data
        dp_dataset_dir = os.path.join(args.output_dir, 'dp-dataset')
        dp_models_dir = os.path.join(args.output_dir, 'dp-models')
        model_devi_dir = os.path.join(args.output_dir, 'model-devi')
        os.makedirs(dp_dataset_dir, exist_ok=True)
        os.makedirs(dp_models_dir, exist_ok=True)
        os.makedirs(model_devi_dir, exist_ok=True)
        workflow.s3_download('iter-dataset', dp_dataset_dir)
        workflow.s3_download('train-deepmd', dp_models_dir)
        workflow.s3_download('screen-model-devi', model_devi_dir)
        try:
            gen_report(dp_models_dir=dp_models_dir,
                    model_devi_dir=model_devi_dir,
                    max_iters=args.max_iters,
                    output_dir=str(args.output_dir))
        except:
            logger.exception('Failed to generate report')
    return 0


def _get_executor_config(args: DynacatTeslaArgs):
    return {
        'executors': {
            'bohrium': {
                'bohrium': {},
                'apps': {
                    'python': {
                        'resource': {
                            'bohrium': {**args.python_resource, 'job_name':'dynacat_tesla_python'},
                        }
                    },
                    'deepmd': {
                        'resource': {
                            'bohrium': {**args.deepmd_resource, 'job_name':'dynacat_tesla_deepmd'},
                        },
                        'dp_cmd': args.deepmd.cmd,
                        'concurrency': args.deepmd.concurrency,
                        'setup_script': args.deepmd.setup_script,
                    },
                    'lammps': {
                        'resource': {
                            'bohrium': {**args.lammps_resource, 'job_name':'dynacat_tesla_lammps'},
                        },
                        'lammps_cmd': args.lammps.cmd,
                        'concurrency': args.lammps.concurrency,
                        'setup_script': args.lammps.setup_script,
                    },
                    'cp2k': {
                        'resource': {
                            'bohrium': {**args.cp2k_resource, 'job_name': 'dynacat_tesla_cp2k'},
                        },
                        'cp2k_cmd': args.cp2k.cmd,
                        'concurrency': args.cp2k.concurrency,
                        'setup_script':  args.cp2k.setup_script,
                    }
                }
            }
        },
        'orchestration': {
            'deepmd': 'bohrium',
            'lammps': 'bohrium',
            'model_devi': 'bohrium',
            'cp2k': 'bohrium'
        },
    }


def _get_workflow_config(args: DynacatTeslaArgs, dp_dataset_config: dict):
    # process system file
    explore_data_file = args.lammps_system_file.get_full_path()
    explore_data_key = os.path.basename(explore_data_file)
    atoms = ase.io.read(explore_data_file, index=0)
    type_map, mass_map = ai2cat.get_type_map(atoms)  # type: ignore

    if args.deepmd_input_template:
        deepmd_template_file = args.deepmd_input_template.get_full_path()
    else:
        deepmd_template_file = str(get_res_path() / 'dynacat' / 'deepmd.json')
    deepmd_template = load_json(deepmd_template_file)
    cp2k_input_template = load_text(args.cp2k_input_template.get_full_path())

    if args.deepmd.steps and args.deepmd.steps > 0:
        deepmd_template['training']['numb_steps'] = args.deepmd.steps
    assert deepmd_template['training']['numb_steps'] > 0, 'numb_steps is required in the input template or input'
    deepmd_template['training']['disp_file'] = 'lcurve.out'  # force to use lcurve.out

    product_vars, broadcast_vars = _get_lammps_vars(args.lammps.explore_vars)

    return {
        'datasets': {
            **dp_dataset_config,
            explore_data_key: {  # data key must be a normal file name or else ase cannot detect the format
                'url': explore_data_file,
            },
        },
        'workflow': {
            'general': {
                'type_map': type_map,
                'mass_map': mass_map,
            },
            'train': {
                'deepmd': {
                    'init_dataset': list(dp_dataset_config.keys()),
                    'input_template': deepmd_template,
                    'compress_model': args.deepmd.compress_model,
                }
            },
            'explore':{
                'lammps': {
                    'systems': [explore_data_key],
                    'nsteps': args.lammps.nsteps,
                    'ensemble': args.lammps.ensemble.value,
                    'timestep': args.lammps.timestep,
                    'sample_freq': args.lammps.sample_freq,
                    'no_pbc': args.lammps.no_pbc,
                    'plumed_config': str_or_none(args.lammps.plumed_config),
                    'product_vars': product_vars,
                    'broadcast_vars': broadcast_vars,
                    'template_vars': dict((item.key, item.value) for item in args.lammps.template_vars),
                }
            },
            'screen':{
                'model_devi': {
                    'metric': args.model_deviation.metric,
                    'decent_range': [args.model_deviation.lo, args.model_deviation.hi],
                }
            },
            'label': {
                'cp2k': {
                    'input_template': cp2k_input_template,
                    'limit': args.cp2k.limit,
                }
            },
        }
    }


def _get_lammps_vars(explore_vars: List[ExploreItem]):
    broadcast_vars = {}
    product_vars = {}
    for item in explore_vars:
        if item.broadcast:
            broadcast_vars[item.key] = parse_string_array(item.value, dtype=float, delimiter=',')
        else:
            product_vars[item.key] = parse_string_array(item.value, dtype=float, delimiter=',')
    return product_vars, broadcast_vars


def _unpack_dpdata(file: str, extract_dir: str):
    extract_dir = os.path.normpath(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)
    shutil.unpack_archive(file, extract_dir=extract_dir)
    # use type.raw to locate the dpdata folder
    paths = glob.glob(f'{extract_dir}/**/type.raw', recursive=True)
    return [ os.path.dirname(p) for p in paths]


def main():
    to_runner(
        DynacatTeslaArgs,
        launch_app,
        version="0.1.0",
    )(sys.argv[1:])


if __name__ == "__main__":
    fire.Fire({
        'main': main,
        'gen_report': gen_report,
    })
