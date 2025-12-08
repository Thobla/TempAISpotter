import torch
from PoseFormerV2.lib.models.poseformerV2 import PoseTransformerV2

class PoseFormerV2Inference:
    def __init__(self, ckpt_path, device="cpu"):
        self.device = device
        self.model = PoseTransformerV2(num_joints=17, in_chans=2)
        checkpoint = torch.load(ckpt_path, map_location=device)
        self.model.load_state_dict(checkpoint['model'], strict=False)
        self.model.head = torch.nn.Identity()  # use as feature extractor
        self.model.eval()

    def get_embedding(self, pose_seq):
        x = torch.tensor(pose_seq, dtype=torch.float32).unsqueeze(0).to(self.device)
        with torch.no_grad():
            emb = self.model(x)
        return emb.cpu().numpy()
