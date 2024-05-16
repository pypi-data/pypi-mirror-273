import torch
import numpy as np

def get_num_frames(pose_tensor3,pose_tensor4):
    average_distance_per_frame = 0.0217
    vector_diff = pose_tensor3[27] - pose_tensor4[27]
    euclidean_distance = np.linalg.norm(vector_diff.cpu(), ord=2)
    number_of_frame_interpolation = ((euclidean_distance / average_distance_per_frame)/1.25)+6
    return int(number_of_frame_interpolation)
 
# This function adds a portion of the difference between the poses to the start pose, so interpolating from start to the end
def interpolate_between_poses_small_tensor(pose_results_start,pose_results_end,portion):
    output_pose_results = pose_results_start + (pose_results_end - pose_results_start) * portion
    return output_pose_results

## New Interpolate Code
def interpolate_between_poses(start_pose_result,end_pose_result):
    filler_n = get_num_frames(start_pose_result,end_pose_result)
    # For this many interpolation steps, slowly interpolate from one pose to the next in the keypoint space
    interpolated_pose_results = torch.Tensor().to(end_pose_result.device)
    for s in range(filler_n):
        pose_results_inter_s = interpolate_between_poses_small_tensor(start_pose_result,end_pose_result, (s + 1) / filler_n)
        interpolated_pose_results = torch.cat((interpolated_pose_results,pose_results_inter_s.unsqueeze(0)))
    return interpolated_pose_results
