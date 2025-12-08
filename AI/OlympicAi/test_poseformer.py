from AI.PoseFormerV2.inference import PoseFormerV2Inference
from AI.PoseFormerV2.preprocess import PosePreprocessor
import numpy as np

poseformer = PoseFormerV2Inference("AI/PoseFormerV2/checkpoints/poseformerv2_h36m.pth")
preproc = PosePreprocessor()

fake_pose = np.random.rand(100, 33, 3)  # mock MediaPipe output
pose_17 = preproc.select_17_keypoints(fake_pose)
norm = preproc.normalize(pose_17)
emb = poseformer.get_embedding(norm)

print("Embedding shape:", emb.shape)
