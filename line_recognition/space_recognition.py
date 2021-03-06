import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import cv2
from PIL import Image


def make_prediction(img_path):
    model = CNN()
    model.load_state_dict(torch.load("current_model_2.pth"))
    image = Image.open(img_path)
    image = image.convert('RGB')
    width, height = image.size
    num = round(width/height/0.78)
    w = width/num

    letters=""
    for i in range (0,num):
        cropped = image.crop((i*w,0,(i+1)*w,height))
        # cropped.show()
        cropped = np.array(cropped)
        cropped = cv2.resize(cropped, (28, 28))
        cropped = cropped.astype(np.float32) / 255.0
        cropped = torch.from_numpy(cropped[None, :, :, :])
        cropped = cropped.permute(0, 3, 1, 2)
        predicted_tensor = model(cropped)
        _, predicted_letter = torch.max(predicted_tensor, 1)
        if int(predicted_letter) == 26:
            letters=letters+str(chr(32))
        else:
            letters = letters + str(chr(97 + predicted_letter))
            # letters.append(chr(97 + predicted_letter))

    return letters




    image = np.array(image)
    image = cv2.resize(image, (28, 28))
    image = image.astype(np.float32) / 255.0
    image = torch.from_numpy(image[None, :, :, :])
    image = image.permute(0, 3, 1, 2)
    predicted_tensor = model(image)
    _, predicted_letter = torch.max(predicted_tensor, 1)
    # for testing:
    print(chr(97+predicted_letter))
    return chr(97+predicted_letter)


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.block1 = nn.Sequential(
            # 3x28x28
            nn.Conv2d(in_channels=3,
                      out_channels=16,
                      kernel_size=5,
                      stride=1,
                      padding=2),
            # 16x28x28
            nn.MaxPool2d(kernel_size=2),
            # 16x14x14
            nn.LeakyReLU()
        )
        # 16x14x14
        self.block2 = nn.Sequential(
            nn.Conv2d(in_channels=16,
                      out_channels=32,
                      kernel_size=5,
                      stride=1,
                      padding=2),
            # 32x14x14
            nn.MaxPool2d(kernel_size=2),
            # 32x7x7
            nn.LeakyReLU()
        )
        # linearly
        self.block3 = nn.Sequential(
            nn.Linear(32 * 7 * 7, 100),
            nn.LeakyReLU(),
            nn.Linear(100, 27)
        )

        # 1x26

    def forward(self, x):
        out = self.block1(x)
        out = self.block2(out)
        # flatten the dataset
        out = out.view(-1, 32 * 7 * 7)
        out = self.block3(out)

        return out


print(make_prediction("threw_the_ball.png"))
print(make_prediction("little_girl.png"))
print(make_prediction("with_his_family.png"))
print(make_prediction("the_little.png"))
print(make_prediction("the_daddy.png"))
print(make_prediction("and_laughed.png"))
print(make_prediction("would_run_and_get_it.png"))
print(make_prediction("he_took_it_home_to_play.png"))
print(make_prediction("picked_it_up_with_his_mouth.png"))

print(make_prediction("family.jpg"))
print(make_prediction("home.jpg"))
print(make_prediction("took.jpg"))
print(make_prediction("would.png"))

