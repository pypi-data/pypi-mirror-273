import pathlib as paths
import cv2 as cv
import pandas as pd
from tqdm.auto import tqdm


class ImageSizeGenerator:
    def __init__(self, image_files: list):
        assert len(image_files) > 0
        assert all(isinstance(f, paths.Path) for f in image_files)
        self.image_files = image_files

    def __iter__(self):
        for file_path in self.image_files:
            img = cv.imread(str(file_path))
            height, width, channels = img.shape
            yield (width, height, channels)


def calculate_image_statistics(image_files: list, recommend_by: str = 'width'):
    image_size_generator = ImageSizeGenerator(image_files)

    widths = []
    heights = []
    channel_counts = []
    for width, height, channels in image_size_generator:
        widths.append(width)
        heights.append(height)
        channel_counts.append(channels)

    min_width, max_width = min(widths), max(widths)
    min_height, max_height = min(heights), max(heights)
    avg_width, avg_height = sum(widths) / len(widths), sum(heights) / len(heights)

    recommended_width = -1
    recommended_height = -1
#     resize_with = 'height' if avg_height > avg_width else 'width'
    resize_with = recommend_by
    if resize_with == 'height':
        recommended_height = int(round(avg_height, 0))
        scale_ratios = [recommended_height / height for height in heights]
        recommended_width = int(round(max(width * scale_ratios[i] for i, width in enumerate(widths)), 0))
    elif resize_with == 'width':
        recommended_width = int(round(avg_width, 0))
        scale_ratios = [recommended_width / width for width in widths]
        recommended_height = int(round(max(height * scale_ratios[i] for i, height in enumerate(heights)), 0))
    else:
        raise NotImplementedError()

    return (min_width, max_width, min_height, max_height, avg_width, avg_height, channel_counts, recommended_width, recommended_height)

class ImageResizingGenerator:
    def __init__(self, image_series, target_fixed_height, target_fixed_width, target_channels, output_directory, pbar):
        self.image_series = image_series
        self.target_fixed_height = target_fixed_height
        self.target_fixed_width = target_fixed_width
        self.output_directory = output_directory
        self.target_channels = target_channels
        self.pbar = pbar

    def generate_images(self):
        for idx, image_path in self.image_series.items():
            img = cv.imread(str(image_path))
            # img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img_to_change = None
            if self.target_channels == 1:
                img_to_change = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to grayscale
            else:
                img_to_change = img
#             current_height, current_width, _ = img.shape

#             ratio = self.target_fixed_height / current_height
            resized_img = cv.resize(
                img_to_change, (self.target_fixed_width, self.target_fixed_height),
                interpolation=cv.INTER_LANCZOS4
            )

            new_img = resized_img

            new_image_path = self.output_directory / f'image_{idx}.jpg'
            self.pbar.set_description(f"Resized 🖼-#{idx} {resized_img.shape}➡{new_img.shape}🖬➡\"{new_image_path}\"")

            cv.imwrite(str(new_image_path), new_img)

            self.pbar.update(1)
            yield idx, new_image_path


def dataset_load_image(file_path: paths.Path, target_channels: int):
    image = cv.imread(str(file_path))
    if target_channels == 1:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    return image
