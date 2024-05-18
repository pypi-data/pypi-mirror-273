import os
import random
from os import path
from contextlib import nullcontext
from sys import platform
import torch
from PIL import Image, ImageOps
from .util import timer
from .setting import cache_path


is_mac = platform == "darwin"


def get_device():
    return (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )


def resize(img: Image.Image):
    maxs = max(img.size[0], img.size[1])
    if maxs < 900:
        return img
    ratio = 800 / maxs
    hsize = int((float(img.size[1]) * float(ratio)))
    wsize = int((float(img.size[0]) * float(ratio)))
    return img.resize((wsize, hsize))


def should_use_fp16():
    if is_mac:
        return True

    gpu_props = torch.cuda.get_device_properties("cuda")

    if gpu_props.major < 6:
        return False

    nvidia_16_series = ["1660", "1650", "1630"]

    for x in nvidia_16_series:
        if x in gpu_props.name:
            return False

    return True


def load_sdxl_refine():
    import torch
    from diffusers import StableDiffusionXLImg2ImgPipeline, LCMScheduler, AutoencoderKL
    from diffusers.utils import load_image

    lcm_lora_id = "latent-consistency/lcm-lora-sdv1-5"
    vae = AutoencoderKL.from_pretrained(
        "madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16
    )
    pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        cache_dir=cache_path,
        safety_checker=None,
        resume_download=True,
        vae=vae,
    )
    # pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    # pipe.load_lora_weights(lcm_lora_id)
    # pipe.fuse_lora()
    pipe.enable_vae_slicing()
    pipe.enable_vae_tiling()
    device = get_device()
    pipe.to(device)

    def infer(
        prompt,
        image,
        num_inference_steps=1,
        guidance_scale=1,
        strength=0.9,
        seed=random.randrange(0, 2**63),
    ):
        image = load_image(image).convert("RGB")
        print(image)
        generator = torch.Generator(device=pipe.device).manual_seed(seed)
        with torch.inference_mode():
            with torch.autocast("cuda") if device == "cuda" else nullcontext():
                with timer("inference"):
                    return pipe(
                        prompt=prompt,
                        image=image,
                        generator=generator,
                        # https://huggingface.co/docs/diffusers/main/en/using-diffusers/lcm#image-to-image
                        guidance_scale=guidance_scale,
                    ).images[0]

    return infer


def load_sdxl_t2i():
    import torch
    from diffusers import DiffusionPipeline, LCMScheduler
    from diffusers.utils import load_image

    pipe = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
        cache_dir=cache_path,
        safety_checker=None,
        resume_download=True,
    )

    device = get_device()
    pipe.to(device)
    # set scheduler
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    # load LCM-LoRA
    pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")
    pipe.fuse_lora()

    def infer(
        prompt,
        image,
        num_inference_steps=4,
        guidance_scale=1,
        strength=0.9,
        seed=random.randrange(0, 2**63),
    ):
        generator = torch.Generator(device=pipe.device).manual_seed(seed)
        with torch.inference_mode():
            with torch.autocast("cuda") if device == "cuda" else nullcontext():
                with timer("inference"):
                    return pipe(
                        prompt=prompt,
                        generator=generator,
                        num_inference_steps=num_inference_steps,
                        # https://huggingface.co/docs/diffusers/main/en/using-diffusers/lcm#image-to-image
                        guidance_scale=guidance_scale,
                    ).images[0]

    return infer


