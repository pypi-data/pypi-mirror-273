# Reading Image
"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

image = mpimg.imread('/content/pikachu.jpeg')
plt.imshow(image)

"""# Grayscale"""

def grayscale(image):
  return np.dot(image[...,:3],[0.2989, 0.5870, 0.1140])

"""# Addition"""

def add_images(image_1, image_2):
  image1 = np.array(image_1)
  image2 = np.array(image_2)

  result = image1 + image2
  result = np.clip(result, 0, 255)
  result = result.astype(np.uint8)

  return result

"""# Subtraction"""

def subtract(image_1, image_2):
  image1 = np.array(image_1)
  image2 = np.array(image_2)

  result = image1 - image2
  result = np.clip(result, 0, 255)
  result = result.astype(np.uint8)

  return result

"""# Multiplication"""

def multiply(image_1, image_2):

  image1 = np.array(image_1)
  image2 = np.array(image_2)

  result = image1 * image2

  return result

"""# Division"""

def divide(image_1, image_2):

  image1 = np.array(image_1)
  image1[image1 == 0] = 1
  image2 = np.array(image_2)
  image2[image2 == 0] = 1

  result = image1 / image2

  return result

"""# Blending"""

def blend(image_1, image_2):

  image1 = np.array(image_1)
  image2 = np.array(image_2)

  result = 0.6*image1 + 0.4*image2
  result = np.clip(result, 0, 255)
  result = result.astype(np.uint8)

  return result

"""# AND"""

def and_images(image_1, image_2):
  image_1 = np.array(image_1, dtype=np.uint8)
  image_2 = np.array(image_2, dtype=np.uint8)

  and_image = image_1 & image_2

  return and_image

"""# OR"""

def or_images(image_1, image_2):
  image_1 = np.array(image_1, dtype=np.uint8)
  image_2 = np.array(image_2, dtype=np.uint8)

  or_image = image_1 | image_2

  return or_image

"""# XOR"""

def xor_images(image_1, image_2):
  image_1 = np.array(image_1, dtype=np.uint8)
  image_2 = np.array(image_2, dtype=np.uint8)

  xor_image = image_1 ^ image_2

  return xor_image

"""#NOT"""

def not_images(image_1):

  not_image = 255 - image_1

  return not_image

"""#Left Shift"""

def ls_images(image_1):

  image_1 = np.array(image_1, dtype=np.uint8)

  ls_image = image_1 << 1

  return ls_image

"""#Right Shift"""

def rs_images(image_1):

  image_1 = np.array(image_1, dtype=np.uint8)

  ls_image = image_1 >> 1

  return ls_image

"""# Thresholding"""

def thresholding(image, threshold):
  thresholded_image = np.zeros_like(image)

  thresholded_image[image > threshold] = 255
  thresholded_image[image <= threshold] = 0

  return thresholded_image

"""# Gray Level with background"""

def gray_level_back(image, lower_limit, upper_limit, highlight_value = 255):

  image_1 = np.copy(image)

  image_1[(image > lower_limit)&(image<=upper_limit)] = highlight_value

  return image_1

"""# Gray Level without background"""

def gray_level_withoutback(image, lower_limit, upper_limit, highlight_value = 255):

  image_1 = np.zeros_like(image)

  image_1[(image > lower_limit)&(image<=upper_limit)] = highlight_value

  return image_1

"""# Contrast Stretching"""

def contrast_stretching(image):
    min_val, max_val = np.min(image), np.max(image)
    result = 255 * (image - min_val) / (max_val - min_val)
    return result

"""# Power Law Transform"""

def power_law(image, gamma):
    normalized_image = image / 255.0

    transformed_image = np.power(normalized_image, gamma)

    transformed_image = np.uint8(transformed_image * 255)

    return transformed_image

"""# Log Transform"""

def log_transform(image, c):
  image_float = image.astype(float)
  logged = c * np.log1p(image_float)
  transformed_image = np.uint8(255 * (logged / np.max(logged)))
  return transformed_image

"""# Histogram Equalization"""

def histogram_equalization(image):
    hist, bins = np.histogram(image.flatten(), bins=256, range=(0, 255))
    pmf = hist / image.size
    cdf = np.cumsum(pmf)
    cdf = cdf * 255
    new_image = np.zeros_like(image)
    for i in range(256):
        new_image[image == i] = int(round(cdf[i]))
    return new_image

"""# Median Filter"""

