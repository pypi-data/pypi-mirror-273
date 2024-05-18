from typing import Union, Optional
import os
import subprocess
from simba.utils.read_write import get_fn_ext, find_all_videos_in_directory, get_video_meta_data
from simba.video_processors.roi_selector import ROISelector
from simba.utils.checks import check_ffmpeg_available, check_float, check_if_dir_exists, check_file_exist_and_readable
from simba.utils.printing import SimbaTimer, stdout_success




def video_to_bw(video_path: Union[str, os.PathLike],
                threshold: Optional[float] = 0.5) -> None:
    """
    Convert video to black and white using passed threshold.

    .. video:: _static/img/video_to_bw.webm
       :loop:

    :param Union[str, os.PathLike] video_path: Path to the video
    :param Optional[float] threshold: Value between 0 and 1. Lower values gives more white and vice versa.
    :return: None.

    :example:
    >>> video_to_bw(video_path='/Users/simon/Downloads/1_LH_clipped_cropped_eq_20240515135926.mp4', threshold=0.02)
    """

    check_float(name=f'{video_to_bw.__name__} threshold', value=threshold, min_value=0, max_value=1.0)
    threshold = int(255 * threshold)
    check_ffmpeg_available(raise_error=True)
    timer = SimbaTimer(start=True)
    _ = get_video_meta_data(video_path=video_path)
    dir, video_name, ext = get_fn_ext(video_path)
    save_path = os.path.join(dir, f'{video_name}_bw{ext}')
    cmd = f"ffmpeg -i '{video_path}' -vf \"format=gray,geq=lum_expr='if(lt(lum(X,Y),{threshold}),0,255)'\" -pix_fmt yuv420p '{save_path}' -y"
    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
    timer.stop_timer()
    stdout_success(msg=f'Video {video_name} converted.', elapsed_time=timer.elapsed_time_str)


video_to_bw(video_path='/Users/simon/Downloads/1_LH_clipped_cropped_eq_20240515135926.mp4', threshold=0.02)
