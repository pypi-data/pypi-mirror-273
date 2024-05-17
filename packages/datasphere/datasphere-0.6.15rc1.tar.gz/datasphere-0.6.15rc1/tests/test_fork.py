import re
from dataclasses import dataclass, field
from pytest import raises
from typing import Dict, List, Optional

from datasphere.api import jobs_pb2 as jobs
from datasphere.config import VariablePath, Config, Environment, DockerImage, Password
from datasphere.fork import (
    Overrides,
    fork_params,
    get_docker_dict_from_cli_args,
    get_working_storage_dict_from_cli_args,
    parse_name_value,
    parse_name_value_list,
)


def test_fork_params(tmp_path):
    source_input_1 = tmp_path / 'source_input_1.txt'
    source_input_1.write_text('source input 1')
    source_input_2 = tmp_path / 'in' / 'source_input_2.txt'
    source_input_2.parent.mkdir()
    source_input_2.write_text('source input 2')
    source_input_3 = tmp_path / 'source_input_3.txt'
    source_input_3.write_text('source input 3')
    source_output_1 = 'out'
    source_output_2 = 'source_output_2.txt'

    source_params = jobs.JobParameters(
        arguments=[
            jobs.Argument(name='ARG1', value='VALUE1'),
            jobs.Argument(name='ARG2', value='VALUE2'),
        ],
        input_files=[
            VariablePath(str(source_input_1), var='INPUT1').get_file(),
            VariablePath(str(source_input_2), var='INPUT2').get_file(),
            VariablePath(str(source_input_3), var='INPUT3').get_file(),
        ],
        output_files=[
            VariablePath(source_output_1, var='OUTPUT1').file_desc,
            VariablePath(source_output_2, var='OUTPUT2').file_desc,
        ]
    )

    new_input_1 = tmp_path / 'new_in'
    new_input_1.mkdir()
    new_input_1_inner_file = new_input_1 / 'new_input_1.txt'
    new_input_1_inner_file.write_text('new input 1')
    new_input_1_overlaps_old = tmp_path / 'in'
    new_input_3 = tmp_path / 'source_input_3.txt'  # even if path matches old one, new file content will be sent
    new_input_3.write_text('new input 3')
    new_output_2_overlaps_old = 'out/new_output_1.txt'
    new_output_2 = 'new_output_2.txt'

    def get_cfg(
            args_: Optional[Dict[str, str]] = None,
            inputs: Optional[List[VariablePath]] = None,
            outputs: Optional[List[VariablePath]] = None,
            env: Optional[Environment] = None,
            cloud_instance_types: Optional[List[str]] = None,
            name: Optional[str] = None,
            desc: Optional[str] = None,
            working_storage: Optional[jobs.ExtendedWorkingStorage] = None,
    ) -> Config:
        return Config(
            cmd='',
            args=args_ or {},
            inputs=inputs or [],
            outputs=outputs or [],
            s3_mounts=[],
            datasets=[],
            env=env or Environment(vars={}, docker_image=None, python=None),
            cloud_instance_types=cloud_instance_types or [],
            attach_project_disk=False,
            content='',
            name=name,
            desc=desc,
            working_storage=working_storage,
        )

    for overrides, expected_cfg, expected_err in (
            (Overrides(vars={'INPUT1': 'foo.txt', 'FOO': 'bar.txt'}), None, 'No variable path in source job: FOO'),
            (Overrides(working_storage_dict={'working-storage': {'type': 'DDT'}}), None, 'possible working storage types are: [SSD]'),
            (Overrides(vars={'INPUT1': str(new_input_1_overlaps_old)}), None, f"Path '{tmp_path}/in/source_input_2.txt' is included in path '{tmp_path}/in'"),
            (Overrides(vars={'OUTPUT2': str(new_output_2_overlaps_old)}), None, "Path 'out/new_output_1.txt' is included in path 'out'"),
            (Overrides(args={'ARG3': 'VALUE'}), None, 'Argument with name \'ARG3\' is not present in source job'),
            (Overrides(), get_cfg(), None),
            (
                    Overrides(docker_dict={'docker': 'b3p16de49mh0f9khpar3'}),
                    get_cfg(env=Environment(vars={}, docker_image='b3p16de49mh0f9khpar3', python=None)),
                    None,
            ),
            (
                    Overrides(
                        args={'ARG2': 'VALUE2_NEW'},
                        vars={'INPUT1': str(new_input_1), 'INPUT3': str(new_input_3), 'OUTPUT2': str(new_output_2)},
                        env_vars={'FOO': 'fjdiw=39m', 'BAR': '777'},
                        docker_dict={
                            'docker': {
                                'image': 'cr.yandex/foo/bar:latest',
                                'username': 'user',
                                'password': {'secret-id': 'my-secret'},
                            }
                        },
                        working_storage_dict={
                            'working-storage': {
                                'type': 'SSD',
                                'size': '3Tb',
                            },
                        },
                        cloud_instance_types=['g2.8'],
                    ),
                    get_cfg(
                        args_={'ARG2': 'VALUE2_NEW'},
                        inputs=[
                            VariablePath(path=str(new_input_1), var='INPUT1', compression_type=jobs.FileCompressionType.ZIP),
                            VariablePath(path=str(new_input_3), var='INPUT3'),
                        ],
                        outputs=[
                            VariablePath(path=new_output_2, var='OUTPUT2'),
                        ],
                        env=Environment(
                            vars={'FOO': 'fjdiw=39m', 'BAR': '777'},
                            docker_image=DockerImage(
                                url='cr.yandex/foo/bar:latest',
                                username='user',
                                password=Password(text='my-secret', is_secret=True),
                            ),
                            python=None,
                        ),
                        cloud_instance_types=['g2.8'],
                        working_storage=jobs.ExtendedWorkingStorage(
                            type=jobs.ExtendedWorkingStorage.StorageType.SSD,
                            size_gb=3072,
                        )
                    ),
                    None,
            ),
    ):
        if expected_err:
            with raises(ValueError, match=re.escape(expected_err)):
                fork_params(overrides, source_params, tmp_path)
        else:
            actual_cfg = fork_params(overrides, source_params, tmp_path)

            # Lazy attrs `_file`, `_archive_path` are hard to test, so we drop it from actual config.
            for f in actual_cfg.inputs:
                f._file = None
                f._archive_path = None

            assert actual_cfg == expected_cfg


