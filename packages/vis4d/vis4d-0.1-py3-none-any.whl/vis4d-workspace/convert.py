import torch

ckpt = torch.load("./last.ckpt")

lstm_ckpt = {}
lstm_state_dict = {}

new_ckpt = {}
new_state_dict = {}
for k, v in ckpt["state_dict"].items():
    new_k = k

    # if "qdtrack" in k:
    #     new_k = k.replace("qdtrack.", "qdtrack_head.")

    # if "detector.backbone.mm_backbone" in k:
    #     new_k = new_k.replace("detector.backbone.mm_backbone", "basemodel")
    # elif "detector.backbone.neck.mm_neck.lateral_convs" in k:
    #     new_k = new_k.replace(
    #         "detector.backbone.neck.mm_neck.lateral_convs",
    #         "fpn.inner_blocks",
    #     )
    #     if "conv" in new_k:
    #         new_k = new_k.replace("conv", "0")
    #     elif "fc" in new_k:
    #         new_k = new_k.replace("fc", "0")
    # elif "detector.backbone.neck.mm_neck.fpn_convs" in k:
    #     new_k = new_k.replace(
    #         "detector.backbone.neck.mm_neck.fpn_convs", "fpn.layer_blocks"
    #     )
    #     if "conv" in new_k:
    #         new_k = new_k.replace("conv", "0")
    #     elif "fc" in new_k:
    #         new_k = new_k.replace("fc", "0")
    # elif "detector.rpn_head.mm_dense_head" in k:
    #     new_k = new_k.replace(
    #         "detector.rpn_head.mm_dense_head", "faster_rcnn_head.rpn_head"
    #     )
    #     if "rpn_reg" in new_k:
    #         new_k = new_k.replace("rpn_reg", "rpn_box")
    # elif "detector.roi_head.mm_roi_head" in k:
    #     new_k = new_k.replace(
    #         "detector.roi_head.mm_roi_head", "faster_rcnn_head.roi_head"
    #     )
    #     if "bbox_head" in new_k:
    #         new_k = new_k.replace(".bbox_head", "")
    #     if "faster_rcnn_head.roi_head.shared_convs" in new_k:
    #         new_k = new_k.replace(".conv", "")
    # elif "similarity_head" in k:
    #     new_k = f"qdtrack_head.{new_k}"

    if "track_graph" in k:
        new_k = new_k.replace("track_graph.lstm_model.", "")
        lstm_state_dict[new_k] = v
        continue

    # new_state_dict[new_k] = v

# new_ckpt["state_dict"] = new_state_dict
# torch.save(new_ckpt, "./test.pt")

lstm_ckpt["state_dict"] = lstm_state_dict
torch.save(lstm_ckpt, "./test_lstm.pt")
