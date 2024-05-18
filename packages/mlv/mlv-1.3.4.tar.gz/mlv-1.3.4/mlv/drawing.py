from base64 import b64decode
from contextlib import nullcontext
from io import BytesIO
import time
import platform
import torch
import os
import random
from PIL import Image, ImageOps
from .mps_workaround import has_mps

is_mac = platform == "darwin"
cache_path = os.getenv("APP_MODEL_PATH", "")
output_path = os.getenv("APP_OUTPUT_PATH", "")
model_path = os.getenv("APP_MODEL_PATH", "")

# This is for load mps_workaround file to packaging
print("has mps", has_mps)


def dataurl_to_image(data_url):
    _, encoded = data_url.split("base64,")
    data = b64decode(encoded)
    o = BytesIO(data)
    m = Image.open(o)
    return m


def resize(img: Image.Image):
    maxs = max(img.size[0], img.size[1])
    if maxs < 900:
        return img
    ratio = 512 / maxs
    hsize = int((float(img.size[1]) * float(ratio)))
    wsize = int((float(img.size[0]) * float(ratio)))
    return img.resize((wsize, hsize))


def get_device():
    return (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )


class timer:
    def __init__(self, method_name="timed process"):
        self.method = method_name

    def __enter__(self):
        self.start = time.time()
        print(f"{self.method} starts")

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        print(f"{self.method} took {str(round(end - self.start, 2))}s")


def load_model_adapter(model, safety_checker, lora_weights=[]):
    from diffusers import (
        StableDiffusionAdapterPipeline,
        LCMScheduler,
        T2IAdapter,
    )

    from diffusers.loaders.single_file_utils import (
        create_diffusers_clip_model_from_ldm,
        load_single_file_checkpoint,
    )
    from diffusers.utils import load_image
    from transformers import CLIPTextConfig, CLIPTokenizer, CLIPTextModel

    adapter = T2IAdapter.from_pretrained(
        # "TencentARC/t2iadapter_sketch_sd15v2",
        os.path.join(cache_path, "adapter"),
        torch_dtype=torch.float16,
        local_files_only=True,
        cache_dir=cache_path,
    )
    checkpoint = load_single_file_checkpoint(
        os.path.join(cache_path, model), local_files_only=True
    )
    text_encoder = create_diffusers_clip_model_from_ldm(
        CLIPTextModel,
        checkpoint,
        config=os.path.join(cache_path, "clip"),
        local_files_only=True,
        torch_dtype=torch.float16,
        # is_legacy_loading=True,
    )
    tokenizer = CLIPTokenizer.from_pretrained(
        os.path.join(cache_path, "clip"), local_files_only=True
    )
    pipe = StableDiffusionAdapterPipeline.from_single_file(
        os.path.join(cache_path, model),
        text_encoder=text_encoder,
        tokenizer=tokenizer,
        cache_dir=cache_path,
        torch_dtype=torch.float16,
        variant="fp16",
        resume_download=True,
        adapter=adapter,
        local_files_only=True,
        original_config_file=os.path.join(cache_path, "v1-inference.yaml"),
    )

    device = get_device()
    pipe.to(device=device)

    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    pipe.load_lora_weights(
        os.path.join(cache_path, "lora", "pytorch_lora_weights.safetensors")
    )
    pipe.fuse_lora()

    generator = torch.Generator()

    def infer(
        prompt,
        image,
        num_inference_steps=3,
        guidance_scale=2,
        strength=0.9,
        seed=random.randrange(0, 2**63),
        invert_color=True,
        negative_prompt=None,
        mode=None,
    ):
        image = load_image(image)
        image = resize(image)
        if invert_color:
            image = ImageOps.invert(image)
        image = image.convert("L")

        with torch.inference_mode():
            with torch.autocast("cuda") if device == "cuda" else nullcontext():
                with timer("inference"):
                    return pipe(
                        prompt=prompt,
                        image=image,
                        generator=generator.manual_seed(seed),
                        num_inference_steps=num_inference_steps,
                        guidance_scale=guidance_scale,
                        negative_prompt=negative_prompt,
                    ).images[0]

    return infer


