import os
import cv2
from insightface.app import FaceAnalysis
from insightface.utils import face_align
import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler, AutoencoderKL
from PIL import Image
from .base_model import AIModel
from .setting import cache_path

from ip_adapter.ip_adapter_faceid import IPAdapterFaceID


def get_image_embeds(url):
    app = FaceAnalysis(
        name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
    )
    app.prepare(ctx_id=0, det_size=(640, 640))

    # image = cv2.imread(url)
    # faces = app.get(image)
    # faceid_embeds = torch.from_numpy(faces[0].normed_embedding).unsqueeze(0)
    # face_image = face_align.norm_crop(image, landmark=faces[0].kps, image_size=224)
    # return {"faceid_embeds": faceid_embeds, "face_image": face_image}

    images = ["me.jpg", "me.jpg", "me.jpg", "me.jpg", "me.jpg"]

    faceid_embeds = []
    for image in images:
        image = cv2.imread(image)
        faces = app.get(image)
        faceid_embeds.append(
            torch.from_numpy(faces[0].normed_embedding).unsqueeze(0).unsqueeze(0)
        )
    faceid_embeds = torch.cat(faceid_embeds, dim=1)
    return {"faceid_embeds": faceid_embeds}


class DiffusionModel(AIModel):
    name = "stable_diffusion"
    model = None

    def __init__(self) -> None:
        super().__init__()

    def load_model(self, args):
        image_encoder_path = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"
        ip_ckpt = os.path.join(cache_path, "ip-adapter-faceid-portrait_sd15.bin")
        device = "cpu"

        noise_scheduler = DDIMScheduler(
            num_train_timesteps=1000,
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
            steps_offset=1,
        )
        pipe = StableDiffusionPipeline.from_single_file(
            os.path.join(cache_path, "dreamshaper_8.safetensors"),
            cache_dir=cache_path,
            torch_dtype=torch.float16,
            variant="fp16",
            local_files_only=True,
            use_safetensors=True,
            original_config_file=os.path.join(cache_path, "v1-inference.yaml"),
            feature_extractor=None,
            safety_checker=None,
            scheduler=noise_scheduler,
        )
        # load ip-adapter
        self.model = IPAdapterFaceID(pipe, ip_ckpt, device, num_tokens=16)

    def run_model(self, args):
        # generate image
        prompt = "photo of a man in black suit in a garden"
        negative_prompt = (
            "monochrome, lowres, bad anatomy, worst quality, low quality, blurry"
        )

        face_args = get_image_embeds(args.get("origin_image"))
        images = self.model.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            faceid_embeds=face_args["faceid_embeds"],
            s_scale=1.0,
            num_samples=4,
            width=512,
            height=512,
            num_inference_steps=30,
            seed=2023,
        )
        print(images)
        for m in images:
            m.show()
        return
