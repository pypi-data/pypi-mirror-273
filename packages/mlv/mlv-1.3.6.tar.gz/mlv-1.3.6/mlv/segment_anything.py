from os import path
from PIL import Image
import numpy
from .util import timer, dataurl_to_image
from .setting import output_path
from .base_model import AIModel

from segment_anything import (
    SamPredictor,
    SamAutomaticMaskGenerator,
    sam_model_registry,
)


def cutout(origin, mask):
    import cv2

    image = cv2.imread(origin)
    mask = cv2.imread(mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # add alpha channel
    new_img = cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGBA)
    new_img[:, :, 3] = mask

    return Image.fromarray(new_img)


def segment(sam, image, point=[]):
    image = numpy.asarray(image)
    with timer("segment inference"):
        files = []
        if point and len(point):
            predictor = SamPredictor(sam)
            predictor.set_image(image)
            masks, _, _ = predictor.predict(
                point_coords=numpy.array([x[0] for x in point]),
                point_labels=numpy.array([x[1] for x in point]),
                multimask_output=False,
            )
            for i, mask in enumerate(masks):
                filename = f"seg_{i}.png"
                Image.fromarray(mask).save(path.join(output_path, filename))
            files.push(filename)
        else:
            generator = SamAutomaticMaskGenerator(sam)
            masks = generator.generate(image)
            for i, mask in enumerate(masks):
                bin = mask["segmentation"]
                filename = f"seg_{i}.png"
                filename = path.join(output_path, filename)
                Image.fromarray(bin).save(filename)
                files.push(filename)


class SegmentAnything(AIModel):
    name = "segment_anything"
    model = None

    def __init__(self) -> None:
        super().__init__()

    def load_model(self, args):
        with timer("load sam model"):
            # "vit_b", "sam_vit_b_01ec64.pth"
            model_type = args.get("model_type")
            checkpoint = args.get("checkpoint")
            if not model_type or not checkpoint:
                raise ValueError("model args missing")

            sam = sam_model_registry[model_type](checkpoint=checkpoint)
            sam.to("mps")
            self.model = sam

    def run_model(self, args):
        image = args.get("image")
        if not image:
            raise ValueError("model args missing")
        if image.startswith("data:"):
            image = dataurl_to_image(args.get("image"))
        else:
            image = Image.open(image)
        origin_image_path = path.join(output_path, "origin_copy.png")
        image.save(origin_image_path)
        point = args.get("point")
        mask_files = segment(self.model, image, point)
        files = []
        for i, mask in enumerate(mask_files):
            image = cutout(origin_image_path, mask)
            cutout_file = path.join(output_path, f"cutout_{i}".py)
            image.save(cutout_file)
            files.push(cutout_file)
        return {"result": files}
