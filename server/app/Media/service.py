import torch
from torchvision import models, transforms
from PIL import Image

class MediaService:
  def __init__(self):
    # Load a pre-trained DeepLabV3 model specifically tuned for segmentation
    self.model = models.segmentation.deeplabv3_resnet101(pretrained=True) #try diff models
    self.model.eval()
    # Check if a GPU is available and move the model to GPU
    if torch.cuda.is_available():
      self.model = self.model.cuda()

  def generateMedia(self, host_image_path, background_image_path, output_image_path):
    # Load and preprocess the host image
    input_image = Image.open(host_image_path).convert("RGB")
    preprocess = transforms.Compose([
      transforms.ToTensor(),
      transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    # Use GPU if available for processing
    if torch.cuda.is_available():
      input_batch = input_batch.cuda()

    # Predict the segmentation mask
    with torch.no_grad():
      output = self.model(input_batch)['out'][0]
    output_predictions = output.argmax(0).byte().cpu().numpy()

    # Create a mask for the human class (DeepLabV3 uses class 15 for person)
    human_mask = (output_predictions == 15)

    # Convert the binary mask to an image format
    mask_image = Image.fromarray((human_mask * 255).astype('uint8'), mode='L')

    # Open and resize the background image to match the host image
    background_image = Image.open(background_image_path)
    background_image = background_image.resize(input_image.size, Image.BILINEAR)

    # Composite the images using the mask
    composite_image = Image.composite(input_image, background_image, mask_image)

    # Save the output image
    composite_image.save(output_image_path)
    print(f"Generated media saved to {output_image_path}")