def median_filter_gray(image, kernel_size):
    pad_size = kernel_size // 2
    padded_image = np.pad(image, ((pad_size, pad_size), (pad_size, pad_size)), mode='edge')
    output_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
              window = padded_image[i:i+kernel_size, j:j+kernel_size]
              output_image[i, j] = np.median(window)
    return output_image

def median_filter_rgb(image, kernel_size):
    pad_size = kernel_size // 2
    padded_image = np.pad(image, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
    output_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                window = padded_image[i:i+kernel_size, j:j+kernel_size, k]
                output_image[i, j, k] = np.median(window)
    return output_image

"""# Averaging Filter"""

def mean_filter_gray(image, kernel_size):
    pad_size = kernel_size // 2
    padded_image = np.pad(image, ((pad_size, pad_size), (pad_size, pad_size)), mode='edge')
    output_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
              window = padded_image[i:i+kernel_size, j:j+kernel_size]
              output_image[i, j] = np.mean(window)
    return output_image

def mean_filter_rgb(image, kernel_size):
    pad_size = kernel_size // 2
    padded_image = np.pad(image, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
    output_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                window = padded_image[i:i+kernel_size, j:j+kernel_size, k]
                output_image[i, j, k] = np.mean(window)
    return output_image

"""# Low Pass Filter"""

def low_pass_gray(image, kernel):
  kernel_size = kernel.shape[0]
  padding = kernel_size // 2

  padded_image = np.pad(image, padding, mode='constant', constant_values=0)

  low_pass_image = np.zeros_like(image)

  for i in range(image.shape[0]):
    for j in range(image.shape[1]):

      for k in range(kernel_size):
        for l in range(kernel_size):
          low_pass_image[i,j] += kernel[k,l]* padded_image[i + k, j + l]

  return low_pass_image

kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]
])

result = low_pass_gray(gray_image_pika, kernel)
plt.imshow(result, cmap='gray')

def low_pass_rgb(image, kernel):
  kernel_size = kernel.shape[0]
  padding = kernel_size // 2

  padded_image = np.pad(image, ((padding, padding), (padding, padding), (0, 0)), mode='constant', constant_values=0)

  low_pass_image = np.zeros_like(image)

  for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for m in range(image.shape[2]):  # Additional loop to handle channels
                sum_pixel = 0
                for k in range(kernel_size):
                    for l in range(kernel_size):
                        sum_pixel += kernel[k, l] * padded_image[i + k, j + l, m]
                low_pass_image[i, j, m] = sum_pixel

  return low_pass_image

kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]
])

result = low_pass_rgb(rgb_image_pika, kernel)
plt.imshow(result)

"""# High Pass Filter"""

def high_pass_gray(image, kernel):
  kernel_size = kernel.shape[0]
  padding = kernel_size // 2

  padded_image = np.pad(image, padding, mode='constant', constant_values=0)

  high_pass_image = np.zeros_like(image)

  for i in range(image.shape[0]):
    for j in range(image.shape[1]):

      for k in range(kernel_size):
        for l in range(kernel_size):
          high_pass_image[i,j] += kernel[k,l]* padded_image[i + k, j + l]

  return high_pass_image

kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, -8/9, 1/9],
    [1/9, 1/9, 1/9]
])

result = high_pass_gray(gray_image_pika, kernel)
plt.imshow(result, cmap='gray')

def high_pass_rgb(image, kernel):
  kernel_size = kernel.shape[0]
  padding = kernel_size // 2

  padded_image = np.pad(image, ((padding, padding), (padding, padding), (0, 0)), mode='constant', constant_values=0)

  high_pass_image = np.zeros_like(image)

  for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for m in range(image.shape[2]):
                sum_pixel = 0
                for k in range(kernel_size):
                    for l in range(kernel_size):
                        sum_pixel += kernel[k, l] * padded_image[i + k, j + l, m]
                high_pass_image[i, j, m] = sum_pixel

  return high_pass_image

kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, -8/9, 1/9],
    [1/9, 1/9, 1/9]
])

result = high_pass_rgb(rgb_image_pika, kernel)
plt.imshow(result)

"""#High Boost Filter"""

def high_boost_gray(image, kernel):
  kernel_size = kernel.shape[0]
  padding = kernel_size // 2

  padded_image = np.pad(image, padding, mode='constant', constant_values=0)

  high_pass_image = np.zeros_like(image)

  for i in range(image.shape[0]):
    for j in range(image.shape[1]):

      for k in range(kernel_size):
        for l in range(kernel_size):
          high_pass_image[i,j] += kernel[k,l]* padded_image[i + k, j + l]

  return high_pass_image

kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, -17/9, 1/9],
    [1/9, 1/9, 1/9]
])

result = high_boost_gray(gray_image_pika, kernel)
plt.imshow(result, cmap='gray')

def high_boost_rgb(image, kernel):
  kernel_size = kernel.shape[0]
  padding = kernel_size // 2

  padded_image = np.pad(image, ((padding, padding), (padding, padding), (0, 0)), mode='constant', constant_values=0)

  high_boost_image = np.zeros_like(image)

  for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for m in range(image.shape[2]):
                sum_pixel = 0
                for k in range(kernel_size):
                    for l in range(kernel_size):
                        sum_pixel += kernel[k, l] * padded_image[i + k, j + l, m]
                high_boost_image[i, j, m] = sum_pixel

  return high_boost_image

kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, -17/9, 1/9],
    [1/9, 1/9, 1/9]
])

result = high_boost_rgb(rgb_image_pika, kernel)
plt.imshow(result)

"""# Erosion"""

def erode_image_gray(image, se):
  image_height, image_width = image.shape
  se_height, se_width = se.shape
  se_center = (se_height // 2, se_width // 2)

  eroded_image = np.full_like(image, 255)

  for i in range(se_center[0], image_height - se_center[0]):
    for j in range(se_center[1], image_width - se_center[1]):
      local_min = 255

      for k in range(se_height):
        for l in range(se_width):
          if se[k, l] == 1:
            local_min = min(local_min, image[i - se_center[0] + k, j - se_center[1] + l])

      eroded_image[i, j] = local_min

  return eroded_image

se = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])

result = erode_image_gray(gray_image_pika, se)
plt.imshow(result, cmap='gray')

def erode_image_rgb(image, se):
    image_height, image_width, num_channels = image.shape
    se_height, se_width = se.shape
    se_center = (se_height // 2, se_width // 2)

    eroded_image = np.full_like(image, 255)

    for channel in range(num_channels):
        for i in range(se_center[0], image_height - se_center[0]):
            for j in range(se_center[1], image_width - se_center[1]):
                local_min = 255
                for k in range(se_height):
                    for l in range(se_width):
                        if se[k, l] == 1:
                            local_min = min(local_min, image[i - se_center[0] + k, j - se_center[1] + l, channel])

                eroded_image[i, j, channel] = local_min

    return eroded_image

se = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])

result = erode_image_rgb(rgb_image_pika, se)
plt.imshow(result)

"""# Dilation"""

def dilate_image_gray(image, se):
  image_height, image_width = image.shape
  se_height, se_width = se.shape
  se_center = (se_height // 2, se_width // 2)

  dilated_image = np.full_like(image, 255)

  for i in range(se_center[0], image_height - se_center[0]):
    for j in range(se_center[1], image_width - se_center[1]):
      local_max = 0

      for k in range(se_height):
        for l in range(se_width):
          if se[k, l] == 1:
            local_max = max(local_max, image[i - se_center[0] + k, j - se_center[1] + l])

      dilated_image[i, j] = local_max

  return dilated_image

se = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])

result = dilate_image_gray(gray_image_pika, se)
plt.imshow(result, cmap='gray')

def dilate_image_rgb(image, se):
    image_height, image_width, num_channels = image.shape
    se_height, se_width = se.shape
    se_center = (se_height // 2, se_width // 2)

    dilated_image = np.full_like(image, 255)

    for channel in range(num_channels):
        for i in range(se_center[0], image_height - se_center[0]):
            for j in range(se_center[1], image_width - se_center[1]):
                local_max = 0
                for k in range(se_height):
                    for l in range(se_width):
                        if se[k, l] == 1:
                            local_max = max(local_max, image[i - se_center[0] + k, j - se_center[1] + l, channel])

                dilated_image[i, j, channel] = local_max

    return dilated_image

se = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])

result = dilate_image_rgb(rgb_image_pika, se)
plt.imshow(result)

"""# Opening"""

def opening_gray(image, se):
  eroded_image = erode_image_gray(image, se)
  dilated_image = dilate_image_gray(eroded_image, se)
  return dilated_image

se = np.array([
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
])