def load_sd_ip_adapter(model_id="dreamshaper_8", safety_checker=True):
    """模型太大了，要多下载2GB+ 暂时先不弄"""
    from diffusers import StableDiffusionPipeline, LCMScheduler
    import torch
    from diffusers.utils import load_image

    # model_id =  "sd-dreambooth-library/herge-style"

    pipe = StableDiffusionPipeline.from_single_file(
        path.join(cache_path, model_id + ".safetensors"),
        torch_dtype=torch.float16,
        variant="fp16",
        load_safety_checker=safety_checker,
        local_files_only=True,
        original_config_file=os.path.join(cache_path, "v1-inference.yaml"),
    )

    pipe.load_ip_adapter(
        "h94/IP-Adapter",
        subfolder="models",
        weight_name="ip-adapter_sd15.bin",
        torch_dtype=torch.float16,
        local_files_only=True,
    )
    pipe.load_lora_weights(
        os.path.join(cache_path, "lora", "pytorch_lora_weights.safetensors")
    )
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    pipe.enable_model_cpu_offload()

    device = get_device()
    pipe.to(device=device)

    generator = torch.Generator()

    def infer(
        prompt,
        image,
        num_inference_steps=4,
        guidance_scale=1,
        strength=0.9,
        seed=random.randrange(0, 2**63),
        invert_color=True,
        negative_prompt=None,
    ):
        image = load_image(image)
        image = resize(image)

        with torch.inference_mode():
            with torch.autocast("cuda") if device == "cuda" else nullcontext():
                with timer("inference"):
                    return pipe(
                        prompt=prompt,
                        ip_adapter_image=image,
                        generator=generator.manual_seed(seed),
                        num_inference_steps=num_inference_steps,
                        guidance_scale=guidance_scale,
                        negative_prompt=negative_prompt,
                    ).images[0]

    return infer