def load_model(model, safety_checker, lora_weights=[]):
    from diffusers import (
        StableDiffusionImg2ImgPipeline,
        StableDiffusionPipeline,
        LCMScheduler,
    )
    from diffusers.loaders.single_file_utils import (
        create_diffusers_clip_model_from_ldm,
        load_single_file_checkpoint,
    )
    from diffusers.utils import load_image
    from transformers import CLIPTextConfig, CLIPTokenizer, CLIPTextModel

    # if not check_safetensors_exist(model_id):
    #     raise ValueError("safetensors file not exist")

    config_name = os.path.join(cache_path, "clip")
    checkpoint = load_single_file_checkpoint(
        os.path.join(cache_path, model), local_files_only=True
    )
    text_encoder = create_diffusers_clip_model_from_ldm(
        CLIPTextModel,
        checkpoint,
        config=os.path.join(cache_path, "clip"),
        local_files_only=True,
        torch_dtype=torch.float16,
    )
    tokenizer = CLIPTokenizer.from_pretrained(config_name, local_files_only=True)
    txt2img_pipe = StableDiffusionPipeline.from_single_file(
        os.path.join(cache_path, model),
        cache_dir=cache_path,
        torch_dtype=torch.float16,
        text_encoder=text_encoder,
        tokenizer=tokenizer,
        variant="fp16",
        local_files_only=True,
        use_safetensors=True,
        original_config_file=os.path.join(cache_path, "v1-inference.yaml"),
    )

    device = get_device()
    txt2img_pipe.to(device=device)
    txt2img_pipe.scheduler = LCMScheduler.from_config(txt2img_pipe.scheduler.config)
    txt2img_pipe.load_lora_weights(
        os.path.join(cache_path, "lora", "pytorch_lora_weights.safetensors")
    )
    txt2img_pipe.fuse_lora()
    if len(lora_weights):
        for i in range(len(lora_weights)):
            txt2img_pipe.load_lora_weights(
                os.path.join(cache_path, "lora", lora_weights[i])
            )
            txt2img_pipe.fuse_lora()
    generator = torch.Generator()

    img2img_pipe = StableDiffusionImg2ImgPipeline(**txt2img_pipe.components)

    def infer(
        prompt,
        image,
        num_inference_steps=5,
        guidance_scale=2,
        strength=0.9,
        negative_prompt=None,
        mode="i2i",
    ):
        with torch.inference_mode():
            with torch.autocast("cuda") if device == "cuda" else nullcontext():
                with timer("inference"):
                    if mode == "i2i":
                        return img2img_pipe(
                            prompt=prompt,
                            image=resize(load_image(image)),
                            generator=generator.manual_seed(int(time.time())),
                            num_inference_steps=num_inference_steps,
                            guidance_scale=guidance_scale,
                            strength=strength,
                            negative_prompt=negative_prompt,
                        ).images[0]
                    elif mode == "t2i":
                        return txt2img_pipe(
                            prompt=prompt,
                            generator=generator.manual_seed(int(time.time())),
                            num_inference_steps=num_inference_steps,
                            guidance_scale=guidance_scale,
                            negative_prompt=negative_prompt,
                        ).images[0]
                    else:
                        raise ValueError("mode not support")

    return infer


class Model:
    name = "drawing_ai"
    model = None

    def __init__(self) -> None:
        super().__init__()

    def load_model(self, args):
        with timer("load sd model"):
            self.model = load_model(
                args.get("model"),
                args.get("safety_checker", False),
                args.get("lora", []),
            )

    def run_model(self, args):
        mode = args.get("mode")
        if not mode:
            raise ValueError("model args missing")
        image = args.get("image")
        prompt = args.get("prompt")
        print("good", image)
        if image:
            if image.startswith("data:"):
                image = dataurl_to_image(args.get("image"))
            else:
                image = Image.open(image)
        out_image_path = os.path.join(output_path, "sd_image.jpg")

        self.model(
            prompt,
            image,
            mode=mode,
            num_inference_steps=args.get("num_inference_steps", 4),
            guidance_scale=args.get("guidance_scale", 2),
            strength=args.get("strength", 0.9),
            negative_prompt=args.get("negative_prompt", "ugly, disform, bad hand"),
        ).save(out_image_path)
        return {"result": out_image_path}