opening_image_gray = opening_gray(gray_image_pika, se)
plt.imshow(opening_image_gray, cmap='gray')

def opening_rgb(image, se):
  eroded_image = erode_image_rgb(image, se)
  dilated_image = dilate_image_rgb(eroded_image, se)
  return dilated_image

se = np.array([
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
])

opening_image_rgb = opening_rgb(rgb_image_pika, se)
plt.imshow(opening_image_rgb)

"""# Closing"""

def closing_gray(image, se):
  dilated_image = dilate_image_gray(image, se)
  eroded_image = erode_image_gray(dilated_image, se)
  return dilated_image

se = np.array([
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
])

closing_image_gray = closing_gray(gray_image_pika, se)
plt.imshow(closing_image_gray, cmap='gray')

def closing_rgb(image, se):
  dilated_image = dilate_image_rgb(image, se)
  eroded_image = erode_image_rgb(dilated_image, se)
  return dilated_image

se = np.array([
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
])

closing_image_rgb = closing_rgb(rgb_image_pika, se)
plt.imshow(closing_image_rgb)

"""# Hit and Miss Transform"""

def hit_and_miss_gray(image, se1, se2):
    A = erode_image_gray(image, se1)

    complement_image = 255 - image
    B = erode_image_gray(complement_image, se2)

    hit_miss_image = np.array(A, dtype=np.uint8) & np.array(B, dtype=np.uint8)
    return hit_miss_image

se1 = np.array([[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]])

se2 = np.array([[1, 0, 1],
                [0, 0, 0],
                [1, 0, 1]])

hit_and_miss_image = hit_and_miss_gray(gray_image_pika, se1, se2)
plt.imshow(hit_and_miss_image, cmap='gray')

def hit_and_miss_rgb(image, se1, se2):
    A = erode_image_rgb(image, se1)

    complement_image = 255 - image
    B = erode_image_rgb(complement_image, se2)

    hit_miss_image = np.array(A, dtype=np.uint8) & np.array(B, dtype=np.uint8)
    return hit_miss_image

se1 = np.array([[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]])

se2 = np.array([[1, 0, 1],
                [0, 0, 0],
                [1, 0, 1]])

hit_and_miss_image = hit_and_miss_rgb(rgb_image_pika, se1, se2)
plt.imshow(hit_and_miss_image)

"""# Ideal Low Pass"""

from scipy.fftpack import fftshift, ifftshift, fft2, ifft2

def ideal_lowpass(shape, cutoff):
    rows, cols = shape
    center_row, center_col = rows // 2, cols // 2
    mask = np.zeros((rows, cols), dtype=float)
    for i in range(rows):
        for j in range(cols):
            if np.sqrt((i - center_row)**2 + (j - center_col)**2) <= cutoff:
                mask[i, j] = 1
    return mask

def apply_filter(image, filter_mask):
    dft = fft2(image)
    dft_shift = fftshift(dft)
    filtered_dft = dft_shift * filter_mask
    ifft_shift = ifftshift(filtered_dft)
    filtered_img = ifft2(ifft_shift)
    return np.abs(filtered_img)

lpf_ideal = ideal_lowpass(gray_image_pika.shape, 30)
filtered_image_ideal_lpf = apply_filter(gray_image_pika, lpf_ideal)
plt.imshow(filtered_image_ideal_lpf, cmap="gray")

"""# Guassian Low Pass"""

from scipy.fftpack import fftshift, ifftshift, fft2, ifft2

def gaussian_lowpass(shape, cutoff):
    rows, cols = shape
    center_row, center_col = rows // 2, cols // 2
    mask = np.zeros((rows, cols), dtype=float)
    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - center_row)**2 + (j - center_col)**2)
            mask[i, j] = np.exp(-(distance**2) / (2 * (cutoff**2)))
    return mask

def apply_filter(image, filter_mask):
    dft = fft2(image)
    dft_shift = fftshift(dft)
    filtered_dft = dft_shift * filter_mask
    ifft_shift = ifftshift(filtered_dft)
    filtered_img = ifft2(ifft_shift)
    return np.abs(filtered_img)

lpf_ideal = gaussian_lowpass(gray_image_pika.shape, 10)
filtered_image_ideal_lpf = apply_filter(gray_image_pika, lpf_ideal)
plt.imshow(filtered_image_ideal_lpf, cmap="gray")

"""# Ideal High Pass"""

from scipy.fftpack import fftshift, ifftshift, fft2, ifft2