def load_sd_adapter(model_id="dreamshaper_8", safety_checker=True, lora_weights=[]):
    from diffusers import (
        StableDiffusionAdapterPipeline,
        AutoencoderKL,
        AutoPipelineForImage2Image,
        LCMScheduler,
        StableDiffusionXLPipeline,
        T2IAdapter,
    )
    from diffusers.utils import load_image
    from diffusers.loaders.lora import LoraLoaderMixin

    if not is_mac:
        torch.backends.cuda.matmul.allow_tf32 = True

    use_fp16 = should_use_fp16()

    adapter = T2IAdapter.from_pretrained(
        "TencentARC/t2iadapter_sketch_sd15v2",
        torch_dtype=torch.float16,
        local_files_only=True,
    )

    if use_fp16:
        pipe = StableDiffusionAdapterPipeline.from_single_file(
            path.join(cache_path, model_id + ".safetensors"),
            cache_dir=cache_path,
            torch_dtype=torch.float16,
            variant="fp16",
            load_safety_checker=safety_checker,
            resume_download=True,
            adapter=adapter,
            local_files_only=True,
            original_config_file=os.path.join(cache_path, "v1-inference.yaml"),
        )
    else:
        pipe = StableDiffusionAdapterPipeline.from_single_file(
            path.join(cache_path, model_id + ".safetensors"),
            cache_dir=cache_path,
            torch_dtype=torch.float16,
            load_safety_checker=safety_checker,
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

    # adpter 加 lora 效果不太好，会互相冲突
    # if len(lora_weights):
    #     for i in range(len(lora_weights)):
    #         pipe.load_lora_weights(os.path.join(cache_path, "lora", lora_weights[i] + ".safetensors"))
    #         pipe.fuse_lora()

    generator = torch.Generator()

    def infer(
        prompt,
        image,
        num_inference_steps=4,
        guidance_scale=1,
        strength=0.9,
        seed=random.randrange(0, 2**63),
        invert_color=True,
        negative_prompt=None,
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


def load_ssd1b(safety_checker=True):
    from diffusers import (
        AutoPipelineForText2Image,
        LCMScheduler,
        AutoPipelineForImage2Image,
    )
    from diffusers.utils import load_image

    text_pipe = AutoPipelineForText2Image.from_pretrained(
        "segmind/SSD-1B",
        torch_dtype=torch.float16,
        variant="fp16",
        cache_dir=cache_path,
        load_safety_checker=safety_checker,
        resume_download=True,
        local_files_only=True,
    )

    device = get_device()
    text_pipe.to(device)
    # set scheduler
    text_pipe.scheduler = LCMScheduler.from_config(text_pipe.scheduler.config)
    # load LCM-LoRA
    text_pipe.load_lora_weights(
        os.path.join(cache_path, "lora", "pytorch_lora_weights_ssd1b.safetensors"),
        local_files_only=True,
    )
    text_pipe.fuse_lora()

    img_pipe = AutoPipelineForImage2Image.from_pipe(text_pipe)

    def infer(
        prompt,
        image,
        num_inference_steps=4,
        guidance_scale=1,
        strength=0.9,
        seed=random.randrange(0, 2**63),
        mode="i2i",
        negative_prompt="",
        invert_color=True,
    ):
        generator = torch.Generator(device=text_pipe.device).manual_seed(seed)
        with torch.inference_mode():
            with torch.autocast("cuda") if device == "cuda" else nullcontext():
                with timer("inference"):
                    if mode == "i2i":
                        return img_pipe(
                            prompt=prompt,
                            image=resize(load_image(image)),
                            generator=generator,
                            num_inference_steps=num_inference_steps,
                            # https://huggingface.co/docs/diffusers/main/en/using-diffusers/lcm#image-to-image
                            guidance_scale=guidance_scale,
                            strength=strength,
                            negative_prompt=negative_prompt,
                        ).images[0]
                    elif mode == "t2i":
                        return text_pipe(
                            prompt=prompt,
                            width=800,
                            height=800,
                            generator=generator,
                            num_inference_steps=num_inference_steps,
                            # https://huggingface.co/docs/diffusers/main/en/using-diffusers/lcm#image-to-image
                            guidance_scale=guidance_scale,
                            negative_prompt=negative_prompt,
                        ).images[0]

    return infer


def check_safetensors_exist(model_id):
    filename = os.path.join(cache_path, model_id + ".safetensors")
    return os.path.isfile(filename)


def load_single_file(model_id, safety_checker, lora_weights=[]):
    from diffusers import (
        StableDiffusionImg2ImgPipeline,
        StableDiffusionPipeline,
        LCMScheduler,
    )
    from diffusers.utils import load_image

    if not check_safetensors_exist(model_id):
        raise ValueError("safetensors file not exist")

    if not is_mac:
        torch.backends.cuda.matmul.allow_tf32 = True

    use_fp16 = should_use_fp16()

    if use_fp16:
        txt2img_pipe = StableDiffusionPipeline.from_single_file(
            os.path.join(cache_path, model_id + ".safetensors"),
            cache_dir=cache_path,
            torch_dtype=torch.float16,
            variant="fp16",
            load_safety_checker=safety_checker,
            local_files_only=True,
            use_safetensors=True,
            original_config_file=os.path.join(cache_path, "v1-inference.yaml"),
        )
    else:
        txt2img_pipe = StableDiffusionPipeline.from_single_file(
            os.path.join(cache_path, model_id + ".safetensors"),
            cache_dir=cache_path,
            load_safety_checker=safety_checker,
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
                os.path.join(cache_path, "lora", lora_weights[i] + ".safetensors")
            )
            txt2img_pipe.fuse_lora()
    generator = torch.Generator()

    img2img_pipe = StableDiffusionImg2ImgPipeline(**txt2img_pipe.components)
    img2img_pipe.disable_lora()
    img2img_pipe.load_lora_weights(
        os.path.join(cache_path, "lora", "pytorch_lora_weights.safetensors")
    )
    img2img_pipe.fuse_lora()

    def infer(
        prompt,
        image,
        num_inference_steps=5,
        guidance_scale=2,
        strength=0.9,
        invert_color=True,
        negative_prompt=None,
        seed=random.randrange(0, 2**63),
        mode="i2i",
    ):
        with torch.inference_mode():
            with torch.autocast("cuda") if device == "cuda" else nullcontext():
                with timer("inference"):
                    if mode == "i2i":
                        return img2img_pipe(
                            prompt=prompt,
                            image=resize(load_image(image)),
                            # generator=generator.manual_seed(seed),
                            generator=generator,
                            num_inference_steps=num_inference_steps,
                            guidance_scale=guidance_scale,
                            strength=strength,
                            negative_prompt=negative_prompt,
                        ).images[0]
                    elif mode == "t2i":
                        return txt2img_pipe(
                            prompt=prompt,
                            # generator=generator.manual_seed(seed),
                            generator=generator,
                            num_inference_steps=num_inference_steps,
                            guidance_scale=guidance_scale,
                            negative_prompt=negative_prompt,
                        ).images[0]
                    else:
                        raise ValueError("mode not support")

    return infer


def load_models_backend(
    model_id="dreamshaper_8",
    technique="safetensors",
    safety_checker=True,
    lora_weights=[],
):
    if technique == "sd1.5_adapter":
        return load_sd_adapter(model_id, safety_checker, lora_weights)
    elif technique == "ssd_1b_t2i":
        return load_ssd1b(safety_checker)
    elif technique == "safetensors":
        return load_single_file(model_id, safety_checker, lora_weights)
