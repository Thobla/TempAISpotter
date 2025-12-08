import torch
from PoseFormerV2.lib.models.poseformerV2 import PoseTransformerV2

def load_poseformer_33x3(ckpt_path, device="cpu"):
    model = PoseTransformerV2(num_joints=33, in_chans=3)
    checkpoint = torch.load(ckpt_path, map_location=device)
    state_dict = checkpoint["model"]

    # remove incompatible layers (input projection)
    for key in list(state_dict.keys()):
        if "patch_embed.proj.weight" in key:
            del state_dict[key]
    model.load_state_dict(state_dict, strict=False)
    model.head = torch.nn.Identity()
    model.eval()
    return model


# Might delete this file