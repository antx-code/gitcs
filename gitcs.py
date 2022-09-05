import asyncio
import uvloop
from loguru import logger
import typer
import importlib
import os
import time
import json
from funcs.fileio import save2file

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
uvloop.install()
app = typer.Typer(help='Antx Fast and Powerful Git Code Search Tool')


def _load_files():
    files = []
    module_path = f'{os.path.dirname(__file__)}/modules'
    filelist = os.listdir(module_path)
    for file in filelist:
        if '__' in file:
            continue
        files.append(file.split(".py")[0])
    return files


def _load_module():
    objects = []
    files = _load_files()
    for file in files:
        mod = f'{file.capitalize().split("cs")[0]}CS'
        try:
            logger.debug(f'Loading {file} module')
            package = importlib.import_module(f"modules.{file}")
            objects.append(getattr(package, mod)())
        except ImportError:
            logger.warning(f'Loading {file} module')
            package = importlib.import_module(f".{file}", package=f'modules')
            objects.append(getattr(package, mod)())
    return objects


@logger.catch(level='ERROR')
@app.command()
def dia(target: str):
    logger.info(f'Welcome to Antx Git Code Search Tool.')
    logger.debug(f'Starting find {target} ......')
    objs = _load_module()
    results = {}
    start = time.time()
    counts = 0
    for obj in objs:
        obj_count, obj_result = obj.dia(target)
        obj_name = obj.__class__.__name__
        counts = counts + obj_count
        results[obj_name] = obj_result
    results = json.dumps(results, indent=4)
    logger.success(results)
    end = time.time()
    save2file(f'gitcs_{target}_results', results)
    logger.success(f'All Task has been finished, total found {counts} code related records, cost {end - start} seconds.')
    return results


if __name__ == '__main__':
    app()
