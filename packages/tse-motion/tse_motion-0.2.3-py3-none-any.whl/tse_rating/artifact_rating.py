import sys
import torch
import nibabel as nib
from torchvision.transforms import CenterCrop
from monai.networks.nets import DenseNet121
from pkg_resources import resource_filename
from monai.visualize import GradCAM, GradCAMpp
import pdb
import matplotlib.pyplot as plt
from monai.visualize import OcclusionSensitivity
from tqdm import tqdm

def rate(input_array, save_gradcam=False):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DenseNet121(spatial_dims=2, in_channels=1, out_channels=5)
    model_path = resource_filename('tse_rating', 'weight.pth')
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    
    transform = CenterCrop((512, 512))
    imgs = torch.tensor(input_array).permute(-1, 0, 1).to(device).float()
    imgs = torch.stack([img/img.max() for img in imgs])
    ratings = []
    cam = GradCAM(nn_module=model, target_layers="class_layers.relu")

    for img in imgs:
        ratings.append(model(transform(img).unsqueeze(0).unsqueeze(0)).softmax(dim=1).argmax().detach().cpu())
    rating = torch.stack(ratings).float().mean()
    
    if save_gradcam:
        grad_cam = cam(x=imgs.unsqueeze(1))
        return rating.item(), grad_cam.squeeze()
    
    return rating.item()

def main():
    if len(sys.argv) < 2:
        print("Usage: rate-motion <path_to_nifti_file>")
        sys.exit(1)
    input_path = sys.argv[1]
    rating = rate(input_path)
    print(f'Input: {input_path} | Motion Rating: {rating}')

if __name__ == '__main__':
    main()
