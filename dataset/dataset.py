# coding:utf-8
import numpy as np
import scipy.misc
import os
import sys
import random
sys.path.append(r'')
from PIL import Image
from torchvision import transforms
from config import *



class CUB():
    def __init__(self, root, is_train=True, data_len=None):
        self.root = root
        self.is_train = is_train
        img_txt_file = open(os.path.join(self.root, 'images.txt'))
        label_txt_file = open(os.path.join(self.root, 'image_class_labels.txt'))
        train_val_file = open(os.path.join(self.root, 'train_test_split.txt'))
        img_name_list = []
        for line in img_txt_file:
            img_name_list.append(line[:-1].split(' ')[-1])
        label_list = []
        for line in label_txt_file:
            label_list.append(int(line[:-1].split(' ')[-1]) - 1)
        train_test_list = []
        for line in train_val_file:
            train_test_list.append(int(line[:-1].split(' ')[-1]))
    
        train_file_list = [x for i, x in zip(train_test_list, img_name_list) if i]
        test_file_list = [x for i, x in zip(train_test_list, img_name_list) if not i]
        if self.is_train:
            self.train_img = [os.path.join(self.root, 'images', train_file) for train_file in
                              train_file_list[:data_len]]
            self.train_label = [x for i, x in zip(train_test_list, label_list) if i][:data_len]
        if not self.is_train:
            self.test_img = [os.path.join(self.root, 'images', test_file) for test_file in
                             test_file_list[:data_len]]
            self.test_label = [x for i, x in zip(train_test_list, label_list) if not i][:data_len]

    def __getitem__(self, index):
        if self.is_train:
            img_path, target = self.train_img[index], self.train_label[index]   
            img = scipy.misc.imread(img_path)   
            if len(img.shape) == 2:
                img = np.stack([img] * 3, 2)     
            img = Image.fromarray(img, mode='RGB')  
            if random.choice([0,1]): 
                img = transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.2)(img)
            if random.choice([0,1]):          
                img = transforms.Resize((600, 600), Image.BILINEAR)(img)
                img = transforms.RandomCrop(INPUT_SIZE)(img)
            if random.choice([0,1]):    
                img = transforms.RandomAffine(30, scale=(0.8,1.2))(img)
            img = transforms.RandomHorizontalFlip()(img)
            img = transforms.RandomApply([transforms.RandomRotation(30)], 
                                    p=0.5)(img)
            img = transforms.Resize((448, 448), Image.BILINEAR)(img)
            img = transforms.ToTensor()(img)
            
            img = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(img)

        else:
            img_path, target = self.test_img[index], self.test_label[index] 
            img = scipy.misc.imread(img_path)   
            if len(img.shape) == 2:
                img = np.stack([img] * 3, 2)                       
            img = Image.fromarray(img, mode='RGB')
            img = transforms.Resize((600, 600), Image.BILINEAR)(img)
            img = transforms.RandomCrop(INPUT_SIZE)(img)
            img = transforms.RandomHorizontalFlip()(img)
            img = transforms.RandomApply([transforms.RandomRotation(30)], 
                                    p=0.5)(img)
            img = transforms.ToTensor()(img)
            img = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(img)

        return img, target

    def __len__(self):
        if self.is_train:
            return len(self.train_label)
        else:
            return len(self.test_label)


if __name__ == '__main__':
    dataset = CUB(root=data_dir)
    print(len(dataset.train_img))
    print(len(dataset.train_label))
    for data in dataset:
        print(data[0].size(), data[1])
    dataset = CUB(root=data_dir, is_train=False)
    print(len(dataset.test_img))
    print(len(dataset.test_label))
    for data in dataset:
        print(data[0].size(), data[1])