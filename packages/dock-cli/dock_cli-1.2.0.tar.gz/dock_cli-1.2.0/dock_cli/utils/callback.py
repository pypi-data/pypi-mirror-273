import functools
import click
from dock_cli.utils import utils

def validate_section(ctx, _param, value):
    if isinstance(value, tuple):
        for section in value:
            ctx.obj.helper.validate_section(section, click.BadArgumentUsage)
    if isinstance(value, str):
        ctx.obj.helper.validate_section(value, click.BadArgumentUsage)
    return value

def transform_to_section(ctx, _param, value):
    if isinstance(value, tuple):
        return tuple(map(functools.partial(utils.to_section, ctx.obj.config_dir), value))
    return utils.to_section(ctx.obj.config_dir, value)

def multiline_values(_ctx, _param, value):
    if isinstance(value, tuple) and value:
        if len(value) == 1:
            return value[0]
        return '\n' + '\n'.join(value)
    return value

def multiline_sections(ctx, param, value):
    return multiline_values(ctx, param, transform_to_section(ctx, param, value))
