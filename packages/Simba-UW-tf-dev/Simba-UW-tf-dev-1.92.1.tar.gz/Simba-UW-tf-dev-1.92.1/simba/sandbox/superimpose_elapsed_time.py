from typing import Union, Optional
import os
import subprocess
from simba.utils.read_write import get_fn_ext, find_all_videos_in_directory, get_video_meta_data
from simba.video_processors.roi_selector import ROISelector
from simba.utils.checks import check_ffmpeg_available, check_float, check_if_dir_exists, check_file_exist_and_readable, check_str, check_int
from simba.utils.printing import SimbaTimer, stdout_success
from simba.utils.errors import InvalidInputError


def superimpose_elapsed_time(video_path: Union[str, os.PathLike],
                             font_size: Optional[int] = 30,
                             font_color: Optional[str] = 'white',
                             font_border_color: Optional[str] = 'black',
                             font_border_width: Optional[int] = 2,
                             position: Optional[Literal['top_left', 'top_right', 'bottom_left', 'bottom_right', 'middle_top', 'middle_bottom']] = 'top_left',
                             save_dir: Optional[Union[str, os.PathLike]] = None) -> None:
    """
    Superimposes elapsed time on the given video file(s) and saves the modified video(s).

    .. video:: _static/img/superimpose_elapsed_time.webm
       :loop:

    :param Union[str, os.PathLike] video_path: Path to the input video file or directory containing video files.
    :param Optional[int] font_size: Font size for the elapsed time text. Default 30.
    :param Optional[str] font_color:  Font color for the elapsed time text. Default white
    :param Optional[str] font_border_color: Font border color for the elapsed time text. Default black.
    :param Optional[int] font_border_width: Font border width for the elapsed time text in pixels. Default 2.
    :param Optional[Literal['top_left', 'top_right', 'bottom_left', 'bottom_right', 'middle_top', 'middle_bottom']] position: Position where the elapsed time text will be superimposed. Default ``top_left``.
    :param Optional[Union[str, os.PathLike]] save_dir: Directory where the modified video(s) will be saved. If not provided, the directory of the input video(s) will be used.
    :return: None

    :example:
    >>> superimpose_elapsed_time(video_path='/Users/simon/Desktop/envs/simba/troubleshooting/mouse_open_field/project_folder/videos/test_4/1.mp4', position='middle_top', font_color='black', font_border_color='pink', font_border_width=5, font_size=30)
    """

    check_ffmpeg_available(raise_error=True)
    timer = SimbaTimer(start=True)
    POSITIONS = ['top_left', 'top_right', 'bottom_left', 'bottom_right', 'middle_top', 'middle_bottom']
    check_str(name=f'{superimpose_elapsed_time.__name__} position', value=position, options=POSITIONS)
    check_int(name=f'{superimpose_elapsed_time.__name__} font_size', value=font_size, min_value=1)
    check_int(name=f'{superimpose_elapsed_time.__name__} font_border_width', value=font_border_width, min_value=1)
    font_color = ''.join(filter(str.isalnum, font_color)).lower()
    font_border_color = ''.join(filter(str.isalnum, font_border_color)).lower()
    if os.path.isfile(video_path):
        video_paths = [video_path]
    elif os.path.isdir(video_path):
        video_paths = list(find_all_videos_in_directory(directory=video_path, as_dict=True, raise_error=True).values())
    else:
        raise InvalidInputError(msg=f'{video_path} is not a valid file path or a valid directory path', source=superimpose_elapsed_time.__name__)
    if save_dir is not None:
        check_if_dir_exists(in_dir=save_dir)
    else:
        save_dir = os.path.dirname(video_paths[0])
    for file_cnt, video_path in enumerate(video_paths):
        _, video_name, ext = get_fn_ext(video_path)
        print(f'Superimposing time {video_name} (Video {file_cnt + 1}/{len(video_paths)})...')
        save_path = os.path.join(save_dir, f'{video_name}_time_superimposed{ext}')
        if position == POSITIONS[0]:
            cmd = f"ffmpeg -i '{video_path}' -vf \"drawtext=fontfile=Arial.ttf:text='%{{pts\:hms}}.%{{eif\:mod(n\\,1000)\\:d\\:3}}':x=5:y=5:fontsize={font_size}:fontcolor={font_color}:borderw={font_border_width}:bordercolor={font_border_color}\" -c:a copy '{save_path}' -loglevel error -stats -hide_banner -y"
        elif position == POSITIONS[1]:
            cmd = f"ffmpeg -i '{video_path}' -vf \"drawtext=fontfile=Arial.ttf:text='%{{pts\:hms}}.%{{eif\:mod(n\\,1000)\\:d\\:3}}':x=(w-tw-5):y=5:fontsize={font_size}:fontcolor={font_color}:borderw={font_border_width}:bordercolor={font_border_color}\" -c:a copy '{save_path}' -loglevel error -stats -hide_banner -y"
        elif position == POSITIONS[2]:
            cmd = f"ffmpeg -i '{video_path}' -vf \"drawtext=fontfile=Arial.ttf:text='%{{pts\:hms}}.%{{eif\:mod(n\\,1000)\\:d\\:3}}':x=5:y=(h-th-5):fontsize={font_size}:fontcolor={font_color}:borderw={font_border_width}:bordercolor={font_border_color}\" -c:a copy '{save_path}' -loglevel error -stats -hide_banner -y"
        elif position == POSITIONS[3]:
            cmd = f"ffmpeg -i '{video_path}' -vf \"drawtext=fontfile=Arial.ttf:text='%{{pts\:hms}}.%{{eif\:mod(n\\,1000)\\:d\\:3}}':x=(w-tw-5):y=(h-th-5):fontsize={font_size}:fontcolor={font_color}:borderw={font_border_width}:bordercolor={font_border_color}\" -c:a copy '{save_path}' -loglevel error -stats -hide_banner -y"
        elif position == POSITIONS[4]:
            cmd = f"ffmpeg -i '{video_path}' -vf \"drawtext=fontfile=Arial.ttf:text='%{{pts\:hms}}.%{{eif\:mod(n\\,1000)\\:d\\:3}}':x=(w-tw)/2:y=10:fontsize={font_size}:fontcolor={font_color}:borderw={font_border_width}:bordercolor={font_border_color}\" -c:a copy '{save_path}' -loglevel error -stats -hide_banner -y"
        else:
            cmd = f"ffmpeg -i '{video_path}' -vf \"drawtext=fontfile=Arial.ttf:text='%{{pts\:hms}}.%{{eif\:mod(n\\,1000)\\:d\\:3}}':x=(w-tw)/2:y=(h-th-10):fontsize={font_size}:fontcolor={font_color}:borderw={font_border_width}:bordercolor={font_border_color}\" -c:a copy '{save_path}' -loglevel error -stats -hide_banner -y"
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
    timer.stop_timer()
    stdout_success(msg=f'Super-imposed time on {len(video_paths)} video(s), saved in {save_dir}', elapsed_time=timer.elapsed_time_str)


# superimpose_elapsed_time(video_path='/Users/simon/Desktop/envs/simba/troubleshooting/mouse_open_field/project_folder/videos/test_4/1.mp4',
#                          position='middle_top',
#                          font_color='black',
#                          font_border_color='pink',
#                          font_border_width=5,
#                          font_size=30)