def ideal_highpass(shape, cutoff):
    return 1 - ideal_lowpass(shape, cutoff)

def apply_filter(image, filter_mask):
    dft = fft2(image)
    dft_shift = fftshift(dft)
    filtered_dft = dft_shift * filter_mask
    ifft_shift = ifftshift(filtered_dft)
    filtered_img = ifft2(ifft_shift)
    return np.abs(filtered_img)

lpf_ideal = ideal_highpass(gray_image_pika.shape, 30)
filtered_image_ideal_hpf = apply_filter(gray_image_pika, lpf_ideal)
plt.imshow(filtered_image_ideal_hpf, cmap="gray")

"""# Guassian High Pass"""

from scipy.fftpack import fftshift, ifftshift, fft2, ifft2

def gaussian_highpass(shape, cutoff):
    return 1 - gaussian_lowpass(shape, cutoff)

def apply_filter(image, filter_mask):
    dft = fft2(image)
    dft_shift = fftshift(dft)
    filtered_dft = dft_shift * filter_mask
    ifft_shift = ifftshift(filtered_dft)
    filtered_img = ifft2(ifft_shift)
    return np.abs(filtered_img)

lpf_ideal = gaussian_highpass(gray_image_pika.shape, 10)
filtered_image_ideal_hpf = apply_filter(gray_image_pika, lpf_ideal)
plt.imshow(filtered_image_ideal_hpf, cmap="gray")

"""# Butterworth Filter"""

from scipy.fftpack import fftshift, ifftshift, fft2, ifft2

def butterworth_lowpass_filter(shape, cutoff, order):
    P, Q = shape
    u = np.arange(P) - P/2
    v = np.arange(Q) - Q/2
    U, V = np.meshgrid(u, v, sparse=False, indexing='ij')
    D = np.sqrt(U**2 + V**2)
    H = 1 / (1 + (D / cutoff)**(2*order))
    return H

def apply_filter(image, filter_mask):
    dft = fft2(image)
    dft_shift = fftshift(dft)
    filtered_dft = dft_shift * filter_mask
    ifft_shift = ifftshift(filtered_dft)
    filtered_img = ifft2(ifft_shift)
    return np.abs(filtered_img)

butter = butterworth_lowpass_filter(gray_image_pika.shape, 10, 2)
butter_image = apply_filter(gray_image_pika, butter)
plt.imshow(butter_image, cmap="gray")

"""# Region Growing"""

import numpy as np
import cv2

def region_growing(image, seed, threshold):
    rows, cols = image.shape
    region_mean = float(image[seed])
    region_size = 1
    output_image = np.zeros((rows, cols), dtype=np.uint8)

    region_points = [seed]
    processed_points = set(region_points)

    while region_points:
        new_points = []
        for point in region_points:
            x, y = point
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in processed_points:
                    processed_points.add((nx, ny))
                    pixel_value = image[nx, ny]
                    if abs(pixel_value - region_mean) < threshold:
                        new_points.append((nx, ny))
                        region_mean = ((region_mean * region_size + pixel_value) / (region_size + 1))
                        region_size += 1
                        output_image[nx, ny] = 255
        region_points = new_points

    return output_image


seed_point = (100, 100)
threshold_value = 10
grown_region = region_growing(gray_image_pika, seed_point, threshold_value)

plt.imshow(grown_region, cmap="gray")

"""# Region Splitting and Merging"""

def merge_regions(regions):
    while True:
        merged = False
        new_regions = []
        while regions:
            current = regions.pop()
            was_merged = False
            for idx, region in enumerate(new_regions):
                if abs(np.mean(region) - np.mean(current)) < 5:
                    new_regions[idx] = np.vstack([region, current])
                    was_merged = True
                    merged = True
                    break
            if not was_merged:
                new_regions.append(current)
        regions = new_regions
        if not merged:
            break
    return regions


def split_and_merge(image, num_regions):
    rows, cols = image.shape
    step = rows // num_regions
    regions = [np.arange(i, min(i + step, rows)) for i in range(0, rows, step)]
    regions = merge_regions(regions)

    output_image = np.zeros_like(image)
    for region in regions:
        for row in region:
            output_image[row, :] = ((np.mean(image[region, :]) - image[row, :]) < 10) * 255
    return output_image


split_merged_image = split_and_merge(gray_image_pika, 4)

plt.imshow(split_merged_image, cmap="gray")