@dataclass
class Args:
    arg: List[str] = field(default_factory=list)
    var: List[str] = field(default_factory=list)
    env_var: List[str] = field(default_factory=list)
    docker_image_id: Optional[str] = None
    docker_image_url: Optional[str] = None
    docker_image_username: Optional[str] = None
    docker_image_password_secret_id: Optional[str] = None
    working_storage_type: Optional[str] = None
    working_storage_size: Optional[str] = None
    cloud_instance_type: Optional[List[str]] = None
    name: Optional[str] = None
    desc: Optional[str] = None


def test_overrides_from_cli_args():
    for args, expected_overrides, expected_err in (
            (Args(env_var=['FOO']), None, 'Invalid name-value pair: FOO'),
            (
                    Args(docker_image_id='b3p16de49mh0f9khpar3'),
                    Overrides(docker_dict={'docker': 'b3p16de49mh0f9khpar3'}),
                    None,
            ),
            (
                    Args(
                        arg=['ARG2=VALUE2_NEW'],
                        var=['INPUT=data.txt', 'OUTPUT=result.txt'],
                        env_var=['FOO=fjdiw=39m', 'BAR=777'],
                        docker_image_url='cr.yandex/foo/bar:latest',
                        docker_image_username='user',
                        docker_image_password_secret_id='my-secret',
                        working_storage_type='SSD',
                        working_storage_size='3Tb',
                        cloud_instance_type=['g2.8'],
                    ),
                    Overrides(
                        args={'ARG2': 'VALUE2_NEW'},
                        vars={'INPUT': 'data.txt', 'OUTPUT': 'result.txt'},
                        env_vars={'FOO': 'fjdiw=39m', 'BAR': '777'},
                        docker_dict={
                            'docker': {
                                'image': 'cr.yandex/foo/bar:latest',
                                'username': 'user',
                                'password': {'secret-id': 'my-secret'},
                            },
                        },
                        working_storage_dict={
                            'working-storage': {
                                'type': 'SSD',
                                'size': '3Tb',
                            },
                        },
                        cloud_instance_types=['g2.8'],
                    ),
                    None,
            ),
    ):
        if expected_err:
            with raises(ValueError, match=re.escape(expected_err)):
                Overrides.from_cli_args(args)
        else:
            assert Overrides.from_cli_args(args) == expected_overrides


def test_get_docker_dict_from_args():
    for args, expected_dict in (
            (Args(), None),
            (Args(docker_image_id='b3p16de49mh0f9khpar3'), {'docker': 'b3p16de49mh0f9khpar3'}),
            (
                    Args(docker_image_url='cr.yandex/foo/bar:latest'),
                    {'docker': {'image': 'cr.yandex/foo/bar:latest'}}
            ),
            (
                    Args(
                        docker_image_url='cr.yandex/foo/bar:latest',
                        docker_image_username='user',
                        docker_image_password_secret_id='my-secret',
                    ),
                    {'docker': {
                        'image': 'cr.yandex/foo/bar:latest',
                        'username': 'user',
                        'password': {'secret-id': 'my-secret'}
                    }}
            )
    ):
        assert get_docker_dict_from_cli_args(args) == expected_dict

    with raises(ValueError, match='For docker image, specify either ID or URL'):
        get_docker_dict_from_cli_args(Args(docker_image_id='id', docker_image_url='url'))


def test_get_working_storage_dict_from_args():
    for args, expected_dict in (
            (Args(), None),
            (Args(working_storage_type='SSD'), {'working-storage': {'type': 'SSD'}}),
            (Args(working_storage_size='30Gb'), {'working-storage': {'size': '30Gb'}}),
            (
                    Args(working_storage_type='SSD', working_storage_size='30Gb'),
                    {'working-storage': {'size': '30Gb', 'type': 'SSD'}},
            ),
    ):
        assert get_working_storage_dict_from_cli_args(args) == expected_dict


def test_parse_name_value():
    assert parse_name_value('NAME=skf=238v=3si') == ('NAME', 'skf=238v=3si')
    assert parse_name_value('NAME=') == ('NAME', '')
    with raises(ValueError, match='Invalid name-value pair: NAME'):
        parse_name_value('NAME')


def test_parse_name_value_list():
    assert parse_name_value_list(None) == {}
    assert parse_name_value_list([]) == {}
    assert parse_name_value_list(['FOO=BAR', 'BAZ=123']) == {'FOO': 'BAR', 'BAZ': '123'}
